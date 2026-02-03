import { Task } from '@/types/tasks';
import { useTasks } from '@/hooks/useTasks';

interface TaskDeleteDialogProps {
  task: Task;
  onConfirm: () => void;
  onCancel: () => void;
}

const TaskDeleteDialog: React.FC<TaskDeleteDialogProps> = ({ task, onConfirm, onCancel }) => {
  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex items-center justify-center">
      <div className="relative p-4 bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
        <div className="text-center p-5">
          <h3 className="text-lg leading-6 font-medium text-gray-900">Confirm Delete</h3>
          <div className="mt-2 px-7 py-3">
            <p className="text-sm text-gray-500">
              Are you sure you want to delete the task "{task.title}"? This action cannot be undone.
            </p>
          </div>
          <div className="mt-5 sm:mt-6 flex justify-center space-x-4">
            <button
              onClick={onConfirm}
              className="inline-flex justify-center px-4 py-2 text-base font-medium rounded-md shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 sm:text-sm"
            >
              Delete
            </button>
            <button
              onClick={onCancel}
              className="inline-flex justify-center px-4 py-2 text-base font-medium rounded-md shadow-sm text-gray-700 bg-gray-100 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 sm:text-sm"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TaskDeleteDialog;