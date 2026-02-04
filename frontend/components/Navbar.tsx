'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import { LayoutDashboard, LogIn, UserPlus, LogOut, User } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';

export default function Navbar() {
    const { isAuthenticated, logout, user } = useAuth();

    return (
        <motion.nav
            initial={{ y: -100 }}
            animate={{ y: 0 }}
            className="fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-6 py-4 glass bg-black/20 backdrop-blur-md border-b border-white/10"
        >
            <Link href="/" className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-blue-500 to-purple-600 flex items-center justify-center">
                    <LayoutDashboard className="w-5 h-5 text-white" />
                </div>
                <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-400">
                    TodoMaster
                </span>
            </Link>

            <div className="flex items-center gap-6">
                {isAuthenticated ? (
                    <>
                        <div className="hidden sm:flex items-center gap-2 text-gray-300">
                            <User className="w-4 h-4" />
                            <span className="text-sm">{user?.email || 'User'}</span>
                        </div>
                        <Link href="/tasks" className="px-4 py-2 rounded-full glass border border-white/10 text-white text-sm font-medium hover:bg-white/10 transition-all flex items-center gap-2">
                            Dashboard
                        </Link>
                        <button
                            onClick={logout}
                            className="text-gray-300 hover:text-white transition-colors text-sm font-medium flex items-center gap-2"
                        >
                            <LogOut className="w-4 h-4" />
                            <span className="hidden sm:inline">Logout</span>
                        </button>
                    </>
                ) : (
                    <>
                        <Link href="/signin" className="text-gray-300 hover:text-white transition-colors text-sm font-medium flex items-center gap-2">
                            <LogIn className="w-4 h-4" />
                            Sign In
                        </Link>
                        <Link href="/signup" className="px-4 py-2 rounded-full bg-white text-black text-sm font-bold hover:bg-gray-200 transition-all flex items-center gap-2">
                            <UserPlus className="w-4 h-4" />
                            Get Started
                        </Link>
                    </>
                )}
            </div>
        </motion.nav>
    );
}
