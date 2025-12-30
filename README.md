# Sagar Furniture - Inventory and Order Management System

A comprehensive inventory and order management system for a wooden furniture manufacturer/showroom. Built with FastAPI (Python) backend and React frontend.

## 🎯 Features

- **Multi-role Access Control**: Admin, Staff, and Customer roles with appropriate permissions
- **Product Catalog Management**: Categories, subcategories, and detailed product information
- **Development Stage Tracking**: Track furniture production from raw material to finished product
- **Image Management**: Upload and manage product images with filesystem storage and SQLite metadata
- **Order Management**: Create orders, track production pipeline, and manage customizations
- **Inventory Control**: Track raw materials, adjust quantities, and monitor stock levels
- **Shopping Cart**: Add products to cart, customize orders
- **Product Replication**: Clone existing products for quick customization
- **Analytics & Reports**: Production reports, profit analysis, inventory valuation with CSV export
- **Audit Logging**: Track all critical changes

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **ORM**: SQLAlchemy
- **Database**: SQLite
- **Authentication**: JWT tokens with OAuth2
- **File Upload**: Python Pillow for image processing

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **HTTP Client**: Axios
- **Routing**: React Router
- **UI**: Modern responsive design for web, tablet, and mobile

## 📁 Project Structure

```
Inventory/
├── backend/
│   ├── app/
│   │   ├── api/v1/         # API endpoints
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   ├── auth.py         # Authentication utilities
│   │   ├── config.py       # Configuration
│   │   ├── db.py           # Database setup
│   │   └── main.py         # FastAPI app
│   ├── requirements.txt
│   ├── Dockerfile
│   └── seed_data.py        # Sample data script
├── frontend/               # React application
├── docker-compose.yml
├── prompt.md              # Project requirements
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (optional)

### Option 1: Local Development

#### Backend Setup

1. Navigate to backend directory:
```powershell
cd backend
```

2. Create virtual environment:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. Install dependencies:
```powershell
pip install -r requirements.txt
```

4. Create `.env` file:
```powershell
cp .env.example .env
```

5. Edit `.env` and set your `SECRET_KEY`:
```
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=sqlite:///./sagar.db
MEDIA_ROOT=./media
```

6. Seed the database:
```powershell
python seed_data.py
```

7. Run the development server:
```powershell
uvicorn app.main:app --reload
```

Backend API will be available at: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

#### Frontend Setup

1. Navigate to frontend directory:
```powershell
cd frontend
```

2. Install dependencies:
```powershell
npm install
```

3. Create `.env` file:
```
VITE_API_URL=http://localhost:8000
```

4. Run development server:
```powershell
npm run dev
```

Frontend will be available at: http://localhost:3000

### Option 2: Docker Setup

1. Build and run with Docker Compose:
```powershell
docker-compose up --build
```

2. Seed the database (in a new terminal):
```powershell
docker-compose exec backend python seed_data.py
```

Services will be available at:
- Backend API: http://localhost:8000
- Frontend: http://localhost:3000

## 👤 Default Users

After seeding the database, use these credentials:

| Role     | Username  | Password     |
|----------|-----------|--------------|
| Admin    | admin     | admin123     |
| Staff    | staff     | staff123     |
| Customer | customer  | customer123  |

## 📚 API Endpoints

### Authentication
- `POST /api/auth/login` - Login and get access token
- `POST /api/auth/register` - Register new user (admin only)
- `POST /api/auth/refresh` - Refresh access token

### Categories
- `GET /api/categories` - List all categories
- `POST /api/categories` - Create category (admin)
- `PUT /api/categories/{id}` - Update category (admin)
- `DELETE /api/categories/{id}` - Delete category (admin)

### Products
- `GET /api/products` - List products (with filters)
- `GET /api/products/{id}` - Get product details
- `POST /api/products` - Create product (staff/admin)
- `PUT /api/products/{id}` - Update product (staff/admin)
- `POST /api/products/{id}/replicate` - Clone product (admin)
- `POST /api/products/{id}/stages` - Add development stage
- `PUT /api/products/{id}/stages/{stage_id}` - Update stage
- `POST /api/products/{id}/images` - Upload product image

### Cart & Orders
- `POST /api/cart` - Create/get cart
- `GET /api/cart/{id}` - Get cart details
- `POST /api/cart/{id}/items` - Add item to cart
- `DELETE /api/cart/{id}/items/{item_id}` - Remove from cart
- `POST /api/orders` - Create order
- `GET /api/orders` - List orders (staff/admin)
- `GET /api/orders/{id}` - Get order details
- `PUT /api/orders/{id}` - Update order (staff/admin)

### Inventory
- `GET /api/inventory` - List inventory items
- `POST /api/inventory` - Create inventory item (admin)
- `PUT /api/inventory/{id}` - Update item (admin)
- `PATCH /api/inventory/{id}/adjust` - Adjust quantity (admin)

### Reports
- `GET /api/reports/production` - Production report
- `GET /api/reports/profit` - Profit report
- `GET /api/reports/pipeline` - Current production pipeline
- `GET /api/reports/inventory-valuation` - Inventory value

## 🗄️ Database Schema

Key tables:
- **users** - User accounts with roles
- **categories** - Product categories (nested)
- **products** - Product catalog
- **product_development_stages** - Production stages per product
- **product_images** - Image metadata
- **inventory_items** - Raw materials and supplies
- **orders** - Customer orders
- **order_items** - Items in each order
- **carts** - Shopping carts
- **cart_items** - Items in carts
- **production_records** - Manufacturing pipeline tracking
- **profit_records** - Revenue and cost tracking
- **audit_logs** - Activity audit trail

## 📸 Image Storage

Images are stored on the filesystem with this structure:
```
media/
  categories/<category-slug>/
    products/<product-uuid>/
      stage-<stage-name>/
        <image-uuid>_<filename>
```

Image metadata (paths, dimensions, etc.) is stored in SQLite.

## 🧪 Testing

### Backend Tests
```powershell
cd backend
pytest
```

### Frontend Tests
```powershell
cd frontend
npm test
```

## 📝 Environment Variables

### Backend (.env)
```
DATABASE_URL=sqlite:///./sagar.db
MEDIA_ROOT=./media
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
MAX_IMAGE_SIZE_MB=10
ALLOWED_IMAGE_TYPES=image/jpeg,image/png,image/webp
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000
```

## 🚢 Production Deployment

1. Set secure `SECRET_KEY` in environment
2. Use production ASGI server (Gunicorn + Uvicorn)
3. Set up reverse proxy (Nginx)
4. Consider migrating to PostgreSQL for better performance
5. Use cloud storage (S3) for images at scale
6. Enable HTTPS
7. Set proper CORS origins

## 📖 Additional Documentation

- Full project requirements: See `prompt.md`
- API Documentation: http://localhost:8000/docs (when running)
- Database Models: See `backend/app/models/`
- API Schemas: See `backend/app/schemas/`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is proprietary software for Sagar Furniture.

## 🆘 Support

For issues and questions:
- Check API documentation at `/docs`
- Review the `prompt.md` for detailed requirements
- Examine seed data in `seed_data.py` for examples

---

**Built with ❤️ for Sagar Furniture**
