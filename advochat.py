import json
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load OpenAI API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def chat_with_gpt(user_message, conversation_history):
    # Append the user's message to the conversation history
    conversation_history.append({"role": "user", "content": user_message})

    try:
        # Make the GPT API call
        response = client.chat.completions.create(
            model="gpt-4",
            messages=conversation_history
        )
        # Extract the response content
        response_content = response.choices[0].message.content  # Access correctly

        # Append the GPT's response to the conversation history
        conversation_history.append({"role": "assistant", "content": response_content})

        return response_content
    except Exception as e:
        return f"Error interacting with GPT API: {e}"



def start_chat(patient_data):
    print("AdvoChat is ready to assist you. Type 'exit' to quit.")
    conversation_history = [
        {"role": "system", "content": "You are AdvoChat, an AI medical assistant."},
        {"role": "system", "content": f"Patient data: {json.dumps(patient_data)}"}
    ]
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("AdvoChat: Goodbye!")
            break
        conversation_history.append({"role": "user", "content": user_input})
        print("AdvoChat:", chat_with_gpt(conversation_history))
