import { useState, useEffect } from 'react';
import { taskService } from '@/services/tasks';
import { Task, CreateTaskData, UpdateTaskData } from '@/types/tasks';

interface TasksState {
  tasks: Task[];
  loading: boolean;
  error: string | null;
}

export const useTasks = () => {
  const [state, setState] = useState<TasksState>({
    tasks: [],
    loading: false,
    error: null,
  });

  // Fetch all tasks
  const fetchTasks = async () => {
    setState(prev => ({ ...prev, loading: true, error: null }));
    try {
      const tasks = await taskService.getTasks();
      setState({
        tasks,
        loading: false,
        error: null,
      });
    } catch (error: any) {
      setState({
        tasks: [],
        loading: false,
        error: error.message || 'Failed to fetch tasks',
      });
    }
  };

  // Create a new task
  const createTask = async (taskData: CreateTaskData) => {
    setState(prev => ({ ...prev, loading: true, error: null }));
    try {
      const newTask = await taskService.createTask(taskData);
      setState(prev => ({
        ...prev,
        tasks: [...prev.tasks, newTask],
        loading: false,
      }));
    } catch (error: any) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: error.message || 'Failed to create task',
      }));
    }
  };

  // Update an existing task
  const updateTask = async (taskId: number, taskData: UpdateTaskData) => {
    setState(prev => ({ ...prev, loading: true, error: null }));
    try {
      const updatedTask = await taskService.updateTask(taskId, taskData);
      setState(prev => ({
        ...prev,
        tasks: prev.tasks.map(task =>
          task.id === taskId ? updatedTask : task
        ),
        loading: false,
      }));
    } catch (error: any) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: error.message || 'Failed to update task',
      }));
    }
  };

  // Delete a task
  const deleteTask = async (taskId: number) => {
    setState(prev => ({ ...prev, loading: true, error: null }));
    try {
      await taskService.deleteTask(taskId);
      setState(prev => ({
        ...prev,
        tasks: prev.tasks.filter(task => task.id !== taskId),
        loading: false,
      }));
    } catch (error: any) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: error.message || 'Failed to delete task',
      }));
    }
  };

  // Toggle task completion status
  const toggleTaskCompletion = async (taskId: number, completed: boolean) => {
    setState(prev => ({ ...prev, loading: true, error: null }));
    try {
      const updatedTask = await taskService.toggleTaskCompletion(taskId, completed);
      setState(prev => ({
        ...prev,
        tasks: prev.tasks.map(task =>
          task.id === taskId ? updatedTask : task
        ),
        loading: false,
      }));
    } catch (error: any) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: error.message || 'Failed to update task completion',
      }));
    }
  };

  return {
    ...state,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion,
  };
};