"""Simple test for N8N client."""

import os
import pytest
from n8n import N8NClient
from n8n.models import Node, Workflow, WorkflowSettings


def test_create_and_delete_workflow():
    """Test creating and deleting a workflow."""
    api_key = os.getenv("N8N_API_KEY")
    if not api_key:
        pytest.skip("N8N_API_KEY environment variable is not set")

    client = N8NClient("http://localhost:5678", api_key)

    # Create a simple workflow with just a webhook trigger
    workflow = Workflow(
        name="Test Workflow",
        nodes=[
            Node(
                id="1",
                name="Webhook",
                type="n8n-nodes-base.webhook",
                typeVersion=1,
                position=[250, 300],
                parameters={
                    "path": "test-webhook",
                    "options": {
                        "responseMode": "lastNode",
                        "responseData": "firstEntryJson",
                        "responseHeaders": {},
                        "responseStatusCode": 200,
                    },
                    "authentication": "none",
                    "httpMethod": "GET",
                },
            ),
        ],
        connections={},
        settings=WorkflowSettings(),
        staticData={},
        tags=[],
    )

    # Create the workflow
    created_workflow = client.workflows.create(workflow)
    assert created_workflow.id is not None
    assert created_workflow.name == "Test Workflow"

    # Delete the workflow
    # client.workflows.delete(created_workflow.id)
