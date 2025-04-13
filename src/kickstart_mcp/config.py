
import os
from dataclasses import dataclass

@dataclass
class Config:
    claude_config_map = {
        "Darwin": os.getenv('HOME', "") + '/Library/Application Support/Claude/claude_desktop_config.json',
        "Windows": "%APPDATA%/Claude/claude_desktop_config.json",
    }
    cursor_config_map = {
        "Darwin": os.getenv('HOME', "") + '.cursor/mcp.json',
        "Windows": "%APPDATA%/Cursor/mcp.json",
    }
    custom_config_map = {
        "Darwin": os.getenv('HOME', "") + '/mcp_config.json',
        "Windows": "%APPDATA%/mcp_config.json",
    }
