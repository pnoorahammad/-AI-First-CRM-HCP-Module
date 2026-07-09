"""Tool 4: Interaction Summary"""

from typing import Type
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from app.database.session import SessionLocal
from app.services.interaction_service import get_interactions
from app.services.hcp_service import get_hcp


class InteractionSummaryInput(BaseModel):
    hcp_id: int = Field(
        description="ID of the Healthcare Professional to summarize interactions for"
    )


class InteractionSummaryTool(BaseTool):
    name: str = "interaction_summary"
    description: str = (
        "Use this tool to retrieve a summary of previous meetings, pending follow-ups, sentiment, and key concerns for an HCP."
    )
    args_schema: Type[BaseModel] = InteractionSummaryInput

    user_id: int = Field(default=None, exclude=True)

    def _run(self, hcp_id: int) -> str:
        """Retrieve interaction history for summary."""
        if not self.user_id:
            return "Error: user_id is required in the tool configuration."

        try:
            db = SessionLocal()
            hcp = get_hcp(db, hcp_id)
            if not hcp:
                return f"Error: HCP with ID {hcp_id} not found."

            interactions = get_interactions(
                db, user_id=self.user_id, hcp_id=hcp_id, limit=5
            )
            db.close()

            if not interactions:
                return f"No previous interactions found for {hcp.name}."

            result = f"Previous interactions with {hcp.name}:\n"
            for inter in interactions:
                result += f"\n- Date: {inter.date} ({inter.visit_type})\n"
                if inter.products_discussed:
                    result += f"  Products: {', '.join(inter.products_discussed)}\n"
                if inter.feedback:
                    result += f"  Feedback: {inter.feedback}\n"
                if inter.notes:
                    result += f"  Notes: {inter.notes}\n"

            return result
        except Exception as e:
            return f"Error retrieving interaction summary: {str(e)}"
