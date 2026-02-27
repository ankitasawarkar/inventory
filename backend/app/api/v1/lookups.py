from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.lookup import Lookup
from app.auth import require_admin
from app.schemas.lookup import LookupCreate, LookupUpdate, LookupResponse


router = APIRouter(prefix="/api/lookups", tags=["Lookups"])


@router.get("", response_model=List[LookupResponse])
def list_lookups(
    set: Optional[str] = Query(None, description="Filter by lookup set"),
    scope: Optional[str] = Query(None, description="Filter by scope, e.g. GLOBAL or TENANT"),
    search: Optional[str] = Query(None, description="Search in key/value/description"),
    include_inactive: bool = Query(False, description="Include inactive lookups"),
    db: Session = Depends(get_db),
):
    """List lookup values, optionally filtered by set/scope/search.

    This endpoint is intentionally public (no auth) so both admin UI and
    customer-facing forms can consume dropdown values.
    """
    query = db.query(Lookup)

    if set:
        query = query.filter(Lookup.set == set)
    if scope:
        query = query.filter(Lookup.scope == scope)
    if not include_inactive:
        query = query.filter(Lookup.is_active.is_(True))
    if search:
        like = f"%{search}%"
        query = query.filter(
            (Lookup.key.ilike(like))
            | (Lookup.value.ilike(like))
            | (Lookup.description.ilike(like))
        )

    items = query.order_by(Lookup.set, Lookup.order_by, Lookup.value).all()
    return items


@router.post("", response_model=LookupResponse)
def create_lookup(
    lookup_in: LookupCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Create a new lookup value (admin only)."""
    # Optional uniqueness check within a set
    existing = (
        db.query(Lookup)
        .filter(Lookup.set == lookup_in.set, Lookup.key == lookup_in.key)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Lookup with this set and key already exists",
        )

    lookup = Lookup(**lookup_in.model_dump())
    db.add(lookup)
    db.commit()
    db.refresh(lookup)
    return lookup


@router.put("/{lookup_id}", response_model=LookupResponse)
def update_lookup(
    lookup_id: int,
    lookup_in: LookupUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Update an existing lookup value (admin only)."""
    lookup = db.query(Lookup).filter(Lookup.id == lookup_id).first()
    if not lookup:
        raise HTTPException(status_code=404, detail="Lookup not found")

    update_data = lookup_in.model_dump(exclude_unset=True)

    # If set/key changed, enforce uniqueness inside the new set
    new_set = update_data.get("set", lookup.set)
    new_key = update_data.get("key", lookup.key)
    if new_set != lookup.set or new_key != lookup.key:
        exists = (
            db.query(Lookup)
            .filter(Lookup.set == new_set, Lookup.key == new_key, Lookup.id != lookup.id)
            .first()
        )
        if exists:
            raise HTTPException(
                status_code=400,
                detail="Another lookup with this set and key already exists",
            )

    for field, value in update_data.items():
        setattr(lookup, field, value)

    db.commit()
    db.refresh(lookup)
    return lookup


@router.delete("/{lookup_id}")
def delete_lookup(
    lookup_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Delete a lookup value (admin only).

    For safety you might later turn this into a soft delete by toggling
    is_active instead of removing the row.
    """
    lookup = db.query(Lookup).filter(Lookup.id == lookup_id).first()
    if not lookup:
        raise HTTPException(status_code=404, detail="Lookup not found")

    db.delete(lookup)
    db.commit()
    return {"message": "Lookup deleted"}
