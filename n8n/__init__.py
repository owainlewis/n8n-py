"""N8N Python Client."""

from .client import N8NClient, N8NError
from .models import (
    Workflow,
    Execution,
    Credential,
    Tag,
    Node,
    Connection,
    CredentialSchema,
    Audit,
    AuditOptions,
    WorkflowList,
    ExecutionList,
    CredentialList,
    TagList,
)

__version__ = "0.1.0"

__all__ = [
    "N8NClient",
    "N8NError",
    "Workflow",
    "Execution",
    "Credential",
    "Tag",
    "Node",
    "Connection",
    "CredentialSchema",
    "Audit",
    "AuditOptions",
    "WorkflowList",
    "ExecutionList",
    "CredentialList",
    "TagList",
]
