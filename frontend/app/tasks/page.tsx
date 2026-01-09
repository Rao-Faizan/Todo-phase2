'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { getUserTasks, createTask, updateTask, deleteTask, toggleTaskCompletion } from '@/lib/api-client';
import { getUserIdFromToken } from '@/lib/auth-utils';
import CreateTaskForm from '@/components/tasks/CreateTaskForm';
import TaskList from '@/components/tasks/TaskList';

interface Task {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [userId, setUserId] = useState<string | null>(null);
  const router = useRouter();

  // Get user ID from auth token
  useEffect(() => {
    const userId = getUserIdFromToken();
    if (!userId) {
      router.push('/signin');
      return;
    }

    setUserId(userId);
  }, [router]);

  useEffect(() => {
    if (userId) {
      fetchTasks();
    }
  }, [userId]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response: any = await getUserTasks();
      // The API returns an array directly, not wrapped in a 'tasks' property
      setTasks(Array.isArray(response) ? response : []);
      setError(null);
    } catch (err: any) {
      setError('Failed to load tasks');
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  };


  const handleToggleComplete = async (task: Task) => {
    try {
      await toggleTaskCompletion(task.id, !task.completed);
      fetchTasks(); // Refresh the list
    } catch (err: any) {
      setError('Failed to update task');
      console.error('Error updating task:', err);
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await deleteTask(taskId);
        fetchTasks(); // Refresh the list
      } catch (err: any) {
        setError('Failed to delete task');
        console.error('Error deleting task:', err);
      }
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading tasks...</div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800">My Tasks</h1>
          <button
            onClick={() => {
              localStorage.removeItem('authToken');
              router.push('/signin');
            }}
            className="bg-red-500 hover:bg-red-600 text-white py-2 px-4 rounded-md"
          >
            Logout
          </button>
        </div>

        {error && (
          <div className="mb-4 p-4 bg-red-50 text-red-700 rounded-md">
            {error}
          </div>
        )}

        {/* Create Task Form */}
        <CreateTaskForm onTaskCreated={fetchTasks} />

        {/* Tasks List */}
        <div>
          <h2 className="text-xl font-semibold mb-4">Your Tasks ({tasks.length})</h2>
          <TaskList
            tasks={tasks}
            onTaskUpdated={fetchTasks}
            onTaskDeleted={fetchTasks}
          />
        </div>
      </div>
    </div>
  );
}