from app.graph import graph

state = {
    "messages": [
        {
            "role": "user",
            "parts": [
                {
                    "text": "Hello"
                }
            ]
        }
    ]
}

result = graph.invoke(state)

print(result["messages"][-1]["parts"][0]["text"])