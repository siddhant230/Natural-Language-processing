##importing libs
import json,nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer=LancasterStemmer()
import numpy as np
from sklearn.externals import joblib
import pickle
import random

nltk.download('punkt')

##loading the contents of intents2 file
with open('/content/drive/My Drive/intents2.json','r') as f:
    data=json.load(f)

words=[]
labels=[]
doc_x,doc_y=[],[]

##segregating words using word tokenizer
for intent in data['intents']:
  for pattern in intent['patterns']:
    wrds=nltk.word_tokenize(pattern)
    words.extend(wrds)
    doc_x.append(wrds)
    doc_y.append(intent['tag'])
  if intent['tag'] not in labels:
    labels.append(intent['tag'])

##stemming the data to get stem words.
#example->beautiful (beauty)
words=[stemmer.stem(w.lower()) for w in words if w!='?']
words=sorted(list(set(words)))
labels=sorted(labels)

training,output=[],[]
out_empty=[0 for _ in range(len(labels))]

##splitting data into x(training),y(output) for training
for x,doc in enumerate(doc_x):
  bag=[]
  wrds=[stemmer.stem(w.lower()) for w in doc]

  for w in words:
    if w in wrds:
      bag.append(1)
    else:
      bag.append(0)

  output_row=out_empty[:]
  output_row[labels.index(doc_y[x])]=1

  training.append(bag)
  output.append(output_row)

training=np.array(training)
output=np.array(output)

######our classifier (you can use anything else like SVM)
from sklearn.neural_network import MLPClassifier
mlp = MLPClassifier(hidden_layer_sizes=(70, 15), max_iter=10000, alpha=1e-5,
                    solver='sgd', verbose=10, tol=1e-5, random_state=1,
                    learning_rate_init=.005)
mlp.fit(training,output)

###saving our trained model as well as file we created by stemming
saved_model=joblib.dump(mlp,'/content/drive/My Drive/chat_bot.pkl')
words_save=joblib.dump(words,'/content/drive/My Drive/words.pkl')
labels_save=joblib.dump(labels,'/content/drive/My Drive/labels.pkl')
data_save=joblib.dump(data,'/content/drive/My Drive/data.pkl')

######loading the model
model=joblib.load('/content/drive/My Drive/chat_bot.pkl')
###################DONE###################
