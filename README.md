# MCP JustWatch Server

A Model Context Protocol (MCP) server built to provide access to JustWatch streaming availability data. Search for movies and TV shows and find out where they are available to stream across different platforms and countries.

## Features

- **Search Content**: Search for movies and TV shows by title with detailed metadata
- **Streaming Availability**: Get comprehensive information about where content is available to stream
- **Multi-Country Support**: Query streaming availability across multiple countries simultaneously
- **Detailed Information**: Access IMDb/TMDb scores, genres, runtime, release dates, and more
- **Offer Details**: Get pricing, quality (HD/4K), and direct URLs to streaming platforms
- **Remote HTTP Mode**: Run the server in FastMCP HTTP mode for reverse-proxied HTTPS deployment
- **Health Check**: Expose `/health` for service managers and reverse proxies in HTTP mode

## Technology Stack

This server is built using:
- **[FastMCP](https://github.com/jlowin/fastmcp)**: A modern, decorator-based framework for building MCP servers with minimal boilerplate
- **[simple-justwatch-python-api](https://github.com/Electronic-Mango/simple-justwatch-python-api)**: GraphQL-based wrapper for the JustWatch API

## Installation

### Prerequisites

- Python 3.11 or higher
- pip or uv package manager

### From Release

Skip to the MCP host configuration section to automatically download the package inside supported MCP clients.

### From Source

1. Clone the repository:
```bash
git clone <repository-url>
cd mcp-justwatch
```

2. Install the package:
```bash
pip install -e .
```

### For Development

Install with development dependencies:
```bash
pip install -e ".[dev]"
```

## Usage

### Local stdio mode

The default runtime mode is stdio, which is suitable for local MCP host integrations:

```bash
python -m mcp_justwatch.server
```

### MCP host configuration

This server is designed to be used with MCP clients. Add it to your MCP client configuration.

#### Claude Desktop configuration

Add to your `claude_desktop_config.json` to automatically download the package at the start of the session using `uvx`.

```json
{
  "mcpServers": {
    "justwatch": {
      "command": "uvx",
      "args": ["mcp-justwatch", "python", "-m", "mcp_justwatch.server"]
    }
  }
}
```

Or if installed in a virtual environment:

```json
{
  "mcpServers": {
    "justwatch": {
      "command": "/path/to/venv/bin/python",
      "args": ["-m", "mcp_justwatch.server"]
    }
  }
}
```

#### Other MCP hosts

See the `mcphost-config.yaml` example file for configuration with other MCP hosts.

## Remote HTTP mode

This fork also supports FastMCP HTTP transport for secure reverse-proxied deployments.

### Environment variables

- `MCP_JUSTWATCH_TRANSPORT`: `stdio` or `http` (default: `stdio`)
- `MCP_JUSTWATCH_HOST`: bind host for HTTP mode (default: `127.0.0.1`)
- `MCP_JUSTWATCH_PORT`: bind port for HTTP mode (default: `8000`)
- `MCP_JUSTWATCH_LOG_LEVEL`: logging level (default: `INFO`)
- `MCP_JUSTWATCH_LOG_FILE`: optional log file path; leave unset for stream logging suitable for journald

### Run in HTTP mode

```bash
env \
  MCP_JUSTWATCH_TRANSPORT=http \
  MCP_JUSTWATCH_HOST=127.0.0.1 \
  MCP_JUSTWATCH_PORT=8000 \
  python -m mcp_justwatch.server
```

### HTTP endpoints

When running in HTTP mode:
- MCP endpoint: `http://127.0.0.1:8000/mcp`
- Health endpoint: `http://127.0.0.1:8000/health`

The MCP endpoint is a protocol endpoint and is not meant to behave like a normal browser page.

## Secure deployment guidance

Recommended deployment shape for Perplexity remote connectors and similar remote MCP clients:
- run the Python process on loopback only
- reverse proxy through Nginx
- terminate TLS at Nginx
- expose only ports 80 and 443 publicly
- optionally enforce API-key auth at the reverse proxy

See:
- `docs/design/2026-04-28-nixos-25.11-deployment.md`
- `docs/design/2026-04-28-perplexity-connector-setup.md`
- `docs/design/examples/nixos-25.11-configuration.nix`
- `docs/design/examples/nginx-api-key-snippet.conf`

## Perplexity remote connector target

For Perplexity custom remote connectors, the intended target shape is:
- public HTTPS URL
- FastMCP HTTP transport behind reverse proxy
- MCP endpoint published at `/mcp`
- optional API-key auth at the proxy layer

## Development

### Running tests

```bash
pytest -q
```

### Code formatting

Format code with Black:
```bash
black src tests
```

Lint with Ruff:
```bash
ruff check src tests
```

## Contributing

Contributions are welcome. Please feel free to submit a Pull Request.

## Disclaimer

This project uses the [simple-justwatch-python-api](https://github.com/Electronic-Mango/simple-justwatch-python-api), an unofficial JustWatch API wrapper. This API is in no way affiliated, associated, authorized, endorsed by, or in any way officially connected with JustWatch. This is an independent and unofficial project. Use at your own risk and discretion.
