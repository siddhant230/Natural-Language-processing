from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from tqdm import tqdm
from selenium.webdriver.chrome.options import Options
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
        expression=TextBlob(text).sentiment
        total+=expression.polarity
        print(expression.polarity)

def get_to_video(title=None):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver=webdriver.Chrome(executable_path='C:\\Users\\tusha\\Downloads\\chromedriver.exe',options=options)
    driver.get("https://www.youtube.com/results?search_query={}".format(title))
    driver.find_element_by_id('video-title').click()
    time.sleep(2)
    button=driver.find_element_by_class_name('html5-video-container')
    button.click()
    SCROLL_PAUSE_TIME = 2
    CYCLES = 10

    html = driver.find_element_by_tag_name('html')
    html.send_keys(Keys.PAGE_DOWN)  # doing it twice for good measure
    html.send_keys(Keys.PAGE_DOWN)  # one time sometimes wasn't enough
    time.sleep(SCROLL_PAUSE_TIME * 3)
    for i in tqdm(range(CYCLES)):
        html.send_keys(Keys.END)
        time.sleep(SCROLL_PAUSE_TIME)

    # --------------- GETTING THE COMMENT TEXTS ---------------
    comment_elems = driver.find_elements_by_xpath('//*[@id="content-text"]')
    all_comments = [elem.text for elem in comment_elems]
    if all_comments!=[]:
        for each_comment in all_comments:
            text=processText(each_comment)
            judge(text)
    else:
        print("comments are turned off")

if __name__=="__main__":
    while True:
        try:
            value=input("Enter video name : ")
            get_to_video(value)
            val=input("Do you want to exit? Enter 'q' to quit : ")
            if val=="q":
                break
        except:
            pass
