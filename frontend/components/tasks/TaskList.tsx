'use client';

import { Task } from '@/app/tasks/page'; // Import Task interface from the page
import { toggleTaskCompletion, deleteTask } from '@/lib/api-client';
import { Trash2, Check, Clock } from 'lucide-react';

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
      <div className="text-center py-12 text-gray-500 border-2 border-dashed border-white/10 rounded-xl">
        <p>No tasks yet. Create your first task!</p>
      </div>
    );
  }

  return (
    <div className="space-y-4" role="list" aria-label="Task list">
      {tasks.map((task) => (
        <div
          key={task.id}
          className={`group p-4 rounded-xl transition-all border ${task.completed
              ? 'bg-slate-800/30 border-green-500/20'
              : 'bg-slate-800/50 border-white/5 hover:border-primary-500/30 hover:bg-slate-800/80'
            }`}
          role="listitem"
        >
          <div className="flex flex-col sm:flex-row sm:items-start gap-4">
            <button
              onClick={() => handleToggleComplete(task)}
              className={`flex-shrink-0 w-6 h-6 rounded-full border flex items-center justify-center transition-colors ${task.completed
                  ? 'bg-green-500 border-green-500 text-white'
                  : 'border-gray-500 hover:border-primary-500 text-transparent'
                }`}
              aria-label={`Mark task "${task.title}" as ${task.completed ? 'incomplete' : 'complete'}`}
            >
              <Check className="w-4 h-4" />
            </button>

            <div className="flex-1 min-w-0">
              <h3 className={`text-lg font-medium break-words transition-colors ${task.completed ? 'line-through text-gray-500' : 'text-gray-200'}`}>
                {task.title}
              </h3>
              {task.description && (
                <p className={`mt-1 break-words ${task.completed ? 'line-through text-gray-600' : 'text-gray-400'}`}>
                  {task.description}
                </p>
              )}
              <div className="mt-3 flex items-center gap-2 text-xs text-gray-500">
                <Clock className="w-3 h-3" />
                <span>{new Date(task.created_at).toLocaleDateString()}</span>
              </div>
            </div>

            <button
              onClick={() => handleDeleteTask(task.id)}
              className="sm:opacity-0 group-hover:opacity-100 transition-opacity p-2 text-gray-500 hover:text-red-400 hover:bg-red-400/10 rounded-lg"
              aria-label={`Delete task "${task.title}"`}
            >
              <Trash2 className="w-4 h-4" />
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}