from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from database import Base


class Recipe(Base):

    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    ingredients = relationship(
        "Ingredient",
        back_populates="recipe",
        cascade="all, delete"
    )


class Ingredient(Base):

    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True)

    recipe_id = Column(
        Integer,
        ForeignKey("recipes.id")
    )

    name = Column(String)

    quantity = Column(Float)

    unit = Column(String)

    recipe = relationship(
        "Recipe",
        back_populates="ingredients"
    )

class ProductionHistory(Base):

    __tablename__ = "production_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    recipe_name = Column(String)

    desired_weight = Column(Float)

    created_at = Column(
        String
    )
