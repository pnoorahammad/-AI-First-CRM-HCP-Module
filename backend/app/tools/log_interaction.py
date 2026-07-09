"""Tool 1: Log Interaction"""

from typing import Type, Optional
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from app.database.session import SessionLocal
from app.schemas.interaction import InteractionCreate
from app.services.interaction_service import create_interaction


class LogInteractionInput(BaseModel):
    hcp_id: int = Field(description="ID of the Healthcare Professional")
    date: str = Field(description="Date of the interaction in YYYY-MM-DD format")
    time: str = Field(description="Time of the interaction in HH:MM format")
    visit_type: str = Field(
        description="Type of visit: 'In-person', 'Virtual', or 'Phone'"
    )
    products_discussed: list[str] = Field(
        description="List of products discussed", default_factory=list
    )
    samples_given: list[str] = Field(
        description="List of samples given", default_factory=list
    )
    feedback: str = Field(description="Feedback from the HCP", default="")
    notes: str = Field(description="General notes about the interaction", default="")
    follow_up_date: Optional[str] = Field(
        description="Optional follow-up date in YYYY-MM-DD format", default=None
    )


class LogInteractionTool(BaseTool):
    name: str = "log_interaction"
    description: str = (
        "Use this tool to save a logged interaction to the database once the user confirms the details."
    )
    args_schema: Type[BaseModel] = LogInteractionInput

    # Needs user ID context injected
    user_id: int = Field(default=None, exclude=True)

    def _run(
        self,
        hcp_id: int,
        date: str,
        time: str,
        visit_type: str,
        products_discussed: list[str] = [],
        samples_given: list[str] = [],
        feedback: str = "",
        notes: str = "",
        follow_up_date: Optional[str] = None,
    ) -> str:
        """Run the tool to create an interaction."""
        if not self.user_id:
            return "Error: user_id is required in the tool configuration."

        try:
            db = SessionLocal()
            interaction_in = InteractionCreate(
                hcp_id=hcp_id,
                date=date,
                time=time,
                visit_type=visit_type,
                products_discussed=products_discussed,
                samples_given=samples_given,
                feedback=feedback,
                notes=notes,
                follow_up_date=follow_up_date,
                source="ai",
            )
            created = create_interaction(db, interaction_in, self.user_id)
            db.close()
            return f"Successfully logged interaction with ID {created.id}"
        except Exception as e:
            return f"Error logging interaction: {str(e)}"
