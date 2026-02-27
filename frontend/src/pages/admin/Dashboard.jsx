function AdminDashboard() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Admin Dashboard</h1>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4 mt-2">
        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="text-sm font-medium mb-1">📦 Total Products</h3>
          <p className="text-3xl font-bold">0</p>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="text-sm font-medium mb-1">🛒 Active Orders</h3>
          <p className="text-3xl font-bold">0</p>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="text-sm font-medium mb-1">📊 Production Pipeline</h3>
          <p className="text-3xl font-bold">0</p>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="text-sm font-medium mb-1">💰 Monthly Revenue</h3>
          <p className="text-3xl font-bold">₹0</p>
        </div>
      </div>
    </div>
  )
}

export default AdminDashboard
