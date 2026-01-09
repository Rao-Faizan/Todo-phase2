'use client';

import { TaskCard } from './TaskCard';

// Define Task interface locally to avoid circular imports
interface Task {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

interface TaskListProps {
  tasks: Task[];
  onTaskUpdated: () => void;
  onTaskDeleted: () => void;
}

export default function TaskList({ tasks, onTaskUpdated, onTaskDeleted }: TaskListProps) {
  if (tasks.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="bg-gradient-to-br from-primary-100 to-primary-200 dark:from-primary-900/30 dark:to-primary-800/20 w-24 h-24 rounded-full flex items-center justify-center mx-auto mb-6">
          <div className="bg-primary-200 dark:bg-primary-800/50 w-16 h-16 rounded-full flex items-center justify-center">
            <span className="text-3xl">📝</span>
          </div>
        </div>
        <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">No tasks yet</h3>
        <p className="text-gray-500 dark:text-gray-400 max-w-md mx-auto">
          Get started by creating your first task
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4" role="list" aria-label="Task list">
      {tasks.map((task) => (
        <TaskCard
          key={task.id}
          task={task}
          onTaskUpdated={onTaskUpdated}
          onTaskDeleted={onTaskDeleted}
        />
      ))}
    </div>
  );
}