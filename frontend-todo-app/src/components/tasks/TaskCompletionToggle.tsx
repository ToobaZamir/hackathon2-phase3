import { Task } from '@/types/tasks';
import { useTasks } from '@/hooks/useTasks';

interface TaskCompletionToggleProps {
  task: Task;
}

const TaskCompletionToggle: React.FC<TaskCompletionToggleProps> = ({ task }) => {
  const { toggleTaskCompletion } = useTasks();

  const handleChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    try {
      await toggleTaskCompletion(task.id, e.target.checked);
    } catch (error) {
      console.error('Error updating task completion:', error);
      // Optionally revert the UI change if the API call fails
    }
  };

  return (
    <input
      type="checkbox"
      checked={task.completed}
      onChange={handleChange}
      className="h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
    />
  );
};

export default TaskCompletionToggle;