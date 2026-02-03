import { useState, useEffect } from 'react';
import { authService } from '@/services/auth';
import { getToken, setToken, removeToken, isAuthenticated as checkAuth } from '@/lib/auth';

interface User {
  id: number;
  username: string;
  email: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  loading: boolean;
  error: string | null;
  isAuthenticated: boolean;
}

interface LoginCredentials {
  username: string;
  password: string;
}

interface RegisterData {
  username: string;
  email: string;
  password: string;
}

export const useAuth = () => {
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    token: null,
    loading: true,
    error: null,
    isAuthenticated: false,
  });

  // Check authentication status on initial load
  useEffect(() => {
    const token = getToken();
    if (token) {
      // In a real app, you might want to validate the token or fetch user data
      setAuthState(prev => ({
        ...prev,
        token,
        isAuthenticated: true,
        loading: false,
      }));
    } else {
      setAuthState(prev => ({
        ...prev,
        loading: false,
        isAuthenticated: false,
      }));
    }
  }, []);

  const login = async (credentials: LoginCredentials) => {
    setAuthState(prev => ({ ...prev, loading: true, error: null }));

    try {
      const response = await authService.login(credentials);

      if (response.success && response.data.token) {
        const { token, user } = response.data;

        setToken(token.access_token);

        setAuthState({
          user,
          token: token.access_token,
          loading: false,
          error: null,
          isAuthenticated: true,
        });
      } else {
        throw new Error(response.message || 'Login failed');
      }
    } catch (error: any) {
      const errorMessage = error.message || 'Login failed';
      setAuthState(prev => ({
        ...prev,
        loading: false,
        error: errorMessage,
      }));
      throw error;
    }
  };

  const register = async (userData: RegisterData) => {
    setAuthState(prev => ({ ...prev, loading: true, error: null }));

    try {
      const response = await authService.register(userData);

      if (response.success && response.data.token) {
        const { token, user } = response.data;

        setToken(token.access_token);

        setAuthState({
          user,
          token: token.access_token,
          loading: false,
          error: null,
          isAuthenticated: true,
        });
      } else {
        throw new Error(response.message || 'Registration failed');
      }
    } catch (error: any) {
      const errorMessage = error.message || 'Registration failed';
      setAuthState(prev => ({
        ...prev,
        loading: false,
        error: errorMessage,
      }));
      throw error;
    }
  };

  const logout = async () => {
    setAuthState(prev => ({ ...prev, loading: true }));

    try {
      // Call the logout API endpoint
      await authService.logout();
    } catch (error) {
      // Even if API call fails, we should clear local state
      console.error('Logout API error:', error);
    } finally {
      // Clear local storage and state regardless of API call outcome
      removeToken();
      setAuthState({
        user: null,
        token: null,
        loading: false,
        error: null,
        isAuthenticated: false,
      });
    }
  };

  return {
    ...authState,
    login,
    register,
    logout,
  };
};