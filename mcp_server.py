# mcp_server.py
import os
import logging
from mcp.server.fastmcp import FastMCP
from github_helper import trigger_workflow_dispatch

# Create MCP instance. Name the toolset whatever you'd like.
mcp = FastMCP("deploy_tools")

# Simple custom MCP error type that tools will raise
class MCPError(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("mcp_server")

# Defaults from env (override when calling)
DEFAULT_WORKFLOW = os.environ.get("GITHUB_WORKFLOW_FILENAME", "deploy.yml")
DEFAULT_BRANCH = os.environ.get("GITHUB_BRANCH", "master")

# ---- Tools ----

@mcp.tool()
def trigger_deploy(workflow_filename: str = None, branch: str = None, actor: str = None) -> dict:
    """
    Trigger the GitHub Actions workflow specified by workflow_filename on branch.
    Returns a dict with status and message.
    Example arguments:
      - workflow_filename: 'deploy.yml' (or the filename in .github/workflows)
      - branch: 'main'
      - actor: optional string describing who triggered (stored as input)
    """
    wf = workflow_filename or DEFAULT_WORKFLOW
    br = branch or DEFAULT_BRANCH
    trigger_inputs = {"triggered_by": actor} if actor else None

    logger.info("Trigger request received: workflow=%s branch=%s actor=%s", wf, br, actor)

    try:
        trigger_workflow_dispatch(wf, ref=br, inputs=trigger_inputs)
        logger.info("Triggered workflow %s on %s", wf, br)
        return {"ok": True, "message": f"Workflow {wf} dispatched on {br}"}
    except Exception as e:
        logger.exception("Failed to trigger workflow")
        # Map to MCPError so clients can see code + message
        raise MCPError(500, f"Failed to trigger workflow: {e}")

# ---- Main ----
if __name__ == "__main__":
    # run using stdio transport so Claude Desktop can launch it as an MCP server
    mcp.run(transport="stdio")