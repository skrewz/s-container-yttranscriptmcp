# YouTube Transcript MCP Server

A stateless MCP server exposing YouTube transcript extraction capabilities via HTTP/SSE transport.

## Quick Start

### Build and Run with Podman

```bash
# Build the container
make build

# Run the server
make run
```

The server will be available at `http://localhost:8000`

### Using with MCP Clients

Connect to the server:
```bash
claude mcp add --transport http youtube-transcript http://localhost:8000/mcp
```

Or use the MCP Inspector:
```bash
npx -y @modelcontextprotocol/inspector http://localhost:8000/mcp
```

## Tools

The server exposes two tools:

### `fetch_transcript`
Extract the full English transcript from a YouTube video.

**Input:**
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

### `list_transcripts`
List all available transcript languages for a video.

**Input:**
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

## Makefile Targets

| Target | Description |
|--------|-------------|
| `make build` | Build the container image |
| `make run` | Build and run the container |
| `make stop` | Stop the running container |
| `make clean` | Stop and remove container and image |
| `make logs` | Follow container logs |
| `make inspect` | Inspect the image |

## Architecture

- **Python 3.13** slim base image
- **Streamable HTTP transport** (SSE) via official `mcp` SDK
- **Stateless** - no persistent storage, transcripts processed in-memory
- **Non-root user** for security
- **Multi-stage build** for smaller image size

## Container Details

- **Image**: `youtube-transcript-mcp`
- **Port**: 8000 (HTTP/SSE)
- **User**: mcp (non-root)
- **Entrypoint**: `python mcp_server.py`

## Development

Run locally for development:
```bash
pip install mcp youtube-transcript-api
python src/mcp_server.py
```

Then connect to `http://localhost:8000/mcp`.
