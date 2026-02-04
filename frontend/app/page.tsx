'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import Navbar from '@/components/Navbar';
import { ArrowRight, CheckCircle2, Shield, Zap } from 'lucide-react';

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-900 relative overflow-hidden">
      <Navbar />

      {/* Background Gradients */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] bg-primary-600/30 rounded-full blur-[100px] animate-blob mix-blend-screen" />
        <div className="absolute top-[-10%] right-[-10%] w-[500px] h-[500px] bg-secondary-500/30 rounded-full blur-[100px] animate-blob animation-delay-2000 mix-blend-screen" />
        <div className="absolute bottom-[-20%] left-[20%] w-[600px] h-[600px] bg-purple-600/30 rounded-full blur-[100px] animate-blob animation-delay-4000 mix-blend-screen" />
        <div className="absolute inset-0 bg-grid-white/[0.05] bg-[length:32px_32px]" />
      </div>

      <div className="relative z-10 pt-32 pb-20 px-6 max-w-7xl mx-auto flex flex-col items-center text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full glass border border-white/10 mb-8">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
            </span>
            <span className="text-xs font-medium text-gray-300 tracking-wide uppercase">Hackathon Ready</span>
          </div>

          <h1 className="text-5xl md:text-7xl font-bold tracking-tight mb-6">
            Organize your life with <br />
            <span className="text-gradient">TodoMaster</span>
          </h1>

          <p className="text-lg md:text-xl text-gray-400 max-w-2xl mx-auto mb-10 leading-relaxed">
            Experience the next generation of task management.
            Beautiful, secure, and lightning fast. Built for high performers.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link href="/signup" className="group relative px-8 py-4 bg-white text-black font-bold rounded-full transition-all hover:scale-105 hover:shadow-[0_0_40px_-10px_rgba(255,255,255,0.3)]">
              Get Started Free
              <ArrowRight className="inline-block ml-2 w-5 h-5 transition-transform group-hover:translate-x-1" />
            </Link>
            <Link href="/signin" className="px-8 py-4 glass text-white font-medium rounded-full hover:bg-white/10 transition-all">
              Sign In
            </Link>
          </div>
        </motion.div>

        {/* Feature Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-32 w-full">
          {[
            { icon: Zap, title: "Lightning Fast", desc: "Built on Next.js 16 for instant interactions and zero lag." },
            { icon: Shield, title: "Secure by Design", desc: "Enterprise-grade encryption keeps your data safe." },
            { icon: CheckCircle2, title: "Stay Organized", desc: "Smart categorization helps you focus on what matters." }
          ].map((feature, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.2 }}
              className="glass-card p-8 rounded-2xl border border-white/5 hover:border-white/20 transition-colors text-left"
            >
              <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center mb-4">
                <feature.icon className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-xl font-bold mb-3">{feature.title}</h3>
              <p className="text-gray-400 leading-relaxed">{feature.desc}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </main>
  );
}