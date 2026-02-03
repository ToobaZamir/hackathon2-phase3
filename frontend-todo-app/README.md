# Todo Frontend Application

A responsive web application for managing personal todo tasks with secure user authentication.

## Features

- User registration and authentication
- Secure JWT-based authentication
- Create, read, update, and delete tasks
- Responsive design for mobile and desktop
- Form validation with Zod
- Loading and error states
- Accessible UI components

## Tech Stack

- Next.js 16+ (App Router)
- TypeScript
- Tailwind CSS
- React Hook Form + Zod for validation
- Custom authentication system with JWT tokens

## Getting Started

1. Install dependencies:
```bash
npm install
```

2. Create a `.env.local` file with the following environment variables:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_AUTH_BASE_URL=http://localhost:8000
```

3. Run the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## API Usage Examples

### Authentication

```typescript
import { useAuth } from '@/hooks/useAuth';

const { login, register, logout } = useAuth();

// Login
await login({ username: 'user', password: 'password' });

// Register
await register({ username: 'user', email: 'user@example.com', password: 'password' });

// Logout
await logout();
```

### Task Management

```typescript
import { useTasks } from '@/hooks/useTasks';

const { tasks, createTask, updateTask, deleteTask } = useTasks();

// Create a task
await createTask({ title: 'New Task', description: 'Task description' });

// Update a task
await updateTask(1, { title: 'Updated Task', completed: true });

// Delete a task
await deleteTask(1);
```

## Project Structure

```
src/
├── app/                    # Next.js App Router pages
│   ├── (auth)/            # Authentication routes
│   ├── dashboard/         # Protected dashboard
│   └── layout.tsx         # Root layout
├── components/            # Reusable UI components
│   ├── auth/             # Authentication components
│   ├── tasks/            # Task management components
│   └── ui/               # Base UI components
├── contexts/              # React contexts
├── hooks/                 # Custom React hooks
├── lib/                   # Utility functions
├── services/              # API service functions
└── types/                 # TypeScript type definitions
```

## Environment Variables

- `NEXT_PUBLIC_API_BASE_URL`: Base URL for the backend API
- `NEXT_PUBLIC_AUTH_BASE_URL`: Base URL for authentication endpoints

## Available Scripts

- `npm run dev`: Start development server
- `npm run build`: Build for production
- `npm run start`: Start production server
- `npm run lint`: Run linter