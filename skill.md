You are an AI systems architect.

Task:
We have an existing Phase II Todo web app. 
We want to upgrade it to Phase III by adding an AI-powered chatbot interface.

Your job is to generate a **complete list of AI agent skills (abilities) for Phase III**, including:

1. **Task creation** – adding tasks from natural language input  
2. **Task listing** – show all, pending, or completed tasks  
3. **Task completion** – mark tasks done  
4. **Task deletion** – remove tasks by name or ID  
5. **Task update** – change task title or description  
6. **Tool chaining** – combining multiple tool calls in one user request  
7. **Error handling** – gracefully handle invalid or missing tasks  
8. **Stateless conversation support** – agent fetches conversation from DB, never uses server memory  
9. **Friendly confirmations** – always reply in clear, positive natural language  
10. **Natural language understanding** – parse diverse user commands into correct actions  

Requirements:
- Output ONLY a **markdown list of skills with a short description for each**  
- Include **1 example of user command per skill**  
- Do NOT write any code, API details, or MCP tool specs  
- Focus purely on **agent abilities / skills**  

Output format example:

### Skill 1: Task Creation
- Description: …
- User Example: “Add a task to buy groceries”
