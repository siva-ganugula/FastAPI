# Document Management API

A small FastAPI backend for managing document metadata stored in Snowflake.

## Tech Stack

- Python
- FastAPI and Uvicorn
- Pydantic
- Snowflake Python Connector (async)
- `python-dotenv`

## Current Features

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Check whether the API is running |
| `GET` | `/documents` | Retrieve all documents |
| `GET` | `/documents?status=UPLOADED` | Filter documents by status |
| `GET` | `/documents/{document_id}` | Retrieve one document by ID |
| `POST` | `/documents` | Create a document metadata record |

The POST endpoint accepts JSON metadata, generates a document ID in the backend, inserts the record into Snowflake, and returns the created document.

Example request:

```json
{
  "fileName": "annual_report.pdf",
  "fileType": "pdf",
  "pageCount": 25
}
```

## Snowflake Table

- **Database:** `DOCUMENT_MANAGEMENT_DB`
- **Schema:** `DOCUMENTS_SCHEMA`
- **Table:** `DOCUMENTS`
- **Full table name:** `DOCUMENT_MANAGEMENT_DB.DOCUMENTS_SCHEMA.DOCUMENTS`

Current metadata columns used by the API:

- `DOCUMENT_ID`
- `FILENAME`
- `FILE_TYPE`
- `PAGE_COUNT`
- `STATUS` (defaults to `UPLOADED`)

## Project Structure

```text
backend/
├── .env
└── app/
    ├── main.py
    ├── database/
    │   └── snowflake.py
    ├── routers/
    │   └── document.py
    ├── schemas/
    │   └── document.py
    ├── services/
    │   └── document_service.py
    └── repositories/
        └── document_repository.py
```

## Configuration

Create a `.env` file in the backend project root. Add your own Snowflake connection values:

```env
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_user
SNOWFLAKE_AUTHENTICATOR=your_authenticator
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=DOCUMENT_MANAGEMENT_DB
SNOWFLAKE_SCHEMA=DOCUMENTS_SCHEMA
SNOWFLAKE_ROLE=your_role
```

Do not commit `.env` or credentials to source control.

## Run Locally

Run these commands from the backend project root (the directory containing `app/`):

```bash
source .venv/bin/activate
python -m uvicorn app.main:app --reload
```

Open the interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

## Current Scope

This project currently handles **document metadata only**. It does not upload or store the actual file contents. Actual file upload using `multipart/form-data` is a separate planned exercise. PUT, PATCH, and DELETE endpoints have not yet been implemented.
