from database import SessionLocal
from models import Recipe

db = SessionLocal()

recipes = db.query(Recipe).all()

for recipe in recipes:

    print("\nRecipe:", recipe.name)

    for ingredient in recipe.ingredients:

        print(
            ingredient.name,
            ingredient.quantity,
            ingredient.unit
        )