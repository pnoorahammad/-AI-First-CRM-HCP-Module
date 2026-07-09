"""Tool 5: Follow-up Recommendation"""

from typing import Type
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from app.database.session import SessionLocal
from app.services.interaction_service import get_interactions
from app.services.hcp_service import get_hcp


class FollowupRecommendationInput(BaseModel):
    hcp_id: int = Field(
        description="ID of the Healthcare Professional to generate follow-up recommendations for"
    )


class FollowupRecommendationTool(BaseTool):
    name: str = "followup_recommendation"
    description: str = (
        "Use this tool to analyze previous interactions and generate next actions, meeting agendas, and suggested products/questions."
    )
    args_schema: Type[BaseModel] = FollowupRecommendationInput

    user_id: int = Field(default=None, exclude=True)

    def _run(self, hcp_id: int) -> str:
        """Generate recommendations based on history."""
        if not self.user_id:
            return "Error: user_id is required in the tool configuration."

        try:
            db = SessionLocal()
            hcp = get_hcp(db, hcp_id)
            if not hcp:
                return f"Error: HCP with ID {hcp_id} not found."

            # Get latest interaction to base recommendations on
            interactions = get_interactions(
                db, user_id=self.user_id, hcp_id=hcp_id, limit=3
            )
            db.close()

            if not interactions:
                return "Not enough history to generate specific recommendations. Suggest a general introductory meeting."

            latest = interactions[0]

            # Simple heuristic recommendation (in a real app, this might use another LLM call)
            result = f"Recommendations for next follow-up with {hcp.name}:\n"

            if latest.products_discussed:
                result += f"- Suggested Agenda: Follow up on their experience with {', '.join(latest.products_discussed)}.\n"
                result += "- Suggested Questions: 'How have your patients responded to the samples provided last time?'\n"
            else:
                result += "- Suggested Agenda: Introduce new product line relevant to their speciality.\n"

            if latest.feedback and "concern" in latest.feedback.lower():
                result += "- Critical: Address previous concerns regarding product efficacy or side effects.\n"

            return result
        except Exception as e:
            return f"Error generating recommendations: {str(e)}"
