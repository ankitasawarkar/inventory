import { useQuery } from '@tanstack/react-query'
import { useParams } from 'react-router-dom'
import { getProduct } from '../api'

function ProductDetail() {
  const { id } = useParams()
  
  const { data: product, isLoading, error } = useQuery({
    queryKey: ['product', id],
    queryFn: () => getProduct(id).then(res => res.data)
  })

  if (isLoading) return <div>Loading product details...</div>
  if (error) return <div>Error loading product: {error.message}</div>

  return (
    <div>
      <div className="card">
        <h1>{product.title}</h1>
        <p style={{ fontSize: '1.5rem', color: 'var(--primary-color)', margin: '1rem 0' }}>
          ₹{product.base_price}
        </p>
        
        <div style={{ marginBottom: '1.5rem' }}>
          <p><strong>SKU:</strong> {product.sku || 'N/A'}</p>
          <p><strong>Status:</strong> {product.status}</p>
          <p><strong>Customizable:</strong> {product.is_customizable ? 'Yes' : 'No'}</p>
        </div>

        <div>
          <h3>Description</h3>
          <p>{product.description || 'No description available.'}</p>
        </div>

        <button className="btn btn-primary" style={{ marginTop: '1.5rem' }}>
          Add to Cart
        </button>
      </div>

      {product.development_stages?.length > 0 && (
        <div className="card" style={{ marginTop: '2rem' }}>
          <h2>Development Timeline</h2>
          
          <div style={{ marginTop: '1.5rem' }}>
            {product.development_stages
              .sort((a, b) => a.stage_order - b.stage_order)
              .map((stage, index) => (
                <div 
                  key={stage.id} 
                  style={{
                    display: 'flex',
                    marginBottom: '1.5rem',
                    paddingBottom: '1.5rem',
                    borderBottom: index < product.development_stages.length - 1 ? '1px solid var(--border-color)' : 'none'
                  }}
                >
                  <div style={{ 
                    width: '40px',
                    height: '40px',
                    borderRadius: '50%',
                    backgroundColor: stage.stage_status === 'completed' ? '#28a745' : '#ffc107',
                    color: 'white',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontWeight: 'bold',
                    marginRight: '1rem',
                    flexShrink: 0
                  }}>
                    {stage.stage_order}
                  </div>
                  
                  <div style={{ flex: 1 }}>
                    <h3>{stage.stage_name}</h3>
                    <p style={{ color: '#666', margin: '0.5rem 0' }}>
                      {stage.stage_description}
                    </p>
                    {stage.expected_days && (
                      <p style={{ fontSize: '0.9rem' }}>
                        <strong>Expected:</strong> {stage.expected_days} days
                      </p>
                    )}
                    <span style={{
                      display: 'inline-block',
                      padding: '0.25rem 0.75rem',
                      backgroundColor: stage.stage_status === 'completed' ? '#28a745' : '#ffc107',
                      color: 'white',
                      borderRadius: '4px',
                      fontSize: '0.85rem',
                      marginTop: '0.5rem'
                    }}>
                      {stage.stage_status.replace('_', ' ')}
                    </span>
                  </div>
                </div>
              ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default ProductDetail
