from github_helper import trigger_workflow_dispatch
trigger_workflow_dispatch("deploy.yml", ref="master")
print("Triggered")