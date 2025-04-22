"""Test workflow blueprints."""

import os
import pytest
from n8n import N8NClient
from n8n.blueprints import (
    load_blueprint,
    blueprint_to_workflow,
    create_workflow_from_blueprint,
)


def test_load_blueprint():
    """Test loading a blueprint from a JSON file."""
    blueprint = load_blueprint("tests/blueprints/simple.json")

    assert blueprint["name"] == "My workflow"
    assert len(blueprint["nodes"]) == 2
    assert blueprint["nodes"][0]["type"] == "n8n-nodes-base.manualTrigger"
    assert blueprint["nodes"][1]["type"] == "n8n-nodes-base.executeCommand"


def test_blueprint_to_workflow():
    """Test converting a blueprint to a workflow model."""
    blueprint = load_blueprint("tests/blueprints/simple.json")
    workflow = blueprint_to_workflow(blueprint)

    assert workflow.name == "My workflow"
    assert len(workflow.nodes) == 2
    assert workflow.nodes[0].type == "n8n-nodes-base.manualTrigger"
    assert workflow.nodes[1].type == "n8n-nodes-base.executeCommand"
    assert workflow.connections == blueprint["connections"]


def test_create_workflow_from_blueprint():
    """Test creating a workflow from a blueprint file."""
    api_key = os.getenv("N8N_API_KEY")
    if not api_key:
        pytest.skip("N8N_API_KEY environment variable is not set")

    client = N8NClient("http://localhost:5678", api_key)

    # Create workflow from blueprint
    workflow = create_workflow_from_blueprint(
        client, "tests/blueprints/simple.json", name="Test Blueprint Workflow"
    )

    assert workflow.name == "Test Blueprint Workflow"
    assert len(workflow.nodes) == 2

    # Clean up
    client.workflows.delete(workflow.id)
