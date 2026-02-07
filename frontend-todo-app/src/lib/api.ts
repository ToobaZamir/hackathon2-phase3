import { getToken, removeToken } from './auth';

// Base API client with JWT token handling
class ApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8001';
  }

  // Generic request method with JWT token handling
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;

    // Get the token and add it to the headers
    const token = getToken();
    const headers = {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options.headers,
    };

    const config: RequestInit = {
      ...options,
      headers,
    };

    try {
      const response = await fetch(url, config);

      // Handle 401 Unauthorized - token might be expired or invalid
      if (response.status === 401) {
        removeToken(); // Remove invalid token
        window.location.href = '/auth/login'; // Redirect to login
        throw new Error('Unauthorized: Please log in again');
      }

      // Handle 403 Forbidden
      if (response.status === 403) {
        throw new Error('Forbidden: Access denied');
      }

      // Try to parse response as JSON
      let data;
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        data = await response.json();
      } else {
        // For non-JSON responses (like some DELETE operations), just return status
        if (response.ok) {
          return { success: true, message: 'Operation completed successfully' } as unknown as T;
        } else {
          data = await response.text();
          throw new Error(data || `HTTP error! status: ${response.status}`);
        }
      }

      if (!response.ok) {
        // Handle validation errors from FastAPI/Pydantic
        if (data && Array.isArray(data)) {
          // This is likely a validation error array from Pydantic
          const validationErrors = data.map(error => error.msg || error.detail || 'Validation error').join('; ');
          throw new Error(`Validation Error: ${validationErrors}`);
        } else if (data && typeof data === 'object') {
          // Handle standard error format - check for detail first (FastAPI format)
          if (data.detail) {
            throw new Error(`Backend Error: ${data.detail}`);
          } else if (data.message) {
            throw new Error(`Backend Error: ${data.message}`);
          } else {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
        } else {
          throw new Error(data || `HTTP error! status: ${response.status}`);
        }
      }

      return data;
    } catch (error) {
      console.error(`API request error for ${url}:`, error);
      throw error;
    }
  }

  // GET request
  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET' });
  }

  // POST request
  async post<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  // PUT request
  async put<T>(endpoint: string, data: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  // PATCH request
  async patch<T>(endpoint: string, data: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  }

  // DELETE request
  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'DELETE' });
  }
}

export const apiClient = new ApiClient();

// Chat API functions
export interface ChatRequest {
  message: string;
  conversation_id?: number | null;
}

export interface ChatResponse {
  message: string;
  conversation_id: number;
  tool_calls?: any[] | null;
}

/**
 * Send a chat message to the AI agent
 * @param userId - User ID from authentication
 * @param message - User's message
 * @param conversationId - Optional conversation ID to resume conversation
 * @param token - JWT token for authentication
 */
export async function sendChatMessage(
  userId: number,
  message: string,
  conversationId: number | null,
  token: string
): Promise<ChatResponse> {
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8001'}/api/${userId}/chat`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({
        message,
        conversation_id: conversationId,
      }),
    }
  );

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error('Authentication required. Please log in.');
    }
    if (response.status === 403) {
      throw new Error('Access denied. You can only access your own conversations.');
    }
    if (response.status === 404) {
      throw new Error('Conversation not found.');
    }
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to send message');
  }

  return await response.json();
}