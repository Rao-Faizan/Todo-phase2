'use client';

import { useState } from 'react';
import { PlusIcon } from '@heroicons/react/24/outline';
import { createTask } from '@/lib/api-client';
import { toast } from 'sonner';

interface CreateTaskFormProps {
  onTaskCreated: () => void;
}

export default function CreateTaskForm({ onTaskCreated }: CreateTaskFormProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    if (title.length > 200) {
      setError('Title must be 200 characters or less');
      return;
    }

    if (description && description.length > 1000) {
      setError('Description must be 1000 characters or less');
      return;
    }

    setLoading(true);
    setError('');

    try {
      await createTask({
        title: title.trim(),
        description: description.trim() || undefined,
      });

      // Reset form
      setTitle('');
      setDescription('');
      setIsOpen(false);

      // Notify parent component
      onTaskCreated();
      toast.success('Task created successfully');
    } catch (err: any) {
      setError(err.message || 'An error occurred while creating the task');
      toast.error('Failed to create task');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mb-8">
      {!isOpen ? (
        <button
          onClick={() => setIsOpen(true)}
          className="w-full flex items-center justify-center gap-2 bg-white/80 dark:bg-dark-800/70 backdrop-blur-[12px] border border-dashed border-white/30 dark:border-dark-600/50 rounded-2xl p-8 text-gray-500 dark:text-dark-300 hover:bg-white/90 dark:hover:bg-dark-700/80 transition-colors duration-300 group"
        >
          <PlusIcon className="h-5 w-5 group-hover:scale-110 transition-transform" />
          <span>Add new task</span>
        </button>
      ) : (
        <form onSubmit={handleSubmit} className="bg-white/80 dark:bg-dark-800/70 backdrop-blur-[12px] border border-white/20 dark:border-dark-600/50 rounded-2xl p-6 shadow-lg shadow-dark-900/10 dark:shadow-dark-900/30" aria-label="Create new task form">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Create New Task</h2>
          {error && (
            <div className="mb-4 p-3 bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300 rounded-lg" role="alert" aria-live="polite">
              {error}
            </div>
          )}
          <div className="grid grid-cols-1 gap-4">
            <div>
              <label htmlFor="title" className="block text-sm font-medium text-gray-700 dark:text-dark-300 mb-2">
                Title *
              </label>
              <input
                type="text"
                id="title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
                maxLength={200}
                className="w-full px-4 py-3 bg-gray-50 dark:bg-dark-700/50 border border-gray-300 dark:border-dark-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                placeholder="What needs to be done?"
                aria-describedby={error ? "create-task-error" : undefined}
              />
            </div>
            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700 dark:text-dark-300 mb-2">
                Description
              </label>
              <textarea
                id="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                rows={3}
                maxLength={1000}
                className="w-full px-4 py-3 bg-gray-50 dark:bg-dark-700/50 border border-gray-300 dark:border-dark-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                placeholder="Add details (optional)"
              />
            </div>
            <div className="flex gap-3 pt-2">
              <button
                type="submit"
                disabled={loading}
                className="flex-1 bg-primary-600 hover:bg-primary-700 text-white py-3 px-4 rounded-lg w-fit disabled:opacity-50 transition-colors duration-300 shadow-sm hover:shadow-md"
                aria-busy={loading}
              >
                {loading ? 'Creating...' : 'Create Task'}
              </button>
              <button
                type="button"
                onClick={() => {
                  setIsOpen(false);
                  setError('');
                }}
                className="px-4 py-3 text-gray-600 dark:text-dark-300 hover:text-gray-800 dark:hover:text-white rounded-lg transition-colors"
              >
                Cancel
              </button>
            </div>
          </div>
          {error && <span id="create-task-error" className="sr-only">{error}</span>}
        </form>
      )}
    </div>
  );
}