#
# websocket.py
#
# Copyright (c) 2024 Daniel Andrlik
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#

async def websocket_application(scope, receive, send):  # noqa: ARG001
    while True:
        event = await receive()

        if event["type"] == "websocket.connect":
            await send({"type": "websocket.accept"})

        if event["type"] == "websocket.disconnect":
            break

        if event["type"] == "websocket.receive":
            if event["text"] == "ping":
                await send({"type": "websocket.send", "text": "pong!"})
