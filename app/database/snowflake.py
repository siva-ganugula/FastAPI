
import os
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from typing import Any

import snowflake.connector.aio
from dotenv import load_dotenv


load_dotenv()


def get_connection_config() -> dict[str, Any]:
    """
    Read and validate Snowflake configuration.
    """

    required_variables = [
        "SNOWFLAKE_ACCOUNT",
        "SNOWFLAKE_USER",
        "SNOWFLAKE_AUTHENTICATOR",
        "SNOWFLAKE_WAREHOUSE",
        "SNOWFLAKE_DATABASE",
        "SNOWFLAKE_SCHEMA",
        "SNOWFLAKE_ROLE",
    ]

    missing_variables = [
        name
        for name in required_variables
        if not os.getenv(name)
    ]

    if missing_variables:
        raise RuntimeError(
            f"Missing environment variables: {missing_variables}"
        )

    return {
        "account": os.environ["SNOWFLAKE_ACCOUNT"],
        "user": os.environ["SNOWFLAKE_USER"],
        "authenticator": os.environ["SNOWFLAKE_AUTHENTICATOR"],
        "warehouse": os.environ["SNOWFLAKE_WAREHOUSE"],
        "database": os.environ["SNOWFLAKE_DATABASE"],
        "schema": os.environ["SNOWFLAKE_SCHEMA"],
        "role": os.environ["SNOWFLAKE_ROLE"],
        "enable_server_session_keep_alive_auto_detection": True,
    }


@asynccontextmanager
async def open_snowflake_connection() -> AsyncIterator[Any]:
    """
    Open a Snowflake connection and close it
    automatically when the context exits.
    """

    connection_config = get_connection_config()

    async with snowflake.connector.aio.connect(
        **connection_config
    ) as connection:
        yield connection


async def get_snowflake_connection() -> AsyncIterator[Any]:
    """
    FastAPI dependency.

    Provides one Snowflake connection per request
    and closes it after the request finishes.
    """

    async with open_snowflake_connection() as connection:
        yield connection
