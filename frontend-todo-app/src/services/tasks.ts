import { apiClient } from '@/lib/api';
import { Task, CreateTaskData, UpdateTaskData } from '@/types/tasks';

interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
}

interface TaskApiResponse {
  success: boolean;
  data: {
    task: Task;
  };
  message: string;
}

interface TaskListApiResponse {
  success: boolean;
  data: {
    tasks: Task[];
    total: number;
  };
  message?: string;
}

export const taskService = {
  // Get all tasks for the authenticated user
  getTasks: async (): Promise<Task[]> => {
    const response = await apiClient.get<{ tasks: Task[], total: number }>('/api/todos/tasks');
    return response.tasks;
  },

  // Get a specific task by ID
  getTaskById: async (taskId: number): Promise<Task> => {
    const response = await apiClient.get<TaskApiResponse>(`/api/todos/tasks/${taskId}`);
    return response.data.task;
  },

  // Create a new task
  createTask: async (taskData: CreateTaskData): Promise<Task> => {
    const response = await apiClient.post<TaskApiResponse>(`/api/todos/tasks`, taskData);
    return response.data.task;
  },

  // Update an existing task
  updateTask: async (taskId: number, taskData: UpdateTaskData): Promise<Task> => {
    const response = await apiClient.put<TaskApiResponse>(`/api/todos/tasks/${taskId}`, taskData);
    return response.data.task;
  },

  // Delete a task
  deleteTask: async (taskId: number): Promise<boolean> => {
    await apiClient.delete(`/api/todos/tasks/${taskId}`);
    return true;
  },

  // Toggle task completion status
  toggleTaskCompletion: async (taskId: number, completed: boolean): Promise<Task> => {
    const response = await apiClient.patch<TaskApiResponse>(`/api/todos/tasks/${taskId}/complete`, {
      completed,
    });
    return response.data.task;
  },
};