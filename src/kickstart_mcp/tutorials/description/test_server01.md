# MCP Weather Server Test Guide

## Overview
This document provides a detailed guide for testing the MCP Weather Server.

## Test Environment Setup
1. Install and Run MCP Inspector
   ```bash
   npx @model_context_protocol/inspector
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

## Troubleshooting
- If connection fails:
  - Verify MCP Inspector is running
  - Check if the directory path is correct
  - Ensure mcp-weather project is built correctly

## Notes
- MCP Inspector is for development and testing purposes only
- Different communication methods may be required in production environments 