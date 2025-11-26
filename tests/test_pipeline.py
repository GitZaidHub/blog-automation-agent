import asyncio
from src.orchestrator import Orchestrator
import pytest

@pytest.mark.asyncio
async def test_run_pipeline_minimal():
    o = Orchestrator()
    payload = {"title": "Test", "brief": "Demo brief", "audience": "devs"}
    sid = await o.start_workflow(payload)
    # wait for completion
    import time
    for _ in range(40):
        status = await o.get_status(sid)
        if status["state"] in ("completed", "failed", "cancelled"):
            break
        await asyncio.sleep(0.2)
    status = await o.get_status(sid)
    assert status["state"] == "completed"
    assert "published" in status["data"]
