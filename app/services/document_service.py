
from typing import Any
from uuid import uuid4

from app.schemas.document import DocumentCreate
from app.repositories.document_repository import DocumentRepository


class DocumentService:

    def __init__(self, repository: DocumentRepository) -> None:
        self.repository = repository

    async def create_document(
        self,
        document_data: DocumentCreate
    ) -> dict[str, Any]:

        # Generate a unique document ID
        document_id = str(uuid4())

        # Call repository to insert and retrieve the document
        created_document = await self.repository.insert_document(
            document_id=document_id,
            filename=document_data.filename,
            file_type=document_data.file_type,
            page_count=document_data.page_count
        )

        return created_document

    async def list_documents(
        self,
        status: str | None = None
    ) -> list[dict[str, Any]]:

        documents = await self.repository.list_documents(
            status=status
        )

        return documents