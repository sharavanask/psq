import psycopg2
from psycopg2 import pool
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os

load_dotenv()

# ✅ Use DSN with sslmode=require for Render PostgreSQL
DSN = f"""
dbname={os.getenv('DB_NAME')}
user={os.getenv('DB_USER')}
password={os.getenv('DB_PASSWORD')}
host={os.getenv('DB_HOST')}
port={os.getenv('DB_PORT')}
sslmode=require
"""

mcp = FastMCP("postgres-mcp-render")

# ✅ Single pool for the Render PostgreSQL instance
db_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    dsn=DSN
)


@mcp.tool()
async def list_tables():
    """List all tables in the connected database"""
    conn, cursor = None, None
    try:
        conn = db_pool.getconn()
        cursor = conn.cursor()
        print("Connected OK. Running query...")
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public';
        """)
        tables = cursor.fetchall()
        print("Query result:", tables)
        return "\n".join([table[0] for table in tables]) or "✅ No tables found in schema 'public'."
    except Exception as e:
        import traceback
        print("Exception:", e)
        traceback.print_exc()
        return f"Error: {e}"
    finally:
        if cursor:
            cursor.close()
        if conn:
            db_pool.putconn(conn)





@mcp.tool()
async def get_table_info(table_name: str):
    """Get column info for a table"""
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
        return "\n".join([f"{col[0]}: {col[1]} ({'nullable' if col[2]=='YES' else 'not nullable'})" for col in columns])
    except Exception as e:
        return f"Error: {e}"
    finally:
        if cursor:
            cursor.close()
        if conn:
            db_pool.putconn(conn)


@mcp.tool()
async def get_relationships():
    """Get foreign key relationships"""
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
        return "\n".join([f"{row[0]}.{row[1]} → {row[2]}.{row[3]}" for row in rows])
    except Exception as e:
        return f"Error: {e}"
    finally:
        if cursor:
            cursor.close()
        if conn:
            db_pool.putconn(conn)


# @mcp.tool()
# async def execute_query(query: str):
#     """Run a raw SQL query"""
#     conn, cursor = None, None
#     try:
#         conn = db_pool.getconn()
#         conn.autocommit = True
#         cursor = conn.cursor()
#         cursor.execute(query)
#         try:
#             result = cursor.fetchall()
#             return result
#         except psycopg2.ProgrammingError:
#             return "✅ Query executed successfully."
#     except Exception as e:
#         return f"Error: {e}"
#     finally:
#         if cursor:
#             cursor.close()
#         if conn:
#             db_pool.putconn(conn)

from pydantic import BaseModel

class QueryInput(BaseModel):
    query: str

@mcp.tool()
async def execute_query(input: QueryInput):
    """Run a raw SQL query"""
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
    print(f"Starting MCP server on port {port}...")
    mcp.run(port=port)
