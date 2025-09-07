import React from 'react'
import ReactDOM from 'react-dom/client'
import './styles.css'
import axios from 'axios'
import SummarizeForm from './components/SummarizeForm'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import ArticleDetail from './pages/ArticleDetail'
import Login from './pages/Login'
import Register from './pages/Register'
import NewArticle from './pages/NewArticle'
import Profile from './pages/Profile'

function Layout({ children }) {
  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <header className="border-b bg-white">
        <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
          <Link to="/" className="text-2xl font-bold">InstaBrief</Link>
          <nav className="space-x-4">
            <Link to="/" className="hover:underline">Home</Link>
            <Link to="/dashboard" className="hover:underline">Dashboard</Link>
            <Link to="/articles/new" className="hover:underline">New</Link>
            <Link to="/login" className="hover:underline">Login</Link>
            <button onClick={()=>{ localStorage.removeItem('token'); alert('Logged out') }} className="hover:underline">Logout</button>
            <Link to="/profile" className="hover:underline">Profile</Link>
          </nav>
        </div>
      </header>
      <main className="max-w-5xl mx-auto px-6 py-6">{children}</main>
    </div>
  )
}

function Home() {
  return (
    <Layout>
      <div className="max-w-3xl">
        <h1 className="text-3xl font-bold mb-4">Summarize articles instantly</h1>
        <SummarizeForm />
      </div>
    </Layout>
  )
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<Layout><Dashboard /></Layout>} />
        <Route path="/articles/:id" element={<Layout><ArticleDetail /></Layout>} />
        <Route path="/articles/new" element={<Layout><NewArticle /></Layout>} />
        <Route path="/login" element={<Layout><Login /></Layout>} />
        <Route path="/register" element={<Layout><Register /></Layout>} />
        <Route path="/profile" element={<Layout><Profile /></Layout>} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>,
)


