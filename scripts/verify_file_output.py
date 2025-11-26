import asyncio
import os
import shutil
from dotenv import load_dotenv

# Load env to ensure we get the key BEFORE imports
load_dotenv()

import logging
logging.basicConfig(level=logging.INFO)

from src.orchestrator import Orchestrator

async def test_file_output():
    print("Starting test...")
    orchestrator = Orchestrator()
    
    payload = {
        "title": "Test Blog Post",
        "brief": "A short test post about AI.",
        "audience": "developers"
    }
    
    # Run the workflow logic directly (or via start_workflow and wait)
    # We'll use start_workflow and poll status
    sid = await orchestrator.start_workflow(payload)
    print(f"Session started: {sid}")
    
    # Poll for completion
    for _ in range(30): # Wait up to 15 seconds
        status = await orchestrator.get_status(sid)
        state = status.get("state")
        print(f"State: {state}")
        
        if state == "completed":
            break
        if state == "failed":
            print(f"Workflow failed: {status.get('data', {}).get('error')}")
            break
        await asyncio.sleep(0.5)
        
    # Check files
    output_dir = os.path.join("outputs", sid)
    draft_path = os.path.join(output_dir, "draft.md")
    edited_path = os.path.join(output_dir, "edited.md")
    
    if os.path.exists(draft_path):
        print(f"SUCCESS: {draft_path} exists.")
        with open(draft_path, "r") as f:
            content = f.read()
            print(f"Draft content start: {content[:50]}...")
            if "[DEMO LLM OUTPUT]" in content:
                print("WARNING: Still using DEMO mode.")
            else:
                print("SUCCESS: Using Real LLM.")
    else:
        print(f"FAILURE: {draft_path} does not exist.")

    if os.path.exists(edited_path):
        print(f"SUCCESS: {edited_path} exists.")
    else:
        print(f"FAILURE: {edited_path} does not exist.")

if __name__ == "__main__":
    asyncio.run(test_file_output())
