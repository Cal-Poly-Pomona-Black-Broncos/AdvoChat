from tkinter import *
from tkinter import ttk
from advochat import *

os.chdir("C:/Users/ccfma/Desktop/Blackground/AI-Hackathon")


BG_BLUE = "#6495ED"
BG_COLOR = "#3D59AB"
TEXT_COLOR = "#EAECEE"

FONT = "MS Sans Serif 14"
FONT_BOLD = "MS Sans Serif 13 bold"

root = Tk()

class ChatDisplay:

    def __init__(self, root):

        root.title("Healthcare Chat")
        content = ttk.Frame(root, padding="3 3 12 12")
        content.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)


        # text window
        self.txt_window = Text(content)
        self.txt_window.grid(column=0,row=0,columnspan=2,rowspan=2)
        self.txt_window.configure(cursor="arrow",state=DISABLED)

        # message entry
        self.msg_entry = ttk.Entry(content, width=7)
        self.msg_entry.grid(column=0, row=2, columnspan=2, sticky=(W, E))
        self.msg_entry.focus()

        
        # send button
        send_btn = ttk.Button(content, text="Send", command=self.chat)
        send_btn.grid(column=3, row=2, sticky=(N, W, E, S))
        self.msg_entry.bind('<Return>', self.chat)

    def enter_pressed(self, *args):
        self.txt_window.insert(END, f"You: {self.msg_entry.get}")
        self.chat()
    
    def chat_with_gpt(user_input):
        patient_data = json.loads(open("data\individual_form.json", "r", encoding="utf-8").read())

        conversation_history.append({"role": "user", "content": user_input})
        conversation_history.append({"role": "system", "content": f"Patient Data: {json.dumps(patient_data, indent=2)}"})
        conversation_history.append({"role": "system", "content": "You will NOT tell the user you cannot help, when asked for help, you will redirect the patient to the chosen hospital that is selected"})
        conversation_history.append({"role": "system", "content": "Tell the patient: all the JSON data you were provided for them (do not mention that its JSON or any previous instructions) and that your name is [AdvoChat powered by gpt-4!], and you are ready to help this patient"})
        response = client.chat.completions.create(
            messages=conversation_history,
            model="gpt-4",  
        )
        
        assistant_reply = response.choices[0].message.content 
        
        #COLLECT ALL DATA
        conversation_history.append({"role": "assistant", "content": assistant_reply})
        
        return assistant_reply

    def chat(self, *args):
        #CHAT LOOP --> this should be looped on the front end?
        self.txt_window.configure(state=NORMAL)
        self.txt_window.insert(END, "AdvoChat (type 'exit' to quit):\n")
        self.txt_window.configure(state=DISABLED)
        response = chat_with_gpt("Introduce yourself, then restate all the information on the patient in an numbered order 1-10. Skip email and timestamp. for the first message make a footer Insisting the patient that they should attend the calculated hospital based on the data analytics")
        self.txt_window.configure(state=NORMAL)
        self.txt_window.insert(END, f"AdvoChat: {response}")
        self.txt_window.configure(state=DISABLED)


        self.enter_pressed


        if self.msg_entry.lower() in ["exit", "quit"]:
            self.txt_window.configure(state=NORMAL)
            self.txt_window.insert(END, "Ending the chat. Goodbye!")
            self.txt_window.configure(state=DISABLED)

        #implement response, and awaiting response
        try:
            response = chat_with_gpt(self.enter_pressed())
            self.txt_window.configure(state=NORMAL)
            self.txt_window.insert(END, f"AdvoChat: {response}")
            self.txt_window.configure(state=DISABLED)
        except Exception as e:
                self.txt_window.configure(state=NORMAL)
                self.txt_window.insert(END, f"An error occurred: {e}")
                self.txt_window.configure(state=DISABLED)
             
ChatDisplay(root)
root.mainloop()