import os

from dotenv import load_dotenv
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.store.postgres.aio import AsyncPostgresStore

load_dotenv()  # take environment variables from .env.


async def main():
    async with (
        AsyncPostgresStore.from_conn_string(
            os.getenv("DB_URL"),
            index={"dims": 1536, "embed": "openai:text-embedding-3-small"},
        ) as store,
        AsyncPostgresSaver.from_conn_string(os.getenv("DB_URL")) as checkpointer,
    ):
        await checkpointer.setup()
        await store.setup()


if __name__ == "__main__":
    import asyncio
    import sys

    if sys.platform.startswith("win"):
        from asyncio import WindowsSelectorEventLoopPolicy
        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
