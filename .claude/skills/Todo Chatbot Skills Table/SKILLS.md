# Phase III Todo Chatbot Skills Table
**Version:** 1.0  
**Date:** 2026-02-07

| Skill Name       | Description                                                                 | Example User Commands / Natural Language Triggers                     | MCP Tool to Call | Tool Parameters                                   |
|-----------------|-----------------------------------------------------------------------------|------------------------------------------------------------------------|-----------------|--------------------------------------------------|
| Add Task        | Creates a new todo task for the user                                        | "Add a task to buy groceries", "Remember to call mom", "Create task Pay bills" | add_task        | user_id, title, description (optional)          |
| List Tasks      | Lists tasks according to status or all tasks                                 | "Show me all my tasks", "What's pending?", "List completed tasks"     | list_tasks      | user_id, status ("all", "pending", "completed") |
| Complete Task   | Marks a specific task as completed                                           | "Mark task 3 as complete", "I finished task 2", "Done with laundry"   | complete_task   | user_id, task_id                                  |
| Delete Task     | Deletes a task from the list                                                | "Delete the meeting task", "Remove task 5", "Cancel task call mom"     | delete_task     | user_id, task_id                                  |
| Update Task     | Updates title or description of an existing task                            | "Change task 1 to 'Call mom tonight'", "Update task 3 description"     | update_task     | user_id, task_id, title (optional), description (optional) |
| Confirm Action  | Sends friendly confirmation message after any successful operation          | N/A (handled internally after add, update, delete, complete)          | N/A             | N/A                                              |
| Handle Errors   | Handles errors gracefully and informs user                                  | N/A (examples: task not found, invalid ID, MCP unavailable)           | N/A             | N/A                                              |
| Bulk Complete   | Marks all tasks matching criteria as complete                                | "Mark all pending tasks as done", "Finish all groceries tasks"        | complete_task   | user_id, task_id (resolved via list_tasks loop) |
| Delete by Name  | Deletes a task by name, resolves via list first                               | "Delete task 'Call mom'", "Remove task 'Buy milk'"                     | list_tasks + delete_task | user_id, task_id (found via list_tasks)       |
| Update by Name  | Updates a task by name, resolves via list first                               | "Change 'Pay bills' to 'Pay electricity bills'"                        | list_tasks + update_task | user_id, task_id (found via list_tasks), title/description |
| Search Tasks    | Finds tasks containing a keyword                                             | "Find tasks with 'meeting'", "Search for bills"                        | list_tasks      | user_id, status (optional)                       |
| Bulk Delete Completed | Deletes all completed tasks                                               | "Delete all completed tasks", "Remove finished tasks"                  | list_tasks + delete_task | user_id, task_ids (found via list_tasks)       |
