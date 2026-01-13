from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BookingBase(BaseModel):
    booking_notes: Optional[str] = None

class BookingCreate(BookingBase):
    session_id: int

class BookingUpdate(BaseModel):
    status: Optional[str] = None
    booking_notes: Optional[str] = None
    payment_status: Optional[str] = None

class Booking(BookingBase):
    id: int
    status: str
    payment_status: str
    student_id: int
    session_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True