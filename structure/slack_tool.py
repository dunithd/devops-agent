import time
from schema import Literal, Optional, Schema

from griptape.artifacts import TextArtifact
from griptape.artifacts.list_artifact import ListArtifact
from griptape.tools import BaseTool
from griptape.utils.decorators import activity
import json
import psycopg2
import logging

class SlackTool(BaseTool):
    @activity(
        config={
            "description": "Sends a Slack alert to #operations about hosts that require manual patching.",
            "schema": Schema(
                {
                    Literal("hosts_to_notify", description="List of hostnames that require manual patching"): [str],
                    Literal("cve_id", description="CVE Identifier"): str,
                }
            )
        }
    )
    def notify_slack(self, cve_id: str, hosts_to_notify: list) -> TextArtifact:
        """Sends a Slack alert to #operations about hosts that require manual patching. Returns a JSON response indicating the success 
        of the operation.

        Args:
            cve_id (str): CVE Identifier
            hosts_to_notify (str): List of hostnames 

        Returns:
            TextArtifact: The patch operation result as a Text Artifact.
        """
        print(f"\n[Tool Call] (Slack) Sending notification to #operations:")
        message = f"ATTN: {cve_id} detected.\nThe following {len(hosts_to_notify)} PROD servers require manual patching:\n"
        message += "\n".join([f"  - {host}" for host in hosts_to_notify])
        print("  " + "*"*50)
        print(message)
        print("  " + "*"*50)

        return self.write_messages_to_db(message)
    
    def write_messages_to_db(self, message: str) -> TextArtifact:
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        try:
            conn = psycopg2.connect(
                dbname="workshop",
                user="edb_admin",
                password="Spr!ng20232025",
                host="p-hjctr79xu3-a-rw-external-ea91f117847d15d5.elb.eu-west-2.amazonaws.com",
                port="5432"
            )
            logger.info("Database connection established.")
            cur = conn.cursor()
            try:
                cur.execute(
                    "INSERT INTO slack.messages (user_id, channel_id, message_text) VALUES (%s, %s, %s)",
                    ("DEVOPS_AGENT","operations", message)
                )
                conn.commit()
                logger.info("Message inserted into database.")
            except Exception as e:
                logger.error(f"Error executing insert query: {e}")
            finally:
                cur.close()
                logger.info("Database cursor closed.")
            conn.close()
            logger.info("Database connection closed.")
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
        
        return TextArtifact(json.dumps({"status": "Slack message sent"}))

def init_tool() -> SlackTool:
    return SlackTool()