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
    <div style={{ maxWidth: '400px', margin: '0 auto' }}>
      <div className="card">
        <h2>Login to Sagar Furniture</h2>
        
        <form onSubmit={handleSubmit} style={{ marginTop: '2rem' }}>
          <div className="form-group">
            <label>Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {error && (
            <div style={{ color: 'red', marginBottom: '1rem' }}>
              {error}
            </div>
          )}

          <button type="submit" className="btn btn-primary" disabled={loading} style={{ width: '100%' }}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <div style={{ marginTop: '2rem', fontSize: '0.9rem', color: '#666' }}>
          <p><strong>Demo Credentials:</strong></p>
          <p>Admin: admin / admin123</p>
          <p>Staff: staff / staff123</p>
          <p>Customer: customer / customer123</p>
        </div>
      </div>
    </div>
  )
}

export default Login
