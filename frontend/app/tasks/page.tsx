'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { Toaster, toast } from 'sonner';
import { getUserTasks, createTask, updateTask, deleteTask, toggleTaskCompletion } from '@/lib/api-client';
import { getUserIdFromToken } from '@/lib/auth-utils';
import CreateTaskForm from '@/components/tasks/CreateTaskForm';
import TaskList from '@/components/tasks/TaskList';
import { FloatingActionButton } from '@/components/ui/FloatingActionButton';
import { ThemeToggle } from '@/components/ui/ThemeToggle';

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
  const [showFab, setShowFab] = useState(false);
  const router = useRouter();
  const createFormRef = useRef<HTMLDivElement>(null);

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
      toast.error('Failed to load tasks');
    } finally {
      setLoading(false);
    }
  };

  const handleToggleComplete = async (task: Task) => {
    try {
      await toggleTaskCompletion(task.id, !task.completed);
      fetchTasks(); // Refresh the list
      toast.success(`${task.completed ? 'Reopened' : 'Completed'} task`);
    } catch (err: any) {
      setError('Failed to update task');
      console.error('Error updating task:', err);
      toast.error('Failed to update task');
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await deleteTask(taskId);
        fetchTasks(); // Refresh the list
        toast.success('Task deleted');
      } catch (err: any) {
        setError('Failed to delete task');
        console.error('Error deleting task:', err);
        toast.error('Failed to delete task');
      }
    }
  };

  const scrollToCreateForm = () => {
    createFormRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-dark-900">
        <div className="text-xl text-gray-600 dark:text-dark-300">Loading tasks...</div>
        <Toaster position="bottom-right" />
      </div>
    );
  }

  return (
    <div className="relative min-h-screen">
      <div className="absolute top-6 right-6 z-10">
        <ThemeToggle />
      </div>

      <div className="max-w-2xl mx-auto px-4 py-8">
        <div className="bg-white/5 dark:bg-dark-800/20 backdrop-blur-lg border border-white/10 dark:border-dark-700/30 rounded-3xl p-8 shadow-xl shadow-dark-900/10 dark:shadow-dark-900/20">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-2xl md:text-3xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">My Tasks</h1>
            <p className="text-gray-500 dark:text-dark-400 text-sm mt-1">Organize your day efficiently</p>
          </div>
          <button
            onClick={() => {
              localStorage.removeItem('authToken');
              router.push('/signin');
            }}
            className="bg-red-500/20 hover:bg-red-500/30 text-red-200 backdrop-blur-sm border border-red-500/30 py-2 px-4 rounded-full transition-all duration-300 shadow-sm shadow-red-500/20 hover:shadow-md hover:shadow-red-500/30"
          >
            Logout
          </button>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-red-500/20 border border-red-500/30 text-red-200 rounded-xl backdrop-blur-sm">
            {error}
          </div>
        )}

        <div ref={createFormRef}>
          {/* Create Task Form */}
          <CreateTaskForm onTaskCreated={fetchTasks} />
        </div>

        {/* Tasks List */}
        <div className="mt-8">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-lg font-semibold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
              Your Tasks <span className="text-gray-400 dark:text-dark-400">({tasks.length})</span>
            </h2>
          </div>

          {loading ? (
            <div className="space-y-4" role="list" aria-label="Loading tasks">
              {[...Array(3)].map((_, index) => (
                <div key={index} className="bg-white/80 dark:bg-dark-800/70 backdrop-blur-[12px] border border-white/20 dark:border-dark-600/50 rounded-2xl p-6 shadow-lg shadow-dark-900/10 dark:shadow-dark-900/30 animate-pulse">
                  <div className="flex items-start gap-4">
                    <div className="w-6 h-6 rounded-full bg-gray-200/50 dark:bg-dark-700/50 mt-1"></div>
                    <div className="flex-1 space-y-3">
                      <div className="h-5 bg-gray-200/50 dark:bg-dark-700/50 rounded w-3/4"></div>
                      <div className="h-4 bg-gray-200/50 dark:bg-dark-700/50 rounded w-full"></div>
                      <div className="h-4 bg-gray-200/50 dark:bg-dark-700/50 rounded w-2/3"></div>
                      <div className="h-8 w-24 bg-gray-200/50 dark:bg-dark-700/50 rounded mt-4"></div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <TaskList
              tasks={tasks}
              onTaskUpdated={fetchTasks}
              onTaskDeleted={fetchTasks}
            />
          )}
        </div>
        </div> {/* Close glassmorphism container */}
      </div>

      <FloatingActionButton onClick={scrollToCreateForm} ariaLabel="Add new task" />

      <Toaster
        position="bottom-right"
        richColors
        expand={true}
        closeButton
        duration={3000}
      />
    </div>
  );
}