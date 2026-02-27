import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import {
  getLookups,
  createLookup,
  updateLookup,
  deleteLookup,
} from '../../api'

function AdminInventory() {
  const queryClient = useQueryClient()
  const [search, setSearch] = useState('')
  const [editing, setEditing] = useState(null) // null = new, object = edit
  const [form, setForm] = useState({
    set: '',
    key: '',
    value: '',
    description: '',
    scope: 'GLOBAL',
    order_by: 0,
    is_active: true,
  })

  const { data: lookups, isLoading } = useQuery({
    queryKey: ['lookups', { search }],
    queryFn: () => getLookups({ search }).then((res) => res.data),
  })

  const resetForm = () => {
    setEditing(null)
    setForm({
      set: '',
      key: '',
      value: '',
      description: '',
      scope: 'GLOBAL',
      order_by: 0,
      is_active: true,
    })
  }

  const upsertMutation = useMutation({
    mutationFn: (payload) => {
      if (editing?.id) {
        return updateLookup(editing.id, payload)
      }
      return createLookup(payload)
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['lookups'])
      resetForm()
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (id) => deleteLookup(id),
    onSuccess: () => {
      queryClient.invalidateQueries(['lookups'])
    },
  })

  const startEdit = (row) => {
    setEditing(row)
    setForm({
      set: row.set,
      key: row.key,
      value: row.value,
      description: row.description || '',
      scope: row.scope,
      order_by: row.order_by,
      is_active: row.is_active,
    })
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    upsertMutation.mutate(form)
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Lookup Management</h1>

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-medium mb-4">
          {editing ? 'Edit Lookup' : 'Add New Lookup'}
        </h2>
        <form
          onSubmit={handleSubmit}
          className="grid gap-4 md:grid-cols-2 lg:grid-cols-3"
        >
          <label className="flex flex-col text-sm">
            <span className="font-medium">Set</span>
            <input
              type="text"
              className="mt-1 rounded border border-slate-300 px-2 py-1 text-sm"
              value={form.set}
              onChange={(e) => setForm({ ...form, set: e.target.value })}
              required
            />
          </label>
          <label className="flex flex-col text-sm">
            <span className="font-medium">Key</span>
            <input
              type="text"
              className="mt-1 rounded border border-slate-300 px-2 py-1 text-sm uppercase tracking-wide"
              value={form.key}
              onChange={(e) => setForm({ ...form, key: e.target.value })}
              required
            />
          </label>
          <label className="flex flex-col text-sm">
            <span className="font-medium">Value</span>
            <input
              type="text"
              className="mt-1 rounded border border-slate-300 px-2 py-1 text-sm"
              value={form.value}
              onChange={(e) => setForm({ ...form, value: e.target.value })}
              required
            />
          </label>
          <label className="flex flex-col text-sm md:col-span-2">
            <span className="font-medium">Description</span>
            <input
              type="text"
              className="mt-1 rounded border border-slate-300 px-2 py-1 text-sm"
              value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })}
            />
          </label>
          <label className="flex flex-col text-sm">
            <span className="font-medium">Scope</span>
            <select
              className="mt-1 rounded border border-slate-300 px-2 py-1 text-sm"
              value={form.scope}
              onChange={(e) => setForm({ ...form, scope: e.target.value })}
            >
              <option value="GLOBAL">GLOBAL</option>
              <option value="TENANT">TENANT</option>
            </select>
          </label>
          <label className="flex flex-col text-sm">
            <span className="font-medium">Order By</span>
            <input
              type="number"
              className="mt-1 rounded border border-slate-300 px-2 py-1 text-sm"
              value={form.order_by}
              onChange={(e) => setForm({ ...form, order_by: Number(e.target.value) })}
            />
          </label>
          <label className="flex items-center gap-2 text-sm mt-6">
            <input
              type="checkbox"
              className="h-4 w-4 rounded border-slate-300"
              checked={form.is_active}
              onChange={(e) => setForm({ ...form, is_active: e.target.checked })}
            />
            <span>Active</span>
          </label>
          <div className="flex justify-end items-center gap-2 md:col-span-2 lg:col-span-3 mt-2">
            <button
              type="button"
              onClick={resetForm}
              className="inline-flex items-center rounded border border-slate-300 px-3 py-1 text-sm hover:bg-slate-50"
            >
              Clear
            </button>
            <button
              type="submit"
              disabled={upsertMutation.isLoading}
              className="inline-flex items-center rounded bg-primary px-4 py-1.5 text-sm font-semibold text-white hover:bg-secondary"
            >
              {editing ? 'Update' : 'Save'}
            </button>
          </div>
        </form>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center justify-between gap-4 mb-4">
          <h2 className="text-lg font-medium">Lookup Values</h2>
          <input
            type="text"
            placeholder="Search by set, key, value..."
            className="w-full max-w-xs rounded border border-slate-300 px-2 py-1 text-sm"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        {isLoading ? (
          <p className="text-sm text-slate-500">Loading...</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full border-collapse text-sm">
              <thead>
                <tr className="border-b border-slate-200 bg-slate-50">
                  <th className="px-3 py-2 text-left font-medium text-slate-700">Set</th>
                  <th className="px-3 py-2 text-left font-medium text-slate-700">Key</th>
                  <th className="px-3 py-2 text-left font-medium text-slate-700">Value</th>
                  <th className="px-3 py-2 text-left font-medium text-slate-700">Scope</th>
                  <th className="px-3 py-2 text-left font-medium text-slate-700">Order</th>
                  <th className="px-3 py-2 text-left font-medium text-slate-700">Active</th>
                  <th className="px-3 py-2 text-left font-medium text-slate-700">Actions</th>
                </tr>
              </thead>
              <tbody>
                {(lookups || []).map((row) => (
                  <tr key={row.id} className="border-b border-slate-100 hover:bg-slate-50">
                    <td className="px-3 py-2 font-mono text-xs">{row.set}</td>
                    <td className="px-3 py-2 font-mono text-xs">{row.key}</td>
                    <td className="px-3 py-2">{row.value}</td>
                    <td className="px-3 py-2 text-xs text-slate-600">{row.scope}</td>
                    <td className="px-3 py-2 text-right">{row.order_by}</td>
                    <td className="px-3 py-2">{row.is_active ? 'Yes' : 'No'}</td>
                    <td className="px-3 py-2 space-x-2">
                      <button
                        type="button"
                        className="text-primary hover:underline text-xs"
                        onClick={() => startEdit(row)}
                      >
                        Edit
                      </button>
                      <button
                        type="button"
                        className="text-red-600 hover:underline text-xs"
                        onClick={() =>
                          window.confirm('Delete this lookup?') &&
                          deleteMutation.mutate(row.id)
                        }
                      >
                        Delete
                      </button>
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

export default AdminInventory
