import os
import yaml
import subprocess
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("sandbox")

@mcp.tool()
def create_sandbox(repo='git@github.com:heng309/llm-auto.git') -> str:
    """
    Create a sandbox from github repo. Then use tool check_dependency to detect necessary dependencies.
    Args:
        path: Path to save the YAML file
        repo: Git repository URL
    """
    name = repo.rstrip(".git").split("/")[-1].lower()
    data = {
        'workspaces': [
            {
                'name': name,
                'checkouts': [
                    {
                        'path': name,
                        'repo': {
                            'git': repo
                        }
                    }
                ]
            }
        ]
    }
    
    path = os.getcwd()
    yaml_file = os.path.join(path, "resources", f"{name}.yaml")
    with open(yaml_file, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)
    
    command = f"cs sandbox create heng-{name} --from def:{yaml_file}"
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True, 
        text=True
     )
    return result

@mcp.tool()
def add_dependency(name: str="llm-auto", dependency: str="redis") -> str:
    """Add dependencies to a sandbox.
    Args:
        name: Name of the sandbox
        dependencies: Dependencies to add
    """
    path = os.getcwd()
    yaml_file = os.path.join(path, "resources", f"{name}.yaml")

    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)   
    
    data['dependencies'] = [{
            'name': dependency,
            'service_type': dependency
        }]

    with open(yaml_file, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)
    
    # Edit the sandbox with the updated YAML file
    command = f"cs sandbox edit heng-{name} --from {yaml_file}"
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True, 
        text=True
     )

    return result

@mcp.tool()
def check_dependency(name: str="llm-auto") -> str:
    """Check the dependency needed in the sandbox. Then use tool add_dependency to add dependency to the sandbox.
    Args:
        name: Name of the sandbox
    """
    commands = [
        f"cd {name}",
        f"cat pyproject.toml",
    ]
    joined_cmd = ' && '.join(commands)
    ssh_cmd = f"cs ssh -W heng-{name}/{name} '{joined_cmd}'"
    result = subprocess.run(
        ssh_cmd,
        shell=True,
        capture_output=True, 
        text=True
     )
    return result

if __name__ == "__main__":
    mcp.run(transport="stdio")