import sys
import argparse
from dotenv import load_dotenv
from griptape.rules import Rule, Ruleset
from griptape.structures import Agent
from griptape.utils import GriptapeCloudStructure 

from scan_tool import ScanTool
from ansible_tool import AnsibleTool
from slack_tool import SlackTool

load_dotenv()

def build_agent() -> Agent:
    """Build the DevOps Structure."""
    return Agent(
        id="operations-agent",
        tools=[ScanTool(), AnsibleTool(), SlackTool()],
        rulesets=[
            Ruleset(
                name="Objective",
                rules=[
                    Rule(
                        value="Autonomously handle threats from end-to-end while strictly following the rules of engagement given.",
                    )
                ],
            ),
            Ruleset(
                name="Background",
                rules=[
                    Rule(
                        value="You are an autonomous, senior-level DevOps agent."
                    )
                ],
            ),
            Ruleset(
                name="Rules of Engagement",
                rules=[
                    Rule(
                        value="If a server's environment is 'staging', its action_to_take is 'auto-patch'.",
                    ),
                    Rule(
                        value="If a server's environment is 'prod', its action_to_take is 'notify-human'."
                    ),
                    Rule(
                        value="""If a server's environment is unknown or not 'prod'/'staging', 
                        its action_to_take is 'notify-human' (the 'default' rule)."""
                    )
                ],
            ),
        ],
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--cve-id",
        default="CVE-2025-12345",
        help="CVE ID",
    )
    parser.add_argument(
        "-n",
        "--package-name",
        default="openssl-lib",
        help="Package name",
    )
    parser.add_argument(
        "-v",
        "--vulnerable-version",
        default="v1.2.3",
        help="Vulnerable version"
    )
    parser.add_argument(
        "-p",
        "--patch-version",
        default="v1.2.4",
        help="Patch version"
    )
    parser.add_argument(
        "-s",
        "--summary",
        default=None,
        help="Summary"
    )
    args = parser.parse_args()
    
    prompt = f"""
    A new critical CVE was just detected. Here is the data:

    - cve_id: {args.cve_id}
    - threat level: critical
    - package name: {args.package_name}
    - vulnerable version: {args.vulnerable_version}
    - patch version: {args.patch_version}
    - summary: {args.summary}

    Handle this threat end-to-end. Provide a summary at the end."""
    
    with GriptapeCloudStructure():
        agent = build_agent()
        agent.run(prompt)