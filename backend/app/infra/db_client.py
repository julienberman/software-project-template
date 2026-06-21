from psycopg_pool import AsyncConnectionPool

async def init_db_pool(conn_info: str, min_size: int = 2, max_size: int = 10):
    pool = AsyncConnectionPool(
        conninfo=conn_info,
        min_size=min_size,
        max_size=max_size,
        open=False,
    )
    await pool.open(wait=True)
    try:
        yield pool
    finally:
        await pool.close()

