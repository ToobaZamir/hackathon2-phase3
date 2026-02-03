import { useState } from 'react';
import { Task, UpdateTaskData } from '@/types/tasks';
import { useTasks } from '@/hooks/useTasks';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

// Define the validation schema using Zod
const taskUpdateSchema = z.object({
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

type TaskUpdateFormInputs = z.infer<typeof taskUpdateSchema>;

interface TaskEditFormProps {
  task: Task;
  onCancel: () => void;
  onSuccess: () => void;
}

const TaskEditForm: React.FC<TaskEditFormProps> = ({ task, onCancel, onSuccess }) => {
  const { updateTask, loading } = useTasks();

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<TaskUpdateFormInputs>({
    resolver: zodResolver(taskUpdateSchema),
    defaultValues: {
      title: task.title,
      description: task.description || '',
    },
  });

  const onSubmit = async (data: TaskUpdateFormInputs) => {
    try {
      await updateTask(task.id, {
        title: data.title,
        description: data.description || undefined,
      });
      reset(); // Clear the form after successful update
      onSuccess(); // Notify parent component of success
    } catch (error) {
      console.error('Error updating task:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 p-4 bg-gray-50 rounded-md">
      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-700">
          Title *
        </label>
        <input
          id="title"
          {...register('title')}
          className={`mt-1 block w-full p-2 border rounded-md ${
            errors.title ? 'border-red-300' : 'border-gray-300'
          }`}
          placeholder="Task title"
        />
        {errors.title && (
          <p className="mt-1 text-sm text-red-600">{errors.title.message}</p>
        )}
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700">
          Description
        </label>
        <textarea
          id="description"
          {...register('description')}
          rows={3}
          className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm"
          placeholder="Task description (optional)"
        />
        {errors.description && (
          <p className="mt-1 text-sm text-red-600">{errors.description.message}</p>
        )}
      </div>

      <div className="flex space-x-2">
        <button
          type="submit"
          disabled={loading}
          className={`inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white ${
            loading ? 'bg-indigo-400' : 'bg-indigo-600 hover:bg-indigo-700'
          } focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500`}
        >
          {loading ? 'Updating...' : 'Update Task'}
        </button>

        <button
          type="button"
          onClick={onCancel}
          className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Cancel
        </button>
      </div>
    </form>
  );
};

export default TaskEditForm;