'use client';

import { useState } from 'react';
import { taskService } from '@/services/tasks';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Button } from '@/components/ui/button';
import { CreateTaskData, Task } from '@/types/tasks';

// Define the validation schema using Zod
const taskCreateSchema = z.object({
  title: z
    .string()
    .min(1, 'Title is required')
    .max(255, 'Title must be at most 255 characters'),
  description: z
    .string()
    .max(1000, 'Description must be at most 1000 characters')
    .optional()
    .nullable(),
});

type TaskCreateFormInputs = z.infer<typeof taskCreateSchema>;

interface TaskCreateFormProps {
  onTaskCreated?: (newTodo: Task) => void;
}

export default function TaskCreateForm({ onTaskCreated }: TaskCreateFormProps) {
  const [loading, setLoading] = useState(false);
  const [showForm, setShowForm] = useState(true);

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<TaskCreateFormInputs>({
    resolver: zodResolver(taskCreateSchema),
  });

  const onSubmit = async (data: TaskCreateFormInputs) => {
    setLoading(true);
    try {
      const newTask = await taskService.createTask({
        title: data.title,
        description: data.description || undefined,
        completed: false,
      });

      if (onTaskCreated) {
        onTaskCreated(newTask);
      }

      reset(); // Clear the form after successful creation
    } catch (error) {
      console.error('Error creating task:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
            Title *
          </label>
          <input
            id="title"
            {...register('title')}
            className={`mt-1 block w-full p-2 border rounded-md ${
              errors.title ? 'border-red-300' : 'border-gray-300'
            } focus:outline-none focus:ring-2 focus:ring-blue-500`}
            placeholder="Task title"
          />
          {errors.title && (
            <p className="mt-1 text-sm text-red-600">{errors.title.message}</p>
          )}
        </div>

        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
            Description
          </label>
          <textarea
            id="description"
            {...register('description')}
            rows={3}
            className="mt-1 block w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Task description (optional)"
          />
          {errors.description && (
            <p className="mt-1 text-sm text-red-600">{errors.description.message}</p>
          )}
        </div>

        <div className="flex space-x-2">
          <Button
            type="submit"
            disabled={loading}
          >
            {loading ? 'Creating...' : 'Create Task'}
          </Button>
        </div>
      </form>
    </div>
  );
}