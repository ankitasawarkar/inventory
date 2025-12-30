# Quick Start Guide - Sagar Furniture

## 🚀 Quick Setup (Local Development)

### Backend Setup

1. **Navigate to backend directory:**
```powershell
cd backend
```

2. **Create and activate virtual environment:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. **Install dependencies:**
```powershell
pip install -r requirements.txt
```

4. **Create .env file:**
```powershell
cp .env.example .env
```

Edit `.env` and set a secure SECRET_KEY:
```
SECRET_KEY=your-super-secret-key-change-this
DATABASE_URL=sqlite:///./sagar.db
MEDIA_ROOT=./media
```

5. **Seed the database:**
```powershell
python seed_data.py
```

6. **Run the server:**
```powershell
uvicorn app.main:app --reload
```

✅ Backend running at: http://localhost:8000
📚 API Docs at: http://localhost:8000/docs

---

### Frontend Setup

1. **Open NEW terminal and navigate to frontend:**
```powershell
cd frontend
```

2. **Install dependencies:**
```powershell
npm install
```

3. **Run development server:**
```powershell
npm run dev
```

✅ Frontend running at: http://localhost:3000

---

## 🔑 Login Credentials

After seeding the database:

| Role     | Username  | Password     |
|----------|-----------|--------------|
| Admin    | admin     | admin123     |
| Staff    | staff     | staff123     |
| Customer | customer  | customer123  |

---

## 🐳 Docker Setup (Alternative)

If you prefer Docker:

```powershell
# Build and start all services
docker-compose up --build

# In another terminal, seed the database
docker-compose exec backend python seed_data.py
```

Access:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000

---

## 🧪 Testing the API

1. Visit http://localhost:8000/docs
2. Click "Authorize" button
3. Use format: `username` and `password` (e.g., admin / admin123)
4. Try endpoints like:
   - GET /api/products
   - GET /api/categories
   - GET /api/inventory

---

## 📱 Key Features to Test

### As Customer:
1. Browse products at http://localhost:3000/products
2. View product details with development timeline
3. Add items to cart

### As Admin:
1. Login at http://localhost:3000/login (use admin credentials)
2. Access Admin Dashboard
3. Manage Products, Orders, and Inventory
4. Generate Reports

---

## 🔧 Troubleshooting

### Backend won't start?
- Check Python version: `python --version` (need 3.11+)
- Verify virtual environment is activated
- Ensure .env file exists with SECRET_KEY

### Frontend won't start?
- Check Node version: `node --version` (need 18+)
- Delete node_modules and run `npm install` again
- Check if port 3000 is available

### Database errors?
- Delete sagar.db and run `python seed_data.py` again
- Check DATABASE_URL in .env

---

## 📖 Next Steps

1. **Explore the API**: Visit http://localhost:8000/docs
2. **Read the Documentation**: Check README.md for detailed information
3. **Review Code**: Explore backend/app/ for API implementation
4. **Customize**: Modify frontend components in frontend/src/

---

## 💡 Pro Tips

- Use the Swagger UI at `/docs` to test all API endpoints
- Check the `seed_data.py` to see sample data structure
- Frontend includes React Query for efficient data fetching
- All images are stored in `backend/media/` directory
- SQLite database file is at `backend/sagar.db`

Happy Coding! 🎉
