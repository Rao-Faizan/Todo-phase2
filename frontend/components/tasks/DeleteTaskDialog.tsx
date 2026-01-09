'use client';

import { deleteTask } from '@/lib/api-client';

interface DeleteTaskDialogProps {
  taskId: string;
  taskTitle: string;
  onTaskDeleted: () => void;
  onCancel: () => void;
}

export default function DeleteTaskDialog({ taskId, taskTitle, onTaskDeleted, onCancel }: DeleteTaskDialogProps) {
  const handleDelete = async () => {
    try {
      await deleteTask(taskId);
      onTaskDeleted();
    } catch (err: any) {
      console.error('Error deleting task:', err);
      alert('Failed to delete task');
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <h3 className="text-lg font-medium text-gray-900 mb-2">Delete Task</h3>
        <p className="text-gray-600 mb-4">
          Are you sure you want to delete the task "{taskTitle}"? This action cannot be undone.
        </p>
        <div className="flex justify-end space-x-3">
          <button
            type="button"
            onClick={onCancel}
            className="px-4 py-2 bg-gray-300 text-gray-800 rounded-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500"
          >
            Cancel
          </button>
          <button
            type="button"
            onClick={handleDelete}
            className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );
}