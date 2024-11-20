from tkinter import *
from tkinter import ttk
from advochat import chat

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
        send_btn = ttk.Button(content, text="Send", command=self.enter_pressed)
        send_btn.grid(column=3, row=2, sticky=(N, W, E, S))
        self.msg_entry.bind('<Return>', self.enter_pressed)

    def enter_pressed(self, *args):
            msg = self.msg_entry.get()
            self.insert_message(msg, "You")
    

    def insert_message(self, msg, sender):
         if not msg:
              return
         
         self.msg_entry.delete(0, END)
         msg1 = f"{sender}: {msg}\n"
         self.txt_window.configure(state=NORMAL)
         self.txt_window.insert(END, msg1)
         self.txt_window.configure(state=DISABLED)

         msg2 = f"Bot: {chat}\n"
         self.txt_window.configure(state=NORMAL)
         self.txt_window.insert(END, msg2)
         self.txt_window.configure(state=DISABLED)

         self.txt_window.see(END)
             
ChatDisplay(root)
root.mainloop()