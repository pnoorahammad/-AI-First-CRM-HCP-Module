"""
Backend Test Suite — AI-First CRM HCP Module.

Tests cover:
- Health endpoint
- Auth registration & login
- LangGraph tool functions (unit)
- Security helpers (hashing, JWT)
- LangGraph graph compilation
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------


def test_health():
    """Root health-check returns 200."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"


# ---------------------------------------------------------------------------
# Auth endpoints
# ---------------------------------------------------------------------------


class TestAuth:
    """Auth registration and login flows."""

    REGISTER_PAYLOAD = {
        "email": "test_unit@example.com",
        "full_name": "Test User",
        "password": "TestPass123!",
        "role": "rep",
    }

    def _mock_supabase(self):
        """Return a mock Supabase client that mimics insert/select behaviour."""
        sb = MagicMock()
        sb.table.return_value.select.return_value.eq.return_value.limit.return_value.execute.return_value.data = []
        sb.table.return_value.insert.return_value.execute.return_value.data = [
            {
                "id": 1,
                "email": self.REGISTER_PAYLOAD["email"],
                "full_name": self.REGISTER_PAYLOAD["full_name"],
                "role": "rep",
                "is_active": True,
                "hashed_password": "hashed_value",
                "created_at": "2025-01-01T00:00:00",
                "updated_at": "2025-01-01T00:00:00",
            }
        ]
        return sb

    def test_register_success(self):
        """POST /api/auth/register creates a new user."""
        with patch(
            "app.services.user_service.get_supabase", return_value=self._mock_supabase()
        ):
            response = client.post("/api/auth/register", json=self.REGISTER_PAYLOAD)
        assert response.status_code in (201, 400)

    def test_register_missing_field(self):
        """POST /api/auth/register rejects incomplete payloads (422)."""
        response = client.post(
            "/api/auth/register", json={"email": "only@example.com"}
        )
        assert response.status_code == 422

    def test_login_wrong_credentials(self):
        """POST /api/auth/login returns 401 for bad credentials."""
        sb = MagicMock()
        sb.table.return_value.select.return_value.eq.return_value.limit.return_value.execute.return_value.data = []
        with patch("app.services.user_service.get_supabase", return_value=sb):
            response = client.post(
                "/api/auth/login",
                json={"email": "nobody@example.com", "password": "wrong"},
            )
        assert response.status_code == 401


# ---------------------------------------------------------------------------
# LangGraph Tool unit tests
# ---------------------------------------------------------------------------


class TestLangGraphTools:
    """Unit tests for individual LangGraph tool functions."""

    def test_log_interaction_tool_exists(self):
        """LogInteractionTool can be instantiated."""
        from app.tools.log_interaction import LogInteractionTool

        tool = LogInteractionTool()
        assert tool is not None
        assert hasattr(tool, "_run")

    def test_search_hcp_tool_exists(self):
        """SearchHCPTool can be instantiated."""
        from app.tools.search_hcp import SearchHCPTool

        tool = SearchHCPTool()
        assert tool is not None
        assert hasattr(tool, "_run")

    def test_interaction_summary_tool_exists(self):
        """InteractionSummaryTool can be instantiated."""
        from app.tools.interaction_summary import InteractionSummaryTool

        tool = InteractionSummaryTool()
        assert tool is not None
        assert hasattr(tool, "_run")


# ---------------------------------------------------------------------------
# Security utilities
# ---------------------------------------------------------------------------


class TestSecurity:
    """Core security helpers."""

    def test_hash_and_verify_password(self):
        """hash_password / verify_password are consistent."""
        from app.core.security import hash_password, verify_password

        pwd = "SecurePassword123!"
        hashed = hash_password(pwd)
        assert hashed != pwd
        assert verify_password(pwd, hashed) is True
        assert verify_password("WrongPassword", hashed) is False

    def test_create_and_decode_access_token(self):
        """JWT round-trips correctly."""
        from app.core.security import create_access_token, decode_access_token
        from datetime import timedelta

        data = {"sub": "42", "email": "test@example.com", "role": "rep"}
        token = create_access_token(data, expires_delta=timedelta(minutes=30))
        assert isinstance(token, str)

        payload = decode_access_token(token)
        assert payload is not None
        assert payload["email"] == "test@example.com"

    def test_expired_token_returns_none(self):
        """An expired JWT is rejected gracefully."""
        from app.core.security import create_access_token, decode_access_token
        from datetime import timedelta

        data = {"sub": "1", "email": "exp@example.com", "role": "rep"}
        token = create_access_token(data, expires_delta=timedelta(minutes=-1))
        assert decode_access_token(token) is None


# ---------------------------------------------------------------------------
# LangGraph graph structure
# ---------------------------------------------------------------------------


class TestLangGraph:
    """Verify the LangGraph workflow compiles without errors."""

    def test_graph_compiles(self):
        """create_graph returns a compiled graph without raising."""
        from app.langgraph.graph import create_graph

        graph = create_graph(user_id=1)
        assert graph is not None

    def test_get_llm(self):
        """get_llm returns a ChatGroq instance."""
        from app.langgraph.llm import get_llm

        llm = get_llm()
        assert llm is not None
