from .project_chatbot_using_aiml.src.chat_application import chatbot_response
import tkinter
from tkinter import *

def send():
    msg = entry_box.get("1.0", "end-1c").strip()
    entry_box.delete("0.0", END)

    if msg != '':
        chat_log.config(state=NORMAL)
        chat_log.insert(END, "You: " + msg + '\n\n')
        chat_log.config(foreground="#442265", font=("Verdana", 12))

        res = chatbot_response(msg)
        chat_log.insert(END, "BOT: " + res + '\n\n')

        chat_log.config(state=DISABLED)
        chat_log.yview(END)


base = Tk()
base.title("Hello")
base.geometry("400x500")
base.resizable(width=False, height=False)

# create the chat window
chat_log = Text(base, bd=0, bg="white", height="8", width="50", font="Arial")

chat_log.config(state=DISABLED)

# bind scrollbar to the Chat window
scrollbar = Scrollbar(base, command=chat_log.yview, cursor="heart")
chat_log['yscrollcommand'] = scrollbar.set

# create button to send message
send_button = Button(base, font=("Verdana", 12, 'bold'), text="Send", width="12", height=5,
                        bd=0, bg="#32de97", activebackground="#3c9d9b", fg="#ffffff", command=send)

# create the box to enter the message
entry_box = Text(base, bd=0, bg="white", width="29", height="5", font="Arial")

# place all the components on the screen
scrollbar.place(x=376, y=6, height=386)
chat_log.place(x=6, y=6, height=386, width=370)
entry_box.place(x=128, y=401, height=90, width=265)
send_button.place(x=6, y=401, height=90)

base.mainloop()