import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import { NextPage } from 'next';
import { apiClient } from '../../lib/api-client';
import Layout from '../../components/layout/Layout';
import MarketplaceFilters from '../../components/marketplace/MarketplaceFilters';
import MarketplaceItemCard from '../../components/marketplace/MarketplaceItemCard';

export interface MarketplaceItem {
  id: string;
  name: string;
  description: string;
  type: 'agent' | 'workflow' | 'model' | 'template';
  category: string;
  author: string;
  rating: number;
  download_count: number;
  price: number | null;
  thumbnail?: string;
  tags: string[];
  created_at: string;
  is_verified: boolean;
}

interface MarketplaceFiltersState {
  type: string[];
  category: string[];
  price: 'all' | 'free' | 'paid';
  search: string;
  sort: 'popular' | 'recent' | 'top_rated';
}

const MarketplacePage: NextPage = () => {
  const [items, setItems] = useState<MarketplaceItem[]>([]);
  const [filteredItems, setFilteredItems] = useState<MarketplaceItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  const [filters, setFilters] = useState<MarketplaceFiltersState>({
    type: [],
    category: [],
    price: 'all',
    search: '',
    sort: 'popular'
  });
  
  const [categories, setCategories] = useState<string[]>([]);
  const [types, setTypes] = useState<string[]>(['agent', 'workflow', 'model', 'template']);

  useEffect(() => {
    fetchMarketplaceItems();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [filters, items]);

  const fetchMarketplaceItems = async () => {
    setLoading(true);
    setError(null);

    try {
      // For development, using mock data
      setTimeout(() => {
        const mockItems: MarketplaceItem[] = [
          {
            id: 'marketplace-item-1',
            name: 'Full-Stack Web App Generator',
            description: 'AI agent that creates complete web applications with React frontend and Node.js backend',
            type: 'agent',
            category: 'builder',
            author: 'SankalpaDev',
            rating: 4.8,
            download_count: 2451,
            price: null,
            tags: ['web', 'react', 'node', 'full-stack'],
            created_at: '2023-05-15T08:30:00Z',
            is_verified: true
          },
          {
            id: 'marketplace-item-2',
            name: 'E-commerce Project Template',
            description: 'Complete project template for building e-commerce applications with user auth, product catalog, cart, and checkout',
            type: 'template',
            category: 'e-commerce',
            author: 'TechBuilders',
            rating: 4.5,
            download_count: 1823,
            price: 29.99,
            tags: ['template', 'e-commerce', 'web'],
            created_at: '2023-06-02T11:45:00Z',
            is_verified: true
          },
          {
            id: 'marketplace-item-3',
            name: 'Database Schema Designer',
            description: 'Creates optimal database schemas based on your project requirements. Supports SQL and NoSQL databases',
            type: 'agent',
            category: 'database',
            author: 'DataMaster',
            rating: 4.7,
            download_count: 1205,
            price: null,
            tags: ['database', 'schema', 'SQL', 'NoSQL'],
            created_at: '2023-04-21T15:20:00Z',
            is_verified: false
          },
          {
            id: 'marketplace-item-4',
            name: 'Project Planning Workflow',
            description: 'Complete workflow for planning software projects from requirements gathering to task breakdown',
            type: 'workflow',
            category: 'planning',
            author: 'AgileDevs',
            rating: 4.6,
            download_count: 956,
            price: 19.99,
            tags: ['planning', 'agile', 'project-management'],
            created_at: '2023-07-10T09:15:00Z',
            is_verified: true
          },
          {
            id: 'marketplace-item-5',
            name: 'React UI Component Generator',
            description: 'Generates high-quality React components based on your design specifications',
            type: 'agent',
            category: 'frontend',
            author: 'UIWizard',
            rating: 4.9,
            download_count: 3012,
            price: 9.99,
            tags: ['react', 'ui', 'components', 'frontend'],
            created_at: '2023-03-18T14:30:00Z',
            is_verified: true
          },
          {
            id: 'marketplace-item-6',
            name: 'API Builder Workflow',
            description: 'End-to-end workflow for designing, building, and testing RESTful APIs',
            type: 'workflow',
            category: 'backend',
            author: 'APIFactory',
            rating: 4.4,
            download_count: 785,
            price: null,
            tags: ['api', 'rest', 'backend'],
            created_at: '2023-05-29T10:40:00Z',
            is_verified: false
          },
          {
            id: 'marketplace-item-7',
            name: 'Documentation Generator',
            description: 'Creates comprehensive documentation for your codebase, including API references and usage guides',
            type: 'agent',
            category: 'documentation',
            author: 'DocsExpert',
            rating: 4.2,
            download_count: 643,
            price: null,
            tags: ['documentation', 'docs', 'readme'],
            created_at: '2023-06-14T16:50:00Z',
            is_verified: false
          },
          {
            id: 'marketplace-item-8',
            name: 'Fine-tuned Code Completion Model',
            description: 'Enhanced code completion model fine-tuned on high-quality open source repositories',
            type: 'model',
            category: 'development',
            author: 'CodeGenius',
            rating: 4.7,
            download_count: 1678,
            price: 49.99,
            tags: ['model', 'code-completion', 'development'],
            created_at: '2023-04-05T08:25:00Z',
            is_verified: true
          }
        ];
        
        setItems(mockItems);
        setFilteredItems(mockItems);
        
        // Extract unique categories
        const uniqueCategories = Array.from(
          new Set(mockItems.map(item => item.category))
        );
        setCategories(uniqueCategories);
        
        setLoading(false);
      }, 1000);
    } catch (err) {
      console.error('Error fetching marketplace items:', err);
      setError('Failed to load marketplace items');
      setLoading(false);
    }
  };

  const applyFilters = () => {
    let result = [...items];
    
    // Filter by type
    if (filters.type.length > 0) {
      result = result.filter(item => 
        filters.type.includes(item.type)
      );
    }
    
    // Filter by category
    if (filters.category.length > 0) {
      result = result.filter(item => 
        filters.category.includes(item.category)
      );
    }
    
    // Filter by price
    if (filters.price === 'free') {
      result = result.filter(item => item.price === null);
    } else if (filters.price === 'paid') {
      result = result.filter(item => item.price !== null);
    }
    
    // Filter by search query
    if (filters.search) {
      const query = filters.search.toLowerCase();
      result = result.filter(item => 
        item.name.toLowerCase().includes(query) ||
        item.description.toLowerCase().includes(query) ||
        item.tags.some(tag => tag.toLowerCase().includes(query))
      );
    }
    
    // Sort items
    if (filters.sort === 'popular') {
      result.sort((a, b) => b.download_count - a.download_count);
    } else if (filters.sort === 'recent') {
      result.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
    } else if (filters.sort === 'top_rated') {
      result.sort((a, b) => b.rating - a.rating);
    }
    
    setFilteredItems(result);
  };

  const handleFilterChange = (newFilters: Partial<MarketplaceFiltersState>) => {
    setFilters(prev => ({ ...prev, ...newFilters }));
  };

  const handleInstall = async (item: MarketplaceItem) => {
    try {
      // This would be an actual API call in production
      console.log(`Installing ${item.name}...`);
      
      // Simulate installation success
      setTimeout(() => {
        // Show success message or redirect to installed item
        console.log(`Successfully installed ${item.name}`);
      }, 1500);
    } catch (err) {
      console.error('Error installing item:', err);
    }
  };

  return (
    <Layout>
      <Head>
        <title>Marketplace | Sankalpa</title>
      </Head>
      
      <div className="py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center mb-6">
            <div>
              <h1 className="text-2xl font-semibold text-gray-900">Sankalpa Marketplace</h1>
              <p className="text-gray-600">
                Discover and download agents, workflows, models, and templates
              </p>
            </div>
            
            <button
              onClick={fetchMarketplaceItems}
              className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              <svg
                className={`mr-2 h-4 w-4 ${loading ? 'animate-spin' : ''}`}
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                />
              </svg>
              Refresh
            </button>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
            {/* Filters sidebar */}
            <div className="lg:col-span-1">
              <MarketplaceFilters
                filters={filters}
                onFilterChange={handleFilterChange}
                availableCategories={categories}
                availableTypes={types}
              />
            </div>
            
            {/* Marketplace items grid */}
            <div className="lg:col-span-3">
              {error && (
                <div className="mb-6 bg-red-50 border-l-4 border-red-400 p-4">
                  <div className="flex">
                    <div className="flex-shrink-0">
                      <svg
                        className="h-5 w-5 text-red-400"
                        viewBox="0 0 20 20"
                        fill="currentColor"
                      >
                        <path
                          fillRule="evenodd"
                          d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                          clipRule="evenodd"
                        />
                      </svg>
                    </div>
                    <div className="ml-3">
                      <p className="text-sm text-red-700">{error}</p>
                    </div>
                  </div>
                </div>
              )}
              
              {loading ? (
                <div className="flex justify-center items-center h-64">
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
                </div>
              ) : filteredItems.length === 0 ? (
                <div className="bg-white p-8 rounded-lg shadow text-center">
                  <svg
                    className="mx-auto h-12 w-12 text-gray-400"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                  <h3 className="mt-2 text-lg font-medium text-gray-900">No items found</h3>
                  <p className="mt-1 text-gray-500">
                    Try adjusting your filters or search terms.
                  </p>
                </div>
              ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                  {filteredItems.map(item => (
                    <MarketplaceItemCard
                      key={item.id}
                      item={item}
                      onInstall={() => handleInstall(item)}
                    />
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default MarketplacePage;