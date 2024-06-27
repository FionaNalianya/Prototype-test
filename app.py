import os
import time
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from langchain_openai import ChatOpenAI
from langchain_core.runnables.base import RunnableSequence
from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
import certifi

# Fix SSL certificate issue
os.environ['SSL_CERT_FILE'] = certifi.where()

# Ensure environment variables are set
if not os.environ.get("SLACK_BOT_TOKEN"):
    raise ValueError("SLACK_BOT_TOKEN environment variable not set")
if not os.environ.get("SLACK_APP_TOKEN"):
    raise ValueError("SLACK_APP_TOKEN environment variable not set")
if not os.environ.get("OPENAI_KEY"):
    raise ValueError("OPENAI_KEY environment variable not set")

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

openai = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key="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")


# Langchain implementation
template = """Assistant is a large language model trained by OpenAI.

    Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

    Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

    Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

    {history}
    Human: {human_input}
    Assistant:"""

prompt = PromptTemplate(
    input_variables=["history", "human_input"], 
    template=template
)

# Retrieve OpenAI API key from environment variables
openai_api_key = os.environ.get("OPENAI_KEY")

# Creating a RunnableSequence (replaces LLMChain)
# chatgpt_chain = prompt | openai | ConversationBufferWindowMemory(k=2)

# Message handler for Slack
# Initialize the memory
memory = ConversationBufferWindowMemory(k=2)

# Create a runnable sequence (PromptTemplate and LLM)
sequence = prompt | openai


# Dictionary to hold conversation history
conversation_history = {}

def process_message(user, text):
    # Get the user's conversation history or create a new one
    history = conversation_history.get(user, "")

    # Prepare input data
    input_data = {"history": history, "human_input": text}
    
    # Generate response
    response = sequence.invoke(input_data)
    
    # Update the conversation history
    new_history = f"{history}\nHuman: {text}\nAssistant: {response}"
    conversation_history[user] = new_history
    
    return response

@app.message(".*")
def message_handler(message, say, logger):
    try:
        user = message['user']
        text = message['text']
        
        # Load memory for the user
        history = memory.load_memory(user)
        
        # Prepare input data
        input_data = {"history": history, "human_input": text}
        
        # Generate response
        response = sequence(input_data)
        
        # Save the conversation to memory
        memory.save_memory(user, text, response)
        
        # Send response back to Slack
        say(response)
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        say("Sorry, I encountered an error while processing your message. Please try again.")
        time.sleep(1)  # Wait before retrying

@app.event("app_mention")
def handle_app_mention_events(body, say, logger):
    try:
        user = body['event']['user']
        text = body['event']['text']
        
        # Process the message
        response = process_message(user, text)
        
        # Send response back to Slack
        say(response)
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        say("Sorry, I encountered an error while processing your message. Please try again.")
        time.sleep(1)

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
