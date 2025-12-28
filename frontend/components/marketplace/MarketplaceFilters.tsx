import React, { useState } from 'react';

interface Category {
  id: string;
  name: string;
  description?: string;
  icon?: string;
  display_order: number;
  parent_id?: string;
  subcategories?: Category[];
}

interface FiltersState {
  type?: string;
  category_id?: string;
  search?: string;
  sort_by: string;
  sort_order: string;
}

interface MarketplaceFiltersProps {
  filters: FiltersState;
  categories: Category[];
  onFilterChange: (newFilters: Partial<FiltersState>) => void;
}

const MarketplaceFilters: React.FC<MarketplaceFiltersProps> = ({
  filters,
  categories,
  onFilterChange,
}) => {
  const [expanded, setExpanded] = useState<string[]>(['type', 'categories']);
  
  // Toggle an accordion section
  const toggleSection = (section: string) => {
    setExpanded(prev => 
      prev.includes(section) 
        ? prev.filter(s => s !== section) 
        : [...prev, section]
    );
  };
  
  // Recursive component for categories and subcategories
  const renderCategories = (cats: Category[], level = 0) => {
    return (
      <ul className={`space-y-1 ${level > 0 ? 'ml-4' : ''}`}>
        {cats.map((category) => (
          <li key={category.id}>
            <div className="flex items-center">
              <input
                id={`category-${category.id}`}
                name="category"
                type="radio"
                checked={filters.category_id === category.id}
                onChange={() => onFilterChange({ category_id: category.id })}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label
                htmlFor={`category-${category.id}`}
                className="ml-3 block text-sm text-gray-700"
              >
                {category.name}
              </label>
            </div>
            
            {category.subcategories && category.subcategories.length > 0 && 
              renderCategories(category.subcategories, level + 1)}
          </li>
        ))}
      </ul>
    );
  };
  
  // Clear all filters
  const clearFilters = () => {
    onFilterChange({
      type: undefined,
      category_id: undefined,
      search: '',
    });
  };
  
  return (
    <div className="bg-white shadow rounded-lg overflow-hidden">
      <div className="p-4 border-b border-gray-200 flex justify-between items-center">
        <h3 className="text-lg font-medium text-gray-900">Filters</h3>
        <button
          onClick={clearFilters}
          className="text-sm text-blue-600 hover:text-blue-500"
        >
          Clear all
        </button>
      </div>
      
      <div className="p-4 border-b border-gray-200">
        <button
          className="flex w-full items-center justify-between text-left"
          onClick={() => toggleSection('type')}
        >
          <span className="text-sm font-medium text-gray-900">Item Type</span>
          <svg
            className={`${
              expanded.includes('type') ? 'transform rotate-180' : ''
            } w-5 h-5 text-gray-500`}
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fillRule="evenodd"
              d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
              clipRule="evenodd"
            />
          </svg>
        </button>
        
        {expanded.includes('type') && (
          <div className="mt-4 space-y-4">
            <div className="flex items-center">
              <input
                id="type-chain"
                name="type"
                type="radio"
                checked={filters.type === 'chain'}
                onChange={() => onFilterChange({ type: 'chain' })}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label
                htmlFor="type-chain"
                className="ml-3 block text-sm text-gray-700"
              >
                Chains
              </label>
            </div>
            
            <div className="flex items-center">
              <input
                id="type-agent"
                name="type"
                type="radio"
                checked={filters.type === 'agent'}
                onChange={() => onFilterChange({ type: 'agent' })}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label
                htmlFor="type-agent"
                className="ml-3 block text-sm text-gray-700"
              >
                Agents
              </label>
            </div>
            
            <div className="flex items-center">
              <input
                id="type-plugin"
                name="type"
                type="radio"
                checked={filters.type === 'plugin'}
                onChange={() => onFilterChange({ type: 'plugin' })}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label
                htmlFor="type-plugin"
                className="ml-3 block text-sm text-gray-700"
              >
                Plugins
              </label>
            </div>
            
            <div className="flex items-center">
              <input
                id="type-all"
                name="type"
                type="radio"
                checked={!filters.type}
                onChange={() => onFilterChange({ type: undefined })}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label
                htmlFor="type-all"
                className="ml-3 block text-sm text-gray-700"
              >
                All Types
              </label>
            </div>
          </div>
        )}
      </div>
      
      <div className="p-4">
        <button
          className="flex w-full items-center justify-between text-left"
          onClick={() => toggleSection('categories')}
        >
          <span className="text-sm font-medium text-gray-900">Categories</span>
          <svg
            className={`${
              expanded.includes('categories') ? 'transform rotate-180' : ''
            } w-5 h-5 text-gray-500`}
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fillRule="evenodd"
              d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
              clipRule="evenodd"
            />
          </svg>
        </button>
        
        {expanded.includes('categories') && (
          <div className="mt-4">
            <div className="flex items-center mb-4">
              <input
                id="category-all"
                name="category"
                type="radio"
                checked={!filters.category_id}
                onChange={() => onFilterChange({ category_id: undefined })}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label
                htmlFor="category-all"
                className="ml-3 block text-sm font-medium text-gray-700"
              >
                All Categories
              </label>
            </div>
            
            {categories.length === 0 ? (
              <p className="text-sm text-gray-500">Loading categories...</p>
            ) : (
              renderCategories(categories)
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default MarketplaceFilters;