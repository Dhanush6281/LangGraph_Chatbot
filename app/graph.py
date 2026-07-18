from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.chatbot import get_response


class ChatState(TypedDict):
    messages: list


def chatbot_node(state: ChatState):
    response = get_response(state["messages"])

    messages = state["messages"].copy()

    messages.append(
        {
            "role": "model",
            "parts": [
                {
                    "text": response
                }
            ]
        }
    )

    return {
        "messages": messages
    }


builder = StateGraph(ChatState)

builder.add_node("chatbot", chatbot_node)

builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

graph = builder.compile()