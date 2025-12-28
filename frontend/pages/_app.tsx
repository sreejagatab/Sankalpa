import type { AppProps } from 'next/app';
import '../styles/globals.css';
import { GlobalAlertProvider } from '../components/alerts/GlobalAlertProvider';
import { WebSocketProvider } from '../components/collaboration/WebSocketProvider';
import Link from 'next/link';

export default function App({ Component, pageProps }: AppProps) {
  return (
    <GlobalAlertProvider>
      <WebSocketProvider>
        <div className="min-h-screen flex flex-col">
          <header className="bg-indigo-600 text-white shadow-md">
            <div className="container mx-auto px-4 py-3 flex justify-between items-center">
              <h1 className="text-2xl font-bold">Sankalpa</h1>
              <nav>
                <ul className="flex space-x-4">
                  <li><Link href="/" className="hover:text-gray-200">Home</Link></li>
                  <li><Link href="/playground" className="hover:text-gray-200">Playground</Link></li>
                  <li><Link href="/composer" className="hover:text-gray-200">Composer</Link></li>
                  <li><Link href="/memory" className="hover:text-gray-200">Memory</Link></li>
                  <li><Link href="/dashboard" className="hover:text-gray-200">Dashboard</Link></li>
                  <li><Link href="/chat-dashboard" className="hover:text-gray-200">Chat</Link></li>
                </ul>
              </nav>
            </div>
          </header>
          
          <main className="flex-grow container mx-auto px-4 py-6">
            <Component {...pageProps} />
          </main>
          
          <footer className="bg-gray-100 border-t">
            <div className="container mx-auto px-4 py-4 text-center text-gray-600">
              <p>Sankalpa - AI-Powered Development Automation Platform</p>
            </div>
          </footer>
        </div>
      </WebSocketProvider>
    </GlobalAlertProvider>
  );
}