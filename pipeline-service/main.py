from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models.customer import Customer
from services.ingestion import ingest_customers

app = FastAPI()


# Create tables on startup
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/api/ingest")
def run_ingestion(db: Session = Depends(get_db)):
    try:
        count = ingest_customers(db)
        return {"status": "success", "records_processed": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/customers")
def get_customers(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Invalid pagination parameters")

    try:
        total = db.query(Customer).count()
        offset = (page - 1) * limit

        customers = db.query(Customer).offset(offset).limit(limit).all()

        return {
            "data": customers,
            "total": total,
            "page": page,
            "limit": limit
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: str, db: Session = Depends(get_db)):
    try:
        customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        return customer
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
