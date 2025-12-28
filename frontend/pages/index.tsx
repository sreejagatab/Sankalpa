import React from 'react';
import Head from 'next/head';
import Link from 'next/link';

interface FeatureCardProps {
  title: string;
  description: string;
  link: string;
  icon: React.ReactNode;
  color?: 'indigo' | 'emerald' | 'amber' | 'purple' | 'blue' | 'rose' | 'cyan';
}

const FeatureCard: React.FC<FeatureCardProps> = ({ 
  title, 
  description, 
  link, 
  icon, 
  color = 'indigo' 
}) => {
  const colorStyles = {
    indigo: { bg: 'bg-indigo-50', text: 'text-indigo-700', hover: 'hover:bg-indigo-100' },
    emerald: { bg: 'bg-emerald-50', text: 'text-emerald-700', hover: 'hover:bg-emerald-100' },
    amber: { bg: 'bg-amber-50', text: 'text-amber-700', hover: 'hover:bg-amber-100' },
    purple: { bg: 'bg-purple-50', text: 'text-purple-700', hover: 'hover:bg-purple-100' },
    blue: { bg: 'bg-blue-50', text: 'text-blue-700', hover: 'hover:bg-blue-100' },
    rose: { bg: 'bg-rose-50', text: 'text-rose-700', hover: 'hover:bg-rose-100' },
    cyan: { bg: 'bg-cyan-50', text: 'text-cyan-700', hover: 'hover:bg-cyan-100' },
  };
  
  const styles = colorStyles[color];

  return (
    <div className={`block border rounded-lg p-6 bg-white shadow-sm hover:shadow-md transition ${styles.hover}`}>
      <Link href={link} passHref legacyBehavior>
        <div className="contents">
          <div className="flex items-center mb-4">
            <div className={`p-2 rounded-full ${styles.bg} ${styles.text} mr-3`}>
              {icon}
            </div>
            <h3 className="text-xl font-semibold">{title}</h3>
          </div>
          <p className="text-gray-600 mb-4">{description}</p>
          <div className={`text-sm font-medium ${styles.text} flex items-center`}>
            Explore {title}
            <svg className="w-4 h-4 ml-1" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L12.586 11H5a1 1 0 110-2h7.586l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
          </div>
        </div>
      </Link>
    </div>
  );
};

