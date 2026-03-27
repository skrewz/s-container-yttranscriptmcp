# MCP Server Skeleton

```python
#!/usr/bin/env python3
"""YouTube Transcript MCP Server"""

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from youtube_transcript_api import YouTubeTranscriptApi
import re

app = Server("youtube-transcript-mcp")


def extract_video_id(url_or_id: str) -> str:
    """Extract YouTube video ID from URL or ID."""
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url_or_id):
        return url_or_id
    pattern = r'(?:https?://)?(?:www\.)?(?:youtube\.com/(?:watch\?v=|embed/|v/)|youtu\.be/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url_or_id)
    if match:
        return match.group(1)
    raise ValueError(f"Invalid YouTube URL or ID: {url_or_id}")


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="fetch_transcript",
            description="Extract transcript from YouTube video",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "YouTube video URL or ID"
                    }
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="list_transcripts",
            description="List available transcripts and languages for a video",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "YouTube video URL or ID"
                    }
                },
                "required": ["url"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "fetch_transcript":
        video_id = extract_video_id(arguments["url"])
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        transcript = transcript_list.find_transcript(["en"]).fetch()
        full_text = " ".join(segment.text for segment in transcript)
        return [TextContent(text=full_text, type="text")]
    
    elif name == "list_transcripts":
        video_id = extract_video_id(arguments["url"])
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        langs = []
        for t in transcript_list:
            langs.append(f"{t.language_code}: {t.language}")
        return [TextContent(text="\n".join(langs), type="text")]
    
    raise ValueError(f"Unknown tool: {name}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(app.run(stdio_server()))
```
