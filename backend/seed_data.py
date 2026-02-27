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


from app.models import Lookup
def seed_database():
    """Seed the database with initial data."""
    # Initialize database
    init_db()
    
    db = SessionLocal()
    
    try:
        # If admin user already exists, assume seeding has been done
        if db.query(User).filter(User.username == "admin").first():
            print("✅ Database already seeded, skipping.")
            return

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
        
        # Create categories with coding system
        chairs = Category(name="Chairs", slug="chairs", code="CH")
        tables = Category(name="Tables", slug="tables", code="TB")
        db.add(chairs)
        db.add(tables)
        db.flush()

        dining_chairs = Category(
            name="Dining Chairs",
            slug="chairs-dining",
            code="DIN",
            parent_id=chairs.id,
        )
        office_chairs = Category(
            name="Office Chairs",
            slug="chairs-office",
            code="OFF",
            parent_id=chairs.id,
        )
        study_tables = Category(
            name="Study Tables",
            slug="tables-study",
            code="STD",
            parent_id=tables.id,
        )
        dining_tables = Category(
            name="Dining Tables",
            slug="tables-dining",
            code="DIN",
            parent_id=tables.id,
        )
        db.add(dining_chairs)
        db.add(office_chairs)
        db.add(study_tables)
        db.add(dining_tables)
        db.flush()
        
        # Create inventory items
        inventory_items = [
            InventoryItem(
                name="Seasoned Oak plank 25mm x 3m",
                sku="INV-MAT-PLK-SAO-25X3M",
                item_code="MAT-PLK-SAO-25X3M",
                material_code="SAO",
                unit="pcs",
                quantity=Decimal("120.00"),
                reorder_level=Decimal("20.00"),
                cost_per_unit=Decimal("1800.00"),
            ),
            InventoryItem(
                name="Seasoned Acacia plank 20mm x 2.4m",
                sku="INV-MAT-PLK-SAA-20X24",
                item_code="MAT-PLK-SAA-20X24",
                material_code="SAA",
                unit="pcs",
                quantity=Decimal("90.00"),
                reorder_level=Decimal("15.00"),
                cost_per_unit=Decimal("1300.00"),
            ),
            InventoryItem(
                name="18mm Plywood sheet",
                sku="INV-MAT-PLY-PLY18-8X4",
                item_code="MAT-PLY-PLY18-8X4",
                material_code="PLY18",
                unit="pcs",
                quantity=Decimal("60.00"),
                reorder_level=Decimal("10.00"),
                cost_per_unit=Decimal("2200.00"),
            ),
            InventoryItem(
                name="Wood Stain - Walnut",
                sku="INV-FIN-LAC-WAL-5L",
                item_code="FIN-LAC-WAL-5L",
                material_code="WAL",
                unit="liters",
                quantity=Decimal("25.00"),
                reorder_level=Decimal("5.00"),
                cost_per_unit=Decimal("30.00"),
            ),
            InventoryItem(
                name="Chipboard screws 30mm",
                sku="INV-HRD-SCR-30MM-BOX",
                item_code="HRD-SCR-30MM-BOX",
                material_code="SCR30",
                unit="pcs",
                quantity=Decimal("2000.00"),
                reorder_level=Decimal("400.00"),
                cost_per_unit=Decimal("0.40"),
            ),
        ]
        
        for item in inventory_items:
            db.add(item)
        
        db.flush()
        
        # Create sample products using the new SKU coding system
        product1 = Product(
            title="Royal Oak Dining Chair",
            sku="CH-DIN-ROYC-WO-WAL-STD",
            model_code="ROYC",
            category_id=chairs.id,
            subcategory_id=dining_chairs.id,
            description="Royal Oak dining chair in walnut finish, standard height",
            base_price=Decimal("8500.00"),
            is_customizable=True,
            status=ProductStatus.READY,
            created_by=admin.id,
        )
        db.add(product1)

        product2 = Product(
            title="Minimal Study Table",
            sku="TB-STD-MIST-WO-NAT-120",
            model_code="MIST",
            category_id=tables.id,
            subcategory_id=study_tables.id,
            description="Minimal wooden study table, 120 cm length, natural finish",
            base_price=Decimal("12500.00"),
            is_customizable=False,
            status=ProductStatus.DEVELOPMENT,
            created_by=admin.id,
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
        
        seed_lookups(db)
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

def seed_lookups(db: Session):
    """Seed core lookup values for dropdowns (idempotent)."""

    # Simple helper to avoid duplicates
    def ensure_lookup(set_name: str, key: str, value: str, description: str = "", scope: str = "GLOBAL", order_by: int = 0):
        existing = (
            db.query(Lookup)
            .filter(Lookup.set == set_name, Lookup.key == key)
            .first()
        )
        if existing:
            return existing
        item = Lookup(
            set=set_name,
            key=key,
            value=value,
            description=description or None,
            scope=scope,
            order_by=order_by,
            is_active=True,
        )
        db.add(item)
        return item

    # Units for inventory
    ensure_lookup("INVENTORY_UNIT", "PCS", "Pieces", "Individual pieces", order_by=1)
    ensure_lookup("INVENTORY_UNIT", "SQFT", "Square Feet", "Area in square feet", order_by=2)
    ensure_lookup("INVENTORY_UNIT", "ML", "Milliliters", "Liquid volume", order_by=3)

    # Product finishes
    ensure_lookup("PRODUCT_FINISH", "NAT", "Natural Finish", order_by=1)
    ensure_lookup("PRODUCT_FINISH", "WAL", "Walnut Finish", order_by=2)
    ensure_lookup("PRODUCT_FINISH", "TEK", "Teak Finish", order_by=3)

    # Wood species / material codes
    ensure_lookup("MATERIAL_CODE", "SAO", "Sheesham A-Grade", order_by=1)
    ensure_lookup("MATERIAL_CODE", "MDF", "MDF Board", order_by=2)
    ensure_lookup("MATERIAL_CODE", "PLY18", "18mm Plywood", order_by=3)

    # Generic yes/no
    ensure_lookup("YES_NO", "Y", "Yes", order_by=1)
    ensure_lookup("YES_NO", "N", "No", order_by=2)

    db.commit()

if __name__ == "__main__":
    seed_database()
