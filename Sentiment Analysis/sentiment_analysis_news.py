from selenium import webdriver
from textblob import TextBlob
import string
import nltk
from nltk.corpus import stopwords
#nltk.download('stopwords')

def processText(text):
    no_punctuation=[i for i in text if i not in string.punctuation]
    no_punctuation=''.join(no_punctuation)
    clean_text=[word for word in no_punctuation.split() if word.lower() not in stopwords.words('english')]
    clean_text=' '.join(clean_text)
    return clean_text

def judge(data):
    total=0
    if len(data)>0:
        text=data
        #text=processText(text)
        expression=TextBlob(text).sentiment
        total+=expression.polarity
        print(expression.polarity)

def get_news():
    category_names="Briefs India Sports Entertainment TV Lifestyle Gadgets World Business".split(" ")
    category={}
    for i,cat in enumerate(category_names):
        category[i]=cat

    for key,value in category.items():
        print(key,value)

    response=int(input("Choose a category : "))

    driver=webdriver.Chrome(executable_path='C:\\Users\\tusha\\Downloads\\chromedriver.exe')
    path="https://timesofindia.indiatimes.com/briefs/{}".format(category[response])
    driver.get(path)

    messages=driver.find_elements_by_class_name("brief_box")

    for msg in messages:
        text=msg.text
        judge(text)
        print("============================================")

if __name__=="__main__":
    while True:
        try:
            get_news()
            val=input("Do you want to exit? Enter 'q' to quit : ")
            if val=="q":
                break
        except:
            pass
