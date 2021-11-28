import numpy as np
import matplotlib.pyplot as plt
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import re
import nltk
import string
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
def dcleaner(txt):
  txt = re.sub(r'@[A-Za-z0-9]+',"",txt) #removing mentions
  txt = re.sub(r'#[A-Za-z0-9]+',"",txt) #Hashtags removing
  txt = re.sub(r'https?:\/\/\S+',"",txt) #Remove urls
  txt = re.sub(r'RT[\s]+', "", txt) #Remove Retwees
  txt = txt.translate(str.maketrans('', '', string.punctuation)) #Remove punctuation's sings.
  txt = txt.lower()
  txt = txt.split()
  txt = ' '.join(txt)
  return txt

#subjectivity
def subjectiveness(txt):
  return TextBlob(txt).sentiment.subjectivity

#Polarity
def Polariness(txt):
  return TextBlob(txt).sentiment.polarity
if __name__ == "__main__":
    data2 = pd.read_csv("Training.csv",
                       names=["sentiment",
                                "id",
                                  "date",
                                  "flag",
                                "user",
                                "tweet"
                              ]
                       , encoding='latin-1')

    data2['tweet'] = data2['tweet'].apply(dcleaner)
    #all_stopwords = stopwords.words('english')
    #all_stopwords.remove('not')
    #data2['tweet'] = data2['tweet'].apply(lambda x: ' '.join([word for word in x.split() if word not in (all_stopwords)]))
    data2["subjectivity"] = data2["tweet"].apply(subjectiveness)
    data2 = data2.loc[data2['subjectivity'] != 0]
    token = RegexpTokenizer(r'[a-zA-Z0-9]+')
    vectorizer = CountVectorizer(ngram_range=(1, 1), tokenizer=token.tokenize)
    algo = vectorizer.fit_transform(data2['tweet'])
    x_train, x_test, y_train, y_test = train_test_split(algo, data2['sentiment'], test_size=0.10, random_state=0)
    classifier = MultinomialNB()
    classifier.fit(x_train, y_train)
    mnb_prediction = classifier.predict(x_test)
    print("Accuracy:", accuracy_score(y_test, mnb_prediction))