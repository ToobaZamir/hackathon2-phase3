/**
 * Chat-related TypeScript types
 */

export interface ChatRequest {
  message: string;
  conversation_id?: number | null;
}

export interface ChatResponse {
  message: string;
  conversation_id: number;
  tool_calls?: ToolCall[] | null;
}

export interface ToolCall {
  tool: string;
  arguments: Record<string, any>;
  result: Record<string, any>;
}

export interface Message {
  role: "user" | "assistant" | "system";
  content: string;
  timestamp?: string;
}
