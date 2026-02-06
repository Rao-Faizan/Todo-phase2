'use client';

import { useState } from 'react';
import { createTask } from '@/lib/api-client';
import { PlusCircle, Loader2 } from 'lucide-react';

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
    <form onSubmit={handleSubmit} className="mb-8" aria-label="Create new task form">
      {error && (
        <div className="mb-4 p-3 bg-red-500/10 border border-red-500/20 text-red-400 rounded-lg text-sm" role="alert" aria-live="polite">
          {error}
        </div>
      )}
      <div className="space-y-4">
        <div>
          <label htmlFor="title" className="block text-xs uppercase tracking-wider text-gray-400 mb-1">
            Task Title
          </label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            maxLength={200}
            className="w-full bg-slate-800/50 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all placeholder:text-gray-600"
            placeholder="What needs to be done?"
            aria-describedby={error ? "create-task-error" : undefined}
          />
        </div>
        <div>
          <label htmlFor="description" className="block text-xs uppercase tracking-wider text-gray-400 mb-1">
            Description
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={3}
            maxLength={1000}
            className="w-full bg-slate-800/50 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all placeholder:text-gray-600 resize-none"
            placeholder="Add details..."
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-primary-600 hover:bg-primary-500 text-white font-medium py-3 px-4 rounded-xl transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          aria-busy={loading}
        >
          {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <PlusCircle className="w-5 h-5" />}
          {loading ? 'Adding...' : 'Add Task'}
        </button>
      </div>
      {error && <span id="create-task-error" className="sr-only">{error}</span>}
    </form>
  );
}