const Home: React.FC = () => {
  return (
    <div>
      <Head>
        <title>Sankalpa - Ultimate AI Development Automation</title>
        <meta name="description" content="An advanced multi-agent AI platform that can autonomously build, test, and deploy projects." />
      </Head>

      <div className="space-y-8">
        <section className="text-center py-12">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 bg-clip-text text-transparent">Welcome to Sankalpa</h1>
          <p className="text-xl text-gray-600 mb-6 max-w-3xl mx-auto">
            The Ultimate AI Development Automation Platform with Self-improving Agents, Multi-model Integration, and Collaborative Workflows
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <span className="bg-blue-100 text-blue-800 text-xs font-medium px-3 py-1.5 rounded-full">GPT/LLM Automation</span>
            <span className="bg-purple-100 text-purple-800 text-xs font-medium px-3 py-1.5 rounded-full">Fine-tuning Capabilities</span>
            <span className="bg-emerald-100 text-emerald-800 text-xs font-medium px-3 py-1.5 rounded-full">Self-replicating Agents</span>
            <span className="bg-amber-100 text-amber-800 text-xs font-medium px-3 py-1.5 rounded-full">Marketplace Integrations</span>
            <span className="bg-rose-100 text-rose-800 text-xs font-medium px-3 py-1.5 rounded-full">Long-term Memory</span>
          </div>
        </section>

        <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-8">
          <FeatureCard
            title="Agent Core"
            description="Browse and interact with specialized AI agents that can autonomously build, test, and deploy complete software projects."
            link="/agents"
            icon={<svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>}
            color="indigo"
          />
          <FeatureCard
            title="Playground"
            description="Test and experiment with AI agents in an interactive environment with model selection and memory integration."
            link="/playground"
            icon={<svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>}
            color="amber"
          />
          <FeatureCard
            title="Chain Composer"
            description="Build and visualize complex agent workflows with our drag-and-drop visual interface for coordinating multi-agent systems."
            link="/composer"
            icon={<svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" /></svg>}
            color="emerald"
          />
          <FeatureCard
            title="Memory Manager"
            description="Explore and manage long-term memory with vector embeddings and contextual recall for enhanced agent capabilities."
            link="/memory"
            icon={<svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>}
            color="blue"
          />
          <FeatureCard
            title="Collaboration"
            description="Real-time collaboration and communication with team members through our WebSocket-powered platform."
            link="/chat"
            icon={<svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586m0 0L11 14h4a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2v4l.586-.586z" /></svg>}
            color="purple"
          />
          <FeatureCard
            title="Marketplace"
            description="Discover and install agents, workflows, models, and templates from our growing community marketplace."
            link="/marketplace"
            icon={<svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" /></svg>}
            color="rose"
          />
        </section>

        <section className="mt-16">
          <div className="bg-gradient-to-r from-indigo-50 to-blue-50 rounded-xl p-8 shadow-sm">
            <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">Ultimate AI Development Capabilities</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div className="bg-white p-5 rounded-lg shadow-sm">
                <div className="text-emerald-600 mb-3">
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
                  </svg>
                </div>
                <h3 className="font-medium text-lg mb-2">Self-improving Agents</h3>
                <p className="text-gray-600 text-sm">Agents that learn from interactions and improve their capabilities over time through feedback loops</p>
              </div>
              <div className="bg-white p-5 rounded-lg shadow-sm">
                <div className="text-purple-600 mb-3">
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 4a2 2 0 114 0v1a1 1 0 001 1h3a1 1 0 011 1v3a1 1 0 01-1 1h-1a2 2 0 100 4h1a1 1 0 011 1v3a1 1 0 01-1 1h-3a1 1 0 01-1-1v-1a2 2 0 10-4 0v1a1 1 0 01-1 1H7a1 1 0 01-1-1v-3a1 1 0 00-1-1H4a2 2 0 110-4h1a1 1 0 001-1V7a1 1 0 011-1h3a1 1 0 001-1V4z" />
                  </svg>
                </div>
                <h3 className="font-medium text-lg mb-2">Multi-model Integration</h3>
                <p className="text-gray-600 text-sm">Use various LLM models like GPT-4o, Claude, Gemini, and Llama for different specialized tasks</p>
              </div>
              <div className="bg-white p-5 rounded-lg shadow-sm">
                <div className="text-blue-600 mb-3">
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
                  </svg>
                </div>
                <h3 className="font-medium text-lg mb-2">Vector Memory</h3>
                <p className="text-gray-600 text-sm">Semantic search and long-term contextual memory using vector embeddings for enhanced reasoning</p>
              </div>
              <div className="bg-white p-5 rounded-lg shadow-sm">
                <div className="text-amber-600 mb-3">
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <h3 className="font-medium text-lg mb-2">Fine-tuning Capabilities</h3>
                <p className="text-gray-600 text-sm">Create and fine-tune specialized models on your custom data for domain-specific knowledge</p>
              </div>
              <div className="bg-white p-5 rounded-lg shadow-sm">
                <div className="text-rose-600 mb-3">
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z" />
                  </svg>
                </div>
                <h3 className="font-medium text-lg mb-2">Visual Workflows</h3>
                <p className="text-gray-600 text-sm">Create complex multi-agent systems with our visual composer tool for orchestrated execution</p>
              </div>
              <div className="bg-white p-5 rounded-lg shadow-sm">
                <div className="text-cyan-600 mb-3">
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122" />
                  </svg>
                </div>
                <h3 className="font-medium text-lg mb-2">Agent Generation</h3>
                <p className="text-gray-600 text-sm">Self-replicating agents that can create new specialized agents based on your requirements</p>
              </div>
            </div>
          </div>
        </section>
        
        <section className="mt-12 mb-8">
          <div className="flex justify-center">
            <Link
              href="/agents"
              passHref
              legacyBehavior
            >
              <div className="inline-flex items-center px-6 py-3 text-base font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 cursor-pointer">
                Get Started with Sankalpa
                <svg className="ml-2 -mr-0.5 h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L12.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
              </div>
            </Link>
          </div>
        </section>
      </div>
    </div>
  );
};

export default Home;
