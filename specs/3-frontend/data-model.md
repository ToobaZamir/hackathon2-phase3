# Frontend Data Model for Todo Application

## Frontend State Entities

### User State
- **Purpose**: Manage user authentication and profile information
- **Structure**:
  - `id` (string/number): Unique user identifier from backend
  - `email` (string): User's email address
  - `username` (string): User's chosen username
  - `isLoggedIn` (boolean): Authentication status
  - `isLoading` (boolean): Loading state during auth operations
  - `error` (string|null): Error message during auth operations

### Task State
- **Purpose**: Manage task data and operations
- **Structure**:
  - `id` (string/number): Unique task identifier from backend
  - `title` (string): Task title (required)
  - `description` (string): Task description (optional)
  - `completed` (boolean): Completion status
  - `userId` (string/number): Associated user ID
  - `createdAt` (Date/string): Creation timestamp
  - `updatedAt` (Date/string): Last update timestamp

### Form State
- **Purpose**: Manage form data and validation
- **Structure**:
  - `formData` (object): Current form input values
  - `errors` (object): Validation errors for each field
  - `isSubmitting` (boolean): Submission loading state
  - `submitSuccess` (boolean): Success state after submission
  - `touchedFields` (object): Track which fields have been interacted with

### Loading State
- **Purpose**: Manage loading indicators for different operations
- **Structure**:
  - `globalLoading` (boolean): Overall app loading state
  - `taskLoading` (object): Individual task operation states
    - `fetching` (boolean): Fetching tasks
    - `creating` (boolean): Creating new task
    - `updating` (boolean): Updating existing task
    - `deleting` (boolean): Deleting task
  - `authLoading` (object): Authentication operation states
    - `loggingIn` (boolean): Logging in
    - `registering` (boolean): Registering
    - `loggingOut` (boolean): Logging out

### Error State
- **Purpose**: Manage error messages and display
- **Structure**:
  - `globalErrors` (array): General application errors
  - `fieldErrors` (object): Form field specific errors
  - `apiErrors` (object): API response errors
  - `errorTimestamp` (Date): Time of last error

## State Relationships

### User ↔ Tasks
- One User to Many Tasks relationship
- Tasks are filtered by userId to show only user's tasks
- Authentication state determines access to task operations

### Form ↔ Validation
- Form state contains validation error information
- Validation state affects form submission ability
- Validation feedback updates in real-time

### Loading ↔ Operations
- Loading states correspond to ongoing operations
- UI updates based on loading state changes
- Prevents duplicate operations during loading periods

## State Transitions

### Authentication Transitions
- `initial` → `loading` → `authenticated` (successful login)
- `initial` → `loading` → `error` (failed login)
- `authenticated` → `loading` → `unauthenticated` (logout)

### Task Operation Transitions
- `idle` → `loading` → `success` (create/update/delete operations)
- `idle` → `loading` → `error` (operation failures)
- `idle` → `loading` → `data_updated` (fetch operations)

### Form Transitions
- `empty` → `filling` → `validating` → `submitting` → `submitted`
- `empty` → `filling` → `validating` → `error` (validation failure)

## Validation Rules

### User Registration Validation
- Email: Must be valid email format
- Username: 3-50 characters, alphanumeric with underscores/dashes
- Password: Minimum 6 characters

### Task Creation/Update Validation
- Title: Required, 1-255 characters
- Description: Optional, 0-1000 characters
- UserId: Must match authenticated user

### Authentication Validation
- Login credentials: Required fields
- Token validity: Checked against backend
- Session persistence: Verified on page load

## Frontend-Specific Considerations

### Caching Strategy
- Cache user data in memory during session
- Cache task lists with configurable TTL
- Invalidate cache on mutations
- Refresh stale data on focus/tab visibility

### Error Recovery
- Provide clear error messages to users
- Offer retry options for failed operations
- Maintain data consistency after errors
- Graceful degradation for network failures

### Performance Optimization
- Debounce API calls to prevent spam
- Optimize re-renders with React.memo
- Lazy load non-critical components
- Implement pagination for large task lists