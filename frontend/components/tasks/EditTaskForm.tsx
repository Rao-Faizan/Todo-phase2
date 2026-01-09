'use client';

import { useState, useEffect } from 'react';
import { updateTask } from '@/lib/api-client';

interface Task {
  id: string;
  title: string;
  description: string | null;
  completed: boolean;
}

interface EditTaskFormProps {
  task: Task;
  onTaskUpdated: () => void;
  onCancel: () => void;
}

export default function EditTaskForm({ task, onTaskUpdated, onCancel }: EditTaskFormProps) {
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

      onTaskUpdated();
    } catch (err: any) {
      setError(err.message || 'An error occurred while updating the task');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-4 p-4 bg-blue-50 rounded-lg border border-blue-200">
      <h3 className="text-lg font-medium text-blue-800 mb-2">Edit Task</h3>

      {error && (
        <div className="mb-2 p-2 bg-red-100 text-red-700 rounded-md">
          {error}
        </div>
      )}

      <div className="space-y-3">
        <div>
          <label htmlFor="edit-title" className="block text-sm font-medium text-gray-700 mb-1">
            Title *
          </label>
          <input
            type="text"
            id="edit-title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            maxLength={200}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Task title"
          />
        </div>

        <div>
          <label htmlFor="edit-description" className="block text-sm font-medium text-gray-700 mb-1">
            Description
          </label>
          <textarea
            id="edit-description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={2}
            maxLength={1000}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Task description (optional)"
          />
        </div>

        <div className="flex items-center">
          <input
            type="checkbox"
            id="edit-completed"
            checked={completed}
            onChange={(e) => setCompleted(e.target.checked)}
            className="h-4 w-4 text-blue-600 rounded focus:ring-blue-500"
          />
          <label htmlFor="edit-completed" className="ml-2 block text-sm text-gray-700">
            Mark as completed
          </label>
        </div>

        <div className="flex space-x-2 pt-2">
          <button
            type="submit"
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 text-white py-1 px-3 rounded-md text-sm disabled:opacity-50"
          >
            {loading ? 'Saving...' : 'Save'}
          </button>
          <button
            type="button"
            onClick={onCancel}
            disabled={loading}
            className="bg-gray-300 hover:bg-gray-400 text-gray-800 py-1 px-3 rounded-md text-sm disabled:opacity-50"
          >
            Cancel
          </button>
        </div>
      </div>
    </form>
  );
}