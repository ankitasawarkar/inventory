from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import json
from datetime import datetime, date
from decimal import Decimal
from app.db import get_db
from app.models.order import Order, OrderItem, OrderStatus
from app.models.cart import Cart, CartItem
from app.models.product import Product
from app.models.user import User
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse
from app.auth import require_staff_or_admin, get_current_active_user

router = APIRouter(prefix="/api/orders", tags=["Orders"])


def generate_order_number() -> str:
    """Generate a unique order number."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"ORD-{timestamp}"


@router.get("", response_model=List[OrderResponse])
def list_orders(
    status: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff_or_admin)
):
    """List all orders with optional status filter."""
    query = db.query(Order)
    
    if status:
        query = query.filter(Order.status == status)
    
    orders = query.order_by(Order.created_at.desc()).offset(skip).limit(limit).all()
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get order details including items and pipeline status."""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post("", response_model=OrderResponse)
def create_order(
    order_data: OrderCreate,
    cart_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Create an order from cart or directly with items."""
    order_items_data = []
    total_amount = Decimal("0.00")
    
    if cart_id:
        # Create order from cart
        cart = db.query(Cart).filter(Cart.id == cart_id).first()
        if not cart or not cart.items:
            raise HTTPException(status_code=404, detail="Cart not found or empty")
        
        for cart_item in cart.items:
            product = db.query(Product).filter(Product.id == cart_item.product_id).first()
            if not product:
                continue
            
            # Create product snapshot
            snapshot = {
                "id": product.id,
                "title": product.title,
                "base_price": float(product.base_price),
                "description": product.description,
            }
            
            unit_price = product.base_price
            subtotal = unit_price * cart_item.quantity
            total_amount += subtotal
            
            order_items_data.append({
                "product_snapshot": json.dumps(snapshot),
                "quantity": cart_item.quantity,
                "custom_requirements": cart_item.selected_options,
                "unit_price": unit_price,
                "subtotal": subtotal
            })
    else:
        # Create order from provided items
        for item in order_data.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if not product:
                raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
            
            snapshot = {
                "id": product.id,
                "title": product.title,
                "base_price": float(product.base_price),
                "description": product.description,
            }
            
            unit_price = product.base_price
            subtotal = unit_price * item.quantity
            total_amount += subtotal
            
            order_items_data.append({
                "product_snapshot": json.dumps(snapshot),
                "quantity": item.quantity,
                "custom_requirements": item.custom_requirements,
                "unit_price": unit_price,
                "subtotal": subtotal
            })
    
    # Create order
    order = Order(
        order_number=generate_order_number(),
        customer_name=order_data.customer_name,
        customer_contact=order_data.customer_contact,
        customer_email=order_data.customer_email,
        total_amount=total_amount,
        notes=order_data.notes,
        is_custom=order_data.is_custom,
        expected_delivery_date=order_data.expected_delivery_date,
        status=OrderStatus.PENDING
    )
    db.add(order)
    db.flush()
    
    # Create order items
    for item_data in order_items_data:
        order_item = OrderItem(order_id=order.id, **item_data)
        db.add(order_item)
    
    # Clear cart if used
    if cart_id:
        db.query(CartItem).filter(CartItem.cart_id == cart_id).delete()
    
    db.commit()
    db.refresh(order)
    
    return order


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    order_data: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff_or_admin)
):
    """Update order details."""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    update_data = order_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(order, field, value)
    
    db.commit()
    db.refresh(order)
    
    return order
