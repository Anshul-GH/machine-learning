import nltk
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
nltk.download('wordnet')
# word = lemmatizer.lemmatize('geese')
# word = lemmatizer.lemmatize('cacti')
# word = lemmatizer.lemmatize('erasers')
# word = lemmatizer.lemmatize('children')
# word = lemmatizer.lemmatize('feet')

# using pos
# word = lemmatizer.lemmatize('better', pos='a')
word = lemmatizer.lemmatize('redder', pos='a')

print(word)