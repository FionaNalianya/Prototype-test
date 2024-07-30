import os
import time
import json
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from langchain_openai import ChatOpenAI
from langchain_core.runnables.base import RunnableSequence
from langchain_core.prompts import PromptTemplate, SystemMessagePromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.messages import AIMessage
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

conversation_history_channel = []

topics = [
    "FreeWorld gets formerly incarcerated people into high-wage jobs to thrive on their own terms. With a newfound sense of stability, prison remains a memory for FreeWorld graduates.",
    "Our mission is to end generational poverty and recidivism.",
    "https://freeworld.org/about"
]

from utils import MarkdownParser

md_parser = MarkdownParser()
# Specify the path to your Markdown file
markdown_filepath = 'background.md'  # Replace 'example.md' with your file path
res_data=md_parser.process_markdown_file(markdown_filepath)

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

openai = ChatOpenAI(model_name="gpt-4", openai_api_key='OPENAI_KEY')

# Langchain implementation
# template = """Assistant is a large language model trained by OpenAI.

#     Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

#     Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

#     Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

#     {history}
#     Human: {human_input}
#     Assistant:"""

# context = "\n".join(conversations)
# major_topics = "\n".join(topics)

# template = f"""
# Here are some recent conversations from a Slack channel:
# {context}

# The major topics to consider are:
# {major_topics}

# Based on the above context, please assist with the following query:
# """

# prompt = PromptTemplate(
#     input_variables=["history", "human_input"], 
#     template=template
# )

# # Retrieve OpenAI API key from environment variables
openai_api_key = os.environ.get("OPENAI_KEY")

# # Message handler for Slack
# # Initialize the memory
memory = ConversationBufferWindowMemory(k=4)

# # Create a runnable sequence (PromptTemplate and LLM)
# sequence = prompt | openai

# Dictionary to hold conversation history
conversation_history = {}

def process_message(user, text):
    # Get the user's conversation history or create a new one
    history = conversation_history.get(user, "")
    human_input = text
    # Prepare input data
    context = "\n".join(conversation_history_channel)
    major_topics = "\n".join(topics)
    input_data = {"history": history, "human_input": human_input, "major_topics": major_topics, "context": context, "res_data": res_data}
    template = f"""
    Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. 
    As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses
    that are coherent and relevant to the topic at hand.
    Assistant is constantly learning and improving, and its capabilities are constantly
    evolving. It is able to process and understand large amounts of text, and can use this knowledge to 
    provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions 
    and provide explanations and descriptions on a wide range of topics.
    Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a
    a wide range of topics.
    Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.
    Assistant is adapted to work with FreeWorld organisation (https://freeworld.org/) whose background covers the major topics here:{major_topics}, and some internal information:{res_data}. you can give feedback based on any information on the 
    internet and any from their website. Also here is slack channel  history chat from some of the latest chats {context}
    {history}
        Human: {human_input}
        Assistant:
        """

    prompt = PromptTemplate(
        input_variables=["history", "human_input"], 
        template=template
    )

    # Retrieve OpenAI API key from environment variables
    # openai_api_key = os.environ.get("OPENAI_KEY")

    # Message handler for Slack
    # Initialize the memory
    # memory = ConversationBufferWindowMemory(k=2)

    # Create a runnable sequence (PromptTemplate and LLM)
    sequence = prompt | openai
    
    # Generate response
    response = sequence.invoke(input_data)

    # Extract text from AIMessage object
    # response_text = response.content if isinstance(response, AIMessage) else str(AIMessage)
    response_text = None
    if isinstance(response, AIMessage):
        print("succeful:\n",response)
        response_text=response.content
    else:
        print("bad:\n",response)
        response_text=str(response)

    # Update the conversation history
    new_history = f"{history}\nHuman: {text}\nAssistant: {response}"
    conversation_history[user] = new_history
    
    return response_text

def extract_messages(slack_data):
    messages = []
    for entry in slack_data:
        if 'text' in entry:
            messages.append(entry['text'])
    return messages

@app.event("message")
def message_handler(message,body, say, logger, event, client):
    try:
        user = body['event']['user']
        text = body['event']['text']
        # Process the message
        channel_id = event['channel']
        result = client.conversations_history(channel=channel_id)
        # print(result)
        conversation_history_channel = result["messages"]
        # print(conversation_history_channel)
        conversations = extract_messages(conversation_history_channel)
        conversation_history_channel = conversations[5]
        # for msg in conversations:
            # print(msg)
        # # Print results
        # logger.info("{} messages found in {}".format(len(conversation_history_channel)))
        response = process_message(user, text)
        # Send response back to Slack
        say(response)
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        say("Sorry, I encountered an error while processing your message. Please try again.")
        time.sleep(1)

@app.message("*")
def message_handler(message, say, logger):
    try:
        user = message['user']
        text = message['text']
        
        # Load memory for the user
        # history = memory.load_memory(user)
        history = ""

        # Prepare input data
        input_data = {"history": history, "human_input": text}
        
        # Generate response
        sequence = openai
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
