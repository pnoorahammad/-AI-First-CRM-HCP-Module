# AI-First CRM HCP Module — Video Presentation Script (12–15 mins)

---

## 1. Opening Hook (1 min)

> *"A pharmaceutical sales rep finishes a long day in the field — they visited three doctors, had detailed conversations about two new drugs, and need to log everything before they forget. Traditionally, they'd spend 20–30 minutes clicking through forms. What if they could just tell their CRM what happened in plain English?"*

That's the problem this project solves.

**Introduce the project:** AI-First CRM HCP Module — a full-stack web application for managing Healthcare Professional (HCP) relationships, powered by a LangGraph conversational AI agent backed by Groq.

---

## 2. Architecture Overview (2 mins)

Walk through the system diagram:

- **Frontend**: React 19 + Vite, Redux Toolkit for state, Material UI v5, TypeScript
- **Backend**: FastAPI 0.115 — REST API with JWT auth, rate limiting (SlowAPI)
- **AI Layer**: LangGraph StateGraph — routes user messages through a chatbot node and a tool-execution node
- **LLM**: Groq API with `gemma2-9b-it` model — extremely fast inference
- **Database**: Supabase (PostgreSQL) for production, SQLite for local dev

**Key insight to communicate:** The LangGraph agent acts as a brain — it reads the user's message, decides which tool (if any) to call, executes it, and formulates a response. All in one API call.

---

## 3. Live Demo — Frontend (3 mins)

### Authentication
- Show the Login page — JWT-based, secure, professional dark theme
- Register a new account and log in

### Dashboard
- Point out the stat cards: total HCPs, recent interactions, follow-ups
- Responsive Material UI layout with Inter font
- Data is pulled from Redux store, synced with backend

### HCP Management
- Navigate to the HCP list
- Show search/filter capability
- Open an HCP profile — specialty, institution, contact info

### Log Interaction (Structured Form)
- Navigate to "Log Interaction"
- Fill in a sample visit: Dr. Smith, today's date, office visit, positive outcome
- Show React Hook Form validation (required fields, date validation)
- Submit — show how it lands in the Redux state and appears in the list

---

## 4. The AI Agent — Live Demo (5 mins) ⭐ KEY SECTION

> *"Now here's where it gets interesting."*

Switch to the **AI Chat** panel.

### Scenario A: Natural Language Logging
Type:
```
I met with Dr. Sarah Chen from City General yesterday at 2pm. We discussed the new oncology drug Verazolam. She had concerns about dosing for elderly patients. Outcome was positive — she agreed to review the clinical data. Please log this interaction and schedule a follow-up for next Friday.
```

**Walk through what happens:**
1. Message hits `POST /api/chat/`
2. LangGraph `chatbot_node` sends the message + history to `gemma2-9b-it`
3. The LLM decides to call `SearchHCPTool` to find "Dr. Sarah Chen"
4. Result returns to the chatbot node — it then calls `LogInteractionTool` with the extracted fields
5. The final response summarises what was logged

### Scenario B: Query Past Interactions
Type:
```
What were the key discussion points in my last 3 meetings with Dr. Chen?
```

Show `InteractionSummaryTool` running — formatted markdown summary returned.

### Scenario C: Follow-up Recommendation
Type:
```
What should I focus on in my next visit with Dr. Chen given her concerns about elderly dosing?
```

Show `FollowupRecommendationTool` — personalized next-action suggestion.

---

## 5. Backend Code Walkthrough (2 mins)

Open these files in the editor:

**`backend/app/langgraph/graph.py`**
```python
workflow = StateGraph(AgentState)
workflow.add_node("chatbot", chatbot_node)
workflow.add_node("tools", tool_node)
workflow.add_conditional_edges("chatbot", should_continue, {...})
```
→ Explain: The `should_continue` function checks if the LLM response has `tool_calls` — if yes, route to tools; if no, end.

**`backend/app/tools/log_interaction.py`**
→ Show the Pydantic `LogInteractionInput` schema — this is what the LLM fills in automatically from natural language.
→ Show the `_run` method — it calls `create_interaction` in the service layer.

**`backend/app/api/chat.py`**
→ Show how the chat endpoint injects the JWT user_id and passes it through to all tools — ensuring data isolation between users.

---

## 6. Testing (1 min)

```bash
cd backend
pytest tests/ -v
```

Show 12 tests passing:
- Health endpoint ✅
- Auth registration + login ✅
- All 5 LangGraph tool instantiation ✅
- Password hashing + JWT round-trip ✅
- Graph compilation ✅

---

## 7. Deployment Strategy (1 min)

- **Backend → Render** — `render.yaml` at project root, single-click deploy
- **Frontend → Vercel** — `vercel.json` in `frontend/`, automatic builds on push
- **Database** — Supabase handles PostgreSQL, scales automatically

Environment variables are kept secure — never committed to git (`.gitignore` covers `.env` files).

---

## 8. Challenges & Design Decisions (1 min)

| Challenge | Solution |
|---|---|
| LLM hallucinating tool arguments | Strict Pydantic schemas with `Field(description=...)` guide the LLM |
| SQLAlchemy + Supabase dual layer | ORM used for local type-checking; all real data ops go through Supabase SDK |
| MUI v5 → v9 migration | Pinned to MUI v5 to match existing codebase syntax |
| React 19 breaking changes | Updated Redux hooks, strict TypeScript with `verbatimModuleSyntax=false` |

---

## 9. Conclusion (30 secs)

> *"This project demonstrates how AI agents — not just AI chat — can fundamentally change enterprise software. The LangGraph pattern makes it easy to add new capabilities: imagine tools for email drafting, competitor intel lookup, or regulatory compliance checks. The same architecture scales."*

> *"Thank you."*

---

## 💡 Tips for Presenting

- Keep the browser devtools open on the Network tab during the AI demo — showing the actual API request/response adds credibility
- If the Groq API is slow, emphasize the `latency_ms` field logged in `ai_logs` — typical response is 800–1200ms
- Mention that every AI interaction is audited and stored in the `ai_logs` table for compliance and debugging
