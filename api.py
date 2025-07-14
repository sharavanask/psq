from fastapi import FastAPI, Query
import psq

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the Postgres MCP API!"}

@app.get("/list_databases")
async def list_databases():
    return await psq.list_databases()


@app.get("/list_tables")
async def list_tables():
    return await psq.list_tables()

@app.get("/get_table_info")
async def get_table_info(table_name: str = Query(...)):
    return await psq.get_table_info(table_name)

@app.get("/get_relationships")
async def get_relationships():
    return await psq.get_relationships()

@app.post("/execute_query")
async def execute_query(query: str = Query(...)):
    return await psq.execute_query(query) 


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)