'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    // Redirect to tasks page or signup depending on auth status
    router.push('/tasks');
  }, [router]);

  return (
    <div className="flex flex-col items-center justify-between min-h-screen p-24">
      <main className="flex flex-col gap-8 row-start-2 items-center">
        <h1 className="text-4xl font-bold">Welcome to the Todo App</h1>
        <p className="text-lg">Secure task management for everyone</p>
      </main>
    </div>
  );
}