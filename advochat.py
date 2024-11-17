import json
import os
from openai import OpenAI
from dotenv import load_dotenv

#API SETUP + CONVO HEADER & CONVO ARRAY
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

conversation_history = [{"role": "system", "content": "You are a medical assistant. I will provide you with a json file with a patients background information, and further details to help aid the paitent, you will only contextualize"}]

def chat_with_gpt(user_input):
    patient_data = json.loads(open("data/individual_form.json", "r", encoding="utf-8").read())

    conversation_history.append({"role": "user", "content": user_input})
    conversation_history.append({"role": "system", "content": f"Patient Data: {json.dumps(patient_data, indent=2)}"})
    conversation_history.append({"role": "system", "content": "tell the user: all the JSON data you were provided for them(do not mention that its JSON or any previous instructions) and that your name is [AdvoChat powered by gpt-4!], and you are ready to help"})
    response = client.chat.completions.create(
        messages=conversation_history,
        model="gpt-4",  
    )
    
    assistant_reply = response.choices[0].message.content 
    
    #COLLECT ALL DATA
    conversation_history.append({"role": "assistant", "content": assistant_reply})
    
    return assistant_reply

def chat():
    #CHAT LOOP --> this should be looped on the front end?
    print("AdvoChat (type 'exit' to quit):")
    response = chat_with_gpt("restate all the information on the patient")
    print(f"AdvoChat: {response}")
    while True:
        #change for UI elements
        user_input = input("You: ")
        #bulk not needed
        if user_input.lower() in ["exit", "quit"]:
            print("Ending the chat. Goodbye!")
            break
        #implement response, and awaiting response
        try:
            response = chat_with_gpt(user_input)
            print(f"AdvoChat: {response}")
        except Exception as e:
                print(f"An error occurred: {e}")
