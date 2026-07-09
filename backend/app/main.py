from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.core.config import settings
from app.database.session import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure tables are created
    create_tables()
    yield
    # Shutdown logic if any


app = FastAPI(
    title="AI-First CRM HCP Module",
    description="CRM backend with LangGraph powered AI capabilities",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS configuration
# Support a comma-separated FRONTEND_URL and fall back to common dev origins.
origins = []
if settings.FRONTEND_URL:
    if "," in settings.FRONTEND_URL:
        origins = [o.strip() for o in settings.FRONTEND_URL.split(",") if o.strip()]
    else:
        origins = [settings.FRONTEND_URL]

# Always allow common local dev hosts in addition to configured origin(s)
for host in ("http://localhost:5173", "http://localhost:3000"):
    if host not in origins:
        origins.append(host)

allow_origins = ["*"] if "*" in origins else origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Print allowed origins at startup so deployment logs show what was picked up
print("CORS allowed_origins:", allow_origins)

from app.api import auth, hcp, interactions, chat, tools


@app.get("/health")
def health_check():
    return {"status": "healthy", "environment": settings.ENVIRONMENT}


@app.get("/")
def root():
    return {"status": "ok", "message": "AI-First CRM HCP Module API is running"}


# Include routers
app.include_router(auth.router)
app.include_router(hcp.router)
app.include_router(interactions.router)
app.include_router(chat.router)
app.include_router(tools.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
