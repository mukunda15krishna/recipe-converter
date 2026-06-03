from fastapi import FastAPI, Request, Form ,Cookie
from fastapi.responses import (HTMLResponse,RedirectResponse)
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.responses import RedirectResponse
from fastapi import Depends

from database import SessionLocal
from models import Recipe, Ingredient
from models import ProductionHistory
from typing import List
from openpyxl import Workbook
from sqlalchemy.orm import Session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    db = SessionLocal()

    recipes = db.query(Recipe).all()

    response = templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "recipes": recipes
        }
    )

    db.close()

    return response

@app.get("/recipes", response_class=HTMLResponse)
def recipes(request: Request):

    db = SessionLocal()

    recipes = db.query(Recipe).all()

    response = templates.TemplateResponse(
        request=request,
        name="recipes.html",
        context={
            "recipes": recipes
        }
    )

    db.close()

    return response


@app.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...)
):

    if (
        username == "admin"
        and
        password == "brownie123"
    ):

        response = RedirectResponse(
            url="/admin",
            status_code=302
        )

        response.set_cookie(
            key="logged_in",
            value="yes"
        )

        return response

    return HTMLResponse(
        """
        <h2>Invalid Login</h2>

        <a href="/login">
            Try Again
        </a>
        """
    )

    if (
        username == "admin"
        and
        password == "Admin123"
    ):

        response = RedirectResponse(
            url="/admin",
            status_code=302
        )

        response.set_cookie(
            key="logged_in",
            value="yes"
        )

        return response

    return HTMLResponse(
        """
        <h2>Invalid Login</h2>

        <a href='/login'>
            Try Again
        </a>
        """
    )

@app.get("/logout")
def logout():

    response = RedirectResponse(
        url="/login",
        status_code=302
    )

    response.delete_cookie(
        key="logged_in"
    )

    return response

from fastapi import Cookie

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )

@app.get("/admin", response_class=HTMLResponse)
def admin(
    request: Request,
    logged_in: str = Cookie(None)
):

    if logged_in != "yes":

        return RedirectResponse(
            url="/login",
            status_code=302
        )

    db = SessionLocal()

    recipes = db.query(Recipe).all()

    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={
            "recipes": recipes
        }
    )

    db.close()

    return response


@app.get("/recipe/{recipe_id}",
         response_class=HTMLResponse)
def recipe_detail(
    request: Request,
    recipe_id: int
):

    db = SessionLocal()

    recipe = db.query(Recipe).filter(
        Recipe.id == recipe_id
    ).first()

    response = templates.TemplateResponse(
        request=request,
        name="recipe_detail.html",
        context={
            "recipe": recipe
        }
    )

    db.close()

    return response


@app.get("/delete_ingredient/{ingredient_id}")
def delete_ingredient(ingredient_id: int):

    db = SessionLocal()

    ingredient = db.query(
        Ingredient
    ).filter(
        Ingredient.id == ingredient_id
    ).first()

    if ingredient is None:

        db.close()

        return HTMLResponse(
            "<h2>Ingredient Not Found</h2>"
        )

    recipe_id = ingredient.recipe_id

    db.delete(ingredient)

    db.commit()

    db.close()

    return RedirectResponse(
        url=f"/admin_recipe/{recipe_id}",
        status_code=302
    )

@app.get("/delete_recipe/{recipe_id}")
def delete_recipe(recipe_id: int):

    db = SessionLocal()

    recipe = db.query(Recipe).filter(
        Recipe.id == recipe_id
    ).first()

    if recipe is None:

        db.close()

        return HTMLResponse(
            "<h2>Recipe Not Found</h2>"
        )

    for ingredient in recipe.ingredients:

        db.delete(ingredient)

    db.delete(recipe)

    db.commit()

    db.close()

    return RedirectResponse(
    url="/admin",
    status_code=302
)

@app.get("/edit_recipe/{recipe_id}",
         response_class=HTMLResponse)
def edit_recipe(recipe_id: int):

    db = SessionLocal()

    recipe = db.query(
        Recipe
    ).filter(
        Recipe.id == recipe_id
    ).first()

    html = f"""
    <h1>Edit Recipe</h1>

    <form action="/update_recipe/{recipe.id}"
          method="post">

        <input
            type="text"
            name="recipe_name"
            value="{recipe.name}"
            required>

        <br><br>

        <button type="submit">
            Update Recipe
        </button>

    </form>
    """
    db.close()

    return HTMLResponse(content=html)

@app.post("/update_recipe/{recipe_id}")
def update_recipe(
    recipe_id: int,
    recipe_name: str = Form(...)
):

    db = SessionLocal()

    recipe = db.query(
        Recipe
    ).filter(
        Recipe.id == recipe_id
    ).first()

    recipe.name = recipe_name

    db.commit()

    db.close()

    return RedirectResponse(
        url=f"/admin_recipe/{recipe_id}",
        status_code=302
    )

