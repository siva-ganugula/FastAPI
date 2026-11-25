
import asyncio

from app.database.snowflake import get_snowflake_connection


async def test_connection():

    print("Connecting to Snowflake...")

    async with get_snowflake_connection() as conn:

        print("Connection established!")

        async with conn.cursor() as cursor:

            query = """
                SELECT
                    CURRENT_VERSION(),
                    CURRENT_USER(),
                    CURRENT_DATABASE(),
                    CURRENT_SCHEMA()
            """

            await cursor.execute(query)

            result = await cursor.fetchone()

            print("\nSnowflake Details")
            print("-----------------")
            print("Version:", result[0])
            print("User:", result[1])
            print("Database:", result[2])
            print("Schema:", result[3])

    print("\nConnection closed successfully!")


if __name__ == "__main__":
    asyncio.run(test_connection())
