'use client';

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { authService } from '@/services/auth';
import { getToken, setToken, removeToken } from '@/lib/auth';

interface User {
  id: number;
  username: string;
  email: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  // Check authentication status on initial load
  useEffect(() => {
    const token = getToken();
    if (token) {
      // In a real app, you might want to validate the token or fetch user data
      // For now, we'll just store a placeholder indicating the user is authenticated
      // In a real scenario, you'd make an API call to validate the token and get user details
      const storedUserData = localStorage.getItem('currentUser');
      if (storedUserData) {
        try {
          setUser(JSON.parse(storedUserData));
        } catch (e) {
          console.error('Error parsing stored user data:', e);
        }
      }
    }
    setLoading(false);
  }, []);

  const login = async (username: string, password: string) => {
    setLoading(true);
    try {
      const response = await authService.login({ username, password });
      if (response.success && response.data.token) {
        const { token, user } = response.data;

        setToken(token.access_token);
        setUser(user);
        localStorage.setItem('currentUser', JSON.stringify(user));
      } else {
        throw new Error(response.message || 'Login failed');
      }
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const register = async (username: string, email: string, password: string) => {
    setLoading(true);
    try {
      const response = await authService.register({ username, email, password });
      if (response.success && response.data.token) {
        const { token, user } = response.data;

        setToken(token.access_token);
        setUser(user);
        localStorage.setItem('currentUser', JSON.stringify(user));
      } else {
        throw new Error(response.message || 'Registration failed');
      }
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    setLoading(true);
    try {
      await authService.logout();
    } catch (error) {
      console.error('Logout API error:', error);
      // Even if API call fails, we should clear local state
    } finally {
      // Clear local storage and state regardless of API call outcome
      removeToken();
      localStorage.removeItem('currentUser');
      setUser(null);
      setLoading(false);
    }
  };

  const value: AuthContextType = {
    user,
    loading,
    login,
    register,
    logout,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};