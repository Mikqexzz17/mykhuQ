import streamlit as st
import requests

st.title("AI Platform & Doublend")

mode = st.sidebar.selectbox("Mode", ["Single Model Chat", "Doublend (Multi-Agent)"])

if mode == "Single Model Chat":
    st.header("Chat with Model")
    model_type = st.selectbox("Model Type", ["APIPM (API)", "HFPM (Local)"])
    model_name = st.text_input("Model Name", "gpt-3.5-turbo" if "API" in model_type else "gpt2")

    api_key = ""
    if "API" in model_type:
        api_key = st.text_input("API Key (e.g. OpenAI Key)", type="password")

    user_input = st.text_input("Message:")
    if st.button("Send"):
        # Call the real backend
        parsed_model_type = "api" if "API" in model_type else "local"

        if parsed_model_type == "api" and not api_key:
            st.error("Please provide an API key for API models.")
        else:
            with st.spinner("Generating response..."):
                response = requests.post(
                    "http://localhost:8000/chat",
                    json={
                        "model": model_name,
                        "model_type": parsed_model_type,
                        "api_key": api_key,
                        "messages": [{"role": "user", "content": user_input}]
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    if "error" in data:
                        st.error(data["error"])
                    else:
                        st.write(data.get("response"))
                else:
                    st.error("Error communicating with backend.")

elif mode == "Doublend (Multi-Agent)":
    st.header("Doublend - Multi-Agent Task")

    model_type = st.selectbox("Model Type", ["APIPM (API)", "HFPM (Local)"], key="doublend_type")
    model_name = st.text_input("Model Name", "gpt-3.5-turbo" if "API" in model_type else "gpt2", key="doublend_name")

    api_key = ""
    if "API" in model_type:
        api_key = st.text_input("API Key (e.g. OpenAI Key)", type="password", key="doublend_key")

    task = st.text_area("Task description:")
    roles = st.text_input("Roles (comma-separated, e.g., planner, coder, reviewer)", "planner, coder, reviewer")

    if st.button("Execute Task"):
        parsed_model_type = "api" if "API" in model_type else "local"

        if parsed_model_type == "api" and not api_key:
            st.error("Please provide an API key for API models.")
        else:
            roles_list = [r.strip() for r in roles.split(",")]
            with st.spinner("Agents are working on the task..."):
                response = requests.post(
                    "http://localhost:8000/agents",
                    json={
                        "task": task,
                        "roles": roles_list,
                        "model_type": parsed_model_type,
                        "model_name": model_name,
                        "api_key": api_key
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    if "error" in data:
                        st.error(data["error"])
                    else:
                        st.write("Result:")
                        st.json(data)
                else:
                    st.error("Error communicating with backend.")
