import { useState, useMemo, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import {
  getProducts,
  getCategories,
  getCatalogCodes,
  createProduct,
  getProduct,
  updateProduct,
} from '../../api'

function AdminProducts() {
  const queryClient = useQueryClient()
  const [showEditor, setShowEditor] = useState(false)
  const [editorMode, setEditorMode] = useState('create') // 'create' | 'edit'
  const [editingProduct, setEditingProduct] = useState(null)

  const {
    data: products = [],
    isLoading: productsLoading,
    isError: productsError,
  } = useQuery({
    queryKey: ['admin-products'],
    queryFn: () => getProducts().then((res) => res.data),
  })

  const { data: categories = [] } = useQuery({
    queryKey: ['categories'],
    queryFn: () => getCategories().then((res) => res.data),
  })

  const { data: catalogCodes } = useQuery({
    queryKey: ['catalog-codes'],
    queryFn: () => getCatalogCodes().then((res) => res.data),
  })

  const handleCreated = () => {
    queryClient.invalidateQueries({ queryKey: ['admin-products'] })
    setShowEditor(false)
    setEditingProduct(null)
    setEditorMode('create')
  }

  const handleUpdated = () => {
    queryClient.invalidateQueries({ queryKey: ['admin-products'] })
    setShowEditor(false)
    setEditingProduct(null)
    setEditorMode('create')
  }

  const handleCreateClick = () => {
    setEditorMode('create')
    setEditingProduct(null)
    setShowEditor(true)
  }

  const handleEditClick = async (productId) => {
    try {
      setEditorMode('edit')
      setShowEditor(true)
      setEditingProduct(null)
      const res = await getProduct(productId)
      setEditingProduct(res.data)
    } catch (e) {
      console.error(e)
      alert('Failed to load product for editing')
      setShowEditor(false)
      setEditingProduct(null)
      setEditorMode('create')
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Manage Products</h1>
        <button
          className="inline-flex items-center rounded bg-primary px-4 py-1.5 text-sm font-semibold text-white hover:bg-secondary"
          onClick={handleCreateClick}
        >
          Create New Product
        </button>
      </div>

      {showEditor && (
        <div className="bg-white rounded-lg shadow p-6">
          <ProductEditor
            categories={categories}
            catalog={catalogCodes?.product}
            mode={editorMode}
            initialProduct={editingProduct}
            existingProducts={products}
            onCancel={() => setShowEditor(false)}
            onCreated={handleCreated}
            onUpdated={handleUpdated}
          />
        </div>
      )}

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-medium mb-3">Existing Products</h2>
        {productsLoading && <p className="text-sm text-slate-500">Loading products...</p>}
        {productsError && <p className="text-sm text-red-600">Error loading products.</p>}
        {!productsLoading && !productsError && products.length === 0 && (
          <p className="text-sm text-slate-600">
            No products yet. Click "Create New Product" to add one.
          </p>
        )}
        {!productsLoading && !productsError && products.length > 0 && (
          <div className="overflow-x-auto mt-3">
            <table className="min-w-full border-collapse text-sm">
              <thead>
                <tr className="border-b border-slate-200 bg-slate-50">
                  <th className="px-3 py-2 text-left font-medium text-slate-700">Name</th>
                  <th className="px-3 py-2 text-left font-medium text-slate-700">SKU</th>
                  <th className="px-3 py-2 text-right font-medium text-slate-700">Base Price</th>
                  <th className="px-3 py-2 text-left font-medium text-slate-700">Status</th>
                </tr>
              </thead>
              <tbody>
                {products.map((p) => (
                  <tr key={p.id} className="border-b border-slate-100 hover:bg-slate-50">
                    <td className="px-3 py-2">
                      <button
                        type="button"
                        className="text-primary hover:underline"
                        onClick={() => handleEditClick(p.id)}
                      >
                        {p.title}
                      </button>
                    </td>
                    <td className="px-3 py-2 font-mono text-xs">{p.sku || '-'}</td>
                    <td className="px-3 py-2 text-right">
                      ₹{Number(p.base_price).toFixed(2)}
                    </td>
                    <td className="px-3 py-2 text-xs uppercase tracking-wide">
                      {p.status}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}

function ProductEditor({ categories, catalog, mode = 'create', initialProduct, existingProducts = [], onCancel, onCreated, onUpdated }) {
  const queryClient = useQueryClient()

  const materials = catalog?.materials || []
  const finishes = catalog?.finishes || []
  const sizeOptions = catalog?.sizes?.generic || []

  const [form, setForm] = useState({
    name: '',
    description: '',
    basePrice: '',
    categoryId: '',
    subcategoryId: '',
    modelCode: '',
    materialCode: materials[0]?.code || 'WO',
    finishCode: finishes[0]?.code || 'NAT',
    sizeCode: sizeOptions[0]?.code || 'STD',
    customSku: '',
    useCustomSku: false,
    status: 'draft',
    isCustomizable: false,
  })

  const [cloneSourceId, setCloneSourceId] = useState('')

  // When editing, prefill the form once the product is loaded
  useEffect(() => {
    if (mode === 'edit' && initialProduct) {
      setForm((prev) => ({
        ...prev,
        name: initialProduct.title || '',
        description: initialProduct.description || '',
        basePrice: initialProduct.base_price != null ? String(initialProduct.base_price) : '',
        categoryId: initialProduct.category_id ? String(initialProduct.category_id) : '',
        subcategoryId: initialProduct.subcategory_id ? String(initialProduct.subcategory_id) : '',
        modelCode: initialProduct.model_code || '',
        // treat existing SKU as custom to preserve it exactly
        customSku: initialProduct.sku || '',
        useCustomSku: !!initialProduct.sku,
        status: initialProduct.status || 'draft',
        isCustomizable: !!initialProduct.is_customizable,
      }))
    }
  }, [mode, initialProduct])

  const selectedCategory = categories.find(
    (c) => String(c.id) === String(form.categoryId),
  )
  const subcategories = selectedCategory?.subcategories || []

  const selectedSubcategory = subcategories.find(
    (sc) => String(sc.id) === String(form.subcategoryId),
  )

  const autoModelCode = slugToCode(form.name)

  const skuPreview = useMemo(() => {
    if (form.useCustomSku && form.customSku.trim()) {
      return form.customSku.trim()
    }
    const parts = [
      selectedCategory?.code,
      selectedSubcategory?.code,
      form.modelCode || autoModelCode,
      form.materialCode,
      form.finishCode,
      form.sizeCode,
    ].filter(Boolean)
    return parts.join('-')
  }, [
    form.useCustomSku,
    form.customSku,
    form.modelCode,
    form.materialCode,
    form.finishCode,
    form.sizeCode,
    autoModelCode,
    selectedCategory?.code,
    selectedSubcategory?.code,
  ])

  const mutation = useMutation({
    mutationFn: (payload) => {
      if (mode === 'edit' && initialProduct?.id) {
        return updateProduct(initialProduct.id, payload).then((res) => res.data)
      }
      return createProduct(payload).then((res) => res.data)
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['admin-products'] })
      if (mode === 'edit') {
        onUpdated?.(data)
      } else {
        onCreated?.(data)
      }
    },
  })

  const handleChange = (field, value) => {
    setForm((prev) => ({ ...prev, [field]: value }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!form.name || !form.basePrice || !form.categoryId) {
      alert('Name, base price, and category are required.')
      return
    }

    const payload = {
      title: form.name,
      description: form.description,
      base_price: Number(form.basePrice),
      category_id: Number(form.categoryId),
      subcategory_id: form.subcategoryId ? Number(form.subcategoryId) : null,
      model_code: form.modelCode || autoModelCode,
      sku: skuPreview,
      status: form.status,
      is_customizable: form.isCustomizable,
    }

    mutation.mutate(payload)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="flex" style={{ justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>{mode === 'edit' ? 'Edit Product' : 'New Product'}</h2>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button type="button" className="btn" onClick={onCancel}>
            Cancel
          </button>
          <button
            type="submit"
            className="btn btn-primary"
            disabled={mutation.isLoading}
          >
            {mutation.isLoading ? 'Saving...' : 'Save Product'}
          </button>
        </div>
      </div>

      {mode === 'create' && existingProducts.length > 0 && (
        <div className="section" style={{ marginTop: '0.75rem', borderTop: '1px solid #eee', paddingTop: '0.75rem' }}>
          <label className="label">Clone from existing product</label>
          <select
            className="input"
            value={cloneSourceId}
            onChange={async (e) => {
              const value = e.target.value
              setCloneSourceId(value)
              if (!value) return
              try {
                const res = await getProduct(value)
                const prod = res.data
                setForm((prev) => ({
                  ...prev,
                  name: prod.title || '',
                  description: prod.description || '',
                  basePrice: prod.base_price != null ? String(prod.base_price) : '',
                  categoryId: prod.category_id ? String(prod.category_id) : '',
                  subcategoryId: prod.subcategory_id ? String(prod.subcategory_id) : '',
                  modelCode: prod.model_code || '',
                  // when cloning, recompute SKU by default
                  customSku: '',
                  useCustomSku: false,
                  status: prod.status || 'draft',
                  isCustomizable: !!prod.is_customizable,
                }))
              } catch (err) {
                console.error(err)
                alert('Failed to load product to clone from')
              }
            }}
          >
            <option value="">Do not clone</option>
            {existingProducts.map((p) => (
              <option key={p.id} value={p.id}>
                {p.title} ({p.sku || 'no SKU'})
              </option>
            ))}
          </select>
          <p className="hint">Choose a product to copy base details from, then adjust codes if needed.</p>
        </div>
      )}

      {/* Basic info */}
      <section className="section" style={{ borderTop: '1px solid #eee', paddingTop: '1rem' }}>
        <h3>Basic info</h3>
        <div className="grid" style={{ gap: '1rem' }}>
          <div>
            <label className="label">Name</label>
            <input
              className="input"
              value={form.name}
              onChange={(e) => handleChange('name', e.target.value)}
            />
          </div>
          <div>
            <label className="label">Base price</label>
            <input
              type="number"
              step="0.01"
              className="input"
              value={form.basePrice}
              onChange={(e) => handleChange('basePrice', e.target.value)}
            />
          </div>
        </div>
        <div style={{ marginTop: '1rem' }}>
          <label className="label">Description</label>
          <textarea
            className="input"
            rows={3}
            value={form.description}
            onChange={(e) => handleChange('description', e.target.value)}
          />
        </div>

        <div style={{ marginTop: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <input
            id="isCustomizable"
            type="checkbox"
            checked={form.isCustomizable}
            onChange={(e) => handleChange('isCustomizable', e.target.checked)}
          />
          <label htmlFor="isCustomizable" className="hint">
            Product is customizable
          </label>
        </div>
      </section>

      {/* Classification & codes */}
      <section className="section" style={{ borderTop: '1px solid #eee', paddingTop: '1rem' }}>
        <h3>Classification & code</h3>

        <div className="grid" style={{ gap: '1rem' }}>
          <div>
            <label className="label">Category</label>
            <select
              className="input"
              value={form.categoryId}
              onChange={(e) => {
                handleChange('categoryId', e.target.value)
                handleChange('subcategoryId', '')
              }}
            >
              <option value="">Select category</option>
              {categories.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name} {c.code ? `(${c.code})` : ''}
                </option>
              ))}
            </select>
            <p className="hint">Code: {selectedCategory?.code || '-'}</p>
          </div>

          <div>
            <label className="label">Subcategory</label>
            <select
              className="input"
              value={form.subcategoryId}
              onChange={(e) => handleChange('subcategoryId', e.target.value)}
              disabled={!selectedCategory}
            >
              <option value="">Select subcategory</option>
              {subcategories.map((sc) => (
                <option key={sc.id} value={sc.id}>
                  {sc.name} {sc.code ? `(${sc.code})` : ''}
                </option>
              ))}
            </select>
            <p className="hint">Code: {selectedSubcategory?.code || '-'}</p>
          </div>
        </div>

        <div className="grid" style={{ gap: '1rem', marginTop: '1rem' }}>
          <div>
            <label className="label">Model code</label>
            <input
              className="input"
              placeholder={autoModelCode || 'ROYC'}
              value={form.modelCode}
              onChange={(e) => handleChange('modelCode', e.target.value.toUpperCase())}
            />
            <p className="hint">Suggested: {autoModelCode || '—'}</p>
          </div>

          <div>
            <label className="label">Status</label>
            <select
              className="input"
              value={form.status}
              onChange={(e) => handleChange('status', e.target.value)}
            >
              <option value="draft">Draft</option>
              <option value="ready">Ready</option>
              <option value="archived">Archived</option>
            </select>
          </div>
        </div>

        <div className="grid" style={{ gap: '1rem', marginTop: '1rem' }}>
          <div>
            <label className="label">Material</label>
            <select
              className="input"
              value={form.materialCode}
              onChange={(e) => handleChange('materialCode', e.target.value)}
            >
              {materials.map((m) => (
                <option key={m.code} value={m.code}>
                  {m.label} ({m.code})
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="label">Finish</label>
            <select
              className="input"
              value={form.finishCode}
              onChange={(e) => handleChange('finishCode', e.target.value)}
            >
              {finishes.map((f) => (
                <option key={f.code} value={f.code}>
                  {f.label} ({f.code})
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="grid" style={{ gap: '1rem', marginTop: '1rem' }}>
          <div>
            <label className="label">Size / variant</label>
            <select
              className="input"
              value={form.sizeCode}
              onChange={(e) => handleChange('sizeCode', e.target.value)}
            >
              {sizeOptions.map((s) => (
                <option key={s.code} value={s.code}>
                  {s.label} ({s.code})
                </option>
              ))}
            </select>
          </div>
        </div>

        <div style={{ marginTop: '1rem' }}>
          <label className="label">SKU preview</label>
          <div
            style={{
              fontFamily: 'monospace',
              background: '#f5f5f5',
              padding: '0.5rem 0.75rem',
              borderRadius: '4px',
            }}
          >
            {skuPreview || 'Select category and enter model details'}
          </div>

          <div style={{ marginTop: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <input
              id="useCustomSku"
              type="checkbox"
              checked={form.useCustomSku}
              onChange={(e) => handleChange('useCustomSku', e.target.checked)}
            />
            <label htmlFor="useCustomSku" className="hint">
              Override SKU manually
            </label>
          </div>

          {form.useCustomSku && (
            <input
              className="input"
              style={{ marginTop: '0.5rem', fontFamily: 'monospace' }}
              value={form.customSku}
              onChange={(e) => handleChange('customSku', e.target.value.toUpperCase())}
              placeholder="Custom SKU"
            />
          )}
        </div>
      </section>
    </form>
  )
}

function slugToCode(name) {
  if (!name) return ''
  return name
    .split(/\s+/)
    .map((part) => part[0]?.toUpperCase())
    .join('')
    .slice(0, 4)
}

export default AdminProducts
