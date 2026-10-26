---
description: Start the Sloperator web playground on a port, reusing a running server if one exists
---

Start the Sloperator web playground and give the user its URL.

Requested port: $ARGUMENTS

Use the requested port if one was given above; if that line is empty, use port
**8080** (the server's default). Never put the port — or anything derived from
the request — inside a shell block; this template only interpolates it here in
the prompt body, so treat it as plain text and use it only as a numeric port
argument in the command below.

## Check for an existing server first

These are the TCP ports currently listening on this machine, captured when this
command was invoked:

!`lsof -nP -iTCP -sTCP:LISTEN`

Look for a `python`/`python3` process listening on the requested port. If one is
there, it is almost certainly an already-running playground: do **not** start a
second one. Verify it answers, then report the existing URL and stop.

If the port is free, start the server. If some *other* process holds the port,
stop and report the conflict rather than killing it — it may be the user's
editor or terminal.

## Start the server

Run it in the background so the command returns while the server keeps running:

```bash
uv run playground/server.py <port>
```

Start it with the `shell` tool in background mode from the project root, using
the numeric port you resolved above in place of `<port>`.

## Confirm and report

Confirm the server is listening on the expected port before telling the user it
is up — re-run the same `lsof` check, or fetch `http://localhost:<port>/`, since
a background start can fail fast (missing dependency, port already taken). Then
give the user the URL:

```text
http://localhost:<port>
```

State plainly which happened: an existing server was reused, or a new one was
started. If startup failed, lead with the error instead of a URL.
