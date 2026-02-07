"use client";

import { useState } from "react";
import Link from "next/link";
import ChatInterface from "@/components/ChatInterface";
import { Button } from "@/components/ui/button";

export default function ChatPage() {
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
        <ChatInterface />
      </div>
    </div>
  );
}
