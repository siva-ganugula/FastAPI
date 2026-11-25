
from typing import Any


class DocumentRepository:

    def __init__(self, connection: Any) -> None:
        self.connection = connection

    async def insert_document(
        self,
        document_id: str,
        filename: str,
        file_type: str,
        page_count: int
    ) -> dict[str, Any]:

        insert_query = """
            INSERT INTO DOCUMENTS (
                DOCUMENT_ID,
                FILENAME,
                FILE_TYPE,
                PAGE_COUNT
            )
            VALUES (%s, %s, %s, %s)
        """

        select_query = """
            SELECT
                DOCUMENT_ID,
                FILENAME,
                FILE_TYPE,
                PAGE_COUNT,
                STATUS
            FROM DOCUMENTS
            WHERE DOCUMENT_ID = %s
        """

        async with self.connection.cursor() as cursor:

            # Insert document metadata
            await cursor.execute(
                insert_query,
                (
                    document_id,
                    filename,
                    file_type,
                    page_count
                )
            )

            # Retrieve the inserted document
            await cursor.execute(
                select_query,
                (document_id,)
            )

            row = await cursor.fetchone()

        if row is None:
            raise RuntimeError(
                "Document was inserted but could not be retrieved"
            )

        return {
            "document_id": row[0],
            "filename": row[1],
            "file_type": row[2],
            "page_count": row[3],
            "status": row[4]
        }


    async def list_documents(
    self,
    status: str | None = None
) -> list[dict[str, Any]]:

        query = """
            SELECT
                DOCUMENT_ID,
                FILENAME,
                FILE_TYPE,
                PAGE_COUNT,
                STATUS
            FROM DOCUMENT_MANAGEMENT_DB.DOCUMENTS_SCHEMA.DOCUMENTS
        """

        if status is not None:
            query += " WHERE STATUS = %s"

        async with self.connection.cursor() as cursor:

            if status is not None:
                await cursor.execute(query, (status,))
            else:
                await cursor.execute(query)

            rows = await cursor.fetchall()

        return [
            {
                "document_id": row[0],
                "filename": row[1],
                "file_type": row[2],
                "page_count": row[3],
                "status": row[4]
            }
            for row in rows
        ]

    async def get_document_by_id(
    self,
    document_id: str
) -> dict[str, Any] | None:

        query = """
            SELECT
                DOCUMENT_ID,
                FILENAME,
                FILE_TYPE,
                PAGE_COUNT,
                STATUS
            FROM DOCUMENT_MANAGEMENT_DB.DOCUMENTS_SCHEMA.DOCUMENTS
            WHERE DOCUMENT_ID = %s
        """

        async with self.connection.cursor() as cursor:

            await cursor.execute(query, (document_id,))

            row = await cursor.fetchone()

        if row is None:
            return None

        return {
            "document_id": row[0],
            "filename": row[1],
            "file_type": row[2],
            "page_count": row[3],
            "status": row[4]
        }





        