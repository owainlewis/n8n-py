"""N8N Python Client."""

from n8n.client import N8NClient
from n8n.models import (
    Workflow,
    WorkflowSettings,
    Node,
    Execution,
    Credential,
    CredentialSchema,
    Tag,
    N8NError,
)
from n8n.blueprints import (
    load_blueprint,
    blueprint_to_workflow,
    create_workflow_from_blueprint,
)

__version__ = "0.1.0"

__all__ = [
    "N8NClient",
    "Workflow",
    "WorkflowSettings",
    "Node",
    "Execution",
    "Credential",
    "CredentialSchema",
    "Tag",
    "N8NError",
    "load_blueprint",
    "blueprint_to_workflow",
    "create_workflow_from_blueprint",
]
