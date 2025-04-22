# n8n-py

A Python client for the N8N API.

## Installation

```bash
pip install n8n-py
```

## Usage

```python
from n8n import N8NClient

# Initialize the client
client = N8NClient(
    base_url="http://your-n8n-instance.com",
    api_key="your-api-key"
)

# List workflows
workflows = client.workflows.list()

# Get a specific workflow
workflow = client.workflows.get(workflow_id="123")

# Create a new workflow
new_workflow = client.workflows.create(
    name="My Workflow",
    nodes=[...],
    connections={...}
)
```

## Features

- Full support for N8N API v1
- Type hints and validation using Pydantic
- Async support
- Comprehensive error handling

## Development

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
3. Run tests:
   ```bash
   pytest
   ```

## License

MIT 