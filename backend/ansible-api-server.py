import asyncio
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import JSONResponse

app = FastAPI()

# This is our "fake" database of patches that have been applied.
# It will be populated when the /run-patch endpoint is called.
applied_patches_db = {}
# Example:
# {
#   "prod-web-01": [
#       {"patch_version": "v1.2.3", "job_id": "job_1678886401", "timestamp": ...}
#   ]
# }


@app.post('/api/v1/run-patch', status_code=201)
async def run_patch(request: Request):
    """
    Simulates running a patch on a host.
    This is the endpoint the Griptape agent's tool will call.
    """
    print("\n[MCP_SERVER] Received request at /api/v1/run-patch")

    data = await request.json()
    hostname = data.get('hostname')
    patch_version = data.get('patch_version')

    if not hostname or not patch_version:
        print(f"[MCP_SERVER] ERROR: Bad request, missing data: {data}")
        # FastAPI will render the HTTPException detail as the response body
        raise HTTPException(status_code=400, detail={"status": "error", "message": "Missing hostname or patch_version"})

    print(f"[MCP_SERVER] Starting 'patch job' for host: {hostname} (Version: {patch_version})")

    # Simulate the job taking 2 seconds (non-blocking)
    await asyncio.sleep(2)

    job_id = f"job_{int(datetime.utcnow().timestamp())}"
    timestamp = datetime.now().isoformat()

    # Add this patch to our "database"
    if hostname not in applied_patches_db:
        applied_patches_db[hostname] = []

    applied_patches_db[hostname].append({
        "patch_version": patch_version,
        "job_id": job_id,
        "timestamp": timestamp
    })

    print(f"[MCP_SERVER] SUCCESS: Job {job_id} completed for {hostname}.")

    # Return a success message to the Griptape agent
    return JSONResponse(status_code=201, content={
        "status": "success",
        "job_id": job_id,
        "host": hostname,
        "message": f"Patch {patch_version} applied successfully."
    })


@app.get('/api/v1/get-applied-patches')
async def get_patches(hostname: Optional[str] = Query(None)):
    """
    Simulates getting a list of all patches that have been applied.
    The agent can call this to verify its work.
    """
    print("\n[MCP_SERVER] Received request at /api/v1/get-applied-patches")

    if hostname:
        print(f"[MCP_SERVER] Filtering for hostname: {hostname}")
        data = applied_patches_db.get(hostname, [])
        total = len(data)
    else:
        print(f"[MCP_SERVER] Returning entire patch database.")
        data = applied_patches_db
        total = len(applied_patches_db)

    return JSONResponse(status_code=200, content={
        "status": "success",
        "total_hosts_patched": total,
        "data": data
    })


if __name__ == '__main__':
    # Run with: python ec2/ansible-mcp-server.py (for quick local dev)
    # Production/dev usage should run via: uvicorn ec2.ansible-mcp-server:app --host 0.0.0.0 --port 5000
    try:
        import uvicorn

        print("==============================================")
        print("Starting Simple MCP (Patching) Server (FastAPI)...")
        print("Running on http://localhost:5000")
        print("Endpoints:")
        print("  POST /api/v1/run-patch")
        print("  GET  /api/v1/get-applied-patches")
        print("==============================================")

        uvicorn.run(app, host="127.0.0.1", port=5000)
    except Exception:
        # If uvicorn is not installed, fall back to ASGI reference server import failure message
        print("uvicorn is not available. Install uvicorn to run the FastAPI server (pip install uvicorn fastapi)")