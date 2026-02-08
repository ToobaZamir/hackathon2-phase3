import { getToken } from '@/lib/auth';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000';

interface Todo {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

class ApiService {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  // Get all todos for the authenticated user
  async getTodos(): Promise<Todo[]> {
    try {
      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
      };

      // Add authentication token if available
      const token = getToken();
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(`${this.baseUrl}/api/todos/tasks`, {
        method: 'GET',
        headers,
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch todos: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching todos:', error);
      throw error;
    }
  }

  // Create a new todo
  async createTodo(todoData: Omit<Todo, 'id' | 'created_at' | 'updated_at'>): Promise<Todo> {
    try {
      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
      };

      // Add authentication token if available
      const token = getToken();
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(`${this.baseUrl}/api/todos/tasks`, {
        method: 'POST',
        headers,
        body: JSON.stringify(todoData),
      });

      if (!response.ok) {
        throw new Error(`Failed to create todo: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error creating todo:', error);
      throw error;
    }
  }

  // Update an existing todo
  async updateTodo(id: number, todoData: Partial<Todo>): Promise<Todo> {
    try {
      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
      };

      // Add authentication token if available
      const token = getToken();
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(`${this.baseUrl}/api/todos/tasks/${id}`, {
        method: 'PUT',
        headers,
        body: JSON.stringify(todoData),
      });

      if (!response.ok) {
        throw new Error(`Failed to update todo: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error updating todo:', error);
      throw error;
    }
  }

  // Delete a todo
  async deleteTodo(id: number): Promise<void> {
    try {
      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
      };

      // Add authentication token if available
      const token = getToken();
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(`${this.baseUrl}/api/todos/tasks/${id}`, {
        method: 'DELETE',
        headers,
      });

      if (!response.ok) {
        throw new Error(`Failed to delete todo: ${response.status}`);
      }
    } catch (error) {
      console.error('Error deleting todo:', error);
      throw error;
    }
  }

  // Toggle todo completion status
  async toggleTodoCompletion(id: number): Promise<Todo> {
    try {
      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
      };

      // Add authentication token if available
      const token = getToken();
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(`${this.baseUrl}/api/todos/tasks/${id}/complete`, {
        method: 'PATCH',
        headers,
      });

      if (!response.ok) {
        throw new Error(`Failed to toggle todo completion: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error toggling todo completion:', error);
      throw error;
    }
  }
}

export const apiService = new ApiService();
export type { Todo };