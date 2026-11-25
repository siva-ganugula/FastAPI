
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from app.database.snowflake import open_snowflake_connection
from app.routers.document import router as document_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown operations.
    """

    print("Starting FastAPI application...")
    print("Checking Snowflake connectivity...")

    # Verify Snowflake connection during startup
    async with open_snowflake_connection() as connection:

        async with connection.cursor() as cursor:

            await cursor.execute(
                "SELECT CURRENT_VERSION()"
            )

            result = await cursor.fetchone()

            app.state.snowflake_version = result[0]

    print("Snowflake connection verified!")
    print("Snowflake version:", app.state.snowflake_version)

    # Application starts accepting requests
    yield

    # Application shutdown
    print("Shutting down FastAPI application...")


app = FastAPI(
    title="Enterprise Document Management API",
    description="FastAPI with Snowflake integration",
    version="1.0.0",
    lifespan=lifespan
)


app.include_router(
    document_router,
    prefix="/api/v1",
    tags=["Documents"]
)


@app.get("/health")
async def health_check(request: Request):

    return {
        "status": "healthy",
        "snowflake_version": request.app.state.snowflake_version
    }
