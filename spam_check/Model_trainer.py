import string
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
import pandas as pd
from sklearn.externals import joblib

df=pd.read_csv('spam.csv')
df.drop_duplicates(inplace=True)

def processText(text):
    no_punctuation=[i for i in text if i not in string.punctuation]
    no_punctuation=''.join(no_punctuation)
    clean_text=[word for word in no_punctuation.split() if word.lower() not in stopwords.words('english')]
    return clean_text

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(df['EmailText'], df['Label'], test_size = 0.15, random_state = 0)

from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer()
X_train_cv=cv.fit_transform(X_train)
X_test_cv=cv.transform(X_test)

from sklearn.naive_bayes import MultinomialNB
classifier = MultinomialNB()
classifier.fit(X_train_cv, y_train)

saved_model=joblib.dump(classifier,'model.pkl')
joblib.dump(cv,'vector.pkl')
