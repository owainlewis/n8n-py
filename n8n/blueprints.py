"""N8N Workflow Blueprints."""

import json
from pathlib import Path
from typing import Dict, Any, Optional

from n8n.models import Workflow, Node, WorkflowSettings
from n8n.client import N8NClient


def load_blueprint(file_path: str) -> Dict[str, Any]:
    """Load a workflow blueprint from a JSON file.

    Args:
        file_path: Path to the JSON blueprint file

    Returns:
        Dict containing the workflow data
    """
    with open(file_path, "r") as f:
        return json.load(f)


def blueprint_to_workflow(blueprint: Dict[str, Any]) -> Workflow:
    """Convert a blueprint dictionary to a Workflow model.

    Args:
        blueprint: Dictionary containing workflow blueprint data

    Returns:
        Workflow model instance
    """
    # Extract nodes and convert to Node models
    nodes = []
    for node_data in blueprint["nodes"]:
        node = Node(
            id=node_data["id"],
            name=node_data["name"],
            type=node_data["type"],
            typeVersion=node_data["typeVersion"],
            position=node_data["position"],
            parameters=node_data.get("parameters", {}),
        )
        nodes.append(node)

    # Create workflow settings
    settings = WorkflowSettings(
        executionOrder=blueprint["settings"].get("executionOrder", "v1")
    )

    # Create and return workflow
    return Workflow(
        name=blueprint["name"],
        nodes=nodes,
        connections=blueprint["connections"],
        settings=settings,
        staticData=blueprint.get("staticData", {}),
    )


def create_workflow_from_blueprint(
    client: N8NClient, file_path: str, name: Optional[str] = None
) -> Workflow:
    """Create a workflow from a blueprint file.

    Args:
        client: N8NClient instance
        file_path: Path to the JSON blueprint file
        name: Optional name to override the blueprint name

    Returns:
        Created Workflow instance
    """
    # Load blueprint
    blueprint = load_blueprint(file_path)

    # Convert to workflow model
    workflow = blueprint_to_workflow(blueprint)

    # Override name if provided
    if name:
        workflow.name = name

    # Create workflow
    return client.workflows.create(workflow)
