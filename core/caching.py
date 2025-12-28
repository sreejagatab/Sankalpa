
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import time
import json
import hashlib
import functools
from typing import Any, Dict, Optional, Callable, TypeVar, cast

from core import get_logger, config

logger = get_logger("cache")

# Type variables for function signatures
T = TypeVar('T')
F = TypeVar('F', bound=Callable[..., Any])

class CacheBackend:
    """Base class for cache backends"""
    
    def get(self, key: str) -> Optional[Any]:
        """Get a value from the cache"""
        raise NotImplementedError("Cache backend must implement get")
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set a value in the cache"""
        raise NotImplementedError("Cache backend must implement set")
    
    def delete(self, key: str) -> None:
        """Delete a value from the cache"""
        raise NotImplementedError("Cache backend must implement delete")
    
    def exists(self, key: str) -> bool:
        """Check if a key exists in the cache"""
        raise NotImplementedError("Cache backend must implement exists")
    
    def clear(self) -> None:
        """Clear all values from the cache"""
        raise NotImplementedError("Cache backend must implement clear")

class InMemoryCache(CacheBackend):
    """Simple in-memory cache implementation"""
    
    def __init__(self):
        self.cache: Dict[str, Dict[str, Any]] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get a value from the cache"""
        entry = self.cache.get(key)
        if not entry:
            return None
            
        # Check if the entry has expired
        if entry["expires"] > 0 and entry["expires"] < time.time():
            self.delete(key)
            return None
            
        return entry["value"]
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set a value in the cache"""
        expires = 0
        if ttl:
            expires = time.time() + ttl
            
        self.cache[key] = {
            "value": value,
            "expires": expires
        }
    
    def delete(self, key: str) -> None:
        """Delete a value from the cache"""
        if key in self.cache:
            del self.cache[key]
    
    def exists(self, key: str) -> bool:
        """Check if a key exists in the cache"""
        if key not in self.cache:
            return False
            
        entry = self.cache[key]
        if entry["expires"] > 0 and entry["expires"] < time.time():
            self.delete(key)
            return False
            
        return True
    
    def clear(self) -> None:
        """Clear all values from the cache"""
        self.cache.clear()

class RedisCache(CacheBackend):
    """Redis-based cache implementation"""
    
    def __init__(self, redis_url: Optional[str] = None):
        """Initialize Redis cache
        
        Args:
            redis_url: Redis connection string (redis://host:port/db)
        """
        try:
            import redis
            from redis.exceptions import RedisError
            
            self.redis_url = redis_url or config.get("memory.redis_url")
            self.redis = redis.from_url(self.redis_url)
            self.available = True
            
            # Test connection
            self.redis.ping()
            
            logger.info(f"Redis cache initialized: {self.redis_url}")
            
        except (ImportError, RedisError) as e:
            logger.warning(f"Redis cache initialization failed: {str(e)}")
            self.available = False
    
    def get(self, key: str) -> Optional[Any]:
        """Get a value from the cache"""
        if not self.available:
            return None
            
        try:
            value = self.redis.get(key)
            if value is None:
                return None
                
            return json.loads(value)
            
        except Exception as e:
            logger.error(f"Redis get failed: {str(e)}")
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set a value in the cache"""
        if not self.available:
            return
            
        try:
            serialized = json.dumps(value)
            if ttl:
                self.redis.setex(key, ttl, serialized)
            else:
                self.redis.set(key, serialized)
                
        except Exception as e:
            logger.error(f"Redis set failed: {str(e)}")
    
    def delete(self, key: str) -> None:
        """Delete a value from the cache"""
        if not self.available:
            return
            
        try:
            self.redis.delete(key)
        except Exception as e:
            logger.error(f"Redis delete failed: {str(e)}")
    
    def exists(self, key: str) -> bool:
        """Check if a key exists in the cache"""
        if not self.available:
            return False
            
        try:
            return bool(self.redis.exists(key))
        except Exception as e:
            logger.error(f"Redis exists failed: {str(e)}")
            return False
    
    def clear(self) -> None:
        """Clear all values from the cache"""
        if not self.available:
            return
            
        try:
            self.redis.flushdb()
        except Exception as e:
            logger.error(f"Redis clear failed: {str(e)}")

class Cache:
    """Main cache interface with automatic backend selection"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Cache, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize the cache system"""
        # Determine which backend to use
        backend_type = config.get("cache.backend", "memory")
        
        if backend_type == "redis":
            self.backend = RedisCache()
            if not self.backend.available:
                logger.warning("Redis cache not available, falling back to in-memory cache")
                self.backend = InMemoryCache()
                
        else:
            self.backend = InMemoryCache()
            
        # Set default TTL
        self.default_ttl = config.get("cache.default_ttl", 3600)  # 1 hour
        
        logger.info(f"Cache initialized with {self.backend.__class__.__name__}")
    
    def generate_key(self, namespace: str, data: Any) -> str:
        """Generate a cache key from data
        
        Args:
            namespace: Namespace for the key
            data: Data to hash for the key
            
        Returns:
            Cache key
        """
        # Convert data to a stable string representation
        if isinstance(data, (dict, list, tuple)):
            data_str = json.dumps(data, sort_keys=True)
        else:
            data_str = str(data)
            
        # Hash the data
        hash_key = hashlib.md5(data_str.encode()).hexdigest()
        
        # Combine namespace and hash
        return f"sankalpa:{namespace}:{hash_key}"
    
    def get(self, key: str) -> Optional[Any]:
        """Get a value from the cache"""
        return self.backend.get(key)
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set a value in the cache"""
        self.backend.set(key, value, ttl or self.default_ttl)
    
    def delete(self, key: str) -> None:
        """Delete a value from the cache"""
        self.backend.delete(key)
    
    def exists(self, key: str) -> bool:
        """Check if a key exists in the cache"""
        return self.backend.exists(key)
    
    def clear(self) -> None:
        """Clear all values from the cache"""
        self.backend.clear()

# Function decorator for caching
def cached(namespace: str, ttl: Optional[int] = None):
    """Decorator for caching function results
    
    Args:
        namespace: Namespace for the cache key
        ttl: Time-to-live in seconds
        
    Returns:
        Decorated function
    """
    cache_instance = Cache()
    
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Generate a cache key from the function arguments
            key_data = {
                "func": func.__name__,
                "args": args,
                "kwargs": kwargs
            }
            cache_key = cache_instance.generate_key(namespace, key_data)
            
            # Check if result is cached
            cached_result = cache_instance.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit: {cache_key}")
                return cached_result
                
            # Get the result from the function
            logger.debug(f"Cache miss: {cache_key}")
            result = func(*args, **kwargs)
            
            # Cache the result
            cache_instance.set(cache_key, result, ttl)
            
            return result
            
        return cast(F, wrapper)
        
    return decorator

# Global cache instance
cache = Cache()