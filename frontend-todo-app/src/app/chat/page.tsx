"use client";

import { useState } from "react";
import ChatInterface from "@/components/ChatInterface";

export default function ChatPage() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            AI Todo Assistant
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-2">
            Manage your tasks with natural language
          </p>
        </div>
        <ChatInterface />
      </div>
    </div>
  );
}
