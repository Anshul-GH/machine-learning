import nltk
from nltk.stem import WordNetLemmatizer
import json
import pickle

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
import random

words = []
classes = []
documents = []
ignore_words = ['?', '!']
data_file = open('../data/intents.json').read()
intents = json.loads(data_file)

lemmatizer = WordNetLemmatizer()

# preprocessing the data
# tokenizing using nltk
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # tokenize each word
        word = nltk.word_tokenize(pattern)
        words.extend(word)

        # add the documents to the corpus
        documents.append((word, intent['tag']))

        # add to the classes list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# lemmatize each word and remove duplicates
words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_words]
words = sorted(list(set(words)))

# sort classes
classes = sorted(list(set(classes)))

# print the words, classes and document counts
# documents: combination between patterns and intents
# classes: intents
# words: all words, vocabulary
print('Count of documents: ', len(documents))
print('Count of classes: ', len(classes))
print('Count of unique lemmatized words: ', len(words))

# pickle the words and classes
pickle.dump(words, open('../out/words.pkl', 'wb'))
pickle.dump(classes, open('../out/classes.pkl', 'wb'))

# training the model
# create the training data
training = []

# create an empty array for output
output_empty = [0] * len(classes)

# training set, bag of words for each sentence
for doc in documents:
    # initialize our bag of words
    bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0]

    # lemmatize each word and create a base word to represent related word
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]

    # create the bag of words array with value 1 if there is a match in the current pattern, else a 0
    for word in words:
        bag.append(1) if word in pattern_words else bag.append(0)

    # output is going to be a 0 for each tag and 1 for current tag (for each pattern)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])

# shuffle our features and turn them into an array
random.shuffle(training)
training = np.array(training)

# create training and test lists. X - patterns, Y - intents
train_x = list(training[:, 0])
train_y = list(training[:, 1])

print('Training data created ..... ')

# create the model - 3 layered model:
# layer-1: 128 neurons
# layer-2: 64 neurons
# layer-3: output layer

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]), ), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

# compile the model using SGD with Nesterov accelerated gradient
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])

# fitting and saving the model
hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save('../out/chatbot_model.h5', hist)

print('Model has been created and saved .... ')
