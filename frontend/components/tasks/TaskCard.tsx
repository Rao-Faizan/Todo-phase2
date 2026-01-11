'use client';

import { useState } from 'react';
import { PencilIcon, TrashIcon, CheckCircleIcon, CircleStackIcon } from '@heroicons/react/24/outline';
import { toggleTaskCompletion, deleteTask } from '@/lib/api-client';
import EditTaskForm from './EditTaskForm';
import { toast } from 'sonner';

interface Task {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

interface TaskCardProps {
  task: Task;
  onTaskUpdated: () => void;
  onTaskDeleted: () => void;
}

export function TaskCard({ task, onTaskUpdated, onTaskDeleted }: TaskCardProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [isHovered, setIsHovered] = useState(false);

  const handleToggleComplete = async () => {
    try {
      await toggleTaskCompletion(task.id, !task.completed);
      onTaskUpdated();
      toast.success(`${task.completed ? 'Reopened' : 'Completed'} task`);
    } catch (err: any) {
      console.error('Error updating task:', err);
      toast.error('Failed to update task');
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await deleteTask(task.id);
        onTaskDeleted();
        toast.success('Task deleted');
      } catch (err: any) {
        console.error('Error deleting task:', err);
        toast.error('Failed to delete task');
      }
    }
  };

  const handleEditSuccess = () => {
    setIsEditing(false);
    onTaskUpdated();
    toast.success('Task updated');
  };

  const handleCancelEdit = () => {
    setIsEditing(false);
  };

  if (isEditing) {
    return (
      <div className="bg-white/80 dark:bg-dark-800/70 backdrop-blur-[12px] border border-white/20 dark:border-dark-600/50 rounded-2xl p-6 shadow-lg shadow-dark-900/10 dark:shadow-dark-900/30 hover:shadow-xl hover:shadow-primary-500/10 transition-all duration-300">
        <EditTaskForm
          task={task}
          onEditSuccess={handleEditSuccess}
          onCancel={handleCancelEdit}
        />
      </div>
    );
  }

  return (
    <div
      className={`bg-white/80 dark:bg-dark-800/70 backdrop-blur-[12px] border border-white/20 dark:border-dark-600/50 rounded-2xl p-6 shadow-lg shadow-dark-900/10 dark:shadow-dark-900/30 hover:shadow-xl hover:shadow-primary-500/10 transition-all duration-300 transform hover:scale-[1.02] ${
        task.completed ? 'opacity-70' : ''
      }`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="flex items-start gap-4">
        <button
          onClick={handleToggleComplete}
          className={`flex-shrink-0 mt-1 w-6 h-6 rounded-full flex items-center justify-center transition-all duration-300 ${
            task.completed
              ? 'bg-primary-500 text-white shadow-inner shadow-primary-500/30'
              : 'border-2 border-white/30 dark:border-dark-600/50 bg-white/10 dark:bg-dark-700/30 backdrop-blur-sm hover:border-primary-500 hover:shadow-md hover:shadow-primary-500/20'
          }`}
          aria-label={task.completed ? 'Mark as incomplete' : 'Mark as complete'}
        >
          {task.completed && <CheckCircleIcon className="w-4 h-4" />}
        </button>

        <div className="flex-1 min-w-0">
          <h3 className={`text-lg font-semibold break-words transition-colors ${
            task.completed
              ? 'line-through text-gray-500 dark:text-dark-400'
              : 'text-gray-900 dark:text-white'
          }`}>
            {task.title}
          </h3>

          {task.description && (
            <p className={`mt-2 text-gray-600 dark:text-dark-300 break-words whitespace-pre-wrap ${
              task.completed ? 'line-through' : ''
            }`}>
              {task.description}
            </p>
          )}

          <div className="mt-4 flex items-center gap-2 text-xs text-gray-500 dark:text-dark-400">
            <CircleStackIcon className="h-3 w-3 inline" />
            <span>
              Created: {new Date(task.created_at).toLocaleDateString()}
              {task.updated_at !== task.created_at && (
                <span>, Updated: {new Date(task.updated_at).toLocaleDateString()}</span>
              )}
            </span>
          </div>
        </div>

        {(isHovered || window.innerWidth < 768) && (
          <div className="flex gap-2 ml-2 flex-shrink-0">
            <button
              onClick={() => setIsEditing(true)}
              className="p-2 text-gray-500 hover:text-primary-600 dark:text-dark-400 dark:hover:text-primary-400 rounded-full hover:bg-gray-100 dark:hover:bg-dark-700/50 transition-colors"
              aria-label="Edit task"
            >
              <PencilIcon className="h-4 w-4" />
            </button>
            <button
              onClick={handleDelete}
              className="p-2 text-gray-500 hover:text-red-600 dark:text-dark-400 dark:hover:text-red-400 rounded-full hover:bg-gray-100 dark:hover:bg-dark-700/50 transition-colors"
              aria-label="Delete task"
            >
              <TrashIcon className="h-4 w-4" />
            </button>
          </div>
        )}
      </div>
    </div>
  );
}