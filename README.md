# bug-sentinel
### Converts raw Jenkins automation logs into business-friendly dashboard.

---

## Overview

The **QA Automation Analytics Portal** is a complete end-to-end platform designed to:

* Collect & parse logs from multiple Jenkins servers
* Extract failures and normalize error messages
* Use **ML-based classification** to identify "real bugs" vs infra/locator/test issues
* Provide a **React dashboard** for stakeholders with charts and insights
* Provide a **human review loop** for improving ML accuracy
* Store all data in **PostgreSQL** with model versioning

This tool helps stakeholders understand the real value of automation and gives QA teams deep insights into test stability, flakiness, and product quality.

---

## Features

### Data Pipeline

* Automated log ingestion from Jenkins (via webhook or scraping)
* Robust parser to extract failures with normalization and metadata
* Storage of runs, failures, labels, and model metadata in PostgreSQL

### Machine Learning

* TF‑IDF + XGBoost baseline classifier
* Optional fine‑tuned DistilBERT model
* Confidence‑based routing to human review queue
* Scheduled re-training (active learning)

### Dashboard

* Bugs detected per website
* Quarterly trends
* Flakiness heatmap
* Top recurring issues
* Model performance
* Manual review queue

### Architecture

* **Backend:** FastAPI + SQLAlchemy + PostgreSQL
* **Frontend:** React + Tailwind + Recharts
* **ML Engine:** Python (scikit-learn, transformers)
* **Infra:** Docker / Kubernetes

---

## Getting Started

### 1.Clone the repo

```
git clone https://github.com/your-org/qa-automation-analytics-portal.git
cd qa-automation-analytics-portal
```

### 2.Start services via Docker Compose

```
docker-compose up --build
```

This starts:

* FastAPI backend
* React frontend
* PostgreSQL database

### 3. Access the UI

[http://localhost:3000](http://localhost:3000)

### 4. Access API docs

[http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📦 ML Training

To train the baseline ML classifier:

```
cd ml/training
python3 train_xgboost.py
```

Models are saved into `ml/models/` and automatically used by the backend.

---

## 🗄️ Environment Variables

Create a `.env` file under `backend/`:

```
DATABASE_URL=postgresql://user:password@db:5432/qa_analytics
SECRET_KEY=your_jwt_secret_key
MODEL_PATH=/app/ml/models/current
```

---

## Future Enhancements

* Full BERT‑based classification
* CI/CD deployment to Kubernetes
* Advanced flakiness prediction using time-series models
* SSO authentication

---

## License

MIT License
