## EC2 

ssh -i "dunith-tmm.pem" admin@ec2-3-8-233-150.eu-west-2.compute.amazonaws.com

sudo apt update
sudo apt install -y python3 python3-pip

scp -i "dunith-tmm.pem" admin@ec2-3-8-233-150.eu-west-2.compute.amazonaws.com:

## Running the MCP server (FastAPI)

The project MCP (patching) server was converted from Flask to FastAPI. Below are quick steps to install dependencies and run the server locally for development and testing.

1. Install dependencies

```bash
pip install fastapi uvicorn
```

2. Start the server (recommended):

```bash
# from the repository root
uvicorn ec2.ansible-mcp-server:app --host 127.0.0.1 --port 5000 --reload
```

3. Quick alternative (falls back to printing an instruction if uvicorn is not installed):

```bash
python ec2/ansible-mcp-server.py
```

4. Endpoints

- POST /api/v1/run-patch
	- Request JSON: { "hostname": "<host>", "patch_version": "<version>" }
	- Successful response: 201 Created with job_id and message

- GET /api/v1/get-applied-patches
	- Optional query param: hostname (e.g. ?hostname=prod-web-01)

5. Smoke-test examples

```bash
# Apply a patch (POST)
curl -s -X POST http://127.0.0.1:5000/api/v1/run-patch \
	-H "Content-Type: application/json" \
	-d '{"hostname":"prod-web-01","patch_version":"v1.2.3"}' | jq

# Get all patches (GET)
curl -s http://127.0.0.1:5000/api/v1/get-applied-patches | jq

# Get patches for a specific host
curl -s 'http://127.0.0.1:5000/api/v1/get-applied-patches?hostname=prod-web-01' | jq