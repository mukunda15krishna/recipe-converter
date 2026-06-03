from database import SessionLocal
from models import Recipe, Ingredient

db = SessionLocal()

# Check if recipe already exists
existing = db.query(Recipe).filter(
    Recipe.name == "Brownie"
).first()

if not existing:

    recipe = Recipe(
        name="Brownie"
    )

    db.add(recipe)
    db.commit()
    db.refresh(recipe)

    ingredients = [

        Ingredient(
            recipe_id=recipe.id,
            name="Brownie Mix",
            quantity=600,
            unit="g"
        ),

        Ingredient(
            recipe_id=recipe.id,
            name="Cake Mix",
            quantity=600,
            unit="g"
        ),

        Ingredient(
            recipe_id=recipe.id,
            name="Oil",
            quantity=160,
            unit="ml"
        ),

        Ingredient(
            recipe_id=recipe.id,
            name="Water",
            quantity=640,
            unit="ml"
        )
    ]

    db.add_all(ingredients)
    db.commit()

    print("Brownie recipe added")

else:

    print("Recipe already exists")