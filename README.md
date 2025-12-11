# Claude MCP - Trigger GitHub Actions

This repository demonstrates a complete DevOps workflow using an MCP server combined with an AI assistant (e.g., Claude Desktop).
It showcases how to:

* Deploy a simple Flask website (John Cena’s retirement demo)
* Configure a GitHub Actions workflow to deploy the site
* Build a local MCP server tool to trigger the GitHub workflow
* Integrate with Claude Desktop to trigger deployments via chat 

Live demo: [https://github-action-mcp-server.fly.dev/](https://github-action-mcp-server.fly.dev/)

<img width="948" height="256" alt="image" src="https://github.com/user-attachments/assets/eaf81fd4-d019-4f13-9290-4a16d624029e" />

---

## Project Structure

* `app.py` – Main Flask application
* `templates/index.html` – HTML template for the static website
* `requirements.txt` – Python dependencies
* `.github/workflows/deploy.yml` – GitHub Actions workflow for deployment
* `.env` – Environment variables for GitHub and Fly.io
* `github_helper.py` – Python helper to trigger GitHub workflow
* `mcp_server.py` – MCP server exposing `trigger_deploy` tool

---

## 🛠 Prerequisites

* Python 3.10+
* Virtual environment (`venv`)
* Git
* GitHub repository
* Fly.io account & Fly CLI
* Claude Desktop (optional, for AI interaction)

---

## Setup Instructions

1. **Clone the repo**

   ```bash
   git clone <repo-url>
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**

   * `pip install -r requirements.txt`
   * `pip install python-dotenv requests`

4. **Configure environment variables** in `.env`

   ```
   GITHUB_TOKEN=your_token
   GITHUB_OWNER=your_username
   GITHUB_REPO=repo_name
   GITHUB_WORKFLOW_FILENAME=deploy.yml
   GITHUB_BRANCH=master
   FLY_API_TOKEN=your_fly_api_token
   ```

5. **Run the MCP server locally**

   ```bash
   python mcp_server.py
   ```

---

## 📦 Deploy Workflow

* GitHub Actions workflow is defined in `.github/workflows/deploy.yml`
* Can be triggered manually via GitHub UI or via MCP server tool `trigger_deploy`
* Deploys the Flask app to Fly.io

---

## Using Claude Desktop

1. Add MCP server configuration pointing to `mcp_server.py`
2. Ask Claude Desktop:

   ```
   Trigger the deploy workflow
   ```
3. MCP server triggers the GitHub Actions workflow

---

## Testing

* Push your code to GitHub (`git add .`, `git commit`, `git push`)
* Verify the workflow run in the **Actions** tab
* App should be live at your Fly.io URL

---

## Notes

* `.env` changes should **not** be committed
* Ensure `workflow_dispatch` is defined in the workflow file for manual/API triggers

---
