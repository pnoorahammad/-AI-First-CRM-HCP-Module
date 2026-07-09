# AI-First CRM HCP Module

<div align="center">

![AI-First CRM](https://img.shields.io/badge/AI--First%20CRM-HCP%20Module-6C63FF?style=for-the-badge&logo=openai&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2-FFA500?style=for-the-badge&logo=python&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-gemma2--9b--it-F55036?style=for-the-badge)
![PostgreSQL](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)

**An intelligent CRM module for managing Healthcare Professional (HCP) relationships, powered by a LangGraph AI agent with Groq LLM integration.**

</div>

---

## 🚀 Project Overview

The **AI-First CRM HCP Module** is a full-stack web application that allows pharmaceutical sales representatives to:

- **Manage HCP profiles** — search, create, and view healthcare professional records
- **Log interaction records** — structured forms for visit notes, outcomes, and follow-ups
- **Chat with an AI agent** — a LangGraph-powered conversational agent that can:
  - Search HCP records
  - Log new interactions
  - Edit existing interactions
  - Generate interaction summaries
  - Suggest follow-up actions

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    FRONTEND (React 19 + Vite)                │
│  Redux Toolkit  │  MUI v5  │  React Hook Form  │  Axios      │
└────────────────────────┬─────────────────────────────────────┘
                         │ REST API (JSON/JWT)
┌────────────────────────▼─────────────────────────────────────┐
│                  BACKEND (FastAPI 0.115)                      │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │            API Routers (auth / hcp / interactions)      │  │
│  ├─────────────────────────────────────────────────────────┤  │
│  │         LangGraph Agent (StateGraph + ToolNode)         │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │  │
│  │  │search_hcp│ │log_inter.│ │edit_inter│ │followup  │  │  │
│  │  │  Tool    │ │  Tool    │ │  Tool    │ │ Tool     │  │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │  │
│  │              ┌──────────────┐                          │  │
│  │              │interaction   │                          │  │
│  │              │summary Tool  │                          │  │
│  │              └──────────────┘                          │  │
│  ├─────────────────────────────────────────────────────────┤  │
│  │              Groq LLM (gemma2-9b-it)                   │  │
│  └─────────────────────────────────────────────────────────┘  │
└────────────────────────┬─────────────────────────────────────┘
                         │ HTTPS API / PostgreSQL
┌────────────────────────▼─────────────────────────────────────┐
│                  Supabase (PostgreSQL)                        │
│  users  │  hcps  │  interactions  │  followups  │  ai_logs   │
└──────────────────────────────────────────────────────────────┘
```

---

## 🧠 LangGraph AI Tools

| Tool | Description |
|---|---|
| `SearchHCPTool` | Searches HCP records by name/specialty/keyword |
| `LogInteractionTool` | Creates a new interaction record from natural language |
| `EditInteractionTool` | Updates an existing interaction by ID |
| `InteractionSummaryTool` | Returns a formatted summary of past HCP interactions |
| `FollowupRecommendationTool` | Suggests next best action based on interaction history |

---

## 🛠️ Tech Stack

### Backend
| Technology | Version | Purpose |
|---|---|---|
| FastAPI | 0.115.6 | REST API framework |
| LangGraph | 0.2.60 | AI agent orchestration |
| LangChain-Groq | 0.2.4 | Groq LLM integration |
| SQLAlchemy | 2.0.36 | ORM (local SQLite) |
| Supabase | ≥2.0.0 | Cloud PostgreSQL data layer |
| Alembic | 1.14.1 | Database migrations |
| python-jose | 3.3.0 | JWT authentication |
| passlib + bcrypt | 1.7.4 / 4.2.1 | Password hashing |
| Pydantic v2 | 2.10.4 | Data validation |

### Frontend
| Technology | Version | Purpose |
|---|---|---|
| React | 19.2.7 | UI framework |
| Vite | 8.1.1 | Build tool |
| Redux Toolkit | 2.12.0 | State management |
| Material UI | 5.x | Component library |
| React Router | 7.18.1 | Client-side routing |
| React Hook Form | 7.81.0 | Form management |
| Axios | 1.18.1 | HTTP client |
| TypeScript | 6.0.2 | Static typing |

---

## ⚙️ Environment Setup

### Prerequisites
- Python 3.12+
- Node.js 20+
- Supabase account (or local PostgreSQL)
- Groq API key (free at [console.groq.com](https://console.groq.com))

---

## 🔧 Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux / macOS

# Install dependencies
pip install -r requirements.txt

# Copy environment file and configure it
cp .env.example .env
```

### Backend `.env` configuration

```env
# Database (Supabase PostgreSQL recommended)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Security
SECRET_KEY=your-random-secret-key-at-least-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Groq AI (get free key at console.groq.com)
GROQ_API_KEY=your_groq_api_key
LLM_MODEL=gemma2-9b-it

# CORS
FRONTEND_URL=http://localhost:5173

# Environment
ENVIRONMENT=development
```

```bash
# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs available at: `http://localhost:8000/docs`

### Database Schema

Run the SQL below in your Supabase SQL editor to set up tables:

```sql
-- Users table
create table if not exists users (
  id bigserial primary key,
  email text unique not null,
  full_name text not null,
  hashed_password text not null,
  role text default 'rep',
  is_active boolean default true,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- HCPs table
create table if not exists hcps (
  id bigserial primary key,
  user_id bigint references users(id),
  name text not null,
  specialty text,
  institution text,
  email text,
  phone text,
  territory text,
  notes text,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- Interactions table
create table if not exists interactions (
  id bigserial primary key,
  user_id bigint references users(id),
  hcp_id bigint references hcps(id),
  date date not null,
  time time,
  visit_type text,
  location text,
  outcome text,
  notes text,
  follow_up_date date,
  ai_summary text,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- AI logs table
create table if not exists ai_logs (
  id bigserial primary key,
  user_id bigint references users(id),
  session_id text,
  input_text text,
  output_text text,
  tool_used text,
  latency_ms int,
  created_at timestamptz default now()
);

-- Follow-ups table
create table if not exists followups (
  id bigserial primary key,
  user_id bigint references users(id),
  hcp_id bigint references hcps(id),
  interaction_id bigint references interactions(id),
  due_date date,
  status text default 'pending',
  notes text,
  created_at timestamptz default now()
);
```

---

## 🎨 Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env.local
# Set VITE_API_URL=http://localhost:8000
```

```bash
# Development server
npm run dev

# Production build
npm run build
```

Frontend runs at: `http://localhost:5173`

---

## 🧪 Running Tests

### Backend

```bash
cd backend
venv\Scripts\activate
pytest tests/ -v
```

**12 tests** covering health checks, auth flows, LangGraph tools, security helpers, and graph compilation.

### Frontend Type Check

```bash
cd frontend
npx tsc --noEmit
npm run build
```

---

## 🚀 Deployment

### Backend — Render

1. Connect your GitHub repo to [Render](https://render.com)
2. Create a **Web Service** with:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment:** Add all `.env` variables in the Render dashboard

### Frontend — Vercel

1. Connect repo to [Vercel](https://vercel.com)
2. Set **Root Directory** to `frontend`
3. Add environment variable: `VITE_API_URL=https://your-render-backend.onrender.com`

---

## 📁 Project Structure

```
AI-First CRM HCP Module/
├── backend/
│   ├── app/
│   │   ├── api/            # FastAPI routers
│   │   │   ├── auth.py
│   │   │   ├── hcp.py
│   │   │   ├── interactions.py
│   │   │   ├── chat.py
│   │   │   └── tools.py
│   │   ├── auth/
│   │   │   └── dependencies.py   # JWT auth dependency
│   │   ├── core/
│   │   │   ├── config.py         # Pydantic settings
│   │   │   └── security.py       # JWT + bcrypt helpers
│   │   ├── database/
│   │   │   └── session.py        # SQLAlchemy + Supabase session
│   │   ├── langgraph/
│   │   │   ├── graph.py          # StateGraph compilation
│   │   │   ├── llm.py            # Groq ChatGroq factory
│   │   │   ├── nodes.py          # chatbot_node, should_continue
│   │   │   └── state.py          # AgentState TypedDict
│   │   ├── models/               # SQLAlchemy ORM models
│   │   ├── schemas/              # Pydantic request/response schemas
│   │   ├── services/             # Business logic (Supabase ops)
│   │   ├── tools/                # LangGraph tools (5 tools)
│   │   │   ├── search_hcp.py
│   │   │   ├── log_interaction.py
│   │   │   ├── edit_interaction.py
│   │   │   ├── interaction_summary.py
│   │   │   └── followup_recommendation.py
│   │   └── main.py
│   ├── tests/
│   │   └── test_backend.py       # 12 pytest tests
│   ├── .flake8
│   ├── mypy.ini
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/           # Reusable UI components
│   │   │   ├── chat/             # AI chat panel
│   │   │   ├── interactions/     # Structured form
│   │   │   ├── Sidebar.tsx
│   │   │   └── TopNavbar.tsx
│   │   ├── layouts/
│   │   │   └── MainLayout.tsx
│   │   ├── pages/
│   │   │   ├── DashboardPage.tsx
│   │   │   ├── HCPListPage.tsx
│   │   │   ├── LogInteractionPage.tsx
│   │   │   ├── LoginPage.tsx
│   │   │   └── RegisterPage.tsx
│   │   ├── store/
│   │   │   ├── index.ts          # Redux store
│   │   │   └── slices/           # authSlice, hcpSlice, etc.
│   │   └── main.tsx
│   ├── tsconfig.app.json
│   └── package.json
├── README.md
└── PRESENTATION_SCRIPT.md
```

---

## 🔐 API Reference

### Authentication
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Login and receive JWT |

### HCP Management
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/hcp/` | List all HCPs for user |
| POST | `/api/hcp/` | Create a new HCP |
| GET | `/api/hcp/{id}` | Get HCP details |
| PUT | `/api/hcp/{id}` | Update HCP |
| DELETE | `/api/hcp/{id}` | Delete HCP |

### Interactions
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/interactions/` | List interactions |
| POST | `/api/interactions/` | Create interaction |
| GET | `/api/interactions/{id}` | Get interaction |
| PUT | `/api/interactions/{id}` | Update interaction |
| GET | `/api/interactions/{id}/history` | Audit history |

### AI Chat
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/chat/` | Send message to AI agent |
| GET | `/api/chat/{session_id}` | Get chat history |

---

## 🎯 Key Features

- ✅ **JWT Authentication** — Secure token-based auth with role support (rep/manager/admin)
- ✅ **HCP Management** — Full CRUD for healthcare professional profiles
- ✅ **Interaction Logging** — Structured form with date, time, visit type, outcome, follow-up
- ✅ **AI Chat Interface** — Conversational agent via LangGraph + Groq
- ✅ **5 LangGraph Tools** — Search, log, edit, summarise, recommend
- ✅ **Audit History** — Every interaction change is tracked
- ✅ **Dark-themed UI** — Material Design with Inter font, responsive layout
- ✅ **Rate Limiting** — SlowAPI integrated on sensitive endpoints
- ✅ **Type Safety** — TypeScript + mypy throughout

---

## 👤 Author

Built as a technical interview submission demonstrating full-stack AI engineering capabilities.

**Stack:** React 19 · FastAPI · LangGraph · Groq · Supabase · PostgreSQL · Redux Toolkit
