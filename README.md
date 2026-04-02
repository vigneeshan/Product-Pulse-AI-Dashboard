# 📈 ProductPulse AI Dashboard

ProductPulse is a full-stack market intelligence dashboard designed to track product metrics, monitor competitor pricing, and perform real-time Natural Language Processing (NLP) sentiment analysis on customer reviews.

## 🚀 The Business Value
Traditional market analysis requires manual data entry and human review reading. ProductPulse automates this pipeline:
* **Automated Competitor Tracking:** Integrates with external REST APIs to fetch real-time market pricing, replacing manual data entry.
* **Instant AI Sentiment Analysis:** Routes customer reviews through Hugging Face's DistilBERT NLP models to instantly calculate product health scores, removing human bias and drastically reducing analysis time.
* **Dynamic Visualization:** Maps AI sentiment against competitor pricing via interactive dual-axis charts to identify market opportunities at a glance.

## 🛠️ Tech Stack
* **Frontend:** React.js, Vite, Tailwind CSS, Recharts, Axios
* **Backend:** Python, FastAPI, SQLAlchemy, Pydantic, Requests
* **Database:** SQLite (Easily scalable to PostgreSQL)
* **AI/ML:** Hugging Face Inference API (Sentiment Analysis)

## 💻 How to Run Locally

### 1. Backend Setup
Navigate to the backend folder, install dependencies, and start the FastAPI server:
```bash
cd productpulse-backend
pip install -r ../requirements.txt
uvicorn main:app --reload