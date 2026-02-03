# JWT Authentication Quickstart Guide

## Overview
This guide provides instructions for implementing JWT-based authentication in the Todo Backend system.

## Prerequisites
- FastAPI application with SQLModel/PostgreSQL
- python-jose[cryptography] for JWT handling
- passlib[bcrypt] for password hashing
- Environment variables configured for JWT settings

## Setup Steps

### 1. Install Dependencies
```bash
pip install python-jose[cryptography] passlib[bcrypt] python-multipart
```

### 2. Environment Configuration
Ensure the following environment variables are set:
```bash
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Create User Model
- Implement User model with authentication fields
- Include password hashing methods
- Add proper constraints and indexes

### 4. Create JWT Utilities
- Implement token creation function
- Implement token verification function
- Create authentication dependency

### 5. Create Authentication Endpoints
- POST /auth/register - User registration
- POST /auth/login - User login
- POST /auth/logout - User logout (client-side)

### 6. Protect Existing Endpoints
- Update existing task endpoints to require authentication
- Implement user ID verification to prevent cross-user access
- Add proper error handling

## API Usage

### Registration
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword"
  }'
```

### Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "securepassword"
  }'
```

### Accessing Protected Resources
```bash
curl -X GET "http://localhost:8000/api/1/tasks" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

## Security Considerations
- Never expose user IDs in tokens if they can be guessed
- Always validate that the user_id in the URL matches the token
- Use HTTPS in production
- Rotate SECRET_KEY periodically
- Implement proper rate limiting on auth endpoints
- Log authentication attempts for security monitoring

## Error Handling
- 401: Unauthenticated (invalid or missing token)
- 403: Unauthorized (user_id mismatch)
- 404: Resource not found (to prevent user enumeration)