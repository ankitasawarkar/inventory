import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { getProducts } from '../api'

function Products() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['products'],
    queryFn: () => getProducts().then(res => res.data)
  })

  if (isLoading) return <div>Loading products...</div>
  if (error) return <div>Error loading products: {error.message}</div>

  return (
    <div>
      <h1>Our Products</h1>
      
      <div className="grid">
        {data?.map(product => (
          <Link key={product.id} to={`/products/${product.id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
            <div className="card" style={{ cursor: 'pointer', transition: 'transform 0.2s' }}>
              <h3>{product.title}</h3>
              <p style={{ color: '#666', margin: '0.5rem 0' }}>SKU: {product.sku || 'N/A'}</p>
              <p style={{ fontSize: '1.2rem', fontWeight: 'bold', color: 'var(--primary-color)' }}>
                ₹{product.base_price}
              </p>
              <span style={{ 
                display: 'inline-block',
                padding: '0.25rem 0.75rem',
                backgroundColor: product.status === 'ready' ? '#28a745' : '#ffc107',
                color: 'white',
                borderRadius: '4px',
                fontSize: '0.9rem',
                marginTop: '0.5rem'
              }}>
                {product.status}
              </span>
            </div>
          </Link>
        ))}
      </div>
      
      {data?.length === 0 && (
        <div className="card">
          <p>No products available yet. Check back soon!</p>
        </div>
      )}
    </div>
  )
}

export default Products
