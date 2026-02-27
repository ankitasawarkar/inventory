import { useQuery } from '@tanstack/react-query'
import { useParams } from 'react-router-dom'
import { getProduct } from '../api'

function ProductDetail() {
  const { id } = useParams()

  const {
    data: product,
    isLoading,
    error,
  } = useQuery({
    queryKey: ['product', id],
    queryFn: () => getProduct(id).then((res) => res.data),
  })

  if (isLoading) return <div>Loading product details...</div>
  if (error) return <div>Error loading product: {error.message}</div>

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow p-6">
        <h1 className="text-2xl font-semibold mb-2">{product.title}</h1>
        <p className="text-2xl font-bold text-primary mb-4">
          ₹{product.base_price}
        </p>

        <div className="space-y-1 text-sm mb-4">
          <p>
            <span className="font-semibold">SKU:</span> {product.sku || 'N/A'}
          </p>
          <p>
            <span className="font-semibold">Status:</span> {product.status}
          </p>
          <p>
            <span className="font-semibold">Customizable:</span>{' '}
            {product.is_customizable ? 'Yes' : 'No'}
          </p>
        </div>

        <div className="space-y-1 text-sm">
          <h3 className="font-semibold">Description</h3>
          <p className="text-slate-700">
            {product.description || 'No description available.'}
          </p>
        </div>

        <button className="mt-6 inline-flex items-center rounded bg-primary px-4 py-2 text-sm font-semibold text-white hover:bg-secondary">
          Add to Cart
        </button>
      </div>

      {product.development_stages?.length > 0 && (
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold">Development Timeline</h2>

          <div className="mt-4 space-y-4">
            {product.development_stages
              .sort((a, b) => a.stage_order - b.stage_order)
              .map((stage, index) => (
                <div
                  key={stage.id}
                  className={`flex pb-4 ${
                    index < product.development_stages.length - 1
                      ? 'border-b border-slate-200'
                      : ''
                  }`}
                >
                  <div
                    className={`mr-4 flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full text-white font-bold ${
                      stage.stage_status === 'completed'
                        ? 'bg-emerald-500'
                        : 'bg-amber-500'
                    }`}
                  >
                    {stage.stage_order}
                  </div>

                  <div className="flex-1 text-sm">
                    <h3 className="font-semibold">{stage.stage_name}</h3>
                    <p className="text-slate-600 mt-1">
                      {stage.stage_description}
                    </p>
                    {stage.expected_days && (
                      <p className="text-xs mt-1">
                        <span className="font-semibold">Expected:</span>{' '}
                        {stage.expected_days} days
                      </p>
                    )}
                    <span
                      className={`mt-2 inline-flex items-center rounded-full px-3 py-0.5 text-xs font-medium text-white ${
                        stage.stage_status === 'completed'
                          ? 'bg-emerald-500'
                          : 'bg-amber-500'
                      }`}
                    >
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
