from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool

DATABASE_URL = "sqlite:///recipe.db"

import os

print("DATABASE PATH:")
print(os.path.abspath("recipe.db"))

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=NullPool
)


def ensure_recipe_output_columns():
    with engine.begin() as conn:
        columns = conn.execute(text("PRAGMA table_info(recipes)")).fetchall()
        existing = {column[1] for column in columns}

        if "output_quantity" not in existing:
            conn.execute(text("ALTER TABLE recipes ADD COLUMN output_quantity FLOAT"))

        if "output_unit" not in existing:
            conn.execute(text("ALTER TABLE recipes ADD COLUMN output_unit VARCHAR"))


ensure_recipe_output_columns()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()