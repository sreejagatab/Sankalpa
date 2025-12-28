
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from agents.base import BaseAgent

class MarkdownEditorAgent(BaseAgent):
    def run(self, input_data):
        files = {
            "frontend/components/MarkdownEditor.tsx": """
import { useState } from 'react';
import ReactMarkdown from 'react-markdown';

export default function MarkdownEditor() {
  const [markdown, setMarkdown] = useState('');

  return (
    <div className='p-4'>
      <textarea
        value={markdown}
        onChange={(e) => setMarkdown(e.target.value)}
        className='w-full h-40 p-2 border rounded mb-4'
      />
      <h2 className='text-lg font-bold mb-2'>Preview:</h2>
      <div className='border p-4 rounded bg-white dark:bg-gray-800'>
        <ReactMarkdown>{markdown}</ReactMarkdown>
      </div>
    </div>
  );
}
"""
        }

        return {
            "message": "Markdown editor component generated.",
            "files": files
        }
