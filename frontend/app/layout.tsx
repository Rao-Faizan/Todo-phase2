import './globals.css';
import { AuthProvider } from '@/contexts/AuthContext';
import ClientOnly from '@/components/ClientOnly';

export const metadata = {
  title: 'Todo App',
  description: 'A secure task management application',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50">
        <ClientOnly>
          <AuthProvider>
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              {children}
            </div>
          </AuthProvider>
        </ClientOnly>
      </body>
    </html>
  );
}