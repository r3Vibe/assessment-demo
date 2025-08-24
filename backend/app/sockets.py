import asyncio
import logging

import socketio

logger = logging.getLogger("uvicorn.error")

origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=origins)
app = socketio.ASGIApp(sio)


@sio.event
async def connect(sid, environ):
    logger.info(f"Client connected: {sid}")


@sio.event
async def disconnect(sid):
    logger.info(f"Client disconnected: {sid}")


@sio.event
async def message(sid, data):
    logger.info(f"Message from {sid}: {data}")
    from app.agent.graph import get_graph

    initial_state = {
        "query": data["message"],
        "message_type": data["message_type"],
        "file_content": data["file"],
    }
    config = {
        "configurable": {
            "thread_id": data["chat_id"],
            "sid": sid,
            "user_id": "test-user-demo",
        }
    }

    await sio.emit("start_typing", to=sid)

    async for token in get_graph(initial_state, config):
        await sio.emit("message", token, to=sid)
        await asyncio.sleep(0.01)

    await sio.emit("stop_typing", to=sid)
