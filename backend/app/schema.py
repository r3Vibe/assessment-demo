"""REST API Schemas"""

from pydantic import BaseModel, Field


class ResponseModel(BaseModel):
    """Common response model"""

    data: dict = Field(..., description="Response data")
    error: dict = Field(..., description="Error message, if any")
    status: bool = Field(True, description="Status of the response")


class UploadResponse(BaseModel):
    """Response model data for file upload"""

    message: str = Field(..., description="Upload status message")


class FileUploadResponse(ResponseModel):
    """Response model data for file upload"""

    data: UploadResponse = Field(..., description="Uploaded file information")
