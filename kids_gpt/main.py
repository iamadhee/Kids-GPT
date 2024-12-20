import uuid

import gradio as gr

from agent import Agent

# Initialize agent
agent_runnable = Agent()

# Default messages at the start
default_messages = [
    {"role": "assistant", "content": "Hello! How can I help you today?"}
]


def initialize_session():
    """Initializes a new session with fresh UUID and default messages."""
    return default_messages, uuid.uuid4()


def respond(user_input, messages, thread_id):
    # Append user message to history
    messages.append({"role": "user", "content": user_input})

    # Get response from the agent
    response = agent_runnable.run(user_input, thread_id=thread_id)
    ai_message = response["messages"][-1].content
    character_tabs = response["characteristics"]

    # Append assistant's message to history
    messages.append({"role": "assistant", "content": ai_message})

    # Format character_tabs as a Markdown string
    if character_tabs:
        character_tabs_markdown = "\n".join(f"- {item}" for item in character_tabs)
    else:
        character_tabs_markdown = "No characteristics available."

    # Return updated messages, clear input box, character_tabs_markdown, and messages state
    return messages, "", character_tabs_markdown, messages


with gr.Blocks() as demo:
    # Initialize session state for messages and thread_id
    messages_initial, thread_id_initial = initialize_session()
    messages_state = gr.State(messages_initial)  # Stores chat history
    thread_id_state = gr.State(thread_id_initial)  # Stores unique session ID

    # Main layout with two columns
    with gr.Row():
        with gr.Column(scale=3):
            gr.Markdown("# Kids-GPT")
            chatbox = gr.Chatbot(
                value=default_messages, elem_id="chatbot", type="messages"
            )
            user_input = gr.Textbox(
                label="Ask me anything...",
                placeholder="Type your question here and press enter",
            )

            # Placeholder for character tabs
            character_tabs_display = gr.Markdown("### Characteristics")

            # Call respond function, passing in states for messages and thread_id
            user_input.submit(
                respond,
                inputs=[user_input, messages_state, thread_id_state],
                outputs=[chatbox, user_input, character_tabs_display, messages_state],
            )

# Launch the Gradio app
demo.launch()
