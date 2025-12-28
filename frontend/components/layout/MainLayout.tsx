import React, { ReactNode } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';

interface MainLayoutProps {
  children: ReactNode;
}

const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  const router = useRouter();

  const navItems = [
    { name: 'Home', path: '/' },
    { name: 'Playground', path: '/playground' },
    { name: 'Composer', path: '/composer' },
    { name: 'Memory', path: '/memory' },
    { name: 'Agents', path: '/agents' },
    { name: 'Agent Chat', path: '/agent-chat' },
    { name: 'Dashboard', path: '/dashboard' },
  ];

  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-indigo-600 text-white shadow-md">
        <div className="container mx-auto px-4 py-3 flex justify-between items-center">
          <Link href="/" className="text-2xl font-bold">
            Sankalpa
          </Link>
          <nav className="hidden md:flex space-x-6">
            {navItems.map((item) => (
              <Link
                key={item.path}
                href={item.path}
                className={`hover:text-indigo-200 transition ${
                  router.pathname === item.path ? 'font-bold text-white' : 'text-indigo-100'
                }`}
              >
                {item.name}
              </Link>
            ))}
          </nav>
          <div className="md:hidden">
            {/* Mobile menu button goes here if needed */}
            <button className="p-2">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                className="h-6 w-6"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              </svg>
            </button>
          </div>
        </div>
      </header>

      <main className="flex-grow container mx-auto px-4 py-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          {children}
        </div>
      </main>

      <footer className="bg-gray-100 border-t">
        <div className="container mx-auto px-4 py-4 text-center text-gray-600">
          <p>Sankalpa - AI-Powered Development Automation Platform</p>
        </div>
      </footer>
    </div>
  );
};

export default MainLayout;