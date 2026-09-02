from pydantic import BaseModel, Field


class MessageResponse(BaseModel):
    msg: str = Field(..., description="Result of the operation", examples=["Operation successful"])


class ErrorOutput(BaseModel):
    error: str = Field(..., description="Reason the request was rejected", examples=["Resource not found"])


class PaginatedResponse(BaseModel):
    total: int = Field(..., description="Total number of items", examples=[1])
    page: int = Field(..., description="Current page number", examples=[1])
    per_page: int = Field(..., description="Number of items per page", examples=[10])
    total_pages: int = Field(..., description="Total number of pages", examples=[1])
