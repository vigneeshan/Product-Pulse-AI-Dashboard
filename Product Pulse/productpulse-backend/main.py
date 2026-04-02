from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func
from pydantic import BaseModel
import requests
import models

# --- Database Setup ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./productpulse.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="ProductPulse API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Data Models for Frontend Input ---
class ProductInput(BaseModel):
    name: str
    category: str
    price: float
    review_text: str

# --- AI Sentiment Engine ---
def analyze_sentiment(text: str) -> float:
    """Uses Hugging Face API for sentiment, with a local fallback logic."""
    try:
        API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
        response = requests.post(API_URL, json={"inputs": text}, timeout=3)
        
        if response.status_code == 200:
            results = response.json()[0]
            # Convert the POSITIVE score to a 0.0 - 1.0 format
            for res in results:
                if res['label'] == 'POSITIVE':
                    return round(res['score'], 2)
            return 0.2 # If NEGATIVE is the highest label
            
        return fallback_sentiment(text)
    except:
        return fallback_sentiment(text)

def fallback_sentiment(text: str) -> float:
    """Safety fallback so the app never crashes if the free API is busy."""
    text_lower = text.lower()
    score = 0.5
    positive = ['great', 'awesome', 'good', 'love', 'amazing', 'perfect', 'best']
    negative = ['bad', 'terrible', 'awful', 'hate', 'poor', 'broken', 'worst', 'expensive']
    
    if any(word in text_lower for word in positive): score += 0.4
    if any(word in text_lower for word in negative): score -= 0.4
    return max(0.0, min(1.0, score))

# --- API Endpoints ---

@app.get("/api/dashboard/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    total_products = db.query(models.Product).count()
    avg_sentiment = db.query(func.avg(models.Review.sentiment_score)).scalar() or 0.0
    
    chart_data = []
    products = db.query(models.Product).all()

    # --- START OF REAL API LOGIC ---
    try:
        print("Attempting to fetch real API data from DummyJSON...")
        
        # Adding a User-Agent so the API doesn't think we are a spam bot
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        external_response = requests.get("https://dummyjson.com/products?limit=50", headers=headers, timeout=10)
        
        # DummyJSON puts the list inside a 'products' key
        external_data = external_response.json().get('products', []) 
        
        print(f"Success! Fetched {len(external_data)} competitor prices.")
    except Exception as e:
        print(f"API FAILED. Using Math Fallback. Reason: {e}")
        external_data = []
    # --- END OF REAL API LOGIC ---

    for index, p in enumerate(products):
        p_reviews = db.query(models.Review).filter(models.Review.product_id == p.id).all()
        sent_score = sum([r.sentiment_score for r in p_reviews]) / len(p_reviews) if p_reviews else 0.5
        
        # We try to get the price from the API response based on the loop index
        # If the API fails or index is out of bounds, we fall back to our math
        if index < len(external_data):
            comp_price = external_data[index]['price']
        else:
            comp_price = p.price * 0.90 
        
        chart_data.append({
            "name": (p.name[:10] + '..') if len(p.name) > 10 else p.name,
            "sentiment": round(sent_score, 2),
            "competitor_price": round(comp_price, 2)
        })

    return {
        "total_products": total_products,
        "average_product_sentiment": round(avg_sentiment, 2),
        "active_alerts": len([p for p in chart_data if p["sentiment"] < 0.5]), # Alert if sentiment drops
        "chart_data": chart_data
    }

@app.post("/api/products")
def add_product_and_analyze(product_data: ProductInput, db: Session = Depends(get_db)):
    # 1. Save new product
    new_product = models.Product(
        name=product_data.name,
        category=product_data.category,
        price=product_data.price,
        stock=100
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    # 2. Run AI Sentiment Analysis on the review
    ai_score = analyze_sentiment(product_data.review_text)

    # 3. Save the review and AI score
    new_review = models.Review(
        product_id=new_product.id,
        text=product_data.review_text,
        sentiment_score=ai_score
    )
    db.add(new_review)
    db.commit()

    return {"message": "Product and AI Review added successfully!"}