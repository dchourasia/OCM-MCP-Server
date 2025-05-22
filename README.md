# OCM-MCP-Server

Server implementation for OCM (OpenShift Cluster Manager) and MCP (Managed Control Plane) integration.

## Overview

This project provides a server implementation to facilitate integration between OpenShift Cluster Manager (OCM) and Managed Control Plane (MCP). It handles the communication, data synchronization, and management operations between these two systems.

## Features

- OCM Integration
- MCP Integration
- API Endpoints
- Authentication & Authorization
- Data Synchronization
- Monitoring & Logging

## Prerequisites

- Python 3.9+
- pip
- virtualenv (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/dchourasia/OCM-MCP-Server.git
cd OCM-MCP-Server
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
OCM-MCP-Server/
│
├── src/                    # Source code
│   ├── api/               # API endpoints
│   ├── core/              # Core business logic
│   ├── models/            # Data models
│   └── utils/             # Utility functions
│
├── tests/                 # Test files
│   ├── unit/             # Unit tests
│   └── integration/      # Integration tests
│
├── docs/                  # Documentation
│
├── config/               # Configuration files
│
├── requirements.txt      # Project dependencies
├── requirements-dev.txt  # Development dependencies
├── setup.py             # Package setup file
└── README.md            # This file
```

## Configuration

1. Copy the example configuration file:
```bash
cp config/config.example.yaml config/config.yaml
```

2. Update the configuration with your settings:
```yaml
ocm:
  api_url: "https://api.openshift.com"
  token: "your-token"

mcp:
  api_url: "https://your-mcp-instance"
  credentials:
    username: "your-username"
    password: "your-password"

server:
  host: "0.0.0.0"
  port: 8000
  debug: false
```

## Usage

1. Start the server:
```bash
python src/main.py
```

2. Access the API documentation:
```
http://localhost:8000/docs
```

## Development

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Run tests:
```bash
pytest
```

3. Run linting:
```bash
flake8 src tests
```

4. Run type checking:
```bash
mypy src
```

## API Documentation

The API documentation is available at `/docs` when the server is running. It includes:

- Available endpoints
- Request/response formats
- Authentication requirements
- Example requests

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Support

For support, please:
1. Check the [documentation](docs/)
2. Open an issue
3. Contact the maintainers

## Maintainers

- Deepak Chourasia (@dchourasia)