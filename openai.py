#IMPORTS
from openai import OpenAI
from dotenv import load_dotenv
import os

#API KEY SETUP
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

conversation_history = [
    {"role": "system", "content": "You are a medical assistant."}
]

#CONTINOUS CHAT RESPONSE 
    #INPUT: User prompt (str)
    #RETURNS: gpt-4 response (str)

def chat_with_gpt(user_input):
    
    conversation_history.append({"role": "user", "content": user_input})
    response = openai
    # response = openai.ChatCompletion.create(
    #     model="gpt-4",
    #     messages=conversation_history
    # )
    
    assistant_reply = response['choices'][0]['message']['content']
    conversation_history.append({"role": "assistant", "content": assistant_reply})
    return assistant_reply

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Ending the chat. Goodbye!")
        break
    response = chat_with_gpt(user_input)
    print(f"Assistant: {response}")