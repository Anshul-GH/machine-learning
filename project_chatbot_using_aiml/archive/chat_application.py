import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

from keras.models import load_model
model = load_model('../out/chatbot_model.h5')
import json
import random
intents = json.loads(open('../data/intents.json').read())
words = pickle.load(open('../out/words.pkl', 'rb'))
classes = pickle.load(open('../out/classes.pkl', 'rb'))

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)

    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)

    # bag of words - matrix of N words, vocabulary matrix
    bag = [0] * len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print(f"Found in bag: {w}")
    
    return (np.array(bag))


def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]

    ERROR_THRESHOLD = 0.25

    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    # sort descending on probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []

    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag'] == tag):
            result = random.choice(i['responses'])
            break
    
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res


# creating a GUI using tkinter
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