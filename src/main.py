import uvicorn
from fastapi import FastAPI
from src.api.router import router

app = FastAPI(
    title="OCM-MCP-Server",
    description="Server implementation for OCM and MCP integration",
    version="0.1.0"
)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
