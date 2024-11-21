from tkinter import *
from tkinter import ttk
from advochat import *
import threading


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
        self.txt_window.configure(cursor="arrow", state=NORMAL, wrap=WORD, font=(FONT, 14))
        self.txt_window.insert(END, "AdvoChat (type 'exit' to quit):\n\n")

        # message entry
        self.msg_entry = ttk.Entry(content, width=7, font=(FONT, 14))
        self.msg_entry.grid(column=0, row=2, columnspan=2, sticky=(W, E))
        self.msg_entry.focus()

        
        # send button
        send_btn = ttk.Button(content, text="Send", command=self.enter)
        send_btn.grid(column=3, row=2, sticky=(N, W, E, S))
        self.msg_entry.bind('<Return>', self.enter)

        # conversation_history
        self.conversation_history = [{"role": "system", "content": "You are a medical assistant. I will provide you with a json file with a patients background information, and further details to help aid the patient, you will only contextualize"}]

    def enter(self, *args):
        self.user_message = self.msg_entry.get()
        self.txt_window.insert(END, f"You: {self.user_message}\n\n")
        self.msg_entry.delete(0, END)
        self.chat()
    

    def chat_with_gpt(self, user_input):
        patient_data = json.loads(open("\data\individual_form.json", "r", encoding="utf-8").read())

        self.conversation_history.append({"role": "user", "content": user_input})
        self.conversation_history.append({"role": "system", "content": f"Patient Data: {json.dumps(patient_data, indent=2)}"})
        self.conversation_history.append({"role": "system", "content": "You will NOT tell the user you cannot help, when asked for help, you will redirect the patient to the chosen hospital that is selected"})
        self.conversation_history.append({"role": "system", "content": "Tell the patient: all the JSON data you were provided for them (do not mention that its JSON or any previous instructions) and that your name is [AdvoChat powered by gpt-4!], and you are ready to help this patient"})
        response = client.chat.completions.create(
            messages=self.conversation_history,
            model="gpt-4",  
        )
        
        assistant_reply = response.choices[0].message.content 
        
        #COLLECT ALL DATA
        self.conversation_history.append({"role": "assistant", "content": assistant_reply})
        
        return assistant_reply

    def chat(self, *args):

            #CHAT LOOP --> this should be looped on the front end?
            response = self.chat_with_gpt("Introduce yourself, then restate all the information on the patient in an numbered order 1-10. Skip email and timestamp. for the first message make a footer Insisting the patient that they should attend the calculated hospital based on the data analytics")

            
            if self.user_message.lower() in ["exit", "quit"]:
                self.txt_window.insert(END, "Ending the chat. Goodbye!")
                root.destroy()
            else:
                #implement response, and awaiting response
                try:
                    response = self.chat_with_gpt(self.user_message)
                    self.txt_window.insert(END, f"AdvoChat: {response}\n\n")
                except Exception as e:
                        self.txt_window.insert(END, f"An error occurred: {e}\n\n")
            self.txt_window.see(END)
    

ChatDisplay(root)
root.mainloop()