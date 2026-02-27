function Home() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-semibold mb-3">Welcome to Sagar Furniture</h1>
        <p className="text-lg text-slate-700 max-w-3xl">
          Your premier destination for handcrafted wooden furniture. Browse our
          collection of tables, chairs, beds, and cabinets, all made with
          premium quality wood.
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4 mt-4">
        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="text-lg font-medium mb-1">🪑 Quality Craftsmanship</h3>
          <p className="text-sm text-slate-700">
            Each piece is handcrafted by skilled artisans with attention to
            detail.
          </p>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="text-lg font-medium mb-1">🌳 Premium Materials</h3>
          <p className="text-sm text-slate-700">
            We use only the finest teak, oak, and other quality hardwoods.
          </p>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="text-lg font-medium mb-1">✨ Custom Options</h3>
          <p className="text-sm text-slate-700">
            Many products can be customized to your specific requirements.
          </p>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="text-lg font-medium mb-1">📦 Track Production</h3>
          <p className="text-sm text-slate-700">
            View the development stages of your custom furniture orders.
          </p>
        </div>
      </div>
    </div>
  )
}

export default Home
