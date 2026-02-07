"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/contexts/auth";
import ChatInterface from "@/components/ChatInterface";
import { Button } from "@/components/ui/button";

export default function ChatPage() {
  const { user, isAuthenticated, loading } = useAuth();
  const router = useRouter();

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push('/auth/login');
    }
  }, [isAuthenticated, loading, router]);

  // Show loading spinner while checking auth
  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  // Don't render if not authenticated
  if (!isAuthenticated) {
    return null;
  }
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">🤖 AI Todo Assistant</h1>
          <nav>
            <Link href="/dashboard">
              <Button variant="outline">← Back to Tasks</Button>
            </Link>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <div className="mb-6">
          <p className="text-gray-600 text-center">
            Manage your tasks with natural language. Try: "Add buy groceries" or "Show my tasks"
          </p>
        </div>

        {/* Debug Panel */}
        <div className="mb-4 p-4 bg-yellow-50 border border-yellow-200 rounded text-sm">
          <strong>Debug Info:</strong>
          <div className="mt-2 font-mono text-xs">
            <div>Token: {typeof window !== 'undefined' && localStorage.getItem('todo_app_auth_token') ? '✅ Present' : '❌ Missing'}</div>
            <div>User: {typeof window !== 'undefined' && localStorage.getItem('currentUser') ? '✅ Present' : '❌ Missing'}</div>
            {typeof window !== 'undefined' && localStorage.getItem('currentUser') && (
              <div>User ID: {JSON.parse(localStorage.getItem('currentUser')!).id}</div>
            )}
          </div>
        </div>

        <ChatInterface />
      </div>
    </div>
  );
}
