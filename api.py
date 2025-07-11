from fastapi import FastAPI, Query
import psq

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the Postgres MCP API!"}

@app.get("/list_databases")
async def list_databases():
    return await psq.list_databases()

@app.get("/connect_to_database")
async def connect_to_database(db_name: str = Query(...)):
    return await psq.connect_to_database(db_name)

@app.get("/list_tables")
async def list_tables(db_name: str = Query(...)):
    return await psq.list_tables(db_name)

@app.get("/get_table_info")
async def get_table_info(db_name: str = Query(...), table_name: str = Query(...)):
    return await psq.get_table_info(db_name, table_name)

@app.get("/get_relationships")
async def get_relationships(db_name: str = Query(...)):
    return await psq.get_relationships(db_name)

@app.post("/execute_query")
async def execute_query(query: str = Query(...), db_name: str = Query(...)):
    return await psq.execute_query(query, db_name) 


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
