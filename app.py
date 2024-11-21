from tkinter import *
from tkinter import ttk
from advochat import *
import threading


BG_COLOR = "#3D59AB"
USER_COLOR = "#6495ED"
BOT_COLOR = "#EAECEE"
TEXT_COLOR = "#000000"

FONT = ("MS Sans Serif", 14)
FONT_BOLD = ("MS Sans Serif", 13, "bold")

root = Tk()


class ChatDisplay:
    def __init__(self, root):
        root.title("AdvoChat")
        content = ttk.Frame(root, padding="3 3 12 12")
        content.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Chat display area
        self.txt_window = Text(content, wrap=WORD, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, state=DISABLED,)
        self.txt_window.grid(column=0, row=0, columnspan=3, sticky=(N, W, E, S))

        # Scrollbar for chat display
        self.scrollbar = ttk.Scrollbar(content, command=self.txt_window.yview)
        self.scrollbar.grid(column=3, row=0, sticky=(N, S))
        self.txt_window['yscrollcommand'] = self.scrollbar.set

        # Message entry
        self.msg_entry = ttk.Entry(content, font=FONT, width=50)
        self.msg_entry.grid(column=0, row=1, columnspan=2, sticky=(W, E))
        self.msg_entry.focus()

        # Send button
        send_btn = ttk.Button(content, text="Send", command=self.enter)
        send_btn.grid(column=2, row=1, sticky=(E))
        self.msg_entry.bind('<Return>', self.enter)

        # conversation history
        self.conversation_history = [{"role": "system", "content": "You are a medical assistant. I will provide you with a json file with a patient's background information, and further details to help aid the patient. You will only contextualize."}]

        # Add custom text tags for bubbles
        self.txt_window.tag_configure("user", foreground="white", background=USER_COLOR, justify="right", lmargin1=100, rmargin=10, wrap=WORD)
        self.txt_window.tag_configure("bot", foreground="black", background=BOT_COLOR, justify="left", lmargin1=10, rmargin=100, wrap=WORD)
        self.txt_window.tag_configure("padding", background=BG_COLOR)

    def enter(self, *args):
        user_message = self.msg_entry.get()
        if user_message.strip():  # Ignore empty messages
            self.display_message("user", user_message)
            self.msg_entry.delete(0, END)
            self.chat(user_message)

    def display_message(self, sender, message):
        """Display a message in the chat window with bubbles."""
        self.txt_window.configure(state=NORMAL)

        if sender == "user":
            self.txt_window.insert(END, "\n", "padding")
            self.txt_window.insert(END, f"You: {message}\n", "user")
        else:
            self.txt_window.insert(END, "\n", "padding")
            self.txt_window.insert(END, f"AdvoChat: {message}\n", "bot")

        self.txt_window.configure(state=DISABLED)
        self.txt_window.see(END)

   
    def chat_with_gpt(self, user_input):
        """Send the conversation to GPT and get a response."""
        try:
            # Simulate loading patient data
            patient_data = {"name": "John Doe", "age": 45, "condition": "Diabetes", "recommendation": "Visit XYZ Hospital"}

            # Update conversation history
            self.conversation_history.append({"role": "user", "content": user_input})

            print(f"Updated conversation history: {self.conversation_history}")

            # Update conversation history with the patient's data in a way that GPT can understand it better
            self.conversation_history.append({"role": "system", "content": f"Patient Data: {json.dumps(patient_data)}"})
            self.conversation_history.append({"role": "system", "content": "Provide assistance and contextualize the patient information, particularly focusing on the hospital recommendation."})

            # Replace the recursive call with the actual API call
            response = client.chat.completions.create(
                messages=self.conversation_history,
                model="gpt-4"
            )

            # Extract the assistant's reply
            assistant_reply = response.choices[0].message.content

            print(f"Assistant reply: {assistant_reply}")

            # Update history
            self.conversation_history.append({"role": "assistant", "content": assistant_reply})
            return assistant_reply

        except Exception as e:
            # Handle any errors gracefully
            return f"An error occurred: {e}"



    def chat(self, user_message):
        """Handle user input and generate a response."""
        if not user_message:
            self.display_message("bot", "I didn't catch that. Please try again.")
            return

        try:
            response = self.chat_with_gpt(user_message)
            self.display_message("bot", response)
        except Exception as e:
            self.display_message("bot", f"An error occurred: {e}")
    

ChatDisplay(root)
root.mainloop()