# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "anyio",
#     "fastmcp",
#     "numpy",
# ]
# ///
import anyio
from fastmcp import Client
from fastmcp.client import transports
import numpy as np
import typer

in_progress_enter = 0
in_progress_leave = 0
post_queue_enter = 0
post_queue_leave = 0


def main(host: str, port: int, trans: str, num: int) -> None:
    async def do_test(duration: float | None, transport):
        global in_progress_leave
        global post_queue_enter, post_queue_leave
        post_queue_enter += 1
        try:
            async with Client(transport) as client:
                await client.call_tool("sleep_lightly", {"duration": duration})
        except Exception as e:
            print(str(e), end="; ")
        finally:
            in_progress_leave += 1
            post_queue_leave += 1
            print(f"Finished; in_progress: {(in_progress_enter, in_progress_enter - in_progress_leave, in_progress_leave)}, post_queue: {(post_queue_enter, post_queue_enter - post_queue_leave, post_queue_leave)}")

    if trans == "sse":
        transport = transports.SSETransport(f"http://{host}:{port}/sse")
    elif trans == "stdio":
        transport = transports.StdioTransport("uv", "run --script server.py stdio".split(" "))
    elif trans == "streamable-http":
        transport = transports.StreamableHttpTransport(url=f"http://{host}:{port}/mcp", headers={})
    else:
        raise NotImplemented(trans)

    async def run_all():
        global in_progress_enter
        async with anyio.create_task_group() as tg:
            for _ in range(num):
                in_progress_enter += 1
                #duration = np.random.exponential(scale=1.0)
                duration = None
                tg.start_soon(do_test, duration, transport)
        print("done.")

    anyio.run(run_all)


if __name__ == "__main__":
    typer.run(main)
