import { useState, useEffect, createContext, useContext, ReactNode } from 'react';
import { apiClient } from '../lib/api-client';

export interface User {
  id: string;
  username: string;
  email: string;
  role: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  error: string | null;
  login: (username: string, password: string) => Promise<boolean>;
  logout: () => void;
  isAuthenticated: boolean;
}

// Create context with default values
const AuthContext = createContext<AuthContextType>({
  user: null,
  token: null,
  loading: false,
  error: null,
  login: async () => false,
  logout: () => {},
  isAuthenticated: false,
});

// Mock user data for demo purposes
const mockUser: User = {
  id: '1',
  username: 'demo_user',
  email: 'demo@example.com',
  role: 'user',
};

export function useAuth() {
  // For the demo, we'll use a simulated auth state
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Check for existing auth on mount
  useEffect(() => {
    // In a real app, we would check localStorage, cookies, etc.
    // For demo purposes, we'll just simulate this
    const hasToken = localStorage.getItem('accessToken');
    
    if (hasToken) {
      // Simulate an authenticated user
      setUser(mockUser);
      setToken(hasToken);
    }
  }, []);

  // Login function
  const login = async (username: string, password: string): Promise<boolean> => {
    setLoading(true);
    setError(null);
    
    try {
      // In a real app, we would call an API
      // For demo purposes, we'll just simulate this
      if (username === 'demo' && password === 'password') {
        // Successful login
        const mockToken = 'mock_jwt_token_' + Date.now();
        localStorage.setItem('accessToken', mockToken);
        setUser(mockUser);
        setToken(mockToken);
        setLoading(false);
        return true;
      } else {
        // Failed login
        setError('Invalid username or password');
        setLoading(false);
        return false;
      }
    } catch (err) {
      setError('An error occurred during login');
      setLoading(false);
      return false;
    }
  };

  // Logout function
  const logout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('tokenExpiration');
    setUser(null);
    setToken(null);
  };
  
  return {
    user,
    token,
    loading,
    error,
    login,
    logout,
    isAuthenticated: !!user,
  };
}