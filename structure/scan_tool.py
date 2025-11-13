from schema import Literal, Optional, Schema

from griptape.artifacts import TextArtifact
from griptape.artifacts.list_artifact import ListArtifact
from griptape.tools import BaseTool
from griptape.utils.decorators import activity
import json
from pathlib import Path

CMDB_FILE = "config/cmdb.json"

class ScanTool(BaseTool):
    @activity(
        config={
            "description": "Scans the CMDB file to find all hosts vulnerable to a specific package and version.",
            "schema": Schema(
                {
                    Literal("package_name", description="Vulnerable package name"): str,
                    Literal("vulnerable_version", description="Vulnerable package version"): str,
                }
            )
        }
    )
    def scan_cmdb(self, package_name: str, vulnerable_version: str) -> ListArtifact[TextArtifact]:
        """Scans the CMDB file to find all hosts vulnerable to a 
        specific package and version. Returns a JSON list of vulnerable hosts.

        Args:
            package_name (str): Vulnerable package name.
            vulnerable_version (str): Vulnerable package version.

        Returns:
            TextArtifact: The list of vulnerable servers as a List Artifact of Text Artifacts.
        """
        print(f"\n[Tool Call] scan_cmdb(package_name={package_name}, package_version={vulnerable_version})")
        
        try:
            with open(CMDB_FILE) as f:
                cmdb_data = json.load(f)
        except Exception as e:
            print(f"[AssetScanner] ERROR: Could not read CMDB. {e}")
            return {"error": "Could not read CMDB"}

        vulnerable_hosts = []
        for host in cmdb_data:
            if (host.get('installed_package') == package_name and 
                host.get('package_version') == vulnerable_version):
                vulnerable_hosts.append({
                    "hostname": host.get('hostname'),
                    "environment": host.get('environment')
                })

        print(f"[AssetScanner] CONTEXT: Found {len(vulnerable_hosts)} vulnerable hosts.")
        
        report = {
            "vulnerable_hosts": vulnerable_hosts,
            "summary": {
                "total_vulnerable": len(vulnerable_hosts),
                "prod_count": sum(1 for h in vulnerable_hosts if h['environment'] == 'prod'),
                "staging_count": sum(1 for h in vulnerable_hosts if h['environment'] == 'staging')
            }
        }

        response = json.dumps(report)
        return ListArtifact([TextArtifact(response)])

def init_tool() -> ScanTool:
    return ScanTool()