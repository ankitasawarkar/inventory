"""Utility script to load categories from backend/data/category.json.

Run inside Docker:
    docker-compose exec backend python load_categories_from_json.py
"""
import json
from pathlib import Path

from sqlalchemy.orm import Session

from app.db import SessionLocal, init_db
from app.models.category import Category


# In the Docker container, /app is mounted to backend/, and data/ is /app/data
DATA_PATH = Path(__file__).parent / "data" / "category.json"


def slugify(name: str) -> str:
    """Simple slug generator: lower-case, replace spaces/& with dashes, remove commas."""
    s = name.strip().lower()
    for ch in ["&", "/"]:
        s = s.replace(ch, " and ")
    for ch in [",", "'", ":", ";"]:
        s = s.replace(ch, "")
    s = "-".join(s.split())
    return s


def load_categories_from_json() -> None:
    init_db()
    db: Session = SessionLocal()

    try:
        if not DATA_PATH.exists():
            raise FileNotFoundError(f"category.json not found at {DATA_PATH}")

        with DATA_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)

        root_block = data.get("wood_furniture", {})

        for top_name, sub_block in root_block.items():
            # Create or get top-level category (e.g., "Living Room")
            top_slug = slugify(top_name)
            top_category = (
                db.query(Category)
                .filter(Category.slug == top_slug)
                .first()
            )
            if not top_category:
                top_category = Category(name=top_name, slug=top_slug, parent_id=None)
                db.add(top_category)
                db.flush()  # assign id

            # sub_block is a dict of subcategory name -> list of product names
            for sub_name in sub_block.keys():
                sub_slug = slugify(f"{top_name}-{sub_name}")
                existing = (
                    db.query(Category)
                    .filter(Category.slug == sub_slug)
                    .first()
                )
                if existing:
                    continue

                sub_category = Category(
                    name=sub_name,
                    slug=sub_slug,
                    parent_id=top_category.id,
                )
                db.add(sub_category)

        db.commit()
        print("✅ Categories loaded from category.json")
    except Exception as exc:
        db.rollback()
        print(f"❌ Error loading categories: {exc}")
    finally:
        db.close()


if __name__ == "__main__":
    load_categories_from_json()
