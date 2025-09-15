# basic import
from fastmcp import FastMCP

import math
import pathlib

# instantiate an MCP server client
mcp = FastMCP("Hello World")

# DEFINE TOOLS

def add_to_file(msg):
    with open("/tmp/robot.txt", "a") as f:
        print(msg, file=f)

add_to_file("---")

@mcp.tool()
def MoveForward(steps: int) -> str:
    """
    Move the robot forward of a given number of steps.

    Args:
        steps: the number of steps that the robot should move

    Returns:
        returns the status of the operation (success or failed)
    """

    add_to_file(f"Move forward of {steps} steps")

    return "success"

@mcp.tool()
def TurnRight() -> str:
    """
    Turn the robot to the right

    Args:
        None

    Returns:
        returns the status of the operation (success or failed)
    """

    add_to_file(f"Turn right")

    return "success"


@mcp.tool()
def TurnLeft() -> str:
    """
    Turn the robot to the left

    Args:
        None

    Returns:
        returns the status of the operation (success or failed)
    """

    add_to_file(f"Turn left")

    return "success"

@mcp.tool()
def TurnAround() -> str:
    """
    Turn around the robot

    Args:
        None

    Returns:
        returns the status of the operation (success or failed)
    """

    add_to_file(f"Turn around")

    return "success"

@mcp.tool()
def Explode() -> str:
    """
    Explode the robot. Use with care, this isn't a simulation. Ask the user for confirmation before triggering this function.

    Args:
        None

    Returns:
        returns the status of the operation (success or failed)
    """

    add_to_file(f"Explode!")

    return "success"

# execute and return the stdio output
if __name__ == "__main__":
    #mcp.run(transport="stdio")
    mcp.run(transport="http",  host="127.0.0.1", port=8000)
