import webbrowser
import json
import pandas as pd
import sheetreader
from hospitalRecommender import recommendedHospitals, hospitalDF
from tkinter import *
from tkinter import ttk
import advochat
from advochat import chat_with_gpt


BG_COLOR = "lavender"
USER_COLOR = "#white"
BOT_COLOR = "gray"
TEXT_COLOR = "black"
FONT = ("MS Sans Serif", 11)
FONT_BOLD = ("MS Sans Serif", 11, "bold")


class ChatDisplay:
    def __init__(self, root):
        self.root = root
        self.root.title("AdvoChat")
        
        # UI Components
        content = ttk.Frame(root, padding="3 3 8 8")
        content.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Instructions and form link
        self.instructions_label = Label(
            content, 
            text="Complete the form here", 
            font=FONT_BOLD, 
            fg="blue", 
            cursor="hand2"
        )
        self.instructions_label.grid(column=0, row=0, columnspan=2, pady=5)
        self.instructions_label.bind("<Button-1>", lambda e: self.open_link())

        # Email input field
        self.email_label = ttk.Label(content, text="Email:", font=FONT_BOLD)
        self.email_label.grid(column=0, row=1, sticky=W, padx=5, pady=3)
        self.email_entry = ttk.Entry(content, font=FONT, width=25)
        self.email_entry.grid(column=1, row=1, padx=5, pady=3)

        # Distance input field
        self.distance_label = ttk.Label(content, text="Distance (miles):", font=FONT_BOLD)
        self.distance_label.grid(column=0, row=2, sticky=W, padx=5, pady=3)
        self.distance_entry = ttk.Entry(content, font=FONT, width=25)
        self.distance_entry.grid(column=1, row=2, padx=5, pady=3)

        # Submit button
        self.submit_button = ttk.Button(content, text="Submit", command=self.process_form)
        self.submit_button.grid(column=0, row=3, columnspan=2, pady=10)

        # Chat window
        self.txt_window = Text(content, wrap=WORD, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, state=DISABLED, height=15, width=50)
        self.txt_window.grid(column=0, row=4, columnspan=3, sticky=(N, W, E, S), pady=5)

        # Scrollbar for chat window
        self.scrollbar = ttk.Scrollbar(content, command=self.txt_window.yview)
        self.scrollbar.grid(column=3, row=4, sticky=(N, S))
        self.txt_window['yscrollcommand'] = self.scrollbar.set

        # Message entry and send button
        self.msg_entry = ttk.Entry(content, font=FONT, width=50)
        self.msg_entry.grid(column=0, row=5, columnspan=2, sticky=(W, E), padx=10, pady=10)
        self.msg_entry.insert(0, "Type your message here...")
        self.msg_entry.config(foreground="grey")
        self.msg_entry.bind("<FocusIn>", lambda event: self.clear_placeholder())
        self.msg_entry.bind("<FocusOut>", lambda event: self.add_placeholder())

        self.send_button = ttk.Button(content, text="Send", command=self.enter)
        self.send_button.grid(column=2, row=5, sticky=(E), padx=10, pady=10)

        # Conversation history for AI chatbot
        self.conversation_history = [{"role": "system", "content": "You are a medical assistant. I will provide you with a json file with a patient's background information, and further details to help aid the patient. You will only contextualize."}]

    def open_link(self):
        """Open the form link in the default web browser."""
        webbrowser.open("https://forms.gle/9CLpDPF8fzLHeUQB6")

    def clear_placeholder(self):
        """Clear placeholder text when user focuses on the entry."""
        if self.msg_entry.get() == "Type your message here...":
            self.msg_entry.delete(0, END)
            self.msg_entry.config(foreground=TEXT_COLOR)

    def add_placeholder(self):
        """Re-add placeholder text when entry is empty and loses focus."""
        if not self.msg_entry.get():
            self.msg_entry.insert(0, "Type your message here...")
            self.msg_entry.config(foreground="grey")

    def enter(self, *args):
        """Send user input to the chatbot and display response."""
        user_message = self.msg_entry.get()
        if user_message.strip() and user_message != "Type your message here...":
            self.display_message("user", user_message)
            self.msg_entry.delete(0, END)
            self.chat(user_message)

    def display_message(self, sender, message):
        """Display messages in chat window with custom styling."""
        self.txt_window.configure(state=NORMAL)
        if sender == "user":
            self.txt_window.insert(END, f"You: {message}\n", "user")
        else:
            self.txt_window.insert(END, f"AdvoChat: {message}\n", "bot")
        self.txt_window.configure(state=DISABLED)
        self.txt_window.see(END)

    def chat(self, user_message):
        """Handle chat with GPT."""
        # Send message to GPT model and get a response
        response = advochat.chat_with_gpt(user_message, self.conversation_history)
        self.display_message("bot", response)

    def process_form(self):
        """Process the form submission."""
        email = self.email_entry.get()
        max_distance = self.distance_entry.get()

        if email.strip() and max_distance.strip().isdigit():
            self.display_message("bot", "Processing your data, please wait...")

            # Process form using the email provided
            sheetreader.main(email)

            try:
                # Load patient data
                with open(sheetreader.indiv_form, "r") as file:
                    patient_data = json.load(file)[0]

                max_distance = int(max_distance)
                recommended_hospitals = recommendedHospitals(patient_data, hospitalDF, max_distance)

                if recommended_hospitals:
                    # Convert recommended hospitals list to DataFrame and append predicted class
                    hospitals_df = pd.DataFrame(recommended_hospitals)
                    sheetreader.append_predicted_class(hospitals_df.to_dict(orient="records"))

                    # Format hospitals into a bullet-pointed list
                    hospital_list = "\n".join([f"• {hospital}" for hospital in recommended_hospitals])
                    self.display_message("bot", f"Recommended Hospital(s):\n{hospital_list}")
                else:
                    self.display_message("bot", "No hospitals found within the specified distance.")

                # Start the chatbot interaction
                self.run_chat(patient_data)

            except Exception as e:
                self.display_message("bot", f"An error occurred: {e}")
        else:
            self.display_message("bot", "Please provide a valid email and distance.")


    def run_chat(self, patient_data):
        """Start the chat functionality with AdvoChat."""
        self.display_message("bot", "Welcome to AdvoChat! How can I assist you today?")

        # Add patient data to the conversation history for AdvoChat
        self.conversation_history.append(
            {"role": "user", "content": f"Here is the patient's data: {json.dumps(patient_data)}"}
        )

        # Enable chatting
        self.msg_entry.focus()
