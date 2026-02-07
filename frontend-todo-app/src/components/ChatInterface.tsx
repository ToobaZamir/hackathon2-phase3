"use client";

import { useState, useEffect } from "react";
import MessageList from "./MessageList";
import MessageInput from "./MessageInput";
import { sendChatMessage } from "@/lib/api";
import { getToken } from "@/lib/auth";

interface Message {
  role: "user" | "assistant";
  content: string;
  timestamp?: string;
}

interface User {
  id: number;
  username: string;
  email: string;
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load conversation ID from localStorage on mount
  useEffect(() => {
    const savedConversationId = localStorage.getItem("conversationId");
    if (savedConversationId) {
      setConversationId(parseInt(savedConversationId, 10));
    }
  }, []);

  const handleSendMessage = async (message: string) => {
    if (!message.trim()) return;

    // Add user message optimistically
    const userMessage: Message = {
      role: "user",
      content: message,
      timestamp: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);
    setError(null);

    try {
      // Get authentication data directly from localStorage
      const token = getToken();
      const currentUserStr = localStorage.getItem("currentUser");

      // Extensive debugging
      console.log("=== CHAT SEND DEBUG ===");
      console.log("Token from getToken():", token ? `${token.substring(0, 20)}...` : "NULL");
      console.log("currentUser from localStorage:", currentUserStr ? "EXISTS" : "NULL");
      console.log("All localStorage keys:", Object.keys(localStorage));

      if (!token) {
        console.error("❌ No token found!");
        console.log("Checking localStorage directly:", localStorage.getItem("todo_app_auth_token"));
        throw new Error("No authentication token found. Please log in.");
      }

      if (!currentUserStr) {
        console.error("❌ No currentUser found!");
        throw new Error("User data not found. Please log in again.");
      }

      const currentUser: User = JSON.parse(currentUserStr);
      const userId = currentUser.id;
      console.log("✅ Auth successful! User ID:", userId);

      // Send message to backend
      const response = await sendChatMessage(
        userId,
        message,
        conversationId,
        token
      );

      // Update conversation ID if new conversation
      if (!conversationId && response.conversation_id) {
        setConversationId(response.conversation_id);
        localStorage.setItem(
          "conversationId",
          response.conversation_id.toString()
        );
      }

      // Add assistant message
      const assistantMessage: Message = {
        role: "assistant",
        content: response.message,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err: any) {
      setError(err.message || "Failed to send message");
      console.error("Chat error:", err);

      // Add error message as assistant response
      const errorMessage: Message = {
        role: "assistant",
        content: `Sorry, I encountered an error: ${err.message}`,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleNewConversation = () => {
    setMessages([]);
    setConversationId(null);
    localStorage.removeItem("conversationId");
    setError(null);
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden flex flex-col h-[600px]">
      <div className="flex items-center justify-between px-4 py-3 bg-blue-600 text-white">
        <h2 className="font-semibold">Chat</h2>
        <button
          onClick={handleNewConversation}
          className="text-sm px-3 py-1 bg-blue-700 hover:bg-blue-800 rounded"
        >
          New Conversation
        </button>
      </div>

      {error && (
        <div className="px-4 py-2 bg-red-100 text-red-700 text-sm">
          {error}
        </div>
      )}

      <MessageList messages={messages} loading={loading} />
      <MessageInput onSendMessage={handleSendMessage} disabled={loading} />
    </div>
  );
}
