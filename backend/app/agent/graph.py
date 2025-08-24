from langchain.chat_models import init_chat_model
from langchain_core.messages import (
    AIMessageChunk,
    HumanMessage,
    RemoveMessage,
    SystemMessage,
)
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.config import get_config
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.store.postgres.aio import AsyncPostgresStore
from langmem import create_memory_store_manager

from app.agent.graph_states import OverallState, UserData
from app.agent.tool import repl_tool
from app.config import Settings as settings

# init LLM
llm = init_chat_model(model="gpt-4o", model_provider="openai", streaming=True)
# bind tools
llm = llm.bind_tools([repl_tool])

# init summary llm
summary_llm = init_chat_model(model="gpt-4o-mini", model_provider="openai")


async def get_graph(initial_state, config):
    async with (
        AsyncPostgresStore.from_conn_string(
            settings.DB_URL,
            index={"dims": 1536, "embed": "openai:text-embedding-3-small"},
        ) as store,
        AsyncPostgresSaver.from_conn_string(settings.DB_URL) as checkpointer,
    ):
        # init memory manager
        manager = create_memory_store_manager(
            "openai:gpt-4o",
            namespace=("users", "{user_id}", "profile"),
            schemas=[UserData],
            instructions="Extract meaningfull user related informations from the conversation.",
            enable_inserts=False,
            store=store,
        )

        def summarize(state: OverallState):
            """Summarize the conversation for long-going convos based on the tokens."""
            summary = state.get("summary", "")
            local_messages = state.get("messages", [])

            num_tokens = llm.get_num_tokens_from_messages(local_messages)
            if num_tokens > 128:
                if summary:
                    summary_message = HumanMessage(
                        content=(
                            f"""
                        Expand the summary below by incorporating the above conversation while preserving context, key points, and 
                        user intent. Rework the summary if needed. Ensure that no critical information is lost and that the 
                        conversation can continue naturally without gaps. Keep the summary concise yet informative, removing 
                        unnecessary repetition while maintaining clarity.
                        
                        Only return the updated summary. Do not add explanations, section headers, or extra commentary.

                        Existing summary:

                        {summary}
                        """
                        )
                    )

                else:
                    summary_message = HumanMessage(
                        content="""
                    Summarize the above conversation while preserving full context, key points, and user intent. Your response 
                    should be concise yet detailed enough to ensure seamless continuation of the discussion. Avoid redundancy, 
                    maintain clarity, and retain all necessary details for future exchanges.

                    Only return the summarized content. Do not add explanations, section headers, or extra commentary.
                    """
                    )

                # Add prompt to our history
                messages = state["messages"] + [summary_message]
                response = summary_llm.invoke(messages)

                # Delete all but the 2 most recent messages
                state["messages"] = state["messages"][-2:]
                state["summary"] = response.content

                for m in state["messages"][:-2]:
                    RemoveMessage(id=m.id)

                return state

        async def agent(state: OverallState) -> OverallState:
            """
            Calls the agent with the current state and returns the updated state.

            Args:
                state (OverallState): The current state of the chatbot.

            Returns:
                OverallState: The updated state after processing the input.
            """
            local_messages = state.get("messages", [])
            human_message = HumanMessage(content=state["query"])
            local_messages.append(human_message)

            from datetime import datetime

            config = get_config()
            user_id = config["configurable"]["user_id"]
            current_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            system_message_str = f"""
                    You are an AI assistant designed to help users with their queries. Answer to the user queries to the best of your ability. and if you do not know the answer, please say "I don't know".
                    Your second goal is to analyse your data if given a file to analyze. After analyzing the data, provide insights and answer any questions related to the data and make python code that will
                    plot the data into a graph. Chat with the user casually and engage in a friendly conversation. Always be polite and respectful. Start your conversation with a warm greeting (Hi, How can i help you today!).

                    # What You will analyse:
                        - XRD patterns
                        - Battery performance metrics
                        - Raman spectroscopy results
                        - Other material characterization data.

                    # How You will analyse:
                        - Use the Python REPL tool to run code snippets for data analysis and visualization.
                        - Generate plots as PNG images for the analyzed data.
                        - Process the data, identify patterns, and generate comprehensive insights about your materials and processes.
                        - Make Summary of it and provide actionable recommendations based on the analysis.

                    # Tone and Style
                        - Use a professional and informative tone.
                        - Be concise and clear in your explanations.
                        - Be friendly and approachable in your interactions.
                        - Greet user warmly and offer assistance.

                    # REPL Tool Guideline (**MUST FOLLOW**)
                        - You are allowed to only write code that will plot data and generate PNG images.
                        - You must not include any other code or text outside of the plotting and image generation.
                        - You must not include any print statements or other forms of output.
                        - You must not include any user input or prompts.
                        - You must not include any explanations or descriptions of the code.
                        - You must not write any code that can delete files or data.
                        - You must not include any code that can modify files or data.
                        - You must not include any code that can access the file system.
                        - You must add matplotlib.use("Agg") to use a non-GUI backend.

                    # Information
                        Current Date time: {current_date_time}

                    # Output image from repl tool
                        file_path = os.path.join("app", "output")
                        os.makedirs(file_path, exist_ok=True)

                        Use the above code to save the final file

                    # Emit back the image
                        Once the file is created use the emit_tool to send the file back to the frontend.
            """

            import os

            msg_tp = state.get("message_type", "text")
            file_name = state.get("file_content", None)
            file_content = os.path.join("app", "data", file_name) if file_name else None

            if msg_tp == "file":
                system_message_str = (
                    system_message_str
                    + f"""
                    File Location: {file_content}
                    Above is the file csv location. write a python code to read the csv file and plot the data.
                    Based on the above data analysis, please provide insights and answer any questions related to the data.
                    make a python code and run it to create a graph image of plotted data. after wards need to cleanup the input files.
                    Once the file is created in output folder you need to call the emit_tool to send the file back to the frontend site.
                    In your code add matplotlib.use("Agg") to use a non gui backend. While saving the file make sure to use the same name as the input file.
                """
                )

                with open(file_content, "r") as f:
                    csv_data = f.read()

                state["messages"].append(
                    HumanMessage(
                        content=f""" current file data for analysis: {csv_data} """
                    )
                )

            system_message = SystemMessage(content=system_message_str)

            summary = state.get("summary", None)

            if summary:
                system_message.content += f"""
                    \n\nPrevious Conversation Summary: {summary}
                    The above information is for you to understand the context of the conversation.
                    Use it to provide better responses to the user's queries. do not mention this summary to the user.
                """

            # get long term memory
            memories = await store.asearch(("users", user_id, "profile"))

            if memories:
                system_message.content += f"""
                    \n\nMemory about the User: {memories[0].value}
                    The above information is for you to remember user preferences and details.
                    Based on this adjust your responses no need to mention this details to the user.
                """

            response = await llm.ainvoke([system_message] + local_messages)

            state["messages"].append(response)

            to_process = {"messages": state["messages"]}

            await manager.ainvoke(to_process)

            return state

        def should_continue(state: OverallState) -> str:
            """
            Determines whether the agent should continue processing based on the current state.

            Args:
                state (OverallState): The current state of the chatbot.

            Returns:
                bool: True if the agent should continue, False otherwise.
            """

            last_message = state["messages"][-1]

            if getattr(last_message, "tool_calls", None):
                return "tools"

            return "final_node"

        async def final_node(state: OverallState) -> OverallState:
            import base64
            import os

            file_name = state.get("file_content", None)
            file_path = (
                os.path.join("app", "output", f"{file_name.split('.')[0]}.png")
                if file_name
                else None
            )

            original_file_path = (
                os.path.join("app", "data", file_name) if file_name else None
            )

            message_type = state.get("message_type", "text")

            config = get_config()

            sid = config["configurable"]["sid"]

            if message_type == "file" and file_path and os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    file_bytes = f.read()
                    file_64 = base64.b64encode(file_bytes).decode("utf-8")

                from app.sockets import sio as socketio

                await socketio.emit("image", {"file": file_64}, room=sid)

            import os

            os.remove(file_path) if file_path and os.path.exists(file_path) else None
            os.remove(original_file_path) if original_file_path and os.path.exists(
                original_file_path
            ) else None

            return state

        graph = StateGraph(OverallState)

        graph.add_node("summarize", summarize)
        graph.add_node("agent", agent)
        graph.add_node("tools", ToolNode([repl_tool]))
        graph.add_node("final_node", final_node)

        graph.set_entry_point("summarize")
        graph.add_edge("summarize", "agent")
        graph.add_conditional_edges("agent", should_continue)
        graph.add_edge("tools", "final_node")
        graph.set_finish_point("final_node")

        c_graph = graph.compile(store=store, checkpointer=checkpointer)

        async for token, metadata in c_graph.astream(
            initial_state, stream_mode="messages", config=config
        ):
            if metadata["langgraph_node"] == "agent":
                if isinstance(token, AIMessageChunk):
                    if token.content:
                        yield token.content
