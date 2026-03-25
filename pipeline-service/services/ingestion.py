import requests
from sqlalchemy.orm import Session
from models.customer import Customer

API_URL = "http://mock-server:5000/api/customers"


def ingest_customers(db: Session):
    page = 1
    limit = 10
    total_processed = 0

    try:
        while True:
            response = requests.get(API_URL, params={"page": page, "limit": limit})
            response.raise_for_status()
            data = response.json()

            customers = data.get("data", [])
            if not customers:
                break

            for cust in customers:
                existing = db.query(Customer).filter(Customer.customer_id == cust["customer_id"]).first()

                if existing:
                    # Update existing
                    for key, value in cust.items():
                        setattr(existing, key, value)
                else:
                    # Insert new
                    new_customer = Customer(**cust)
                    db.add(new_customer)

                total_processed += 1

            db.commit()
            page += 1

        return total_processed

    except Exception as e:
        db.rollback()
        raise e
