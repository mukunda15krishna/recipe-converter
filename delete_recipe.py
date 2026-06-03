from database import SessionLocal
from models import Recipe

db = SessionLocal()

recipe = db.query(Recipe).filter(
    Recipe.name == "uvicorn main:app --reload"
).first()

if recipe:
    db.delete(recipe)
    db.commit()
    print("Deleted")
else:
    print("Not Found")