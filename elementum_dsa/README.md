# Elementum DSA Package

This directory contains the main package code for the Elementum DSA framework.

## Structure

- `cli.py` - Command-line interface for the framework
- `__init__.py` - Package initialization

## Usage

The Elementum DSA framework is designed to be used as a Python package. You can import components directly:

```python
from core.mca import MasterControlAgent
from examples.powerpoint.powerpoint_agent import PowerPointAgent

# Create and initialize the Master Control Agent
mca = MasterControlAgent()

# Register an agent
mca.register_agent(PowerPointAgent())

# Process a query
response = mca.process_query(
    "Generate presentation structure for technical overview", 
    domain="presentation_development"
)
```

You can also use the command-line interface:

```bash
# Process a single query
elementum-dsa --query "Generate presentation structure for technical overview" --domain "presentation_development"

# Process queries from a file
elementum-dsa --query-file example_queries.json --output-file responses.json

# List available agents
elementum-dsa --list-agents
```