@app.post("/update_ingredient/{ingredient_id}")
def update_ingredient(
    ingredient_id: int,
    ingredient_name: str = Form(...),
    quantity: float = Form(...),
    unit: str = Form(...)
):

    db = SessionLocal()

    ingredient = db.query(
        Ingredient
    ).filter(
        Ingredient.id == ingredient_id
    ).first()

    ingredient.name = ingredient_name
    ingredient.quantity = quantity
    ingredient.unit = unit

    recipe_id = ingredient.recipe_id

    db.commit()

    db.close()

    return RedirectResponse(
        url=f"/admin_recipe/{recipe_id}",
        status_code=302
    )

@app.get("/edit_ingredient/{ingredient_id}",
         response_class=HTMLResponse)
def edit_ingredient(ingredient_id: int):

    db = SessionLocal()

    ingredient = db.query(Ingredient).filter(
        Ingredient.id == ingredient_id
    ).first()

    html = f"""
    <h1>Edit Ingredient</h1>

    <form action="/update_ingredient/{ingredient.id}"
          method="post">

    Name

    <br>

    <input
        type="text"
        name="ingredient_name"
        value="{ingredient.name}"
        required>

    <br><br>

    Quantity

    <br>

    <input
        type="number"
        step="0.01"
        name="quantity"
        value="{ingredient.quantity}"
        required>

    <br><br>

    Unit

    <br>

    <input
        type="text"
        name="unit"
        value="{ingredient.unit}"
        required>

    <br><br>

    <button type="submit">
        Update Ingredient
    </button>

    </form>
    """
    db.close()

    return HTMLResponse(content=html)


@app.post("/add_ingredient/{recipe_id}")
def add_ingredient(
    recipe_id: int,
    ingredient_name: str = Form(...),
    quantity: float = Form(...),
    unit: str = Form(...)
):

    db = SessionLocal()

    ingredient = Ingredient(
        recipe_id=recipe_id,
        name=ingredient_name,
        quantity=quantity,
        unit=unit
    )

    db.add(ingredient)
    db.commit()

    db.close()

    return HTMLResponse(
        f"""
        <h2>Ingredient Added Successfully</h2>

        <a href="/recipe/{recipe_id}">
            Back To Recipe
        </a>
        """
    )

@app.post("/create_recipe")
def create_recipe(
    recipe_name: str = Form(...)
):
    db = SessionLocal()

    recipe = db.query(Recipe).filter(
        Recipe.name == recipe_name
    ).first()

    if recipe:

        db.close()

        return HTMLResponse(
            """
            <h2>
                ⚠️ Recipe Already Exists
            </h2>

            <br>

            <a href="/admin">
                Back To Admin
            </a>
            """
        )

    recipe = Recipe(
        name=recipe_name
    )

    db.add(recipe)
    db.commit()

    db.close()

    return HTMLResponse(
        """
        <h2>
            ✅ Recipe Created Successfully
        </h2>

        <br>

        <a href="/admin">
            Back To Admin
        </a>
        """
    )



@app.post("/add_ingredient_admin")
def add_ingredient_admin(
    recipe_id: int = Form(...),
    ingredient_name: List[str] = Form(...),
    quantity: List[float] = Form(...),
    unit: List[str] = Form(...)
):
    db = SessionLocal()

    existing_ingredients = db.query(
        Ingredient
    ).filter(
        Ingredient.recipe_id == recipe_id
    ).all()

    existing_names = [
        item.name.strip().lower()
        for item in existing_ingredients
    ]

    for i in range(len(ingredient_name)):

        current_name = (
            ingredient_name[i]
            .strip()
            .lower()
        )

        if current_name in existing_names:

            db.close()

            return HTMLResponse(
                f"""
                <h2>
                    ⚠️ Ingredient '{ingredient_name[i]}' Already Exists
                </h2>

                <br>

                <a href="/admin">
                    ↩ Back To Admin
                </a>
                """
            )

        ingredient = Ingredient(
            recipe_id=recipe_id,
            name=ingredient_name[i].strip(),
            quantity=quantity[i],
            unit=unit[i].strip()
        )

        db.add(ingredient)

    db.commit()
    db.close()

    return HTMLResponse(
        """
        <h2>
            ✅ All Ingredients Added Successfully
        </h2>

        <br>

        <a href="/admin">
            ↩ Back To Admin
        </a>
        """
    )

