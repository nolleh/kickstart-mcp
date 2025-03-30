import os
import json
from typing import Dict, Optional, List
from dataclasses import dataclass, asdict
from collections import defaultdict


@dataclass
class TutorialGroup:
    name: str
    description: str
    tutorials: List[str]


class TutorialState:
    def __init__(self):
        self.state_file = os.path.expanduser("~/.kickstart-mcp-state.json")
        self.state: Dict = self._load_state()
        self.groups: Dict[str, TutorialGroup] = self._load_groups()

    def _load_state(self) -> Dict:
        """Load state from file or create new if not exists"""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return self._create_new_state()
        return self._create_new_state()

    def _create_new_state(self) -> Dict:
        """Create new state structure"""
        return {
            "completed_tutorials": [],
            "current_tutorial": None,
            "last_position": None,
            "last_group": None,
        }

    def _load_groups(self) -> Dict[str, TutorialGroup]:
        """Load tutorial groups configuration"""
        return {
            "hello-mcp": TutorialGroup(
                name="Hello, mcp",
                description="Let's use mcp",
                tutorials=["HelloMcp"],
            ),
            "python-project": TutorialGroup(
                name="Python Project",
                description="Basic project setup and configuration",
                tutorials=["MakingProject", "ModifyToml", "ModifyInit"],
            ),
            "mcp-server": TutorialGroup(
                name="Mcp Server",
                description="Make a MCP server",
                # Add more tutorials as they are created
                tutorials=[
                    "MakeServer",
                    "TestServer01",
                    "ImplementWeather",
                    "ImplementSseTransport",
                    "FastMcpWeather",
                ],
            ),
            "mcp-client": TutorialGroup(
                name="Mcp Client",
                description="Make a MCP client",
                tutorials=[],  # Add more tutorials as they are created
            ),
            "miscellaneous": TutorialGroup(
                name="Miscellaneous",
                description="Before you leave..",
                tutorials=["Credits"],
            ),
        }

    def save_state(self):
        """Save current state to file"""
        with open(self.state_file, "w") as f:
            json.dump(self.state, f, indent=2)

    def mark_tutorial_completed(self, tutorial_name: str):
        """Mark a tutorial as completed"""
        if tutorial_name not in self.state["completed_tutorials"]:
            self.state["completed_tutorials"].append(tutorial_name)
            self.save_state()

    def is_tutorial_completed(self, tutorial_name: str) -> bool:
        """Check if a tutorial is completed"""
        return tutorial_name in self.state["completed_tutorials"]

    def set_current_tutorial(self, tutorial_name: str):
        """Set the current tutorial"""
        self.state["current_tutorial"] = tutorial_name
        self.save_state()

    def get_current_tutorial(self) -> Optional[str]:
        """Get the current tutorial"""
        return self.state["current_tutorial"]

    def set_last_position(self, position: int):
        """Set the last selected position"""
        self.state["last_position"] = position
        self.save_state()

    def get_last_position(self) -> Optional[int]:
        """Set the last selected position"""
        return self.state["last_position"]

    def set_last_group(self, group_name: str):
        """Set the last selected group"""
        self.state["last_group"] = group_name
        self.save_state()

    def get_last_group(self) -> Optional[str]:
        """Get the last selected group"""
        return self.state.get("last_group")

    def get_group_progress(self, group_name: str) -> float:
        """Calculate progress for a specific group"""
        if group_name not in self.groups:
            return 0.0

        group = self.groups[group_name]
        if not group.tutorials:
            return 0.0

        completed = sum(
            1 for tutorial in group.tutorials if self.is_tutorial_completed(tutorial)
        )
        return completed / len(group.tutorials)

    def get_total_progress(self) -> float:
        """Calculate overall progress across all groups"""
        total_tutorials = sum(len(group.tutorials) for group in self.groups.values())
        if total_tutorials == 0:
            return 0.0

        total_completed = sum(
            sum(
                1
                for tutorial in group.tutorials
                if self.is_tutorial_completed(tutorial)
            )
            for group in self.groups.values()
        )
        return total_completed / total_tutorials

    def get_tutorial_group(self, tutorial_name: str) -> Optional[str]:
        """Get the group name for a specific tutorial"""
        for group_name, group in self.groups.items():
            if tutorial_name in group.tutorials:
                return group_name
        return None
