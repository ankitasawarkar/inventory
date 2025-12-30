from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
import json
from datetime import datetime
from app.db import get_db
from app.models.cart import Cart, CartItem
from app.models.product import Product
from app.models.user import User
from app.schemas.cart import CartItemCreate, CartItemUpdate, CartResponse
from app.auth import get_current_active_user, get_optional_user

router = APIRouter(prefix="/api/cart", tags=["Cart"])


@router.post("", response_model=CartResponse)
def get_or_create_cart(
    session_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    """Get or create a cart for the current user or session."""
    if current_user:
        cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
        if not cart:
            cart = Cart(user_id=current_user.id)
            db.add(cart)
            db.commit()
            db.refresh(cart)
    elif session_id:
        cart = db.query(Cart).filter(Cart.session_id == session_id).first()
        if not cart:
            cart = Cart(session_id=session_id)
            db.add(cart)
            db.commit()
            db.refresh(cart)
    else:
        raise HTTPException(status_code=400, detail="User or session ID required")
    
    return cart


@router.get("/{cart_id}", response_model=CartResponse)
def get_cart(cart_id: int, db: Session = Depends(get_db)):
    """Get cart details."""
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart


@router.post("/{cart_id}/items")
def add_to_cart(
    cart_id: int,
    item_data: CartItemCreate,
    db: Session = Depends(get_db)
):
    """Add an item to the cart."""
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    # Verify product exists
    product = db.query(Product).filter(Product.id == item_data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if item already in cart
    existing_item = db.query(CartItem).filter(
        CartItem.cart_id == cart_id,
        CartItem.product_id == item_data.product_id
    ).first()
    
    if existing_item:
        existing_item.quantity += item_data.quantity
        existing_item.selected_options = item_data.selected_options
    else:
        cart_item = CartItem(**item_data.model_dump(), cart_id=cart_id)
        db.add(cart_item)
    
    cart.updated_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Item added to cart successfully"}


@router.delete("/{cart_id}/items/{item_id}")
def remove_from_cart(
    cart_id: int,
    item_id: int,
    db: Session = Depends(get_db)
):
    """Remove an item from the cart."""
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart_id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    db.delete(cart_item)
    
    # Update cart timestamp
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if cart:
        cart.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {"message": "Item removed from cart successfully"}
