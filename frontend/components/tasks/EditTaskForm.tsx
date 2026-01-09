'use client';

import { useState } from 'react';
import { updateTask } from '@/lib/api-client';
import { toast } from 'sonner';

interface Task {
  id: string;
  title: string;
  description: string | null;
  completed: boolean;
}

interface EditTaskFormProps {
  task: Task;
  onEditSuccess: () => void;
  onCancel: () => void;
}

export default function EditTaskForm({ task, onEditSuccess, onCancel }: EditTaskFormProps) {
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || '');
  const [completed, setCompleted] = useState(task.completed);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

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
      await updateTask(task.id, {
        title: title.trim(),
        description: description.trim() || undefined,
        completed,
      });

      onEditSuccess();
      toast.success('Task updated successfully');
    } catch (err: any) {
      setError(err.message || 'An error occurred while updating the task');
      toast.error('Failed to update task');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="edit-title" className="block text-sm font-medium text-gray-700 dark:text-dark-300 mb-2">
          Title *
        </label>
        <input
          type="text"
          id="edit-title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
          maxLength={200}
          className="w-full px-4 py-3 bg-gray-50 dark:bg-dark-700/50 border border-gray-300 dark:border-dark-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
          placeholder="What needs to be done?"
        />
      </div>

      <div>
        <label htmlFor="edit-description" className="block text-sm font-medium text-gray-700 dark:text-dark-300 mb-2">
          Description
        </label>
        <textarea
          id="edit-description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={3}
          maxLength={1000}
          className="w-full px-4 py-3 bg-gray-50 dark:bg-dark-700/50 border border-gray-300 dark:border-dark-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
          placeholder="Add details (optional)"
        />
      </div>

      <div className="flex items-center gap-3 pt-2">
        <div className="flex items-center">
          <input
            type="checkbox"
            id="edit-completed"
            checked={completed}
            onChange={(e) => setCompleted(e.target.checked)}
            className="h-5 w-5 rounded-full border-2 border-gray-300 dark:border-dark-600 text-primary-600 focus:ring-primary-500"
          />
          <label htmlFor="edit-completed" className="ml-2 block text-sm text-gray-700 dark:text-dark-300">
            Mark as completed
          </label>
        </div>

        <div className="flex gap-2 ml-auto">
          <button
            type="submit"
            disabled={loading}
            className="bg-primary-600 hover:bg-primary-700 text-white py-2 px-4 rounded-lg text-sm disabled:opacity-50 transition-colors duration-300 shadow-sm hover:shadow-md"
          >
            {loading ? 'Saving...' : 'Save'}
          </button>
          <button
            type="button"
            onClick={onCancel}
            disabled={loading}
            className="px-4 py-2 text-gray-600 dark:text-dark-300 hover:text-gray-800 dark:hover:text-white rounded-lg transition-colors"
          >
            Cancel
          </button>
        </div>
      </div>

      {error && (
        <div className="p-3 bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300 rounded-lg text-sm" role="alert" aria-live="polite">
          {error}
        </div>
      )}
    </form>
  );
}