@app.get("/admin_recipe/{recipe_id}")
def admin_recipe(
    recipe_id: int,
    request: Request,
    logged_in: str = Cookie(None),
    db: Session = Depends(get_db)
):

    if logged_in != "yes":


        return RedirectResponse(
            url="/login",
            status_code=302
        )

    recipe = db.query(Recipe).filter(
        Recipe.id == recipe_id
    ).first()

    

    return templates.TemplateResponse(
        request=request,
        name="admin_recipe.html",
        context={
            "recipe": recipe
        }
    )

@app.post("/save_recipe")
def save_recipe(
    recipe_name: str = Form(...),
    ingredient_name: List[str] = Form(...),
    quantity: List[float] = Form(...),
    unit: List[str] = Form(...)
):
    db = SessionLocal()

    recipe = db.query(Recipe).filter(
        Recipe.name == recipe_name
    ).first()

    if not recipe:

        recipe = Recipe(
            name=recipe_name
        )

        db.add(recipe)
        db.commit()
        db.refresh(recipe)

    recipe_id = recipe.id
    

    existing_ingredients = db.query(
        Ingredient
    ).filter(
        Ingredient.recipe_id == recipe_id
    ).all()

    existing_names = [
        item.name.strip().lower()
        for item in existing_ingredients
    ]

    for i in range(len(ingredient_name)):

        current_name = (
            ingredient_name[i]
            .strip()
            .lower()
        )

        if current_name in existing_names:

            db.close()

            return HTMLResponse(
                f"""
                <h2>
                    ⚠️ Ingredient '{ingredient_name[i]}' Already Exists
                </h2>

                <br>

                <a href="/admin">
                    ↩ Back To Admin
                </a>
                """
            )

        ingredient = Ingredient(
            recipe_id=recipe_id,
            name=ingredient_name[i].strip(),
            quantity=quantity[i],
            unit=unit[i].strip()
        )

        db.add(ingredient)

    db.commit()

    db.close()

    return HTMLResponse(
        """
        <h2>
            ✅ All Ingredients Added Successfully
        </h2>

        <br>

        <a href="/admin">
            ↩ Back To Admin
        </a>
        """
    )

@app.get("/history", response_class=HTMLResponse)
def history(request: Request):

    db = SessionLocal()

    records = db.query(
        ProductionHistory
    ).order_by(
        ProductionHistory.id.desc()
    ).all()

    html = """
    <h1>Production History</h1>

    <table border='1' cellpadding='10'>

    <tr>
        <th>Date</th>
        <th>Recipe</th>
        <th>Desired Weight</th>
    </tr>
    """

    for record in records:

        html += f"""
        <tr>
            <td>{record.created_at}</td>
            <td>{record.recipe_name}</td>
            <td>{record.desired_weight} g</td>
        </tr>
        """

    html += """
        </table>

        <br><br>

        <a href='/export_excel'>
            Export Excel
        </a>

        <br><br>

        <a href='/recipes'>
    Back To Dashboard
        </a>
    """
    db.close()

    return HTMLResponse(content=html)

@app.get("/export_excel")
def export_excel():

    db = SessionLocal()

    records = db.query(
        ProductionHistory
    ).all()

    wb = Workbook()

    ws = wb.active

    ws.title = "Production History"

    ws.append([
        "Date",
        "Recipe",
        "Desired Weight"
    ])

    for record in records:

        ws.append([
            record.created_at,
            record.recipe_name,
            record.desired_weight
        ])

    file_name = "Production_History.xlsx"

    wb.save(file_name)

    db.close()

    return FileResponse(
        path=file_name,
        filename=file_name,
        media_type=
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@app.post("/calculate", response_class=HTMLResponse)
def calculate(
    recipe_id: int = Form(...),
    desired_weight: float = Form(...)
):
    db = SessionLocal()

    recipe = db.query(Recipe).filter(
        Recipe.id == recipe_id
    ).first()

    total_recipe_weight = sum(
        ingredient.quantity
        for ingredient in recipe.ingredients
    )

    factor = desired_weight / total_recipe_weight

    from datetime import datetime

    history = ProductionHistory(
        recipe_name=recipe.name,
        desired_weight=desired_weight,
        created_at=datetime.now().strftime(
            "%d-%m-%Y %H:%M"
        )
    )

    db.add(history)
    db.commit()

    html = f"""
    <h1>{recipe.name}</h1>

    <table border='1' cellpadding='10'>
        <tr>
            <th>Ingredient</th>
            <th>Required Quantity</th>
        </tr>
    """

    for ingredient in recipe.ingredients:
        qty = round(ingredient.quantity * factor, 2)

        html += f"""
        <tr>
            <td>{ingredient.name}</td>
            <td>{qty} {ingredient.unit}</td>
        </tr>
        """

    html += """
    </table>

    <br>

    <a href="/">Back</a>
    """
    db.close()
    return HTMLResponse(content=html)
