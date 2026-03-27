#!/usr/bin/env python3
"""Invoke YT Transcript MCP tools."""

import argparse
import asyncio
from fastmcp import Client


async def invoke(url: str) -> None:
    async with Client("http://127.0.0.1:9042/mcp") as client:
        tools = await client.list_tools()
        print("Available tools:")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description[:80]}...")
        print()

        result = await client.call_tool("fetch_transcript", {"url": url})
        text = result.content[0].text
        print(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Invoke YT Transcript MCP server")
    parser.add_argument("url", help="YouTube video URL or video ID")
    args = parser.parse_args()
    asyncio.run(invoke(args.url))


if __name__ == "__main__":
    main()
