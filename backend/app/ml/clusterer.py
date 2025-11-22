# ml/clusterer.py
import logging
import json
import numpy as np

from typing import List, Tuple, Optional

logger = logging.getLogger(__name__)

# try to use sentence-transformers first, fallback to sklearn TF-IDF
try:
    from sentence_transformers import SentenceTransformer
    _HAS_ST = True
except Exception:
    _HAS_ST = False

# sklearn fallback
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.decomposition import TruncatedSVD
    from sklearn.cluster import DBSCAN
    from sklearn.metrics.pairwise import cosine_distances
    _HAS_SK = True
except Exception:
    _HAS_SK = False

# local imports will be resolved when used in app context
# we keep DB operations out of core embedder so clusterer is testable
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
TFIDF_DIM = 128  # fallback embedding dim


# ---------- Embedding helpers ----------
class Embedder:
    def __init__(self):
        if _HAS_ST:
            try:
                self.model = SentenceTransformer(EMBED_MODEL_NAME)
                logger.info("Using SentenceTransformer: %s", EMBED_MODEL_NAME)
                self.kind = "sentence-transformer"
            except Exception as e:
                logger.exception("Failed to init SentenceTransformer, fallback to sklearn: %s", e)
                self.model = None
                self.kind = None

        if not _HAS_ST or getattr(self, "model", None) is None:
            if _HAS_SK:
                self.tfidf = TfidfVectorizer(max_features=20000, ngram_range=(1,2))
                self.svd = TruncatedSVD(n_components=TFIDF_DIM, random_state=42)
                self.kind = "tfidf-svd"
                # note: tfidf needs to be fitted before transform; see `fit_transform_corpus`
            else:
                raise RuntimeError("No embedding backend available. Install sentence-transformers or scikit-learn")

    def embed_sentences(self, texts: List[str]) -> np.ndarray:
        if getattr(self, "kind", None) == "sentence-transformer":
            vecs = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
            # normalize to unit vectors for cosine similarity convenience
            norms = np.linalg.norm(vecs, axis=1, keepdims=True)
            norms[norms == 0] = 1.0
            return vecs / norms
        elif getattr(self, "kind", None) == "tfidf-svd":
            # if tfidf not yet fitted (it will throw), user must call fit_transform_corpus first
            X = self.tfidf.transform(texts)
            Xs = self.svd.transform(X)
            norms = np.linalg.norm(Xs, axis=1, keepdims=True)
            norms[norms == 0] = 1.0
            return Xs / norms
        else:
            raise RuntimeError("Embedder not initialized properly")

    def fit_transform_corpus(self, corpus: List[str]) -> np.ndarray:
        """Fit TF-IDF on corpus and return embeddings (fallback path)."""
        if getattr(self, "kind", None) != "tfidf-svd":
            raise RuntimeError("fit_transform_corpus only for tfidf fallback")
        X = self.tfidf.fit_transform(corpus)
        Xs = self.svd.fit_transform(X)
        norms = np.linalg.norm(Xs, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        return Xs / norms


# ---------- Clustering & assignment logic ----------
def cosine_similarity_matrix(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    # assumes rows are normalized; cosine_sim = dot
    return np.dot(a, b.T)


class Clusterer:
    """
    High level utilities for:
      - clustering a batch of normalized messages (offline)
      - assigning one failure to existing clusters (online)
    """

    def __init__(self, embedder: Optional[Embedder] = None):
        self.embedder = embedder or Embedder()

    def cluster_batch(self, texts: List[str], eps: float = 0.35, min_samples: int = 3) -> List[int]:
        """
        Cluster a batch of normalized texts (useful for offline grouping).
        Returns list of labels (-1 = noise).
        """
        if not texts:
            return []

        emb = self._get_embeddings_for_batch(texts)
        # sklearn's DBSCAN with cosine metric uses 1 - cosine_similarity as distance;
        # because we use normalized vectors, Euclidean distance relates to cosine. Simpler: use DBSCAN on embeddings with metric='cosine'.
        if not _HAS_SK:
            raise RuntimeError("scikit-learn required for clustering (DBSCAN). Install scikit-learn")
        db = DBSCAN(eps=eps, min_samples=min_samples, metric="cosine")
        labels = db.fit_predict(emb)
        return labels.tolist()

    def assign_to_cluster(self, db_session, failure_model, cluster_model, failure_obj,
                          threshold: float = 0.65) -> Tuple[int, bool]:
        """
        Assign a single failure to an existing cluster or create a new cluster.
        - db_session: SQLAlchemy session
        - failure_model: app.models.failure.Failure class
        - cluster_model: app.models.cluster.Cluster class
        - failure_obj: instance of Failure that is already saved (has id, error_message)
        Returns: (cluster_id, created_new_flag)
        """
        # compute embedding for this failure message
        normalized = failure_obj.error_message
        emb = self._get_embeddings_for_batch([normalized])[0].reshape(1, -1)  # (1, D)

        # fetch clusters and their representative embeddings
        clusters = db_session.query(cluster_model).all()
        if not clusters:
            # create first cluster
            new_cluster = cluster_model(representative_message=normalized,
                                        member_count=1,
                                        metadata={})
            # store embedding as JSON list
            new_cluster.representative_embedding = json.dumps(emb[0].tolist())
            db_session.add(new_cluster)
            db_session.commit()
            # link failure -> cluster (create link table or set cluster_id on failure)
            failure_obj.cluster_id = new_cluster.id
            failure_obj.embedding = json.dumps(emb[0].tolist())
            db_session.add(failure_obj)
            db_session.commit()
            return new_cluster.id, True

        # compute similarity between failure embedding and each cluster rep embedding
        rep_embs = []
        rep_cluster_map = []
        for c in clusters:
            if not c.representative_embedding:
                continue
            try:
                arr = np.array(json.loads(c.representative_embedding), dtype=float)
                rep_embs.append(arr)
                rep_cluster_map.append(c)
            except Exception:
                logger.exception("Invalid representative_embedding for cluster %s", c.id)

        if rep_embs:
            rep_embs = np.vstack(rep_embs)  # (K, D)
            sims = cosine_similarity_matrix(emb, rep_embs).flatten()  # dot product since normalized
            best_idx = int(np.argmax(sims))
            best_sim = float(sims[best_idx])
            best_cluster = rep_cluster_map[best_idx]
            logger.debug("best_sim=%s for cluster=%s", best_sim, getattr(best_cluster, "id", None))

            if best_sim >= threshold:
                # assign to best_cluster; update member_count and maybe update rep embedding
                failure_obj.cluster_id = best_cluster.id
                failure_obj.embedding = json.dumps(emb[0].tolist())
                db_session.add(failure_obj)

                # simple centroid update: average between old rep and new vector (incremental)
                try:
                    old = np.array(json.loads(best_cluster.representative_embedding), dtype=float)
                    new_rep = (old * float(best_cluster.member_count) + emb[0]) / float(best_cluster.member_count + 1)
                    # renormalize
                    new_rep = new_rep / (np.linalg.norm(new_rep) + 1e-12)
                    best_cluster.representative_embedding = json.dumps(new_rep.tolist())
                except Exception:
                    # fallback: keep representative as-is or replace
                    best_cluster.representative_embedding = json.dumps(emb[0].tolist())

                best_cluster.member_count = (best_cluster.member_count or 0) + 1
                db_session.add(best_cluster)
                db_session.commit()
                return best_cluster.id, False

        # no suitable cluster => create new one
        new_cluster = cluster_model(representative_message=normalized,
                                    member_count=1,
                                    metadata={})
        new_cluster.representative_embedding = json.dumps(emb[0].tolist())
        db_session.add(new_cluster)
        db_session.commit()
        failure_obj.cluster_id = new_cluster.id
        failure_obj.embedding = json.dumps(emb[0].tolist())
        db_session.add(failure_obj)
        db_session.commit()
        return new_cluster.id, True

    def _get_embeddings_for_batch(self, texts: List[str]) -> np.ndarray:
        # If using tfidf fallback and not fitted, attempt to fit on given texts (conservative)
        if getattr(self.embedder, "kind", None) == "tfidf-svd":
            # fit on small local corpus to avoid empty vectorizer
            try:
                emb = self.embedder.fit_transform_corpus(texts)
                return emb
            except Exception as e:
                logger.exception("TFIDF fit failed: %s", e)
                raise
        else:
            return self.embedder.embed_sentences(texts)