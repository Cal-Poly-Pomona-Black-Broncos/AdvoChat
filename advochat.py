import os
from openai import OpenAI

#API SETUP + CONVO HEADER & CONVO ARRAY
client = OpenAI(api_key=API_KEY)

conversation_history = [{"role": "system", "content": "You are a medical assistant. I will provide you with a json file with a patients background information, and further details to help aid the paitent, you will only contextualize"}]

def chat_with_gpt(user_input):
    conversation_history.append({"role": "user", "content": user_input})
    
    response = client.chat.completions.create(
        messages=conversation_history,
        model="gpt-4",  
    )
    
    assistant_reply = response.choices[0].message.content 
    
    #COLLECT ALL DATA
    conversation_history.append({"role": "assistant", "content": assistant_reply})
    
    return assistant_reply

#CHAT LOOP --> this should be looped on the front end?
if __name__ == "__main__":
    print("Chat with GPT (type 'exit' to quit):")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Ending the chat. Goodbye!")
            break
        try:
            response = chat_with_gpt(user_input)
            print(f"Assistant: {response}")
        except Exception as e:
            print(f"An error occurred: {e}")
