from app import ChatDisplay
from tkinter import Tk

def main():
    root = Tk()  # Create a Tkinter root window
    ChatDisplay(root)  # Pass the root window to ChatDisplay
    root.mainloop()  # Start the Tkinter main event loop


main()
