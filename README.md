# Launch Engine

A powerful and flexible engine for launching and managing AI agents, workflows, and automated tasks.

## Features

- **Modular Design**: Easily extendable with plugins and modules
- **Agent Orchestration**: Manage multiple AI agents with different roles and capabilities
- **Workflow Automation**: Create complex workflows with conditional logic and dependencies
- **Integration Ready**: Built-in support for various APIs and services
- **Configuration Driven**: Configure everything via YAML or Python
- **Monitoring & Logging**: Comprehensive logging and monitoring capabilities
- **CLI Interface**: Command-line interface for easy interaction
- **Testing Framework**: Built-in testing utilities for reliable development

## Installation

```bash
pip install launch-engine
```

For development installation:

```bash
git clone https://github.com/your-org/launch-engine.git
cd launch-engine
pip install -e .
```

## Quick Start

### Basic Usage

```python
from launch_engine import Engine

# Initialize the engine
engine = Engine()

# Add a simple agent
engine.add_agent(
    name="assistant",
    role="helpful assistant",
    model="gpt-3.5-turbo"
)

# Run a task
result = engine.run_task(
    agent="assistant",
    prompt="What is the capital of France?"
)

print(result)
```

### CLI Usage

```bash
# Start the engine
launch-engine start

# Run a specific task
launch-engine run --agent assistant --prompt "Hello, world!"
```

## Architecture

Launch Engine follows a modular architecture consisting of:

- **Core Engine**: The central coordinator that manages agents, workflows, and execution
- **Agent System**: Handles creation, configuration, and management of AI agents
- **Workflow Engine**: Manages workflow definition, execution, and monitoring
- **Plugin System**: Allows extension of functionality through plugins
- **Configuration Layer**: Handles loading and validation of configuration
- **Storage Layer**: Provides persistence for state, logs, and results
- **Interface Layer**: Includes CLI, API, and other interaction methods

### Key Components

1. **Engine**: Main entry point and coordinator
2. **Agent**: Individual AI agents with specific roles and capabilities
3. **Workflow**: Defines sequences of tasks and their dependencies
4. **Task**: Individual units of work to be executed
5. **Plugin**: Extends functionality without modifying core code
6. **Storage**: Handles data persistence and retrieval

## API Reference

### Engine Class

```python
class Engine:
    def __init__(self, config=None):
        """Initialize the engine with optional configuration."""
    
    def add_agent(self, name, role, model, **kwargs):
        """Add a new agent to the engine."""
    
    def remove_agent(self, name):
        """Remove an agent from the engine."""
    
    def run_task(self, agent, prompt, **kwargs):
        """Run a task using the specified agent."""
    
    def create_workflow(self, name, tasks):
        """Create a new workflow."""
    
    def run_workflow(self, name, initial_data=None):
        """Execute a workflow."""
```

### Agent Class

```python
class Agent:
    def __init__(self, name, role, model, **kwargs):
        """Initialize an agent."""
    
    def execute(self, prompt, **kwargs):
        """Execute a prompt with the agent."""
    
    def update_config(self, **kwargs):
        """Update agent configuration."""
```

### Workflow Class

```python
class Workflow:
    def __init__(self, name, tasks):
        """Initialize a workflow."""
    
    def add_task(self, task, dependencies=None):
        """Add a task to the workflow."""
    
    def execute(self, initial_data=None):
        """Execute the workflow."""
```

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/launch-engine.git
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
5. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```
6. Run tests:
   ```bash
   pytest
   ```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to all contributors who have helped shape Launch Engine
- Inspired by various AI orchestration frameworks
- Built with ❤️ using Python and the latest AI technologies