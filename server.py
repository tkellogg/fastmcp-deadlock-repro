# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "anyio",
#     "fastmcp",
#     "typer",
# ]
# ///
import anyio
from fastmcp import FastMCP
import typer

mcp = FastMCP("Deadlock Repro")


@mcp.tool()
async def sleep_lightly(duration: float | None):
    if duration is not None:
        await anyio.sleep(duration)
    return "done"


HOST = "0.0.0.0"
PORT = 8000

def main(trans: str) -> None:
    if trans == "stdio":
        mcp.run(transport=trans)
    else:
        mcp.run(transport=trans, host=HOST, port=PORT)


if __name__ == "__main__":
    typer.run(main)
