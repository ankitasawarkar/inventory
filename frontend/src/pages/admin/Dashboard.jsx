function AdminDashboard() {
  return (
    <div>
      <h1>Admin Dashboard</h1>
      
      <div className="grid">
        <div className="card">
          <h3>📦 Total Products</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>0</p>
        </div>
        <div className="card">
          <h3>🛒 Active Orders</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>0</p>
        </div>
        <div className="card">
          <h3>📊 Production Pipeline</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>0</p>
        </div>
        <div className="card">
          <h3>💰 Monthly Revenue</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>₹0</p>
        </div>
      </div>
    </div>
  )
}

export default AdminDashboard
