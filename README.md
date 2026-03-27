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

The server will be available at `http://localhost:9042/mcp`

Feel free to hit it with `make test` at this stage.

Or use the MCP Inspector:
```bash
npx -y @modelcontextprotocol/inspector http://localhost:9042/mcp
```

## Tools

The server exposes two tools:

- `fetch_transcript`
- `list_transcripts`
