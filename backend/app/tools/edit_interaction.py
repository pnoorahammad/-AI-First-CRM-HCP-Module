"""Tool 2: Edit Interaction"""

from typing import Type, Optional
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from app.database.session import SessionLocal
from app.schemas.interaction import InteractionUpdate
from app.services.interaction_service import update_interaction


class EditInteractionInput(BaseModel):
    interaction_id: int = Field(description="ID of the interaction to update")
    visit_type: Optional[str] = Field(
        description="Type of visit: 'In-person', 'Virtual', or 'Phone'", default=None
    )
    products_discussed: Optional[list[str]] = Field(
        description="List of products discussed", default=None
    )
    samples_given: Optional[list[str]] = Field(
        description="List of samples given", default=None
    )
    feedback: Optional[str] = Field(description="Feedback from the HCP", default=None)
    notes: Optional[str] = Field(
        description="General notes about the interaction", default=None
    )
    follow_up_date: Optional[str] = Field(
        description="Optional follow-up date in YYYY-MM-DD format", default=None
    )


class EditInteractionTool(BaseTool):
    name: str = "edit_interaction"
    description: str = (
        "Use this tool to edit or modify an existing interaction in the database."
    )
    args_schema: Type[BaseModel] = EditInteractionInput

    # Needs user ID context injected
    user_id: int = Field(default=None, exclude=True)

    def _run(
        self,
        interaction_id: int,
        visit_type: Optional[str] = None,
        products_discussed: Optional[list[str]] = None,
        samples_given: Optional[list[str]] = None,
        feedback: Optional[str] = None,
        notes: Optional[str] = None,
        follow_up_date: Optional[str] = None,
    ) -> str:
        """Run the tool to update an interaction."""
        if not self.user_id:
            return "Error: user_id is required in the tool configuration."

        try:
            db = SessionLocal()
            interaction_in = InteractionUpdate(
                visit_type=visit_type,
                products_discussed=products_discussed,
                samples_given=samples_given,
                feedback=feedback,
                notes=notes,
                follow_up_date=follow_up_date,
            )
            updated = update_interaction(
                db, interaction_id, interaction_in, self.user_id
            )
            db.close()

            if not updated:
                return f"Error: Interaction {interaction_id} not found."

            return f"Successfully updated interaction with ID {updated.id}"
        except Exception as e:
            return f"Error updating interaction: {str(e)}"
