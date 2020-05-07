import os, re
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

stopwords = list(STOP_WORDS)

path = "C:\\Users\\tusha\miniconda3\Lib\site-packages\en_core_web_sm\\"
nlp = spacy.load(path + "en_core_web_sm-2.2.5")
pattern = '\[\d+\]'


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


def make_text_files(path=None):
    if path is not None:
        files = os.listdir(path)
        text_files = []
        file_name = []
        for file in files:
            if file[-4:] == '.txt':
                file_name.append(file)
                f = open('all_files//{}'.format(file), 'r')
                text = f.read()
                text_files.append(text)
        return (text_files, file_name)
    else:
        print('Path not Entered')


def extraction_and_process(text_files, file_name, top_best_sent_val):
    global punctuation, pattern

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

        sentences_long_val = top_best_sent_val
        summary = get_summary(sent_frequency, sentences_long_val)

        docs_sum = nlp(summary)
        print('-------------------------------------', f, '-------------------------------------------\n')
        for idx, s in enumerate(docs_sum.sents):
            s = str(s)
            s = re.sub(pattern, ' ', s)
            print("{} : {}".format(idx, s))
        print('\n')


if __name__ == '__main__':
    folder_where_txt_files_are_stored = 'all_files'
    text_files, file_name = make_text_files(path=folder_where_txt_files_are_stored)
    extraction_and_process(text_files, file_name, top_best_sent_val=20)
