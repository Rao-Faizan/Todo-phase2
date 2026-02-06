import './globals.css';
import { Inter } from 'next/font/google';
import { AuthProvider } from '@/contexts/AuthContext';
import ClientOnly from '@/components/ClientOnly';
import { ThemeProvider } from 'next-themes';
import { Toaster } from 'sonner';

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' });

export const metadata = {
  title: 'TodoMaster',
  description: 'A secure task management application',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.variable} font-sans min-h-screen bg-slate-900 text-white selection:bg-primary-500 selection:text-white`}>
        <ThemeProvider attribute="class" defaultTheme="dark" enableSystem={false}>
          <ClientOnly>
            <AuthProvider>
              {children}
              <Toaster position="bottom-right" richColors closeButton />
            </AuthProvider>
          </ClientOnly>
        </ThemeProvider>
      </body>
    </html>
  );
}