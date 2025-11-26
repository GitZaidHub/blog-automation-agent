import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.orchestrator import Orchestrator
from prometheus_client import start_http_server, Counter
import logging

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(level=LOG_LEVEL, format='%(message)s')
logger = logging.getLogger("abc")

app = FastAPI(title="Automated Blog Concierge")

# Mount static files
app.mount("/static", StaticFiles(directory="src/static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse("src/static/index.html")

orchestrator = Orchestrator()

WORKFLOWS_STARTED = Counter('workflows_started_total', 'Total workflows started')

@app.on_event("startup")
async def startup_event():
    # start prometheus metrics server on port 8001
    try:
        start_http_server(int(os.getenv("METRICS_PORT", "8001")))
        logger.info("Prometheus metrics server started on port 8001")
    except Exception:
        logger.exception("Failed to start metrics server")

@app.post("/create_post")
async def create_post(payload: dict):
    session_id = await orchestrator.start_workflow(payload)
    WORKFLOWS_STARTED.inc()
    return {"session_id": session_id}

@app.get("/status/{session_id}")
async def status(session_id: str):
    return await orchestrator.get_status(session_id)
