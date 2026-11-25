
from pydantic import BaseModel, Field


# Request model: Data received from the frontend
class DocumentCreate(BaseModel):
    filename: str = Field(
        min_length=1,
        max_length=255,
        validation_alias="fileName"
    )

    file_type: str = Field(
        min_length=1,
        max_length=20,
        validation_alias="fileType"
    )

    page_count: int = Field(
        gt=0,
        validation_alias="pageCount"
    )


# Response model: Data returned to the frontend
class DocumentResponse(BaseModel):
    document_id: str
    filename: str
    file_type: str
    page_count: int
    status: str
