import streamlit as st
import requests

st.title("AI Platform & Doublend")

mode = st.sidebar.selectbox("Mode", ["Single Model Chat", "Doublend (Multi-Agent)"])

if mode == "Single Model Chat":
    st.header("Chat with Model")
    model_type = st.selectbox("Model Type", ["APIPM (API)", "HFPM (Local)"])
    model_name = st.text_input("Model Name", "gpt-3.5-turbo" if "API" in model_type else "llama-2-7b")

    user_input = st.text_input("Message:")
    if st.button("Send"):
        # For now, we simulate calling the backend
        response = requests.post(
            "http://localhost:8000/chat",
            json={
                "model": f"{model_type} - {model_name}",
                "messages": [{"role": "user", "content": user_input}]
            }
        )
        if response.status_code == 200:
            st.write(response.json().get("response"))
        else:
            st.error("Error communicating with backend.")

elif mode == "Doublend (Multi-Agent)":
    st.header("Doublend - Multi-Agent Task")
    task = st.text_area("Task description:")
    roles = st.text_input("Roles (comma-separated, e.g., planner, coder, reviewer)", "planner, coder, reviewer")

    if st.button("Execute Task"):
        roles_list = [r.strip() for r in roles.split(",")]
        response = requests.post(
            "http://localhost:8000/agents",
            json={"task": task, "roles": roles_list}
        )
        if response.status_code == 200:
            st.write("Result:")
            st.json(response.json())
        else:
            st.error("Error communicating with backend.")
