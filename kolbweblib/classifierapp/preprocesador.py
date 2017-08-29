import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.data import load
from nltk.stem import SnowballStemmer
from string import punctuation
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

def vectorizar_clase(clase):
    diccionario_vectorizacion = {'div':0, 'aco':1, 'con':2, 'asi':3}
    v = [0.,0.,0.,0.]
    v[diccionario_vectorizacion[clase]] = 1.
    return v

def vector_a_clase(vector):
    diccionario_vectorizacion_inverso = {0:'div', 1:'aco', 2:'con', 3:'asi'}
    return diccionario_vectorizacion_inverso[np.argmax(vector)]

spanish_stopwords = stopwords.words('spanish')
stemmer = SnowballStemmer('spanish')
non_words = list(punctuation)
non_words.extend(['¿', '¡'])
non_words.extend(map(str,range(10)))

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    # remove punctuation
    text = ''.join([c for c in text if c not in non_words])
    # tokenize
    tokens =  word_tokenize(text)

    # stem
    try:
        stems = stem_tokens(tokens, stemmer)
    except Exception as e:
        print(e)
        print(text)
        stems = ['']
    return stems

vectorizer = CountVectorizer(
                analyzer = 'word',
                tokenizer = tokenize,
                lowercase = True,
                stop_words = spanish_stopwords,
                min_df=2,
                max_df=0.95,
                max_features=500,
                )
