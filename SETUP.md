# 🚀 Complete Setup Instructions

## Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.11 or higher - Check: `python --version`
- ✅ Node.js 18 or higher - Check: `node --version`
- ✅ Git (optional but recommended)
- ✅ PowerShell or Command Prompt (Windows)

---

## Method 1: Local Development (Recommended for Development)

### Step 1: Backend Setup

Open PowerShell/Terminal in the project root:

```powershell
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1
# Note: On Linux/Mac use: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# The .env file is already created with default values
# You can edit it if needed: notepad .env

# Initialize database with sample data
python seed_data.py

# Start the backend server
uvicorn app.main:app --reload
```

**✅ Backend is now running!**
- API Server: http://localhost:8000
- Interactive API Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

Keep this terminal open!

---

### Step 2: Frontend Setup

Open a **NEW** PowerShell/Terminal window (keep backend running):

```powershell
# Navigate to frontend from project root
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**✅ Frontend is now running!**
- Web Application: http://localhost:3000

---

### Step 3: Access the Application

1. **Open your browser** and go to: http://localhost:3000

2. **Login** using one of these accounts:

   | Role     | Username  | Password  | Access Level |
   |----------|-----------|-----------|--------------|
   | Admin    | admin     | admin123  | Full access  |
   | Staff    | staff     | staff123  | Products & Orders |
   | Customer | customer  | customer123 | Browse & Cart |

3. **Explore Features:**
   - Browse products
   - View product development timelines
   - Add items to cart
   - Admin: Access dashboard at http://localhost:3000/admin/dashboard

---

## Method 2: Docker Setup (Recommended for Quick Demo)

If you have Docker Desktop installed:

```powershell
# Build and start all services
docker-compose up --build

# Wait for services to start, then in a NEW terminal:
docker-compose exec backend python seed_data.py
```

**Access:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

**Stop Docker:**
```powershell
docker-compose down
```

---

## 🧪 Verify Installation

### Test Backend
1. Visit http://localhost:8000/docs
2. Try the `/health` endpoint
3. It should return: `{"status": "healthy"}`

### Test Frontend
1. Visit http://localhost:3000
2. You should see the home page
3. Click "Products" to view sample products

### Test Authentication
1. Go to http://localhost:3000/login
2. Login as: admin / admin123
3. You should be redirected to home with "Welcome, admin" shown

---

## 📂 What Gets Created

After setup, you'll have:

```
backend/
├── venv/              # Python virtual environment
├── sagar.db           # SQLite database (created after seed)
├── media/             # Uploaded images folder
└── .env               # Environment variables (already exists)

frontend/
└── node_modules/      # Node.js dependencies
```

---

## 🔍 Common Issues & Solutions

### Backend Issues

**Issue**: `python: command not found`
- **Solution**: Install Python from python.org or Microsoft Store

**Issue**: `uvicorn: command not found`
- **Solution**: Make sure virtual environment is activated
- Check: You should see `(venv)` in your terminal prompt

**Issue**: `No module named 'fastapi'`
- **Solution**: Activate venv and run: `pip install -r requirements.txt`

**Issue**: Database errors
- **Solution**: Delete `sagar.db` and run `python seed_data.py` again

### Frontend Issues

**Issue**: `npm: command not found`
- **Solution**: Install Node.js from nodejs.org

**Issue**: `Port 3000 is already in use`
- **Solution**: Edit `vite.config.js` and change port to 3001
- Or close other apps using port 3000

**Issue**: `Cannot connect to backend`
- **Solution**: Ensure backend is running at http://localhost:8000
- Check frontend `.env` file has correct API URL

### Docker Issues

**Issue**: `docker-compose: command not found`
- **Solution**: Install Docker Desktop from docker.com

**Issue**: Containers won't start
- **Solution**: Make sure Docker Desktop is running
- Try: `docker-compose down` then `docker-compose up --build`

---

## 🎯 Quick Test Checklist

After setup, verify these work:

- [ ] Backend API docs accessible at http://localhost:8000/docs
- [ ] Frontend home page loads at http://localhost:3000
- [ ] Can login with admin/admin123
- [ ] Products page shows sample products
- [ ] Product detail page shows development timeline
- [ ] Admin dashboard accessible after admin login

---

## 📱 Next Steps

1. **Explore the API**
   - Visit http://localhost:8000/docs
   - Try different endpoints
   - Use the "Try it out" feature

2. **Test Product Features**
   - Create new categories
   - Add products
   - Upload images (requires implementation)
   - Track development stages

3. **Test Order Flow**
   - Add products to cart
   - Create orders
   - Track order status

4. **Review Code**
   - Backend: `backend/app/`
   - Frontend: `frontend/src/`
   - Database models: `backend/app/models/`

5. **Customize**
   - Modify styles in `frontend/src/index.css`
   - Add new features
   - Extend API endpoints

---

## 🛠️ Development Commands

### Backend

```powershell
# Run server with auto-reload
uvicorn app.main:app --reload

# Run on different port
uvicorn app.main:app --port 8001

# Reset database
rm sagar.db
python seed_data.py

# Check Python dependencies
pip list
```

### Frontend

```powershell
# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Install new package
npm install package-name
```

---

## 📊 Database Exploration

View the SQLite database:
1. Install SQLite Browser: https://sqlitebrowser.org/
2. Open `backend/sagar.db`
3. Browse tables and data

Or use command line:
```powershell
cd backend
sqlite3 sagar.db
.tables
SELECT * FROM users;
.quit
```

---

## 🎓 Learning Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **React Docs**: https://react.dev/
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org/
- **Vite Docs**: https://vitejs.dev/

---

## 💡 Tips

- Keep both backend and frontend terminals open while developing
- Backend auto-reloads on file changes (if using `--reload`)
- Frontend auto-reloads on file changes
- Check browser console for frontend errors
- Check terminal for backend errors
- Use API docs for testing: http://localhost:8000/docs

---

## 🆘 Need Help?

1. Check the error message in terminal
2. Look at browser console (F12)
3. Review the logs
4. Check if services are running
5. Verify ports 8000 and 3000 are available

---

## 🎉 You're All Set!

The application is now ready for:
- ✅ Development
- ✅ Testing
- ✅ Demonstrations
- ✅ Customization

**Happy Coding!** 🚀
