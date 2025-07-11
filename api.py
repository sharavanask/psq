from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi

import psq

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the Postgres MCP API!"}

@app.post("/openapi.json")
async def openapi_post(request: Request):
    return JSONResponse(get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes
    ))

@app.get("/list_databases")
async def list_databases():
    return await psq.list_databases()

@app.get("/list_tables")
async def list_tables():
    return await psq.list_tables()

@app.get("/get_table_info")
async def get_table_info(table_name: str = Query(...)):
    return await psq.get_table_info(table_name)

# @app.get("/get_relationships")
# async def get_relationships():
#     return await psq.get_relationships()

from pydantic import BaseModel
from fastapi import Body

class QueryInput(BaseModel):
    query: str

@app.post("/execute_query")
async def execute_query(input: QueryInput = Body(...)):
    return await psq.execute_query(input.query)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
