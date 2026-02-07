'use client';

import { ReactNode } from 'react';
import { useAuth } from '@/contexts/auth';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';

interface DashboardLayoutProps {
  children: ReactNode;
}

const DashboardLayout: React.FC<DashboardLayoutProps> = ({ children }) => {
  const { user, isAuthenticated, loading, logout } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push('/auth/login');
    }
  }, [isAuthenticated, loading, router]);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  const handleLogout = async () => {
    await logout();
    router.push('/auth/login');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Todo Dashboard</h1>
          <nav>
            <ul className="flex items-center space-x-4">
              <li>
                <Link href="/dashboard">
                  <Button variant="ghost">Tasks</Button>
                </Link>
              </li>
              <li>
                <Link href="/chat">
                  <Button variant="default" className="bg-blue-600 hover:bg-blue-700">
                    🤖 AI Chat
                  </Button>
                </Link>
              </li>
              <li>
                <span className="text-gray-700">Welcome, {user?.name || user?.email}</span>
              </li>
              <li>
                <Button onClick={handleLogout} variant="ghost">
                  Logout
                </Button>
              </li>
            </ul>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main>
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          {children}
        </div>
      </main>
    </div>
  );
};

export default DashboardLayout;