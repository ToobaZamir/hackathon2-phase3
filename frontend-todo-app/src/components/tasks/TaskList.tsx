'use client';

import { useState, useEffect } from 'react';
import { taskService } from '@/services/tasks';
import TaskItem from '@/components/tasks/TaskItem';
import { Button } from '@/components/ui/button';
import { Task } from '@/types/tasks';

interface TaskListProps {
  refreshKey?: string; // Custom prop for triggering refresh
}

export default function TaskList({ refreshKey }: TaskListProps) {
  const [todos, setTodos] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchTodos();
  }, [refreshKey]); // Re-fetch when refreshKey changes

  const fetchTodos = async () => {
    try {
      setLoading(true);
      const fetchedTasks = await taskService.getTasks();
      setTodos(fetchedTasks);
    } catch (err) {
      setError('Failed to load todos. Please try again later.');
      console.error('Error fetching todos:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center py-4">Loading tasks...</div>;
  }

  if (error) {
    return <div className="text-center py-4 text-red-500">{error}</div>;
  }

  if (todos.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">You don't have any tasks yet.</p>
        <p className="text-gray-500">Create your first task using the form above!</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <ul className="divide-y divide-gray-200">
        {todos.map((todo) => (
          <TaskItem key={todo.id} todo={todo} onUpdate={setTodos} />
        ))}
      </ul>
    </div>
  );
}