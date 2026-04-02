from sqlalchemy.orm import Session
from main import SessionLocal, engine
import models
import random

def seed_data():
    db = SessionLocal()
    
    if db.query(models.Product).count() > 0:
        print("Database already has data!")
        return

    print("Adding dummy products to the database...")
    
    products = [
        {"name": "Wireless Noise-Canceling Headphones", "category": "Electronics", "price": 299.99, "stock": 150},
        {"name": "Ergonomic Office Chair", "category": "Furniture", "price": 199.50, "stock": 45},
        {"name": "Smart Fitness Watch", "category": "Electronics", "price": 149.00, "stock": 300}
    ]

    for p_data in products:
        product = models.Product(**p_data)
        db.add(product)
        db.commit()
        db.refresh(product)

        for _ in range(5):
            review = models.Review(
                product_id=product.id,
                text="Great product!" if random.random() > 0.5 else "Could be better.",
                sentiment_score=round(random.uniform(0.4, 0.95), 2)
            )
            db.add(review)
            
    db.commit()
    db.close()
    print("Done! Database is ready.")

if __name__ == "__main__":
    seed_data()