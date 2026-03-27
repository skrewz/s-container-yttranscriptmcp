#!/usr/bin/env python3
"""YT Transcript MCP Server with HTTP/SSE transport"""

from mcp.server.fastmcp import FastMCP
from youtube_transcript_api import YouTubeTranscriptApi
import os
import re

mcp = FastMCP(
    name="YouTube Transcript MCP",
    instructions="Extract transcripts from YouTube videos",
    host="0.0.0.0",
    port=int(os.environ.get("YTTRANSCRIPTMCP_PORT", "9042")),
)


def extract_video_id(url_or_id: str) -> str:
    """Extract YouTube video ID from URL or ID."""
    if re.match(r"^[a-zA-Z0-9_-]{11}$", url_or_id):
        return url_or_id
    pattern = r"(?:https?://)?(?:www\.)?(?:youtube\.com/(?:watch\?v=|embed/|v/)|youtu\.be/)([a-zA-Z0-9_-]{11})"
    match = re.search(pattern, url_or_id)
    if match:
        return match.group(1)
    raise ValueError(f"Invalid YouTube URL or ID: {url_or_id}")


@mcp.tool()
def fetch_transcript(url: str) -> str:
    """Extract full transcript from YouTube video.

    Args:
        url: YouTube video URL or video ID

    Returns:
        Full transcript text with all segments concatenated
    """
    video_id = extract_video_id(url)
    transcript_list = YouTubeTranscriptApi().list(video_id)
    transcript = transcript_list.find_transcript(["en"])
    segments = transcript.fetch()
    full_text = " ".join(segment.text for segment in segments)
    return full_text


@mcp.tool()
def list_transcripts(url: str) -> str:
    """List available transcript languages for a YouTube video.

    Args:
        url: YouTube video URL or video ID

    Returns:
        Newline-separated list of available languages
    """
    video_id = extract_video_id(url)
    transcript_list = YouTubeTranscriptApi().list(video_id)
    langs = []
    for trans in transcript_list:
        langs.append(f"{trans.language_code}: {trans.language}")
    return "\n".join(langs)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
