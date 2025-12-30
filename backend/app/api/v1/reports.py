from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import List, Dict, Any, Optional
from datetime import datetime, date
from decimal import Decimal
import io
import csv
from fastapi.responses import StreamingResponse
from app.db import get_db
from app.models.order import Order, ProductionRecord, ProfitRecord
from app.models.product import Product
from app.models.inventory import InventoryItem
from app.models.user import User
from app.auth import require_staff_or_admin

router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.get("/production")
def get_production_report(
    period: str = Query("monthly", regex="^(monthly|quarterly|yearly)$"),
    from_date: Optional[date] = Query(None),
    to_date: Optional[date] = Query(None),
    export_csv: bool = Query(False),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff_or_admin)
):
    """Get production report for specified period."""
    query = db.query(
        func.count(ProductionRecord.id).label("production_count"),
        func.date(ProductionRecord.completed_at).label("completion_date")
    ).filter(ProductionRecord.completed_at.isnot(None))
    
    if from_date:
        query = query.filter(ProductionRecord.completed_at >= from_date)
    
    if to_date:
        query = query.filter(ProductionRecord.completed_at <= to_date)
    
    if period == "monthly":
        query = query.group_by(
            extract('year', ProductionRecord.completed_at),
            extract('month', ProductionRecord.completed_at)
        )
    elif period == "quarterly":
        query = query.group_by(
            extract('year', ProductionRecord.completed_at),
            extract('quarter', ProductionRecord.completed_at)
        )
    elif period == "yearly":
        query = query.group_by(extract('year', ProductionRecord.completed_at))
    
    results = query.all()
    
    data = [
        {
            "production_count": r.production_count,
            "date": str(r.completion_date) if r.completion_date else None
        }
        for r in results
    ]
    
    if export_csv:
        # Generate CSV
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=["production_count", "date"])
        writer.writeheader()
        writer.writerows(data)
        
        response = StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv"
        )
        response.headers["Content-Disposition"] = f"attachment; filename=production_report_{period}.csv"
        return response
    
    return {"period": period, "data": data}


@router.get("/profit")
def get_profit_report(
    period: str = Query("monthly", regex="^(monthly|quarterly|yearly)$"),
    from_date: Optional[date] = Query(None),
    to_date: Optional[date] = Query(None),
    export_csv: bool = Query(False),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff_or_admin)
):
    """Get profit report for specified period."""
    query = db.query(
        func.sum(ProfitRecord.revenue).label("total_revenue"),
        func.sum(ProfitRecord.costs).label("total_costs"),
        func.sum(ProfitRecord.profit).label("total_profit"),
        ProfitRecord.date
    )
    
    if from_date:
        query = query.filter(ProfitRecord.date >= from_date)
    
    if to_date:
        query = query.filter(ProfitRecord.date <= to_date)
    
    if period == "monthly":
        query = query.group_by(
            extract('year', ProfitRecord.date),
            extract('month', ProfitRecord.date)
        )
    elif period == "quarterly":
        query = query.group_by(
            extract('year', ProfitRecord.date),
            extract('quarter', ProfitRecord.date)
        )
    elif period == "yearly":
        query = query.group_by(extract('year', ProfitRecord.date))
    
    results = query.all()
    
    data = [
        {
            "total_revenue": float(r.total_revenue) if r.total_revenue else 0,
            "total_costs": float(r.total_costs) if r.total_costs else 0,
            "total_profit": float(r.total_profit) if r.total_profit else 0,
            "date": str(r.date) if r.date else None
        }
        for r in results
    ]
    
    if export_csv:
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=["total_revenue", "total_costs", "total_profit", "date"])
        writer.writeheader()
        writer.writerows(data)
        
        response = StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv"
        )
        response.headers["Content-Disposition"] = f"attachment; filename=profit_report_{period}.csv"
        return response
    
    return {"period": period, "data": data}


@router.get("/pipeline")
def get_pipeline_view(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff_or_admin)
):
    """Get current production pipeline grouped by stage."""
    # Get active production records (started but not completed)
    active_records = db.query(ProductionRecord).filter(
        ProductionRecord.started_at.isnot(None),
        ProductionRecord.completed_at.is_(None)
    ).all()
    
    # Group by stage
    pipeline = {}
    for record in active_records:
        stage = record.stage_name
        if stage not in pipeline:
            pipeline[stage] = []
        
        pipeline[stage].append({
            "id": record.id,
            "order_id": record.order_id,
            "order_item_id": record.order_item_id,
            "product_id": record.product_id,
            "started_at": record.started_at.isoformat() if record.started_at else None,
            "operator_id": record.operator_id,
            "notes": record.notes
        })
    
    return {"pipeline": pipeline}


@router.get("/inventory-valuation")
def get_inventory_valuation(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff_or_admin)
):
    """Calculate total inventory valuation."""
    items = db.query(InventoryItem).all()
    
    total_value = sum(float(item.quantity) * float(item.cost_per_unit) for item in items)
    
    items_detail = [
        {
            "id": item.id,
            "name": item.name,
            "sku": item.sku,
            "quantity": float(item.quantity),
            "cost_per_unit": float(item.cost_per_unit),
            "total_value": float(item.quantity) * float(item.cost_per_unit)
        }
        for item in items
    ]
    
    return {
        "total_valuation": total_value,
        "items": items_detail
    }
