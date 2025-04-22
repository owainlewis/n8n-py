"""N8N API Models."""

from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field


class Tag(BaseModel):
    """Model for N8N tags."""

    id: Optional[str] = None
    name: str
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None


class Node(BaseModel):
    """N8N Node."""

    id: str
    name: str
    type: str
    typeVersion: Union[int, float]
    position: List[float]
    parameters: Dict[str, Any] = Field(default_factory=dict)
    webhookId: Optional[str] = None
    disabled: bool = False
    notesInFlow: bool = False
    notes: Optional[str] = None
    executeOnce: bool = False
    alwaysOutputData: bool = False
    retryOnFail: bool = False
    maxTries: Optional[int] = None
    waitBetweenTries: Optional[int] = None
    continueOnFail: bool = False
    onError: Optional[str] = None
    credentials: Optional[Dict[str, Any]] = None
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None


class Connection(BaseModel):
    """Model for node connections."""

    node: str
    type: str
    index: int


class NodeConnections(BaseModel):
    """Model for node connections structure."""

    main: List[List[Connection]]


class WorkflowSettings(BaseModel):
    """N8N Workflow Settings."""

    saveExecutionProgress: bool = True
    saveManualExecutions: bool = True
    saveDataErrorExecution: str = "all"
    saveDataSuccessExecution: str = "all"
    executionTimeout: Optional[int] = None
    errorWorkflow: Optional[str] = None
    timezone: Optional[str] = None
    executionOrder: str = "v1"


class Workflow(BaseModel):
    """N8N Workflow."""

    id: Optional[str] = None
    name: str
    nodes: List[Node]
    connections: Dict[str, Dict[str, List[List[Dict[str, Any]]]]]
    settings: WorkflowSettings = Field(default_factory=WorkflowSettings)
    staticData: Dict[str, Any] = Field(default_factory=dict)
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None


class Execution(BaseModel):
    """N8N Execution."""

    id: int
    data: Optional[Dict[str, Any]] = None
    finished: bool = False
    mode: str
    retryOf: Optional[int] = None
    retrySuccessId: Optional[int] = None
    startedAt: Optional[str] = None
    stoppedAt: Optional[str] = None
    workflowId: int
    waitTill: Optional[str] = None
    customData: Optional[Dict[str, Any]] = None


class Credential(BaseModel):
    """N8N Credential."""

    id: Optional[str] = None
    name: str
    type: str
    data: Dict[str, Any]
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None


class CredentialSchema(BaseModel):
    """N8N Credential Schema."""

    additionalProperties: bool = False
    type: str = "object"
    properties: Dict[str, Any]
    required: List[str]


class AuditOptions(BaseModel):
    """N8N Audit Options."""

    additionalOptions: Optional[Dict[str, Any]] = None


class Audit(BaseModel):
    """N8N Audit."""

    credentials: Optional[Dict[str, Any]] = None
    database: Optional[Dict[str, Any]] = None
    filesystem: Optional[Dict[str, Any]] = None
    nodes: Optional[Dict[str, Any]] = None
    instance: Optional[Dict[str, Any]] = None


class PaginatedResponse(BaseModel):
    """Base model for paginated responses."""

    data: List[Any]
    nextCursor: Optional[str] = None


class WorkflowList(BaseModel):
    """N8N Workflow List."""

    data: List[Workflow]
    nextCursor: Optional[str] = None


class ExecutionList(BaseModel):
    """N8N Execution List."""

    data: List[Execution]
    nextCursor: Optional[str] = None


class CredentialList(BaseModel):
    """N8N Credential List."""

    data: List[Credential]
    nextCursor: Optional[str] = None


class TagList(BaseModel):
    """N8N Tag List."""

    data: List[Tag]
    nextCursor: Optional[str] = None


class N8NError(Exception):
    """Base exception for N8N API errors."""

    def __init__(self, message: str):
        """Initialize the error.

        Args:
            message: Error message
        """
        self.message = message
        super().__init__(self.message)
