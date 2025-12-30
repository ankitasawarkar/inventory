from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import json
import uuid as uuid_lib
from app.db import get_db
from app.models.product import Product, ProductDevelopmentStage, ProductImage
from app.models.category import Category
from app.models.user import User
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductListResponse,
    ProductDevelopmentStageCreate,
    ProductDevelopmentStageUpdate,
    ProductDevelopmentStageResponse,
)
from app.auth import require_admin, require_staff_or_admin, get_current_active_user
from app.services.file_storage import file_storage

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.get("", response_model=List[ProductListResponse])
def list_products(
    category: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """List products with filtering and pagination."""
    query = db.query(Product)
    
    if category:
        query = query.filter(Product.category_id == category)
    
    if status:
        query = query.filter(Product.status == status)
    
    if search:
        query = query.filter(Product.title.ilike(f"%{search}%"))
    
    products = query.offset(skip).limit(limit).all()
    return products


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get detailed product information including stages and images."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("", response_model=ProductResponse)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff_or_admin)
):
    """Create a new product."""
    # Verify category exists
    category = db.query(Category).filter(Category.id == product_data.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Check SKU uniqueness if provided
    if product_data.sku:
        if db.query(Product).filter(Product.sku == product_data.sku).first():
            raise HTTPException(status_code=400, detail="SKU already exists")
    
    product = Product(
        **product_data.model_dump(),
        created_by=current_user.id
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    
    return product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff_or_admin)
):
    """Update a product."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check SKU uniqueness if being updated
    if product_data.sku and product_data.sku != product.sku:
        if db.query(Product).filter(Product.sku == product_data.sku).first():
            raise HTTPException(status_code=400, detail="SKU already exists")
    
    update_data = product_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    db.commit()
    db.refresh(product)
    
    return product


@router.post("/{product_id}/replicate", response_model=ProductResponse)
def replicate_product(
    product_id: int,
    copy_images: bool = Query(False, description="Whether to physically copy image files"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Replicate a product with all its stages (admin only)."""
    original = db.query(Product).filter(Product.id == product_id).first()
    if not original:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Create new product
    new_product = Product(
        uuid=str(uuid_lib.uuid4()),
        title=f"{original.title} (Copy)",
        sku=None,  # Will need to be set manually
        category_id=original.category_id,
        subcategory_id=original.subcategory_id,
        description=original.description,
        base_price=original.base_price,
        is_customizable=original.is_customizable,
        status=original.status,
        created_by=current_user.id
    )
    db.add(new_product)
    db.flush()
    
    # Copy development stages
    for stage in original.development_stages:
        new_stage = ProductDevelopmentStage(
            product_id=new_product.id,
            stage_order=stage.stage_order,
            stage_name=stage.stage_name,
            stage_description=stage.stage_description,
            materials_used=stage.materials_used,
            labor_hours_estimate=stage.labor_hours_estimate,
            expected_days=stage.expected_days,
            quality_checklist=stage.quality_checklist,
            stage_status=stage.stage_status,
            notes=stage.notes
        )
        db.add(new_stage)
        db.flush()
        
        # Copy images (reference by default, physical copy if requested)
        for img in stage.images:
            new_image = ProductImage(
                product_id=new_product.id,
                stage_id=new_stage.id,
                file_path=img.file_path,  # Reference same file
                original_name=img.original_name,
                width=img.width,
                height=img.height,
                size=img.size,
                uploaded_by=current_user.id
            )
            db.add(new_image)
    
    # Copy product-level images
    for img in original.images:
        if img.stage_id is None:  # Product-level images only
            new_image = ProductImage(
                product_id=new_product.id,
                stage_id=None,
                file_path=img.file_path,
                original_name=img.original_name,
                width=img.width,
                height=img.height,
                size=img.size,
                uploaded_by=current_user.id
            )
            db.add(new_image)
    
    db.commit()
    db.refresh(new_product)
    
    return new_product


@router.post("/{product_id}/stages", response_model=ProductDevelopmentStageResponse)
def add_development_stage(
    product_id: int,
    stage_data: ProductDevelopmentStageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff_or_admin)
):
    """Add a development stage to a product."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if stage_data.product_id != product_id:
        raise HTTPException(status_code=400, detail="Product ID mismatch")
    
    stage = ProductDevelopmentStage(**stage_data.model_dump())
    db.add(stage)
    db.commit()
    db.refresh(stage)
    
    return stage


@router.put("/{product_id}/stages/{stage_id}", response_model=ProductDevelopmentStageResponse)
def update_development_stage(
    product_id: int,
    stage_id: int,
    stage_data: ProductDevelopmentStageUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff_or_admin)
):
    """Update a development stage."""
    stage = db.query(ProductDevelopmentStage).filter(
        ProductDevelopmentStage.id == stage_id,
        ProductDevelopmentStage.product_id == product_id
    ).first()
    
    if not stage:
        raise HTTPException(status_code=404, detail="Development stage not found")
    
    update_data = stage_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(stage, field, value)
    
    db.commit()
    db.refresh(stage)
    
    return stage


@router.post("/{product_id}/images")
def upload_product_image(
    product_id: int,
    file: UploadFile = File(...),
    stage_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff_or_admin)
):
    """Upload an image for a product or a specific development stage."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Get category slug for folder structure
    category = db.query(Category).filter(Category.id == product.category_id).first()
    
    # Get stage name if stage_id provided
    stage_name = None
    if stage_id:
        stage = db.query(ProductDevelopmentStage).filter(
            ProductDevelopmentStage.id == stage_id,
            ProductDevelopmentStage.product_id == product_id
        ).first()
        if not stage:
            raise HTTPException(status_code=404, detail="Development stage not found")
        stage_name = stage.stage_name
    
    # Save image file
    try:
        relative_path, width, height, size = file_storage.save_image(
            file,
            category.slug,
            product.uuid,
            stage_name
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save image: {str(e)}")
    
    # Create database record
    product_image = ProductImage(
        product_id=product_id,
        stage_id=stage_id,
        file_path=relative_path,
        original_name=file.filename,
        width=width,
        height=height,
        size=size,
        uploaded_by=current_user.id
    )
    db.add(product_image)
    db.commit()
    db.refresh(product_image)
    
    return {
        "message": "Image uploaded successfully",
        "image_id": product_image.id,
        "file_path": relative_path
    }
