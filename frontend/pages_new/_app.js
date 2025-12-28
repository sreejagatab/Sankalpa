import '../styles/globals.css'

function MyApp({ Component, pageProps }) {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-indigo-600 text-white p-4">
        <div className="container mx-auto">
          <h1 className="text-2xl font-bold">Sankalpa</h1>
        </div>
      </header>
      
      <main className="flex-grow">
        <Component {...pageProps} />
      </main>
      
      <footer className="bg-gray-100 p-4 border-t">
        <div className="container mx-auto text-center text-gray-600">
          <p>Sankalpa - AI-Powered Development Automation Platform</p>
        </div>
      </footer>
    </div>
  )
}

export default MyApp