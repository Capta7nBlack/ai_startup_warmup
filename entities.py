from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# Pydantic models for request bodies
class RentInstrumentRequest(BaseModel):
    user_id: str
    instrument_id: int
    instrument_name: str


class ReturnInstrumentRequest(BaseModel):
    user_id: str
    instrument_id: int


class CreateInstrumentRequest(BaseModel):
    instrument_name: str


class InstrumentStatusResponse(BaseModel):
    instrument_id: int
    available: bool


class AvailableInstrumentResponse(BaseModel):
    id: int
    instrument_name: str
    available: bool




