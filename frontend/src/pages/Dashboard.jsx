import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'

export default function Dashboard() {
  const [items, setItems] = useState([])
  const [q, setQ] = useState('')
  const [semantic, setSemantic] = useState(false)
  const [page, setPage] = useState(0)

  async function load(nextPage = page) {
    const params = { skip: nextPage * 20, limit: 20 }
    if (q) { params.q = q; params.semantic = semantic }
    const { data } = await axios.get('/api/articles', { params })
    setItems(data)
    setPage(nextPage)
  }

  useEffect(() => { load() }, [])

  return (
    <div>
      <div className="flex items-center gap-3 mb-4">
        <input value={q} onChange={e=>setQ(e.target.value)} placeholder="Search..." className="border rounded px-3 py-2" />
        <label className="flex items-center gap-2 text-sm"><input type="checkbox" checked={semantic} onChange={e=>setSemantic(e.target.checked)} /> Semantic</label>
        <button onClick={()=>load(0)} className="px-3 py-2 bg-black text-white rounded">Search</button>
      </div>
      <ul className="space-y-3">
        {items.map(a => (
          <li key={a.id} className="border rounded p-3 bg-white">
            <Link to={`/articles/${a.id}`} className="font-semibold hover:underline">{a.title || 'Untitled'}</Link>
            <p className="text-sm text-gray-600 line-clamp-2">{a.content?.slice(0,200)}</p>
            {a.tags?.length ? (<div className="mt-2 text-xs text-gray-500">{a.tags.join(', ')}</div>) : null}
          </li>
        ))}
      </ul>
      <div className="mt-4 flex gap-2">
        <button onClick={()=>load(Math.max(0, page-1))} className="px-3 py-2 border rounded" disabled={page===0}>Prev</button>
        <button onClick={()=>load(page+1)} className="px-3 py-2 border rounded">Next</button>
      </div>
    </div>
  )
}


