from flask import Flask, redirect, url_for, request
import nltk
from nltk.corpus import movie_reviews
import random
from bs4 import BeautifulSoup
import requests
import re
from googleapiclient.discovery import build

app = Flask(__name__)

@app.route('/')
def hello_world():
   return "hello"



def crawl_from_url(url):
    source_code = requests.get(str(url))
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")

    for k in soup.findAll('div', {'id': 'div_storyContent'}):
        var=k.contents

    article = re.sub('<.*?>', '',str(var))

    return article



my_api_key = "AIzaSyC1gkYHQMTPdbBYtYPHMk45rkdr4grKq1g"
my_cse_id = "009652909963488507983:kcai5g0i2zg"


def google_search(search_term, api_key, cse_id, **kwargs):
    print("hello")
    service = build("customsearch", "v1", developerKey="AIzaSyC1gkYHQMTPdbBYtYPHMk45rkdr4grKq1g")
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']


def give_me_the_url(movie_name):
    query= movie_name+" movie review hindustan times"
    results = google_search(query , my_api_key, my_cse_id, num=1)
    for i in results:
        var=i['link']
    return var

def document_features(document):
    document_words = set(document)
    features = {}

    for (word, val) in word_features:
        features['contains(%s)' % word] = (word in document_words)

    return features

documents = [(list(movie_reviews.words(fileid)), category)
                    for category in movie_reviews.categories()
                    for fileid in movie_reviews.fileids(category)]

random.shuffle(documents)

all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())

word_features= all_words.most_common(2000)

featuresets = [(document_features(d), c) for (d, c) in documents]
train_set, test_set = featuresets[100:], featuresets[:100]
classifier = nltk.NaiveBayesClassifier.train(train_set)
# save_classifier = open("movie_review_classifier.pickle", "wb")
# pickle.dump(classifier, save_classifier)
# save_classifier.close()

# open_file = open("movie_review_classifier.pickle", "rb")
# classifier = pickle.load(open_file)
# open_file.close()

@app.route('/movie',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      data =request.data
      movie_name=data[10:-2]
      url=give_me_the_url(movie_name)
      article=crawl_from_url(url)

      #var2='''terrible. horrible . pathetic. '''

    #   print(classifier.classify(document_features(nltk.word_tokenize(var2))))

      #return str(classifier.classify(document_features(nltk.word_tokenize(article))))
      return str(article)
   else:
       url = give_me_the_url("piku")
       article = crawl_from_url(url)
       return str(classifier.classify(document_features(nltk.word_tokenize(article))))

   return article



if __name__ == '__main__':
   app.run()