import { useState } from 'react';
import { taskService } from '@/services/tasks';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Task } from '@/types/tasks';

interface TaskItemProps {
  todo: Task;
  onUpdate: (tasks: Task[]) => void;
}

export default function TaskItem({ todo, onUpdate }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(todo.title);
  const [editDescription, setEditDescription] = useState(todo.description || '');
  const [isUpdating, setIsUpdating] = useState(false);

  const handleToggleCompletion = async () => {
    try {
      const updatedTask = await taskService.toggleTaskCompletion(todo.id, !todo.completed);
      onUpdate(prevTasks =>
        prevTasks.map(t => t.id === todo.id ? updatedTask : t)
      );
    } catch (error) {
      console.error('Error toggling task completion:', error);
      alert('Failed to update task completion status. Please try again.');
    }
  };

  const handleDelete = async () => {
    if (window.confirm(`Are you sure you want to delete task "${todo.title}"?`)) {
      try {
        await taskService.deleteTask(todo.id);
        onUpdate(prevTasks => prevTasks.filter(t => t.id !== todo.id));
      } catch (error) {
        console.error('Error deleting task:', error);
        alert('Failed to delete task. Please try again.');
      }
    }
  };

  const handleSaveEdit = async () => {
    if (!editTitle.trim()) {
      alert('Title is required');
      return;
    }

    setIsUpdating(true);
    try {
      const updatedTask = await taskService.updateTask(todo.id, {
        title: editTitle,
        description: editDescription || undefined,
        completed: todo.completed, // Preserve the current completion status
      });

      // Update the parent state with the new task data
      onUpdate(prevTasks =>
        prevTasks.map(t => t.id === todo.id ? updatedTask : t)
      );

      // Exit edit mode
      setIsEditing(false);
    } catch (error) {
      console.error('Error updating task:', error);
      alert('Failed to update task. Please try again.');
    } finally {
      setIsUpdating(false);
    }
  };

  const handleCancelEdit = () => {
    setEditTitle(todo.title);
    setEditDescription(todo.description || '');
    setIsEditing(false);
  };

  if (isEditing) {
    return (
      <li className="p-4 border rounded-lg bg-blue-50">
        <div className="flex items-start space-x-3">
          <Checkbox
            id={`todo-${todo.id}`}
            checked={todo.completed}
            onCheckedChange={handleToggleCompletion}
          />
          <div className="flex-1 space-y-2">
            <input
              type="text"
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Task title"
            />
            <textarea
              value={editDescription}
              onChange={(e) => setEditDescription(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Task description (optional)"
              rows={2}
            />
          </div>
        </div>
        <div className="flex justify-end space-x-2 mt-3">
          <Button type="button" variant="outline" onClick={handleCancelEdit} disabled={isUpdating}>
            Cancel
          </Button>
          <Button type="button" onClick={handleSaveEdit} disabled={isUpdating}>
            {isUpdating ? 'Saving...' : 'Save'}
          </Button>
        </div>
      </li>
    );
  }

  return (
    <li className={`p-4 border rounded-lg ${todo.completed ? 'bg-green-50' : 'bg-white'}`}>
      <div className="flex items-start justify-between">
        <div className="flex items-start space-x-3 flex-1">
          <Checkbox
            id={`todo-${todo.id}`}
            checked={todo.completed}
            onCheckedChange={handleToggleCompletion}
          />
          <div className="flex-1">
            <h3 className={`font-medium ${todo.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
              {todo.title}
            </h3>
            {todo.description && (
              <p className={`text-sm mt-1 ${todo.completed ? 'line-through text-gray-400' : 'text-gray-600'}`}>
                {todo.description}
              </p>
            )}
            <p className="text-xs text-gray-500 mt-2">
              Updated: {new Date(todo.updated_at).toLocaleString()}
            </p>
          </div>
        </div>
        <div className="flex space-x-2">
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={() => setIsEditing(true)}
          >
            Edit
          </Button>
          <Button
            type="button"
            variant="destructive"
            size="sm"
            onClick={handleDelete}
          >
            Delete
          </Button>
        </div>
      </div>
    </li>
  );
}