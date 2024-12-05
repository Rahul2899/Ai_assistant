import { useState, useEffect } from 'react'
import Head from 'next/head'

export default function Home() {
  const [overview, setOverview] = useState('')
  const [issue, setIssue] = useState('')
  const [resolution, setResolution] = useState('')

  useEffect(() => {
    fetchSystemOverview()
  }, [])

  const fetchSystemOverview = async () => {
    const res = await fetch('http://localhost:8000/system-overview')
    const data = await res.json()
    setOverview(data.overview)
  }

  const handleResolveIncident = async () => {
    const res = await fetch('http://localhost:8000/resolve-incident', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description: issue })
    })
    const data = await res.json()
    setResolution(data.resolution)
  }

  const handleDocumentIncident = async () => {
    await fetch('http://localhost:8000/document-incident', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description: issue, resolution: resolution })
    })
    alert('Incident documented successfully')
  }

  return (
    <div className="container mx-auto p-4">
      <Head>
        <title>AI-Powered Operations Assistant</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main>
        <h1 className="text-4xl font-bold mb-4">AI-Powered Operations Assistant</h1>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-2">System Overview</h2>
          <p className="bg-gray-100 p-4 rounded">{overview}</p>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-2">Incident Resolution</h2>
          <textarea
            className="w-full p-2 border rounded mb-2"
            value={issue}
            onChange={(e) => setIssue(e.target.value)}
            placeholder="Describe the issue..."
          />
          <button
            className="bg-blue-500 text-white px-4 py-2 rounded"
            onClick={handleResolveIncident}
          >
            Resolve Incident
          </button>
          {resolution && (
            <div className="mt-4 bg-gray-100 p-4 rounded">
              <h3 className="font-semibold">Resolution:</h3>
              <p>{resolution}</p>
            </div>
          )}
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-2">Incident Documentation</h2>
          <button
            className="bg-green-500 text-white px-4 py-2 rounded"
            onClick={handleDocumentIncident}
            disabled={!issue || !resolution}
          >
            Document Incident
          </button>
        </section>
      </main>
    </div>
  )
}