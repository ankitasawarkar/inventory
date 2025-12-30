import { Outlet, Link } from 'react-router-dom'

function Layout() {
  const token = localStorage.getItem('token')
  const user = JSON.parse(localStorage.getItem('user') || '{}')

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    window.location.href = '/'
  }

  return (
    <div>
      <header className="header">
        <nav className="container">
          <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
            <Link to="/" style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>
              🪑 Sagar Furniture
            </Link>
            <Link to="/products">Products</Link>
            {token && user.role === 'admin' && (
              <>
                <Link to="/admin/dashboard">Dashboard</Link>
                <Link to="/admin/products">Manage Products</Link>
                <Link to="/admin/orders">Orders</Link>
                <Link to="/admin/inventory">Inventory</Link>
              </>
            )}
          </div>
          <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
            <Link to="/cart">🛒 Cart</Link>
            {token ? (
              <>
                <span>Welcome, {user.username}</span>
                <button onClick={handleLogout} className="btn btn-secondary">
                  Logout
                </button>
              </>
            ) : (
              <Link to="/login" className="btn btn-primary">
                Login
              </Link>
            )}
          </div>
        </nav>
      </header>
      <main className="container" style={{ marginTop: '2rem' }}>
        <Outlet />
      </main>
    </div>
  )
}

export default Layout
