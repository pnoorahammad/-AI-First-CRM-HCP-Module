"""Tool 3: Search HCP"""

from typing import Type
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from app.database.session import SessionLocal
from app.services.hcp_service import get_hcps


class SearchHCPInput(BaseModel):
    query: str = Field(
        description="Search term (name, hospital, location, speciality) to find the HCP"
    )


class SearchHCPTool(BaseTool):
    name: str = "search_hcp"
    description: str = (
        "Use this tool to search for a Healthcare Professional (HCP) by name, hospital, speciality, or location. Returns their ID which is needed to log an interaction."
    )
    args_schema: Type[BaseModel] = SearchHCPInput

    def _run(self, query: str) -> str:
        """Search for HCPs."""
        try:
            db = SessionLocal()
            hcps = get_hcps(db, search=query, limit=5)
            db.close()

            if not hcps:
                return f"No Healthcare Professionals found matching '{query}'."

            result = "Found the following HCPs:\n"
            for hcp in hcps:
                result += f"- ID: {hcp.id}, Name: {hcp.name}, Speciality: {hcp.speciality}, Hospital: {hcp.hospital}\n"
            return result
        except Exception as e:
            return f"Error searching HCPs: {str(e)}"
