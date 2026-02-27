import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom'
import { useEffect, useState } from 'react'

function Layout() {
  const location = useLocation()
  const navigate = useNavigate()
  const [token, setToken] = useState(() => localStorage.getItem('token'))
  const [user, setUser] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem('user') || 'null') || {}
    } catch {
      return {}
    }
  })

  // Sync auth state from localStorage whenever route changes
  useEffect(() => {
    const storedToken = localStorage.getItem('token')
    let storedUser = {}
    try {
      storedUser = JSON.parse(localStorage.getItem('user') || 'null') || {}
    } catch {
      storedUser = {}
    }
    setToken(storedToken)
    setUser(storedUser)
  }, [location])

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setToken(null)
    setUser({})
    navigate('/')
  }

  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-primary text-white shadow">
        <nav className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link to="/" className="text-xl font-bold flex items-center gap-2">
              <span role="img" aria-label="chair">
                🪑
              </span>
              <span>Sagar Furniture</span>
            </Link>
            <Link to="/products" className="hover:bg-secondary/80 rounded px-3 py-1">
              Products
            </Link>
            {token && user.role === 'admin' && (
              <>
                <Link
                  to="/admin/dashboard"
                  className="hover:bg-secondary/80 rounded px-3 py-1"
                >
                  Dashboard
                </Link>
                <Link
                  to="/admin/products"
                  className="hover:bg-secondary/80 rounded px-3 py-1"
                >
                  Manage Products
                </Link>
                <Link
                  to="/admin/orders"
                  className="hover:bg-secondary/80 rounded px-3 py-1"
                >
                  Orders
                </Link>
                <Link
                  to="/admin/inventory"
                  className="hover:bg-secondary/80 rounded px-3 py-1"
                >
                  Inventory
                </Link>
              </>
            )}
          </div>
          <div className="flex items-center gap-4">
            <Link to="/cart" className="hover:bg-secondary/80 rounded px-3 py-1">
              🛒 Cart
            </Link>
            {token ? (
              <>
                <span className="text-sm">Welcome, {user.username}</span>
                <button
                  onClick={handleLogout}
                  className="inline-flex items-center rounded bg-slate-600 px-3 py-1 text-sm font-medium hover:bg-slate-700"
                >
                  Logout
                </button>
              </>
            ) : (
              <Link
                to="/login"
                className="inline-flex items-center rounded bg-secondary px-4 py-1.5 text-sm font-semibold hover:bg-secondary/90"
              >
                Login
              </Link>
            )}
          </div>
        </nav>
      </header>
      <main className="flex-1 max-w-6xl mx-auto px-4 py-8">
        <Outlet />
      </main>
    </div>
  )
}

export default Layout
