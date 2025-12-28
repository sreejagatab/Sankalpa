
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from agents.base import BaseAgent

class FrontendBuilderAgent(BaseAgent):
    def run(self, input_data):
        prompt = input_data.get("prompt", "")

        files = {
            "frontend/pages/index.tsx": """
import Head from 'next/head';

export default function Home() {
  return (
    <>
      <Head>
        <title>Sankalpa App</title>
      </Head>
      <main className=\"flex min-h-screen items-center justify-center\">
        <h1 className=\"text-4xl font-bold\">Welcome to Sankalpa</h1>
      </main>
    </>
  );
}
""",
            "frontend/components/Navbar.tsx": """
export default function Navbar() {
  return (
    <nav className=\"p-4 shadow-md bg-white dark:bg-gray-900\">
      <div className=\"text-xl font-bold\">Sankalpa</div>
    </nav>
  );
}
""",
            "frontend/styles/globals.css": """
@tailwind base;
@tailwind components;
@tailwind utilities;
"""
        }

        return {
            "message": "Frontend scaffold generated.",
            "files": files
        }
