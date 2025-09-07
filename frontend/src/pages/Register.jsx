import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { api, setToken } from '../lib/api'

export default function Register() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()

  async function onSubmit(e) {
    e.preventDefault()
    setError('')
    try {
      await api.post('/auth/register', { email, password })
      const { data } = await api.post('/auth/login', { email, password })
      setToken(data.access_token)
      navigate('/dashboard')
    } catch (e) {
      setError('Registration failed')
    }
  }

  return (
    <div className="max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4">Register</h1>
      <form onSubmit={onSubmit} className="space-y-3">
        <input value={email} onChange={e=>setEmail(e.target.value)} type="email" placeholder="Email" className="w-full border rounded px-3 py-2" />
        <input value={password} onChange={e=>setPassword(e.target.value)} type="password" placeholder="Password" className="w-full border rounded px-3 py-2" />
        {error && <div className="text-red-600 text-sm">{error}</div>}
        <button className="px-4 py-2 bg-black text-white rounded w-full">Create account</button>
      </form>
      <p className="mt-3 text-sm">Have an account? <Link to="/login" className="underline">Login</Link></p>
    </div>
  )
}


