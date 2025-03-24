# MCP Weather Server Test Guide

## Overview

This document provides a detailed guide for testing the MCP Weather Server.

## Test Environment Setup

1. Install and Run MCP Inspector
   ```bash
   npx @model_context_protocol/inspector
   Starting MCP inspector...
   Proxy server listening on port 3000
   🔍 MCP Inspector is up and running at http://localhost:5173 🚀
   ```

2. Access Inspector in Browser
- Navigate to http://localhost:5173
- Connection Type: STDIO
- Command: `uv, --directory path/to/kickstart-mcp/mcp-weather run mcp-weather`
- Click Connect button

## Test Scenarios

### 1. Verify Tool List
- Check the available tools list in the Inspector's Tools tab
- The `get_weather` tool should be visible in the list

### 2. Test Tool Invocation
1. Select the `get_weather` tool
2. In the Parameters section:
- Enter state: "Seoul"
3. Click Call button
4. Verify Response
- Expected response: "Hello Seoul"

## Description
1. If you followed the tutorials well, then you can connect and see the get the list tools like this.
![](./image/tools.png)
- As you can see, tool has the name / description that we've set, and received state parameter as string, as we defined.
- When click ListTools or RunTools, It send RPC message to our server.

![](./image/list_rpc.png)


2. When MCPHost (inspector) queried list,
```json
{
    "method": "tools/list",
    "params": {}
}
```

Our Weather server response with tool-list `@server.list_tools()` has defined. 

```python

@server.list_tools()
async def list_tools() -> list[Tool]:
    ...

        Tool(
            name="get_weather",
            description="Get the weather",
            inputSchema={
                "type": "object",
                "properties": {"state": {"type": "string"}},
            },
        )
```

3. MCPHost (inspector) is based on this information, listing the tools, and if user requested get_weather,  
then it calls tools/call method with parameter about get_weather.
The Request / Response is well represented in image.

![](./image/call_rpc.png)

- And when our MCP weather received the @RPC request, especially "tools/call", then @server.call_tool is invoked.  

```python
@server.call_tool()
async def get_weather(name: str, state: str) -> Sequence[TextContent]:
    return [TextContent(type="text", text=f"Hello {state}")]
```

## Troubleshooting
- If connection fails:
- Verify MCP Inspector is running
- Check if the directory path is correct
- Ensure mcp-weather project is built correctly

## Notes
- MCP Inspector is for development and testing purposes only
- Different communication methods may be required in production environments

