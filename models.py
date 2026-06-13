from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship


from datetime import datetime
from database import Base


class Recipe(Base):

    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True)

    name = Column(String, unique=True)

    notes = Column(
        Text,
        nullable=True
    )

    ingredients = relationship(
        "Ingredient",
        back_populates="recipe",
        cascade="all, delete"
    )

    note_requests = relationship(
    "NoteRequest",
    back_populates="recipe"
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

class NoteRequest(Base):

    __tablename__ = "note_requests"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    recipe_id = Column(
        Integer,
        ForeignKey("recipes.id")
    )

    request_type = Column(String)

    note_content = Column(Text)

    status = Column(String)

    created_at = Column(String)
    
    submitted_by = Column(String)

    recipe = relationship(
        "Recipe",
        back_populates="note_requests"
    )