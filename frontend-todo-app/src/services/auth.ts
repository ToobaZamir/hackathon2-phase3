import { apiClient } from '@/lib/api';

interface LoginCredentials {
  username: string;
  password: string;
}

interface RegisterData {
  username: string;
  email: string;
  password: string;
}

interface LoginResponse {
  success: boolean;
  data: {
    token: {
      access_token: string;
      token_type: string;
    };
    user: {
      id: number;
      username: string;
      email: string;
      is_active: boolean;
      created_at: string;
      updated_at: string;
    };
  };
  message: string;
}

interface RegisterResponse extends LoginResponse {}

export const authService = {
  login: async (credentials: LoginCredentials): Promise<LoginResponse> => {
    return apiClient.post<LoginResponse>('/api/auth/sign-in/email', {
      username: credentials.username,
      password: credentials.password
    });
  },

  register: async (userData: RegisterData): Promise<RegisterResponse> => {
    return apiClient.post<RegisterResponse>('/api/auth/sign-up/email', userData);
  },

  logout: async (): Promise<any> => {
    return apiClient.post('/api/auth/logout');
  },
};