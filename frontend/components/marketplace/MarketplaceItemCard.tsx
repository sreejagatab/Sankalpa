import React from 'react';
import Link from 'next/link';
import Image from 'next/image';

// Type definitions
interface MarketplaceItem {
  id: string;
  name: string;
  description: string;
  type: 'chain' | 'agent' | 'plugin';
  tags?: string[];
  preview_image?: string;
  author_id: string;
  rating: number;
  rating_count: number;
  download_count: number;
  is_verified: boolean;
  created_at: string;
  updated_at: string;
}

interface MarketplaceItemCardProps {
  item: MarketplaceItem;
}

// Default images for different item types
const DEFAULT_IMAGES = {
  chain: '/images/marketplace/default-chain.svg',
  agent: '/images/marketplace/default-agent.svg',
  plugin: '/images/marketplace/default-plugin.svg',
};

// Component for displaying a star rating
const StarRating: React.FC<{ rating: number; count: number }> = ({ rating, count }) => {
  return (
    <div className="flex items-center">
      <div className="flex items-center">
        {[1, 2, 3, 4, 5].map((star) => (
          <svg
            key={star}
            className={`w-4 h-4 ${
              star <= Math.round(rating) ? 'text-yellow-400' : 'text-gray-300'
            }`}
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
          </svg>
        ))}
      </div>
      <p className="ml-2 text-xs text-gray-500">{count} reviews</p>
    </div>
  );
};

// Type badge component
const TypeBadge: React.FC<{ type: 'chain' | 'agent' | 'plugin' }> = ({ type }) => {
  const colors = {
    chain: 'bg-blue-100 text-blue-800',
    agent: 'bg-green-100 text-green-800',
    plugin: 'bg-purple-100 text-purple-800',
  };
  
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${colors[type]}`}>
      {type.charAt(0).toUpperCase() + type.slice(1)}
    </span>
  );
};

const MarketplaceItemCard: React.FC<MarketplaceItemCardProps> = ({ item }) => {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };
  
  return (
    <Link href={`/marketplace/items/${item.id}`} className="block">
      <div className="bg-white overflow-hidden shadow rounded-lg hover:shadow-md transition-shadow duration-200">
        {/* Preview image */}
        <div className="relative h-48 bg-gray-200">
          <Image
            src={item.preview_image || DEFAULT_IMAGES[item.type]}
            alt={item.name}
            fill
            className="object-cover"
          />
          {/* Verification badge if verified */}
          {item.is_verified && (
            <div className="absolute top-2 right-2 bg-blue-600 text-white rounded-full p-1" title="Verified">
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                  clipRule="evenodd"
                />
              </svg>
            </div>
          )}
        </div>
        
        {/* Content */}
        <div className="p-4">
          <div className="flex justify-between items-start">
            <TypeBadge type={item.type} />
            <div className="text-xs text-gray-500">{formatDate(item.created_at)}</div>
          </div>
          
          <h3 className="mt-2 text-lg font-medium text-gray-900">{item.name}</h3>
          
          <p className="mt-1 text-sm text-gray-500 line-clamp-2">{item.description}</p>
          
          {/* Tags */}
          {item.tags && item.tags.length > 0 && (
            <div className="mt-2 flex flex-wrap gap-1">
              {item.tags.slice(0, 3).map((tag) => (
                <span
                  key={tag}
                  className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800"
                >
                  {tag}
                </span>
              ))}
              {item.tags.length > 3 && (
                <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800">
                  +{item.tags.length - 3}
                </span>
              )}
            </div>
          )}
          
          <div className="mt-3 flex justify-between items-center">
            <StarRating rating={item.rating} count={item.rating_count} />
            
            <div className="flex items-center text-sm text-gray-500">
              <svg
                className="mr-1 h-4 w-4 text-gray-400"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fillRule="evenodd"
                  d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z"
                  clipRule="evenodd"
                />
              </svg>
              {item.download_count}
            </div>
          </div>
        </div>
      </div>
    </Link>
  );
};

export default MarketplaceItemCard;