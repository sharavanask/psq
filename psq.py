import psycopg2
from psycopg2 import pool
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from fastapi import Body
from pydantic import BaseModel
import os

load_dotenv()

DSN = f"""
dbname={os.getenv('DB_NAME')}
user={os.getenv('DB_USER')}
password={os.getenv('DB_PASSWORD')}
host={os.getenv('DB_HOST')}
port={os.getenv('DB_PORT')}
sslmode=require
"""

mcp = FastMCP("postgres-mcp-render")

db_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    dsn=DSN
)

@mcp.tool()
async def list_databases():
    conn, cursor = None, None
    try:
        conn = db_pool.getconn()
        cursor = conn.cursor()
        cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
        databases = cursor.fetchall()
        return [db[0] for db in databases]
    except Exception as e:
        return f"Error: {e}"
    finally:
        if cursor:
            cursor.close()
        if conn:
            db_pool.putconn(conn)

@mcp.tool()
async def list_tables():
    conn, cursor = None, None
    try:
        conn = db_pool.getconn()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public';
        """)
        tables = cursor.fetchall()
        return [table[0] for table in tables]
    except Exception as e:
        return f"Error: {e}"
    finally:
        if cursor:
            cursor.close()
        if conn:
            db_pool.putconn(conn)

@mcp.tool()
async def get_table_info(table_name: str):
    conn, cursor = None, None
    try:
        conn = db_pool.getconn()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = %s
        """, (table_name,))
        columns = cursor.fetchall()
        return [
            {"column": col[0], "type": col[1], "nullable": col[2] == 'YES'}
            for col in columns
        ]
    except Exception as e:
        return f"Error: {e}"
    finally:
        if cursor:
            cursor.close()
        if conn:
            db_pool.putconn(conn)

@mcp.tool()
async def get_relationships():
    conn, cursor = None, None
    try:
        conn = db_pool.getconn()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                conrelid::regclass AS child_table,
                a.attname AS child_column,
                confrelid::regclass AS parent_table,
                af.attname AS parent_column
            FROM
                pg_constraint AS c
                JOIN pg_attribute AS a ON a.attnum = ANY (c.conkey) AND a.attrelid = c.conrelid
                JOIN pg_attribute AS af ON af.attnum = ANY (c.confkey) AND af.attrelid = c.confrelid
            WHERE
                c.contype = 'f';
        """)
        rows = cursor.fetchall()
        return [
            {"child_table": row[0], "child_column": row[1],
             "parent_table": row[2], "parent_column": row[3]}
            for row in rows
        ]
    except Exception as e:
        return f"Error: {e}"
    finally:
        if cursor:
            cursor.close()
        if conn:
            db_pool.putconn(conn)

class QueryInput(BaseModel):
    query: str

@mcp.tool()
async def execute_query(input: QueryInput = Body(...)):
    conn, cursor = None, None
    try:
        conn = db_pool.getconn()
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(input.query)
        try:
            result = cursor.fetchall()
            return result
        except psycopg2.ProgrammingError:
            return "✅ Query executed successfully."
    except Exception as e:
        return f"Error: {e}"
    finally:
        if cursor:
            cursor.close()
        if conn:
            db_pool.putconn(conn)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    mcp.run(port=port)
