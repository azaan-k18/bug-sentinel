# 🛡️ bugSentinel – Project Documentation

## 1️⃣ Project Vision

bugSentinel is a backend system that:

1. **Ingests** raw logs from Jenkins, LambdaTest, Playwright, Appium, Selenium.
2. **Normalizes + Classifies** failures into:
   - real_bug  
   - script_issue  
   - environment_issue  
   - unknown  
3. **Stores** detailed build + test metadata in a database.
4. **Scores** each failure for **flakiness**.
5. **Prepares data** for dashboards showing:
   - total tests executed  
   - failures categorized  
   - real bugs vs flaky failures  
   - test stability trends  

The goal is to automatically identify:
- Which failures are real product bugs  
- Which failures are flaky or environmental  
- Which tests need maintenance  
- Which frameworks are unstable  

---

## 2️⃣ High-Level Architecture

- Logs from Jenkins / LambdaTest → Ingestion API → Normalizer
        ↓
- Classifier (ML)
        ↓
- Flakiness Scoring Engine
        ↓
- Database Storage
        ↓
- Dashboard API
        ↓
- Frontend Dashboard


---

## 3️⃣ Key Components & What Each File Does

### ✔️ backend/main.py
- Entry point for the FastAPI server.
- Registers all API routes.
- Health endpoint.

### ✔️ backend/routes/ingest.py
- API endpoint for receiving logs.
- Validates input and hands data to pipeline.

### ✔️ backend/services/normalizer.py
- Converts raw errors into normalized signatures.

### ✔️ backend/services/classifier.py
- ML classification to categorize failures.

### ✔️ backend/services/flakiness.py
Contains:
- `TestHistory` dataclass  
- `calculate_flakiness_score()`  
- `compute_flakiness()` wrapper  

### ✔️ backend/services/pipeline.py
- Orchestrates normalization → classification → history fetching → scoring → DB save.

### ✔️ backend/db/models.py
Defines database tables.

### ✔️ backend/db/queries.py
SQL/ORM queries:
- fetch history  
- insert failures  
- insert run metadata  

---

## 4️⃣ Data Flow: How the System Works

### 1. Jenkins/LambdaTest calls POST /api/ingest
Includes test name, log, framework, run ID, website, etc.

### 2. Normalization
Raw log → normalized error signature.

### 3. Classification
ML model labels the failure.

### 4. History Fetching
DB checks:
- past failures  
- unique error messages  
- frameworks involved  
- total runs  

### 5. Flakiness Scoring
Using the formula in `flakiness.py` to compute a score 0–1.

### 6. Save to DB
Full structured record stored.

---

## 5️⃣ Current Status

### ✅ Ingestion works  
### ✅ Classification works  
### ✅ Flakiness scoring module complete  
### 🟡 Pending:
- DB integration for history  
- API for dashboard  
- Visual charts & reporting  

---

## 6️⃣ Future Roadmap

### Phase 1 — Backend stabilization  
- Connect DB history queries  
- Save flakiness scores  
- Add pipeline logging  

### Phase 2 — Dashboard APIs  
- `/stats`  
- `/flaky-tests`  
- `/runs/{id}`  
- `/tests/{name}`  

### Phase 3 — Frontend UI  
- Charts  
- Tables  
- Trends  
- Filters  

---