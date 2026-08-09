# TravelPulse Weather Agent

A FastAPI-based weather agent service for the TravelPulse platform that provides intelligent weather information and insights through MCP (Model Context Protocol) integration.

## Overview

The Weather Agent is a microservice component of the TravelPulse travel planning application. It leverages AI capabilities to deliver weather-related data and insights to support travel planning decisions. The service integrates with OpenAI for intelligent chat capabilities and uses the Model Context Protocol (MCP) for tool management.

## Features

- **FastAPI Server**: Lightweight and high-performance REST API
- **MCP Integration**: Model Context Protocol support for extensible tool management
- **Weather Chat API**: Natural language weather queries and insights
- **Async Support**: Built with async/await for better concurrency
- **Database Ready**: SQLAlchemy ORM with async PostgreSQL support via asyncpg
- **Structured Logging**: Using structlog for comprehensive logging
- **Docker Support**: Pre-configured Docker and Docker Compose setup
- **Database Migrations**: Alembic support for schema versioning

## Tech Stack

- **Python 3.12+**
- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **SQLAlchemy 2.0+** - ORM
- **asyncpg** - Async PostgreSQL driver
- **Pydantic 2+** - Data validation
- **OpenAI** - AI language model integration
- **MCP 2.0+** - Model Context Protocol
- **Alembic** - Database migrations
- **Structlog** - Structured logging

## Project Structure

```
weather-agent/
├── app/
│   ├── agents/          # Agent implementations
│   ├── api/             # API route handlers
│   │   └── weather_chat.py
│   ├── clients/         # External service clients
│   ├── core/            # Core utilities and helpers
│   ├── mcp/             # MCP configuration and management
│   ├── models/          # SQLAlchemy ORM models
│   ├── schemas/         # Pydantic schemas for request/response validation
│   ├── services/        # Business logic services
│   ├── config.py        # Configuration management
│   ├── database.py      # Database connection setup
│   ├── logging.py       # Logging configuration
│   └── main.py          # FastAPI application entry point
├── tests/               # Test suite
├── Dockerfile           # Docker container definition
├── docker-compose.yml   # Multi-container orchestration
├── pyproject.toml       # Project metadata and dependencies
├── alembic.ini         # Database migration configuration
└── .gitignore          # Git ignore rules
```

## Installation

### Prerequisites

- Python 3.12 or higher
- PostgreSQL (for production/database features)
- Docker and Docker Compose (optional, for containerized deployment)

### Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd travelpulse/weather-agent
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -e .
   ```

4. **Configure environment variables:**
   Create a `.env` file in the `weather-agent` directory:
   ```
   OPENAI_API_KEY=your_openai_api_key
   OPENAI_MODEL=gpt-5
   MCP_SERVER_PATH=/path/to/mcp/server
   DATABASE_URL=postgresql+asyncpg://user:password@localhost/travelpulse_weather
   WEATHER_SERVICE_URL=http://127.0.0.1:8001
   MCP_COMMAND=python
   MCP_ARGS=-m,mcp_server
   MCP_TIMEOUT=30
   ```

5. **Run the application:**
   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`

## Docker Setup

### Build and Run with Docker Compose

```bash
docker compose up --build
```

The service will start on port 8000.

### Build Docker Image Manually

```bash
docker build -t travelpulse-weather-agent .
docker run -p 8000:8000 --env-file .env travelpulse-weather-agent
```

## API Endpoints

### Health Check
- **GET** `/` - Root endpoint, returns service status
  ```json
  {
    "service": "TravelPulse Weather Agent",
    "status": "ok"
  }
  ```

### MCP Status
- **GET** `/mcp/status` - Check MCP connection status
  ```json
  {
    "mcp_connected": true,
    "mcp_command": "python",
    "mcp_args": ["-m", "mcp_server"]
  }
  ```

### MCP Tool Execution
- **POST** `/mcp/tool` - Execute an MCP tool
  ```json
  {
    "tool": "tool_name",
    "arguments": {
      "param1": "value1"
    }
  }
  ```

### Weather Chat
- Endpoints provided by `weather_chat` router in `app/api/weather_chat.py`

## Configuration

The application uses `pydantic-settings` for configuration management. Settings are loaded from:

1. Environment variables
2. `.env` file (if present)

### Key Configuration Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | Required | OpenAI API key for LLM integration |
| `OPENAI_MODEL` | `gpt-5` | OpenAI model to use |
| `MCP_SERVER_PATH` | Required | Path to MCP server executable |
| `DATABASE_URL` | Optional | PostgreSQL connection string |
| `WEATHER_SERVICE_URL` | `http://127.0.0.1:8001` | Weather service endpoint |
| `MCP_COMMAND` | Required | Command to start MCP server |
| `MCP_ARGS` | Required | Comma-separated arguments for MCP command |
| `MCP_TIMEOUT` | Default from manager | MCP operation timeout in seconds |

## Database Migrations

### Create a New Migration

```bash
alembic revision --autogenerate -m "migration description"
```

### Run Migrations

```bash
alembic upgrade head
```

### Rollback

```bash
alembic downgrade -1
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

The project uses Python best practices. Consider setting up:
- `black` for code formatting
- `flake8` or `ruff` for linting
- `mypy` for type checking

### Logging

The application uses structured logging via `structlog`. Logs are configured in `app/logging.py`.

## Troubleshooting

### MCP Connection Issues

If you see "MCP manager is not connected":
1. Check the `MCP_COMMAND` and `MCP_ARGS` in your `.env`
2. Verify the MCP server is running
3. Check logs for connection errors

### Database Connection Issues

If experiencing database connection problems:
1. Verify `DATABASE_URL` is correctly configured
2. Ensure PostgreSQL is running
3. Check network connectivity to database host

### Port Already in Use

If port 8000 is already in use:
```bash
uvicorn app.main:app --reload --port 8001
```

## Contributing

1. Create a feature branch from `main`
2. Make your changes
3. Write or update tests
4. Submit a pull request

## License

See the main repository for license information.

## Support

For issues and questions, please refer to the main TravelPulse repository or contact the development team.
