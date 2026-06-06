from fastapi import FastAPI
from app.api.routes import router
from app.config import settings

from app.core.database import db
import logging
import sys

# Configure Logging to Console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)],
    force=True
)

from contextlib import asynccontextmanager
from app.core.database import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    db.connect()
    yield
    # Shutdown
    db.close()

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Document Extraction Service", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)
from app.ai_agent.api.routes import router as ai_agent_router
app.include_router(ai_agent_router)


@app.api_route("/health", methods=["GET", "HEAD"])
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=10000, reload=True)
