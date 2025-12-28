import React from 'react'

export default function Home() {
  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold text-center mb-6">Sankalpa</h1>
      <p className="text-xl text-center mb-8">AI-Powered Development Automation Platform</p>
      
      <div className="bg-yellow-100 p-4 rounded-lg text-center mb-12">
        <p className="text-yellow-800">Demo Mode - API Unavailable</p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="border rounded-lg p-6 shadow-sm">
          <h2 className="text-2xl font-semibold mb-3">Playground</h2>
          <p className="mb-4">Test and experiment with AI agents in an interactive environment</p>
          <a href="/playground" className="text-blue-600 hover:underline">Explore →</a>
        </div>
        
        <div className="border rounded-lg p-6 shadow-sm">
          <h2 className="text-2xl font-semibold mb-3">Composer</h2>
          <p className="mb-4">Build and visualize complex agent workflows with drag-and-drop</p>
          <a href="/composer" className="text-blue-600 hover:underline">Explore →</a>
        </div>
        
        <div className="border rounded-lg p-6 shadow-sm">
          <h2 className="text-2xl font-semibold mb-3">Memory</h2>
          <p className="mb-4">Explore and manage agent memory and context</p>
          <a href="/memory" className="text-blue-600 hover:underline">Explore →</a>
        </div>
      </div>
    </div>
  )
}