"""Pydantic schemas for the Interaction model."""

from pydantic import BaseModel
from datetime import datetime, date, time
from typing import Optional, List, Dict, Any


class InteractionBase(BaseModel):
    hcp_id: int
    date: date
    time: time
    visit_type: str
    products_discussed: List[str] = []
    samples_given: List[str] = []
    feedback: Optional[str] = None
    notes: Optional[str] = None
    source: str = "form"


class InteractionCreate(InteractionBase):
    follow_up_date: Optional[date] = None


class InteractionUpdate(BaseModel):
    visit_type: Optional[str] = None
    products_discussed: Optional[List[str]] = None
    samples_given: Optional[List[str]] = None
    feedback: Optional[str] = None
    notes: Optional[str] = None
    follow_up_date: Optional[date] = None


class InteractionResponse(InteractionBase):
    id: int
    user_id: int
    ai_summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class InteractionHistoryResponse(BaseModel):
    id: int
    interaction_id: int
    changed_by: int
    change_type: str
    old_data: Optional[Dict[str, Any]] = None
    new_data: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True
