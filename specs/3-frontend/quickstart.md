# Frontend Todo Application Quickstart Guide

## Overview
This guide provides instructions for developing and running the responsive frontend web application for the multi-user todo system using Next.js 16+ with Better Auth integration.

## Prerequisites
- Node.js 18+ installed
- npm or yarn package manager
- Access to the backend API server
- Basic knowledge of React and Next.js

## Setup Steps

### 1. Project Initialization
```bash
npx create-next-app@latest todo-frontend --typescript --tailwind --eslint
cd todo-frontend
```

### 2. Install Dependencies
```bash
npm install @better-auth/react @better-auth/client
npm install zod react-hook-form
npm install @hookform/resolvers
# Additional UI dependencies as needed
```

### 3. Environment Configuration
Create a `.env.local` file with the following variables:
```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_AUTH_BASE_URL=http://localhost:8000
```

### 4. Better Auth Setup
- Configure Better Auth provider
- Set up authentication context
- Implement auth hooks and components

### 5. API Client Setup
- Create centralized API client
- Implement JWT token handling
- Set up request/response interceptors
- Configure error handling

## Development Workflow

### Running the Application
```bash
npm run dev
```
The application will be available at http://localhost:3000

### Folder Structure
```
src/
├── app/                    # Next.js App Router pages
│   ├── (auth)/            # Public routes (login, signup)
│   │   ├── login/
│   │   └── signup/
│   ├── dashboard/         # Protected dashboard route
│   ├── tasks/            # Protected tasks route
│   ├── layout.tsx        # Root layout
│   └── page.tsx          # Home page
├── components/            # Reusable UI components
│   ├── auth/             # Authentication components
│   ├── tasks/            # Task management components
│   ├── ui/               # Base UI components
│   └── forms/            # Form components
├── lib/                  # Utility functions and constants
│   ├── api.ts            # API client and services
│   ├── auth.ts           # Authentication utilities
│   └── utils.ts          # General utilities
├── hooks/                # Custom React hooks
│   ├── useAuth.ts        # Authentication hook
│   └── useTasks.ts       # Task management hook
└── types/                # TypeScript type definitions
    ├── auth.ts           # Authentication types
    └── tasks.ts          # Task types
```

## API Usage

### Authentication
```javascript
// Login
const login = async (credentials) => {
  const response = await apiClient.post('/auth/login', credentials);
  // Handle token storage and user state
};

// Register
const register = async (userData) => {
  const response = await apiClient.post('/auth/register', userData);
  // Handle token storage and user state
};
```

### Task Management
```javascript
// Get user tasks
const getUserTasks = async (userId) => {
  const response = await apiClient.get(`/api/${userId}/tasks`);
  return response.data;
};

// Create new task
const createTask = async (userId, taskData) => {
  const response = await apiClient.post(`/api/${userId}/tasks`, taskData);
  return response.data;
};

// Update task
const updateTask = async (userId, taskId, taskData) => {
  const response = await apiClient.put(`/api/${userId}/tasks/${taskId}`, taskData);
  return response.data;
};

// Delete task
const deleteTask = async (userId, taskId) => {
  const response = await apiClient.delete(`/api/${userId}/tasks/${taskId}`);
  return response.data;
};
```

## Security Considerations
- Store JWT tokens securely (preferably in httpOnly cookies)
- Always include Authorization header in API requests
- Implement proper 401/403 error handling
- Sanitize user inputs before sending to API
- Use HTTPS in production

## Error Handling
- Catch and display user-friendly error messages
- Handle network failures gracefully
- Redirect to login on authentication failures
- Implement retry mechanisms for failed requests

## Testing
- Unit tests for individual components
- Integration tests for authentication flows
- End-to-end tests for critical user journeys
- Accessibility testing using automated tools