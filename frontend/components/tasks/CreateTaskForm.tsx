'use client';

import { useState } from 'react';
import { createTask } from '@/lib/api-client';

interface CreateTaskFormProps {
  onTaskCreated: () => void;
}

export default function CreateTaskForm({ onTaskCreated }: CreateTaskFormProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
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
      await createTask({
        title: title.trim(),
        description: description.trim() || undefined,
      });

      // Reset form
      setTitle('');
      setDescription('');

      // Notify parent component
      onTaskCreated();
    } catch (err: any) {
      setError(err.message || 'An error occurred while creating the task');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-8 p-6 bg-white rounded-lg shadow-md" aria-label="Create new task form">
      <h2 className="text-xl font-semibold mb-4">Create New Task</h2>
      {error && (
        <div className="mb-4 p-2 bg-red-50 text-red-700 rounded-md" role="alert" aria-live="polite">
          {error}
        </div>
      )}
      <div className="grid grid-cols-1 gap-4">
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
            Title *
          </label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            maxLength={200}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder="Task title"
            aria-describedby={error ? "create-task-error" : undefined}
          />
        </div>
        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
            Description
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={3}
            maxLength={1000}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder="Task description (optional)"
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="bg-indigo-600 hover:bg-indigo-700 text-white py-2 px-4 rounded-md w-fit disabled:opacity-50"
          aria-busy={loading}
        >
          {loading ? 'Creating...' : 'Create Task'}
        </button>
      </div>
      {error && <span id="create-task-error" className="sr-only">{error}</span>}
    </form>
  );
}