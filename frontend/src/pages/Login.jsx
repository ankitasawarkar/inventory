import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { login } from '../api'

function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await login(username, password)
      localStorage.setItem('token', response.data.access_token)
      
      // Decode JWT to get user info (simple approach)
      const payload = JSON.parse(atob(response.data.access_token.split('.')[1]))
      localStorage.setItem('user', JSON.stringify({ username: payload.sub, role: payload.role || 'customer' }))
      
      navigate('/')
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-md mx-auto">
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold">Login to Sagar Furniture</h2>

        <form onSubmit={handleSubmit} className="mt-6 space-y-4">
          <div className="space-y-1 text-sm">
            <label className="block font-medium">Username</label>
            <input
              type="text"
              className="w-full rounded border border-slate-300 px-3 py-2 text-sm"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>

          <div className="space-y-1 text-sm">
            <label className="block font-medium">Password</label>
            <input
              type="password"
              className="w-full rounded border border-slate-300 px-3 py-2 text-sm"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {error && (
            <div className="text-sm text-red-600">{error}</div>
          )}

          <button
            type="submit"
            className="w-full inline-flex justify-center items-center rounded bg-primary px-4 py-2 text-sm font-semibold text-white hover:bg-secondary disabled:opacity-60"
            disabled={loading}
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <div className="mt-6 text-xs text-slate-600 space-y-1">
          <p className="font-semibold">Demo Credentials:</p>
          <p>Admin: admin / admin123</p>
          <p>Staff: staff / staff123</p>
          <p>Customer: customer / customer123</p>
        </div>
      </div>
    </div>
  )
}

export default Login
