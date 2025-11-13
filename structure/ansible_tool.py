import time
from schema import Literal, Optional, Schema

from griptape.artifacts import TextArtifact
from griptape.artifacts.list_artifact import ListArtifact
from griptape.tools import BaseTool
from griptape.utils.decorators import activity
from dotenv import load_dotenv
import json
import requests
import os

load_dotenv()

API_SERVER_URL = os.getenv("API_SERVER_URL", "http://localhost:5000/api/v1/run-patch")

class AnsibleTool(BaseTool):
    @activity(
        config={
            "description": "Runs an Ansible playbook to patch a single host.",
            "schema": Schema(
                {
                    Literal("hostname", description="Vulnerable host's name"): str,
                    Literal("patch_version", description="Patch version"): str,
                }
            )
        }
    )
    def run_ansible_patch(self, hostname: str, patch_version: str) -> TextArtifact:
        """Runs an Ansible playbook to patch a single host. Returns a JSON response indicating the success 
        of the operation.

        Args:
            hostname (str): Vulnerable host's name.
            patch_version (str): Patch version.

        Returns:
            TextArtifact: The patch operation result as a Text Artifact.
        """
        print(f"\n[Tool Call] (Ansible) Running 'patch-{patch_version}' on {hostname}...")
        time.sleep(2) # Simulate work
        
        response = json.dumps({"hostname": hostname, "status": "patch_successful"})
        
        return TextArtifact(response)

def init_tool() -> AnsibleTool:
    return AnsibleTool()