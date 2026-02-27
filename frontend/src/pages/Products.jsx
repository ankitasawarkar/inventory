import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { getProducts } from '../api'

function Products() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['products'],
    queryFn: () => getProducts().then((res) => res.data),
  })

  if (isLoading) return <div>Loading products...</div>
  if (error) return <div>Error loading products: {error.message}</div>

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Our Products</h1>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {data?.map((product) => (
          <Link
            key={product.id}
            to={`/products/${product.id}`}
            className="no-underline text-inherit"
          >
            <div className="bg-white rounded-lg shadow p-4 hover:shadow-md transition-shadow cursor-pointer h-full flex flex-col">
              <h3 className="text-lg font-medium mb-1">{product.title}</h3>
              <p className="text-xs text-slate-500 mb-1">
                SKU: {product.sku || 'N/A'}
              </p>
              <p className="text-lg font-semibold text-primary">
                ₹{product.base_price}
              </p>
              <span
                className={`mt-2 inline-flex items-center rounded-full px-3 py-0.5 text-xs font-medium text-white ${
                  product.status === 'ready'
                    ? 'bg-emerald-500'
                    : 'bg-amber-500'
                }`}
              >
                {product.status}
              </span>
            </div>
          </Link>
        ))}
      </div>

      {data?.length === 0 && (
        <div className="bg-white rounded-lg shadow p-4">
          <p className="text-slate-700">No products available yet. Check back soon!</p>
        </div>
      )}
    </div>
  )
}

export default Products
