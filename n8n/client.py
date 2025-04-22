from typing import Optional, List, Dict, Any
import httpx
from pydantic import BaseModel
import json

from .models import (
    Workflow,
    Execution,
    Credential,
    Tag,
    CredentialSchema,
    Audit,
    AuditOptions,
    WorkflowList,
    ExecutionList,
    CredentialList,
    TagList,
    N8NError,
)


class N8NClient:
    """Client for interacting with the N8N API."""

    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        timeout: int = 30,
    ):
        """Initialize the N8N client.

        Args:
            base_url: The base URL of the N8N instance
            api_key: Optional API key for authentication
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self._client = httpx.Client(
            base_url=f"{self.base_url}/api/v1",
            timeout=self.timeout,
            headers=self._get_headers(),
        )

        # Initialize sub-clients
        self.workflows = WorkflowsClient(self._client)
        self.executions = ExecutionsClient(self._client)
        self.credentials = CredentialsClient(self._client)
        self.tags = TagsClient(self._client)
        self.audit = AuditClient(self._client)

        # Verify connection
        self._verify_connection()

    def _verify_connection(self) -> None:
        """Verify that the N8N instance is accessible."""
        try:
            response = self._client.get("/workflows")
            response.raise_for_status()
            print(f"N8N instance is accessible at {self.base_url}")
            print(f"Connection verified successfully")
        except httpx.HTTPError as e:
            print(f"Failed to connect to N8N instance at {self.base_url}")
            print(f"Error: {str(e)}")
            raise N8NError(f"Failed to connect to N8N instance: {str(e)}") from e

    def _get_headers(self) -> Dict[str, str]:
        """Get the headers for API requests."""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.api_key:
            headers["X-N8N-API-KEY"] = self.api_key
        return headers

    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any,
    ) -> Any:
        """Make a request to the N8N API.

        Args:
            method: HTTP method
            endpoint: API endpoint
            **kwargs: Additional arguments to pass to the request

        Returns:
            The response from the API

        Raises:
            N8NError: If the request fails
        """
        try:
            response = self._client.request(method, endpoint, **kwargs)
            if not response.is_success:
                print(f"Request URL: {response.url}")
                print(
                    f"Request Headers: {json.dumps(dict(response.request.headers), indent=2)}"
                )
                if response.request.content:
                    print(f"Request Body: {response.request.content.decode()}")
                print(f"Response Status: {response.status_code}")
                print(
                    f"Response Headers: {json.dumps(dict(response.headers), indent=2)}"
                )
                print(f"Response Body: {response.text}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise N8NError(f"API request failed: {str(e)}") from e

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self) -> "N8NClient":
        """Enter the context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the context manager."""
        self.close()


class AuditClient:
    """Client for audit-related operations."""

    def __init__(self, client: httpx.Client):
        self._client = client

    def generate(self, options: Optional[AuditOptions] = None) -> Audit:
        """Generate a security audit.

        Args:
            options: Optional audit generation options

        Returns:
            Audit results
        """
        response = self._client.post(
            "/audit", json=options.dict(exclude_none=True) if options else None
        )
        response.raise_for_status()
        return Audit.parse_obj(response.json())


class WorkflowsClient:
    """Client for workflow-related operations."""

    def __init__(self, client: httpx.Client):
        self._client = client

    def list(self, limit: int = 100, cursor: Optional[str] = None) -> WorkflowList:
        """List workflows.

        Args:
            limit: Maximum number of workflows to return
            cursor: Cursor for pagination

        Returns:
            List of workflows
        """
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor

        response = self._client.get("/workflows", params=params)
        response.raise_for_status()
        return WorkflowList.parse_obj(response.json())

    def get(self, workflow_id: str) -> Workflow:
        """Get a specific workflow.

        Args:
            workflow_id: ID of the workflow to retrieve

        Returns:
            Workflow details
        """
        response = self._client.get(f"/workflows/{workflow_id}")
        response.raise_for_status()
        return Workflow.parse_obj(response.json())

    def create(self, workflow: Workflow) -> Workflow:
        """Create a new workflow.

        Args:
            workflow: The workflow to create

        Returns:
            The created workflow
        """
        workflow_data = workflow.model_dump(exclude_none=True, exclude={"id"})
        print(f"Creating workflow with data: {json.dumps(workflow_data, indent=2)}")

        response = self._client.post(
            "/workflows",
            json=workflow_data,
        )
        if not response.is_success:
            print(f"Error response: {response.text}")
        response.raise_for_status()
        return Workflow.model_validate(response.json())

    def update(self, workflow_id: str, workflow: Workflow) -> Workflow:
        """Update an existing workflow.

        Args:
            workflow_id: ID of the workflow to update
            workflow: Updated workflow data

        Returns:
            Updated workflow
        """
        response = self._client.put(
            f"/workflows/{workflow_id}", json=workflow.dict(exclude_none=True)
        )
        response.raise_for_status()
        return Workflow.parse_obj(response.json())

    def delete(self, workflow_id: str) -> None:
        """Delete a workflow.

        Args:
            workflow_id: ID of the workflow to delete
        """
        response = self._client.delete(f"/workflows/{workflow_id}")
        response.raise_for_status()


class ExecutionsClient:
    """Client for execution-related operations."""

    def __init__(self, client: httpx.Client):
        self._client = client

    def list(
        self,
        limit: int = 100,
        cursor: Optional[str] = None,
        status: Optional[str] = None,
        workflow_id: Optional[str] = None,
        include_data: bool = False,
    ) -> ExecutionList:
        """List executions.

        Args:
            limit: Maximum number of executions to return
            cursor: Cursor for pagination
            status: Filter by execution status
            workflow_id: Filter by workflow ID
            include_data: Whether to include execution data

        Returns:
            List of executions
        """
        params = {"limit": limit, "includeData": include_data}
        if cursor:
            params["cursor"] = cursor
        if status:
            params["status"] = status
        if workflow_id:
            params["workflowId"] = workflow_id

        response = self._client.get("/executions", params=params)
        response.raise_for_status()
        return ExecutionList.parse_obj(response.json())

    def get(self, execution_id: str, include_data: bool = False) -> Execution:
        """Get a specific execution.

        Args:
            execution_id: ID of the execution to retrieve
            include_data: Whether to include execution data

        Returns:
            Execution details
        """
        response = self._client.get(
            f"/executions/{execution_id}", params={"includeData": include_data}
        )
        response.raise_for_status()
        return Execution.parse_obj(response.json())

    def delete(self, execution_id: str) -> None:
        """Delete an execution.

        Args:
            execution_id: ID of the execution to delete
        """
        response = self._client.delete(f"/executions/{execution_id}")
        response.raise_for_status()


class CredentialsClient:
    """Client for credential-related operations."""

    def __init__(self, client: httpx.Client):
        self._client = client

    def list(self, limit: int = 100, cursor: Optional[str] = None) -> CredentialList:
        """List credentials.

        Args:
            limit: Maximum number of credentials to return
            cursor: Cursor for pagination

        Returns:
            List of credentials
        """
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor

        response = self._client.get("/credentials", params=params)
        response.raise_for_status()
        return CredentialList.parse_obj(response.json())

    def create(self, credential: Credential) -> Credential:
        """Create a new credential.

        Args:
            credential: Credential to create

        Returns:
            Created credential
        """
        response = self._client.post(
            "/credentials", json=credential.dict(exclude_none=True)
        )
        response.raise_for_status()
        return Credential.parse_obj(response.json())

    def delete(self, credential_id: str) -> None:
        """Delete a credential.

        Args:
            credential_id: ID of the credential to delete
        """
        response = self._client.delete(f"/credentials/{credential_id}")
        response.raise_for_status()

    def get_schema(self, credential_type: str) -> CredentialSchema:
        """Get schema for a credential type.

        Args:
            credential_type: Type of credential to get schema for

        Returns:
            Credential schema
        """
        response = self._client.get(f"/credentials/schema/{credential_type}")
        response.raise_for_status()
        return CredentialSchema.parse_obj(response.json())


class TagsClient:
    """Client for tag-related operations."""

    def __init__(self, client: httpx.Client):
        self._client = client

    def list(self, limit: int = 100, cursor: Optional[str] = None) -> TagList:
        """List tags.

        Args:
            limit: Maximum number of tags to return
            cursor: Cursor for pagination

        Returns:
            List of tags
        """
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor

        response = self._client.get("/tags", params=params)
        response.raise_for_status()
        return TagList.parse_obj(response.json())

    def create(self, tag: Tag) -> Tag:
        """Create a new tag.

        Args:
            tag: Tag to create

        Returns:
            Created tag
        """
        response = self._client.post("/tags", json=tag.dict(exclude_none=True))
        response.raise_for_status()
        return Tag.parse_obj(response.json())

    def get(self, tag_id: str) -> Tag:
        """Get a specific tag.

        Args:
            tag_id: ID of the tag to retrieve

        Returns:
            Tag details
        """
        response = self._client.get(f"/tags/{tag_id}")
        response.raise_for_status()
        return Tag.parse_obj(response.json())

    def delete(self, tag_id: str) -> None:
        """Delete a tag.

        Args:
            tag_id: ID of the tag to delete
        """
        response = self._client.delete(f"/tags/{tag_id}")
        response.raise_for_status()
