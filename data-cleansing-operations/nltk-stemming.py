import nltk
from nltk.stem import PorterStemmer

# words=['write', 'writer', 'writing', 'writers', 'written', 'wrote', 'writable', 'writes']
words = ['game', 'gaming', 'gamed', 'games']
ps = PorterStemmer()

# for word in words:
#     print(f"{word}: {ps.stem(word)}")


# stemming an entire sentence
from nltk.tokenize import word_tokenize
nltk.download('punkt')
sentence = 'I enjoy writing this tutorial; I love write and I have written 266 words so far. I wrote more than you did; I am a writer.'

words = word_tokenize(sentence)
for word in words:
    print(f"{word}: {ps.stem(word)}")