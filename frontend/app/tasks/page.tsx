'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { getUserTasks } from '@/lib/api-client';
import { getUserIdFromToken } from '@/lib/auth-utils';
import CreateTaskForm from '@/components/tasks/CreateTaskForm';
import TaskList from '@/components/tasks/TaskList';
import ChatWidget from '@/components/chat/ChatWidget';
import Navbar from '@/components/Navbar';
import { Loader2 } from 'lucide-react';

export interface Task {
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
      setTasks(response.tasks || []);
      setError(null);
    } catch (err: any) {
      setError('Failed to load tasks');
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  };




  if (loading) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center">
        <Loader2 className="w-10 h-10 text-primary-500 animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-900 pb-20 overflow-x-hidden">
      {/* Re-use Navbar logic or create a dashboard specific one. For now, a custom header. */}
      <Navbar />

      <main className="max-w-5xl mx-auto px-4 py-8 pt-24">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">My Tasks</h1>
          <p className="text-gray-400">Manage your daily goals and stay productive.</p>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-red-500/10 border border-red-500/20 text-red-400 rounded-xl">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 space-y-6">
            {/* Tasks List Wrapper */}
            <div className="glass-card rounded-2xl p-6 border border-white/5">
              <h2 className="text-xl font-semibold mb-6 flex items-center justify-between">
                <span>Active Tasks</span>
                <span className="text-xs px-2 py-1 bg-white/10 rounded-full text-gray-300">{tasks.length}</span>
              </h2>
              <TaskList
                tasks={tasks}
                onTaskUpdated={fetchTasks}
                onTaskDeleted={fetchTasks}
              />
            </div>
          </div>

          <div className="space-y-6">
            <div className="glass-card rounded-2xl p-6 border border-white/5 sticky top-24">
              <h2 className="text-lg font-semibold mb-4 text-white">Add New Task</h2>
              <CreateTaskForm onTaskCreated={fetchTasks} />
            </div>

            {/* Chat Widget Wrapper */}
            <div className="glass-card rounded-2xl overflow-hidden border border-white/5">
              <ChatWidget onTaskUpdate={fetchTasks} />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}