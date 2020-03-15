import os
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

def get_summary(sent_frequency, val):
    n_value = val
    # getting top n_value best sentences
    new_dic = {}
    for k, v in sent_frequency.items():
        new_dic[v] = k

    values = list(new_dic.keys())
    values.sort()

    req_values = values[:n_value]
    best_sent = []
    for r_val in req_values:
        best_sent.append(new_dic[r_val])

    best_sent = [best.text for best in best_sent]
    summary = ''.join(best_sent)
    return summary


files = os.listdir('/content/drive/My Drive/text_summarizer/')
text_files = []
file_name = []
for file in files:
    if file[-4:] == '.txt':
        file_name.append(file)
        f = open('/content/New Text Document.txt'.format(file), 'r')
        text = f.read()
        text_files.append(text)

stopwords = list(STOP_WORDS)
nlp = spacy.load('en_core_web_sm')

docs = []
for text in text_files:
    doc = nlp(text)
    docs.append(doc)

punctuation = punctuation + '\n'

for f, doc in zip(file_name, docs):
    # word frequencing
    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    # normalization of w_frequency
    max_freq = max(list(word_frequencies.values()))
    for w in word_frequencies:
        word_frequencies[w] /= max_freq

    # sentence frequencing
    sentence_tokens = [sent for sent in doc.sents]

    sent_frequency = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sent_frequency.keys():
                    freq = word_frequencies[word.text.lower()]
                    sent_frequency[sent] = freq
                else:
                    freq = word_frequencies[word.text.lower()]
                    sent_frequency[sent] += freq
    print(len(sent_frequency))
    val = int(len(sent_frequency) * 1)
    sentences_long_val = 10
    summary = get_summary(sent_frequency, sentences_long_val)
    print(f, "=>", summary)
