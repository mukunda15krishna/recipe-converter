from database import SessionLocal
from models import ProductionHistory

db = SessionLocal()

records = db.query(
    ProductionHistory
).all()

print("History Records:", len(records))