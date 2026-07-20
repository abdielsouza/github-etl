import os
import asyncpg
from dotenv import load_dotenv

async def test_postgres_connection():
    load_dotenv()

    db_host = os.getenv('POSTGRES_DB_HOST')
    assert db_host is not None, "database host is none"

    db_name = os.getenv('POSTGRES_DB_NAME')
    assert db_name is not None, "database name is none"

    db_user = os.getenv('POSTGRES_DB_USER')
    assert db_user is not None, "database user is none"

    db_port = os.getenv('POSTGRES_DB_PORT')
    assert db_port is not None, "database port is none"

    db_pass = os.getenv('POSTGRES_DB_PASSWORD')
    assert db_pass is not None, "database pass is none"

    try:
        conn = await asyncpg.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            port=db_port,
            password=db_pass,
        )
        await conn.close()
    except Exception as err:
        raise RuntimeError(err.args[0])