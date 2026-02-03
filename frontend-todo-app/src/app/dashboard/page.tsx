'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/auth';
import TaskList from '@/components/tasks/TaskList';
import TaskCreateForm from '@/components/tasks/TaskCreateForm';
import { Task } from '@/types/tasks';

const DashboardPage = () => {
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  // Function to refresh the task list
  const refreshTasks = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  // Callback when a new task is created
  const handleTaskCreated = (newTask: Task) => {
    // Refresh the task list to show the new task
    refreshTasks();
  };

  return (
    <div className="px-4 py-6 sm:px-0">
      <div className="border-4 border-dashed border-gray-200 rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4">Create New Task</h2>
        <TaskCreateForm onTaskCreated={handleTaskCreated} />

        <h2 className="text-xl font-semibold mt-8 mb-4">Your Tasks</h2>
        <TaskList
          refreshKey={`task-list-${refreshTrigger}`} // Trigger refresh when refreshTrigger changes
        />
      </div>
    </div>
  );
};

export default DashboardPage;