# YouTube Transcript Summarizer MCP

A Python tool that extracts transcripts from YouTube videos using the `youtube-transcript-api` library, with plans for MCP integration.

## Usage

```bash
uv run --with youtube-transcript-api python youtube_transcript.py
```

## Requirements

- Python 3.10+
- `youtube-transcript-api` library

## What it does

This tool:
1. Extracts video ID from YouTube URLs
2. Fetches transcripts (including auto-generated)
3. Outputs the full transcript text
4. Saves to `transcript.txt`

---

## Extending to MCP (Model Context Protocol)

### Current Approach vs MCP

**Current**: CLI tool requiring direct execution
**MCP**: Server exposing capabilities as structured tools/context

### What's Required for MCP Extension

#### 1. **MCP Server Implementation**

Choose one of:
- **Python**: Use [`mcp-server-python`](https://github.com/modelcontextprotocol/python-sdk)
- **Node.js**: Use [`mcp-server-node`](https://github.com/modelcontextprotocol/node-sdk)

Example Python skeleton:
```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
from pydantic import BaseModel

server = Server("youtube-transcript")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="fetch_youtube_transcript",
            description="Extract transcript from YouTube video",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "YouTube URL or video ID"}
                },
                "required": ["url"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "fetch_youtube_transcript":
        transcript = get_transcript(arguments["url"])
        return [TextContent(text=full_transcript_text)]
```

#### 2. **Structured Output Format**

Consider returning:
- Full transcript text
- Summarized version (with LLM)
- Timestamped segments for navigation
- Available languages/captions

#### 3. **Error Handling**

MCP tools should handle:
- Invalid URLs
- Videos without transcripts
- Rate limiting / IP blocking
- Transcripts disabled

Return proper error messages in MCP format.

#### 4. **Optional Enhancements**

| Feature | Effort | Value |
|---------|--------|-------|
| **Transcript summarization** | Low | Medium - Use LLM to condense |
| **Multiple language support** | Low | Medium - Auto-detect or specify |
| **Chunked output** | Medium | High - For long videos |
| **Search within transcript** | Medium | High - Find specific topics |
| **Audio download** | Medium | Low - Separate concern |
| **Batch processing** | High | Medium - Multiple URLs |

#### 5. **Configuration**

MCP servers often need configuration:
```json
{
  "youtube": {
    "default_language": "en",
    "max_retries": 3,
    "timeout_seconds": 30
  }
}
```

#### 6. **Server Transport**

Choose transport method:
- **STDIO** (simplest): `mcp-server-youtube` via CLI
- **HTTP**: WebSocket or SSE for remote access
- **SSE**: Server-Sent Events for streaming

### Development Roadmap

1. **MVP**: Basic MCP server with `fetch_transcript` tool
2. **Phase 2**: Add summarization endpoint (integrate with LLM)
3. **Phase 3**: Add metadata extraction (title, author, duration)
4. **Phase 4**: Add search/navigate within transcript

### Testing

```bash
# Test MCP server with model context protocol client
npx @modelcontextprotocol/inspector uv run mcp_server.py
```

### Deployment

Options:
- **Local**: Run MCP server alongside LLM IDE/assistant
- **Remote**: Host as HTTP server, connect via URL
- **Container**: Docker image with embedded MCP server
