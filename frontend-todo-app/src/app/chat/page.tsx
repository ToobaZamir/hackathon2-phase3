"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import ChatInterface from "@/components/ChatInterface";
import { Button } from "@/components/ui/button";
import { getToken } from "@/lib/auth";

export default function ChatPage() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [debugInfo, setDebugInfo] = useState({ hasToken: false, hasUser: false, userId: null as number | null });

  // Check authentication on mount
  useEffect(() => {
    const checkAuth = () => {
      const token = getToken();
      const userStr = localStorage.getItem('currentUser');

      const hasToken = !!token;
      const hasUser = !!userStr;
      let userId: number | null = null;

      if (hasUser && userStr) {
        try {
          const user = JSON.parse(userStr);
          userId = user.id;
        } catch (e) {
          console.error('Error parsing user:', e);
        }
      }

      setDebugInfo({ hasToken, hasUser, userId });
      setIsAuthenticated(hasToken && hasUser);
      setLoading(false);
    };

    checkAuth();
  }, []);

  // Show loading spinner
  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  // Show login prompt if not authenticated
  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <div className="max-w-md w-full bg-white shadow-lg rounded-lg p-8 text-center">
          <div className="text-6xl mb-4">🔒</div>
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Authentication Required</h1>
          <p className="text-gray-600 mb-6">
            Please log in to use the AI Todo Assistant.
          </p>

          {/* Debug Info */}
          <div className="mb-6 p-4 bg-yellow-50 border border-yellow-200 rounded text-left text-sm">
            <strong>Diagnostic Info:</strong>
            <div className="mt-2 font-mono text-xs space-y-1">
              <div>Token: {debugInfo.hasToken ? '✅ Found' : '❌ Not Found'}</div>
              <div>User Data: {debugInfo.hasUser ? '✅ Found' : '❌ Not Found'}</div>
              {!debugInfo.hasToken && !debugInfo.hasUser && (
                <div className="mt-2 text-red-600">→ You need to log in first</div>
              )}
            </div>
          </div>

          <div className="space-y-3">
            <Link href="/auth/login" className="block">
              <Button className="w-full bg-blue-600 hover:bg-blue-700" size="lg">
                Go to Login Page
              </Button>
            </Link>
            <Link href="/dashboard" className="block">
              <Button variant="outline" className="w-full">
                Back to Dashboard
              </Button>
            </Link>
          </div>
        </div>
      </div>
    );
  }

  // Authenticated - show chat interface
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

        {/* Success Status */}
        <div className="mb-4 p-4 bg-green-50 border border-green-200 rounded text-sm">
          <strong className="text-green-800">✅ Ready to Chat</strong>
          <div className="mt-1 font-mono text-xs text-green-700">
            User ID: {debugInfo.userId} | Authenticated
          </div>
        </div>

        <ChatInterface />
      </div>
    </div>
  );
}
