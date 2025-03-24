# SPDX-FileCopyrightText: 2025-present nolleh <nolleh7707@gmail.com>
#
# SPDX-License-Identifier: MIT

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from mcp.server import Server
import mcp.server.stdio
from mcp.server.models import InitializationOptions
from mcp.server.lowlevel.server import NotificationOptions
from mcp.types import Tool


@asynccontextmanager
async def server_lifespan(server: Server) -> AsyncIterator[str]:
    try:
        ## this is just example. actually code,
        ## use yield with consuming resource, like db connection
        yield server.name
    finally:
        pass


server = Server("weather", lifespan=server_lifespan)


@server.list_tools()
async def list_tools() -> list[Tool]:
    tools = []
    ctx = server.request_context.lifespan_context

    if ctx and "weather":
        tools.extend(
            [
                Tool(
                    name="get_weather",
                    description="Get the weather",
                    inputSchema={
                        "type": "object",
                        "properties": {"state": {"type": "string"}},
                    },
                )
            ]
        )
    return tools


async def run():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="weather",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


def main():
    print("server is running...")
    import asyncio

    asyncio.run(run())


if __name__ == "__main__":
    main()
