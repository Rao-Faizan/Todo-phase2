'use client';

import { Task } from '@/app/tasks/page'; // Import Task interface from the page
import { toggleTaskCompletion, deleteTask } from '@/lib/api-client';

interface TaskListProps {
  tasks: Task[];
  onTaskUpdated: () => void;
  onTaskDeleted: () => void;
}

export default function TaskList({ tasks, onTaskUpdated, onTaskDeleted }: TaskListProps) {
  const handleToggleComplete = async (task: Task) => {
    try {
      await toggleTaskCompletion(task.id, !task.completed);
      onTaskUpdated();
    } catch (err: any) {
      console.error('Error updating task:', err);
      alert('Failed to update task');
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await deleteTask(taskId);
        onTaskDeleted();
      } catch (err: any) {
        console.error('Error deleting task:', err);
        alert('Failed to delete task');
      }
    }
  };

  if (tasks.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <p>No tasks yet. Create your first task!</p>
      </div>
    );
  }

  return (
    <div className="space-y-4" role="list" aria-label="Task list">
      {tasks.map((task) => (
        <div
          key={task.id}
          className={`p-4 rounded-lg shadow-md ${
            task.completed ? 'bg-green-50 border-l-4 border-green-500' : 'bg-white'
          }`}
          role="listitem"
        >
          <div className="flex flex-col sm:flex-row sm:items-start gap-3">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={() => handleToggleComplete(task)}
              className="mt-1 sm:mt-0.5 h-5 w-5 text-indigo-600 rounded focus:ring-indigo-500"
              aria-label={`Mark task "${task.title}" as ${task.completed ? 'incomplete' : 'complete'}`}
            />
            <div className="flex-1 min-w-0">
              <h3 className={`text-lg font-medium break-words ${task.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}>
                {task.title}
              </h3>
              {task.description && (
                <p className={`mt-1 break-words ${task.completed ? 'line-through text-gray-500' : 'text-gray-600'}`}>
                  {task.description}
                </p>
              )}
              <div className="mt-2 text-xs text-gray-500">
                Created: {new Date(task.created_at).toLocaleString()}
                {task.updated_at !== task.created_at && (
                  <span>, Updated: {new Date(task.updated_at).toLocaleString()}</span>
                )}
              </div>
            </div>
            <button
              onClick={() => handleDeleteTask(task.id)}
              className="sm:self-start text-red-500 hover:text-red-700"
              aria-label={`Delete task "${task.title}"`}
            >
              Delete
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}