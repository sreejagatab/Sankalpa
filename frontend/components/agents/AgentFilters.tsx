import React, { useState } from 'react';

export interface AgentFilters {
  categories: string[];
  searchQuery: string;
  selfImproving: boolean;
  memoryEnabled: boolean;
}

interface AgentFiltersProps {
  onFilterChange: (filters: AgentFilters) => void;
  availableCategories: string[];
}

const AgentFilters: React.FC<AgentFiltersProps> = ({ onFilterChange, availableCategories }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategories, setSelectedCategories] = useState<string[]>([]);
  const [selfImproving, setSelfImproving] = useState(false);
  const [memoryEnabled, setMemoryEnabled] = useState(false);

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const query = e.target.value;
    setSearchQuery(query);
    updateFilters(query, selectedCategories, selfImproving, memoryEnabled);
  };

  const handleCategoryChange = (category: string) => {
    const updatedCategories = selectedCategories.includes(category)
      ? selectedCategories.filter(c => c !== category)
      : [...selectedCategories, category];
    
    setSelectedCategories(updatedCategories);
    updateFilters(searchQuery, updatedCategories, selfImproving, memoryEnabled);
  };

  const handleSelfImprovingChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const checked = e.target.checked;
    setSelfImproving(checked);
    updateFilters(searchQuery, selectedCategories, checked, memoryEnabled);
  };

  const handleMemoryEnabledChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const checked = e.target.checked;
    setMemoryEnabled(checked);
    updateFilters(searchQuery, selectedCategories, selfImproving, checked);
  };

  const updateFilters = (search: string, categories: string[], selfImprove: boolean, memory: boolean) => {
    onFilterChange({
      searchQuery: search,
      categories: categories,
      selfImproving: selfImprove,
      memoryEnabled: memory
    });
  };

  const clearFilters = () => {
    setSearchQuery('');
    setSelectedCategories([]);
    setSelfImproving(false);
    setMemoryEnabled(false);
    
    onFilterChange({
      searchQuery: '',
      categories: [],
      selfImproving: false,
      memoryEnabled: false
    });
  };

  return (
    <div className="bg-white shadow p-4 rounded-lg mb-6">
      <div className="space-y-4">
        <div>
          <label htmlFor="search" className="block text-sm font-medium text-gray-700">Search Agents</label>
          <div className="mt-1 relative rounded-md shadow-sm">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg className="h-5 w-5 text-gray-400" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd" />
              </svg>
            </div>
            <input
              type="text"
              name="search"
              id="search"
              className="focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 sm:text-sm border-gray-300 rounded-md"
              placeholder="Search by name, description or capabilities..."
              value={searchQuery}
              onChange={handleSearchChange}
            />
          </div>
        </div>

        <div>
          <h3 className="text-sm font-medium text-gray-700 mb-2">Special Capabilities</h3>
          <div className="flex flex-wrap gap-4">
            <div className="flex items-center">
              <input
                id="self-improving"
                type="checkbox"
                className="h-4 w-4 text-emerald-600 focus:ring-emerald-500 border-gray-300 rounded"
                checked={selfImproving}
                onChange={handleSelfImprovingChange}
              />
              <label htmlFor="self-improving" className="ml-2 flex items-center text-sm text-gray-700">
                <div className="bg-emerald-500 rounded-full w-2 h-2 mr-1.5"></div>
                Self-improving
              </label>
            </div>
            
            <div className="flex items-center">
              <input
                id="memory-enabled"
                type="checkbox"
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                checked={memoryEnabled}
                onChange={handleMemoryEnabledChange}
              />
              <label htmlFor="memory-enabled" className="ml-2 flex items-center text-sm text-gray-700">
                <svg className="h-3.5 w-3.5 text-blue-500 mr-1.5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                  <path d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM14 11a1 1 0 011 1v1h1a1 1 0 110 2h-1v1a1 1 0 11-2 0v-1h-1a1 1 0 110-2h1v-1a1 1 0 011-1z" />
                </svg>
                Memory enabled
              </label>
            </div>
          </div>
        </div>

        <div>
          <h3 className="text-sm font-medium text-gray-700">Categories</h3>
          <div className="mt-2 flex flex-wrap gap-2">
            {availableCategories.map(category => (
              <button
                key={category}
                onClick={() => handleCategoryChange(category)}
                className={`inline-flex items-center px-3 py-1.5 rounded-full text-xs font-medium ${
                  selectedCategories.includes(category)
                    ? 'bg-blue-100 text-blue-800 border-blue-200'
                    : 'bg-gray-100 text-gray-800 border-gray-200'
                } border hover:bg-opacity-80 transition-colors duration-200`}
              >
                {category}
              </button>
            ))}
          </div>
        </div>

        {(searchQuery || selectedCategories.length > 0 || selfImproving || memoryEnabled) && (
          <div className="flex justify-end">
            <button
              onClick={clearFilters}
              className="text-sm text-blue-600 hover:text-blue-800"
            >
              Clear filters
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default AgentFilters;