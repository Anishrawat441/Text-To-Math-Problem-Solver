import streamlit as st
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_core.tools import tool
import re


## Creating UI
st.title("TEXT_TO_MATH Problem Solver")


# LLM

# model = ChatOllama(
#     model="gemma3:latest",
#     temperature=0
# )

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    api_key=st.secrets["GROQ_API_KEY"]
)
## Calculator Tool
@tool
def calculator(expression: str) -> str:
    """Use this tool to calculate arithmetic expressions such as 2000 + 500, 25 * 40, or 100 / 5."""

    try:
        expression = expression.replace("^", "**")

        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )

        return str(result)

    except Exception as e:
        return f"Calculation error: {e}"

## Math agent
def math_agent(question):
    if re.fullmatch(r"[\d\s+\-*/().%^]+", question.strip()):

        expression = question.replace("^", "**")

        return calculator.invoke(expression)
    response = model.invoke(
        f"""
Solve this mathematical problem step by step.

Question:
{question}

Give a clear final answer.
"""
    )

    return response.content

## session state
if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! I am your Math Assistant. "
                "Ask me a mathematical question."
            )
        }
    ]

# Display Conversation History

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])



# User Input

question = st.chat_input(
    "Ask your mathematical question..."
)


# store user question

if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })


    # Display User Question

    with st.chat_message("user"):
        st.write(question)


    # Create Context from Previous Messages

    conversation_history = ""

    for message in st.session_state.messages:

        conversation_history += (
            f"{message['role']}: "
            f"{message['content']}\n"
        )
    # Generate Response
with st.spinner("Generating Response..."):
    response = model.invoke(
                    {
                        "messages": [
                            {
                            "role": "user",
                            "content": question}]})


answer = response["messages"][-1].content


# Save assistant response
st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })
# Display answer
with st.chat_message("assistant"):
    st.write(answer)

        