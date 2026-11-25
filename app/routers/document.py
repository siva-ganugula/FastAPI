
from typing import Any

from fastapi import APIRouter, Depends, Query, status as http_status, HTTPException

from app.database.snowflake import get_snowflake_connection
from app.schemas.document import DocumentCreate, DocumentResponse
from app.services.document_service import DocumentService
from app.repositories.document_repository import DocumentRepository

router = APIRouter(tags=["Documents"])

# GET all documents
@router.get(
    "/documents",
    response_model=list[DocumentResponse]
)
async def get_documents(
    status: str | None = Query(
        default=None,
        description="Filter documents by status"
    ),
    connection: Any = Depends(get_snowflake_connection)
):

    repository = DocumentRepository(connection)
    service = DocumentService(repository)

    documents = await service.list_documents(
        status=status
    )

    return documents


# POST a document

@router.post(
    "/documents",
    response_model=DocumentResponse,
    status_code=http_status.HTTP_201_CREATED
)
async def create_document(
    document_data: DocumentCreate,
    connection: Any = Depends(get_snowflake_connection)
):

    repository = DocumentRepository(connection)
    service = DocumentService(repository)

    created_document = await service.create_document(
        document_data
    )

    return created_document



# GET document by ID
@router.get(
    "/documents/{document_id}",
    response_model=DocumentResponse
)
async def get_document(
    document_id: str,
    connection: Any = Depends(get_snowflake_connection)
):
    repository = DocumentRepository(connection)

    document = await repository.get_document_by_id(
        document_id=document_id
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return document