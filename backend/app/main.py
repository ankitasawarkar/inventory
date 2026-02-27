from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.db import init_db
from app.api.v1 import auth, categories, products, cart, orders, inventory, reports, catalog, inventory_categories, lookups
from app.config import settings
from seed_data import seed_database

# Create FastAPI app
app = FastAPI(
    title="Sagar Furniture API",
    description="Inventory and Order Management System for Wooden Furniture",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(inventory.router)
app.include_router(reports.router)
app.include_router(catalog.router)
app.include_router(inventory_categories.router)
app.include_router(lookups.router)

# Mount media files
media_path = Path(settings.MEDIA_ROOT)
media_path.mkdir(parents=True, exist_ok=True)
app.mount("/media", StaticFiles(directory=str(media_path)), name="media")


@app.on_event("startup")
def on_startup():
    """Initialize and seed database on startup."""
    init_db()
    # Seed with demo users/products/inventory. The seed script is
    # idempotent and will skip if data already exists.
    try:
        seed_database()
    except Exception as exc:
        # In production you might want to log this instead of printing.
        print(f"Database seed failed: {exc}")


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Sagar Furniture API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
