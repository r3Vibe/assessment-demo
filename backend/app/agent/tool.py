from typing import Annotated

from langchain_core.messages import ToolMessage
from langchain_core.tools import StructuredTool, Tool
from langchain_core.tools.base import InjectedToolCallId
from langchain_experimental.utilities import PythonREPL
from langgraph.types import Command
from pydantic import BaseModel, Field

python_repl = PythonREPL()

repl_tool = Tool(
    name="python_repl",
    description="A Python shell. Use this to execute python commands. Input should be a valid python command.",
    func=python_repl.run,
)


class emit_tool_args(BaseModel):
    file_name: str = Field(description="File name to be sent to the frontend")
    sid: str = Field(description="Socket.IO session id")
    tool_call_id: Annotated[str, InjectedToolCallId] = Field(description="Tool call id")


async def emit_event(
    file_name: str,
    sid: str,
    tool_call_id: Annotated[str, InjectedToolCallId],
):
    try:
        import base64
        import os

        from app.sockets import sio as socketio

        file_loc = os.path.join("app", "output")

        os.makedirs(file_loc, exist_ok=True)

        final_file_path = os.path.join(file_loc, file_name)

        with open(final_file_path, "rb") as f:
            file_data = f.read()
            base64_data = base64.b64encode(file_data).decode("utf-8")

        await socketio.emit("image", {"file": base64_data}, room=sid)

        return Command(
            update={
                "messages": [
                    ToolMessage(
                        "Image sent successfully to the frontend",
                        tool_call_id=tool_call_id,
                    )
                ]
            }
        )
    except Exception as e:
        return Command(
            update={
                "messages": [
                    ToolMessage(
                        f"Error sending image to the frontend: {str(e)}",
                        tool_call_id=tool_call_id,
                    )
                ]
            }
        )


emit_tool = StructuredTool.from_function(
    coroutine=emit_event,
    name="emit_tool",
    description="A tool to emit events to the frontend.",
    args_schema=None,
)
