from project_chatbot_using_aiml.src.chat_application import chatbot_response
import tkinter
from tkinter import *

def send():
    msg = EntryBox.get("1.0", "end-1c").strip()
    EntryBox.delete("0.0", END)

    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12))

        res = chatbot_response(msg)
        ChatLog.insert(END, "BOT: " + res + '\n\n')

        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)


base = Tk()
base.title("Hello")