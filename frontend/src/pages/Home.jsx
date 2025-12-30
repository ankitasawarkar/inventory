function Home() {
  return (
    <div>
      <h1>Welcome to Sagar Furniture</h1>
      <p style={{ fontSize: '1.2rem', margin: '2rem 0' }}>
        Your premier destination for handcrafted wooden furniture. Browse our collection
        of tables, chairs, beds, and cabinets, all made with premium quality wood.
      </p>
      
      <div className="grid" style={{ marginTop: '3rem' }}>
        <div className="card">
          <h3>🪑 Quality Craftsmanship</h3>
          <p>Each piece is handcrafted by skilled artisans with attention to detail.</p>
        </div>
        <div className="card">
          <h3>🌳 Premium Materials</h3>
          <p>We use only the finest teak, oak, and other quality hardwoods.</p>
        </div>
        <div className="card">
          <h3>✨ Custom Options</h3>
          <p>Many products can be customized to your specific requirements.</p>
        </div>
        <div className="card">
          <h3>📦 Track Production</h3>
          <p>View the development stages of your custom furniture orders.</p>
        </div>
      </div>
    </div>
  )
}

export default Home
