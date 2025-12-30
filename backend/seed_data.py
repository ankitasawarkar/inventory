"""
Seed script to populate the database with sample data.
"""
from sqlalchemy.orm import Session
from app.db import SessionLocal, init_db
from app.models.user import User, UserRole
from app.models.category import Category
from app.models.product import Product, ProductDevelopmentStage, ProductStatus, StageStatus
from app.models.inventory import InventoryItem
from app.auth import get_password_hash
from decimal import Decimal


def seed_database():
    """Seed the database with initial data."""
    # Initialize database
    init_db()
    
    db = SessionLocal()
    
    try:
        # Create admin user
        admin = User(
            username="admin",
            email="admin@sagarfurniture.com",
            full_name="Admin User",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.ADMIN,
            is_active=True
        )
        db.add(admin)
        
        # Create staff user
        staff = User(
            username="staff",
            email="staff@sagarfurniture.com",
            full_name="Staff User",
            hashed_password=get_password_hash("staff123"),
            role=UserRole.STAFF,
            is_active=True
        )
        db.add(staff)
        
        # Create customer user
        customer = User(
            username="customer",
            email="customer@example.com",
            full_name="Customer User",
            hashed_password=get_password_hash("customer123"),
            role=UserRole.CUSTOMER,
            is_active=True
        )
        db.add(customer)
        
        db.flush()
        
        # Create categories
        categories = [
            Category(name="Tables", slug="tables"),
            Category(name="Chairs", slug="chairs"),
            Category(name="Beds", slug="beds"),
            Category(name="Cabinets", slug="cabinets"),
        ]
        
        for cat in categories:
            db.add(cat)
        
        db.flush()
        
        # Create subcategories
        dining_table = Category(
            name="Dining Tables",
            slug="dining-tables",
            parent_id=categories[0].id
        )
        db.add(dining_table)
        
        office_chair = Category(
            name="Office Chairs",
            slug="office-chairs",
            parent_id=categories[1].id
        )
        db.add(office_chair)
        
        db.flush()
        
        # Create inventory items
        inventory_items = [
            InventoryItem(
                name="Teak Wood",
                sku="INV-TEAK-001",
                unit="kg",
                quantity=Decimal("500.00"),
                reorder_level=Decimal("100.00"),
                cost_per_unit=Decimal("150.00")
            ),
            InventoryItem(
                name="Oak Wood",
                sku="INV-OAK-001",
                unit="kg",
                quantity=Decimal("300.00"),
                reorder_level=Decimal("80.00"),
                cost_per_unit=Decimal("200.00")
            ),
            InventoryItem(
                name="Wood Stain - Dark Brown",
                sku="INV-STAIN-DB",
                unit="liters",
                quantity=Decimal("50.00"),
                reorder_level=Decimal("10.00"),
                cost_per_unit=Decimal("25.00")
            ),
            InventoryItem(
                name="Wood Varnish",
                sku="INV-VARNISH-001",
                unit="liters",
                quantity=Decimal("40.00"),
                reorder_level=Decimal("10.00"),
                cost_per_unit=Decimal("30.00")
            ),
            InventoryItem(
                name="Screws & Bolts Set",
                sku="INV-BOLT-001",
                unit="pcs",
                quantity=Decimal("1000.00"),
                reorder_level=Decimal("200.00"),
                cost_per_unit=Decimal("0.50")
            ),
        ]
        
        for item in inventory_items:
            db.add(item)
        
        db.flush()
        
        # Create sample products
        product1 = Product(
            title="Classic Dining Table",
            sku="PROD-DT-001",
            category_id=categories[0].id,
            subcategory_id=dining_table.id,
            description="A beautiful classic dining table made from solid teak wood",
            base_price=Decimal("25000.00"),
            is_customizable=True,
            status=ProductStatus.READY,
            created_by=admin.id
        )
        db.add(product1)
        
        product2 = Product(
            title="Executive Office Chair",
            sku="PROD-OC-001",
            category_id=categories[1].id,
            subcategory_id=office_chair.id,
            description="Ergonomic office chair with leather upholstery",
            base_price=Decimal("15000.00"),
            is_customizable=False,
            status=ProductStatus.DEVELOPMENT,
            created_by=admin.id
        )
        db.add(product2)
        
        db.flush()
        
        # Create development stages for product1
        stages = [
            ProductDevelopmentStage(
                product_id=product1.id,
                stage_order=1,
                stage_name="Raw Material",
                stage_description="Select and prepare raw teak wood",
                expected_days=2,
                stage_status=StageStatus.COMPLETED,
                responsible_person=staff.id
            ),
            ProductDevelopmentStage(
                product_id=product1.id,
                stage_order=2,
                stage_name="Cutting",
                stage_description="Cut wood pieces according to design",
                expected_days=3,
                stage_status=StageStatus.COMPLETED,
                responsible_person=staff.id
            ),
            ProductDevelopmentStage(
                product_id=product1.id,
                stage_order=3,
                stage_name="Assembly",
                stage_description="Assemble table components",
                expected_days=4,
                stage_status=StageStatus.COMPLETED,
                responsible_person=staff.id
            ),
            ProductDevelopmentStage(
                product_id=product1.id,
                stage_order=4,
                stage_name="Sanding",
                stage_description="Sand surfaces for smooth finish",
                expected_days=2,
                stage_status=StageStatus.COMPLETED,
                responsible_person=staff.id
            ),
            ProductDevelopmentStage(
                product_id=product1.id,
                stage_order=5,
                stage_name="Staining",
                stage_description="Apply wood stain",
                expected_days=1,
                stage_status=StageStatus.COMPLETED,
                responsible_person=staff.id
            ),
            ProductDevelopmentStage(
                product_id=product1.id,
                stage_order=6,
                stage_name="Polishing",
                stage_description="Final polish and varnish",
                expected_days=2,
                stage_status=StageStatus.COMPLETED,
                responsible_person=staff.id
            ),
            ProductDevelopmentStage(
                product_id=product1.id,
                stage_order=7,
                stage_name="Photography",
                stage_description="Professional product photography",
                expected_days=1,
                stage_status=StageStatus.COMPLETED,
                responsible_person=admin.id
            ),
        ]
        
        for stage in stages:
            db.add(stage)
        
        db.commit()
        print("✅ Database seeded successfully!")
        print("\n📝 Sample Users Created:")
        print("  Admin    - username: admin,    password: admin123")
        print("  Staff    - username: staff,    password: staff123")
        print("  Customer - username: customer, password: customer123")
        print("\n🏷️  Sample Products and Categories created")
        print("📦 Sample Inventory items created")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
