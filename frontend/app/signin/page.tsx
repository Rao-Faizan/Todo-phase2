'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { loginUser } from '@/lib/api-client';

export default function SigninPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    setLoading(true);
    setError('');

    try {
      const response = await loginUser({ email, password });

      // Store token in localStorage or sessionStorage
      if (response.token) {
        localStorage.setItem('authToken', response.token);
        // Redirect to tasks page after successful signin
        router.push('/tasks');
      }
    } catch (err: any) {
      setError(err.message || 'An error occurred during sign in');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
      {/* Glassmorphic card container */}
      <div className="max-w-md w-full">
        <div className="bg-white/10 dark:bg-dark-800/30 backdrop-blur-xl border border-white/20 dark:border-dark-600/50 rounded-3xl p-8 shadow-login-card shadow-dark-900/20 dark:shadow-dark-900/40">
          <div className="text-center">
            <h2 className="mt-2 text-2xl md:text-3xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
              Sign in to your account
            </h2>
            <p className="mt-2 text-sm text-gray-300 dark:text-dark-400">
              Organize your tasks and boost productivity
            </p>
          </div>

          <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
            {error && (
              <div className="p-3 bg-red-500/20 border border-red-500/30 rounded-xl text-red-200 text-sm">
                {error}
              </div>
            )}

            <input type="hidden" name="remember" defaultValue="true" />
            <div className="space-y-4">
              <div>
                <label htmlFor="email-address" className="sr-only">
                  Email address
                </label>
                <input
                  id="email-address"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full px-4 py-3 bg-white/10 dark:bg-dark-700/30 border border-white/20 dark:border-dark-600/30 rounded-xl placeholder-gray-400 text-white focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent focus:bg-white/20 dark:focus:bg-dark-600/40 transition-all duration-300"
                  placeholder="Email address"
                />
              </div>
              <div>
                <label htmlFor="password" className="sr-only">
                  Password
                </label>
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-4 py-3 bg-white/10 dark:bg-dark-700/30 border border-white/20 dark:border-dark-600/30 rounded-xl placeholder-gray-400 text-white focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent focus:bg-white/20 dark:focus:bg-dark-600/40 transition-all duration-300"
                  placeholder="Password"
                />
              </div>
            </div>

            <div>
              <button
                type="submit"
                disabled={loading}
                className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-base font-medium rounded-xl text-white bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 focus:ring-offset-transparent shadow-lg shadow-blue-500/20 hover:shadow-xl hover:shadow-blue-500/30 disabled:opacity-50 transition-all duration-300 transform hover:scale-[1.02]"
              >
                {loading ? 'Signing in...' : 'Sign in'}
              </button>
            </div>
          </form>

          <div className="text-center mt-6">
            <p className="text-sm text-gray-300 dark:text-dark-400">
              Don't have an account?{' '}
              <Link href="/signup" className="font-medium text-blue-400 hover:text-blue-300 transition-colors duration-300">
                Sign up
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}