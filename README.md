# Deadlock Bug

This is reproducible in `streamable-http` and `sse` but not `stdio`. That makes me think it's a core
concurrency issue in `mcp`.

# Running
In all these examples, change the numeric argument on the client. What I've found

* 10 — works easily, fast
* 100 — works
* 200 — works in `streamable-http`, deadlock in `sse`
* 250 - deadlock in `streamable-http`
* 500 — deadlock
* 1000 — big deadlock

For both `streamable-http` and `sse`, the following error occurs frequently, followed by the script hanging:

```
Error in post_writer: All connection attempts failed
```

If it fails and I kill the client but not the server and re-run with a much lower number
(e.g. 250 and then 10), the second small run works fine.

conclusion: maybe the deadlock is in the client and the server is uneffected?

## Running streamable-http

server:

```bash
uv run --script server.py streamable-http
```

client:

```bash
uv run --script client.py 0.0.0.0 8000 streamable-http 1000
```

## Running sse

server:

```bash
uv run --script server.py streamable-http
```

client:

```bash
uv run --script client.py 0.0.0.0 8000 sse 1000
```


## Running stdio

```bash
# lots of excess noise on stderr
uv run --script client.py 0.0.0.0 8000 stdio 10 2>/dev/null
```
