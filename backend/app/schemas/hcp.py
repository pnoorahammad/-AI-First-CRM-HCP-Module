"""Pydantic schemas for the HCP (Healthcare Professional) model."""

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class HCPBase(BaseModel):
    name: str
    hospital: Optional[str] = None
    speciality: Optional[str] = None
    location: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    notes: Optional[str] = None


class HCPCreate(HCPBase):
    pass


class HCPUpdate(HCPBase):
    name: Optional[str] = None


class HCPResponse(HCPBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
