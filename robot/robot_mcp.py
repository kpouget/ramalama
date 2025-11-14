import sys
import logging

from fastmcp import FastMCP

import math
import pathlib

import robot_lib

# instantiate an MCP server client
mcp = FastMCP("Robot MCP")

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

    robot_lib.move(steps, 200, 200)

    return "success"

@mcp.tool()
def MoveBackward(steps: int) -> str:
    """
    Move the robot backward of a given number of steps.

    Args:
        steps: the number of steps that the robot should move

    Returns:
        returns the status of the operation (success or failed)
    """

    add_to_file(f"Move forward of {steps} steps")

    robot_lib.move(steps, -200, -200)

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

    robot_lib.move(1, -200, 200)

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
    robot_lib.move(1, 200, -200)

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
    robot_lib.move(2, -200, 200)

    return "success"

@mcp.tool()
def Beep() -> str:
    """
    Make the robot beep

    Args:
        None

    Returns:
        returns the status of the operation (success or failed)
    """

    add_to_file(f"Beep!")
    robot_lib.beep()


    return "success"

@mcp.tool()
def NewSession() -> str:
    """
    Starts a new session of the robot.

    Args:
        None

    Returns:
        returns the status of the operation (success or failed)
    """

    add_to_file(f"----")

    return "success"



# execute and return the stdio output
if __name__ == "__main__":
    #mcp.run(transport="stdio")
    mcp.run(transport="http",  host="127.0.0.1", port=int(sys.argv[1]))
