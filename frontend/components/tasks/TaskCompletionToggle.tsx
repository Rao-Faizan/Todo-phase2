'use client';

import { useState } from 'react';
import { toggleTaskCompletion } from '@/lib/api-client';

interface TaskCompletionToggleProps {
  taskId: string;
  initialCompleted: boolean;
  onTaskUpdated: () => void;
}

export default function TaskCompletionToggle({ taskId, initialCompleted, onTaskUpdated }: TaskCompletionToggleProps) {
  const [completed, setCompleted] = useState(initialCompleted);
  const [loading, setLoading] = useState(false);

  const handleToggle = async () => {
    if (loading) return;

    setLoading(true);
    try {
      await toggleTaskCompletion(taskId, !completed);
      setCompleted(!completed);
      onTaskUpdated();
    } catch (err: any) {
      console.error('Error toggling task completion:', err);
      alert('Failed to update task status');
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      type="button"
      onClick={handleToggle}
      disabled={loading}
      className={`h-5 w-5 rounded border flex items-center justify-center ${
        completed
          ? 'bg-green-500 border-green-500 text-white'
          : 'border-gray-300 hover:border-indigo-500'
      } ${loading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
      aria-label={completed ? 'Mark as incomplete' : 'Mark as complete'}
    >
      {completed && (
        <svg className="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
        </svg>
      )}
    </button>
  );
}