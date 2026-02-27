from fastapi import APIRouter, HTTPException
from pathlib import Path
import json


router = APIRouter(prefix="/api/catalog", tags=["Catalog"])


def _read_json_file(path: Path) -> dict:
    """Read a JSON file and return its content as a dict."""
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail=f"JSON file not found: {path.name}")
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=500, detail=f"Invalid JSON in {path.name}: {exc}")


@router.get("/codes")
def get_catalog_codes() -> dict:
    """Return catalog coding system (categories, materials, finishes, sizes)."""
    # app/api/v1 -> app -> backend
    base_dir = Path(__file__).resolve().parents[2].parent
    codes_path = base_dir / "data" / "catalog_codes.json"
    return _read_json_file(codes_path)


@router.get("/category-template")
def get_category_template() -> dict:
    """Return the original category.json structure used for seeding categories."""
    base_dir = Path(__file__).resolve().parents[2].parent
    category_path = base_dir / "data" / "category.json"
    return _read_json_file(category_path)
