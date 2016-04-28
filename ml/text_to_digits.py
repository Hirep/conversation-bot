from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.corpus import wordnet
import enchant
import collections
import re
import os
from time import time
import multiprocessing

pool = multiprocessing.Pool()
map = pool.map


allowed_ratio = 0.55
regex = re.compile( '(\\n|\?|_|\[|\]|{|}|,|\.|"|-|!|@|#|\$|%|\^|&|\*|\(|\)|~|\||\'|/|\\\\|;|:|<|>)')
input_folder_path = os.path.join(os.getcwd(), "parsed")
output_folder_path = os.path.join(os.getcwd(), "featured")
isEnglish = enchant.Dict('en_US')
lemmatizer = WordNetLemmatizer()

text_len = 0

def get_wordnet_tag(word):
    treebank_tag = pos_tag(word)[0][1]  # get only pos
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    if len(word) > 3 and word[-3:] == "ing":
        return 'v'
    else:
        return 'n'  # noun is default

def get_lemma(word, tag):
    return lemmatizer.lemmatize(word, tag)

def foo(word):
    return lemmatizer.lemmatize(word, get_wordnet_tag(word))

def bar(x):
    return (x[0], x[1]/text_len)

def make_dict():
    global text_len
    c = 1
    for root, subdirs, files in os.walk(input_folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            print("#{}  File: {}".format(c ,file_path))
            t = time()
            with open(file_path) as f:
                data = f.read()
                data = regex.sub(' ', data).lower().split(' ')
                valid_text = [el for el in data if el != '' and isEnglish.check(el)]
                english_ration = len(valid_text)/len(data)
                if english_ration < allowed_ratio:     # if english text > allowed_ratio%
                    with open('log.txt', 'a') as er:
                        er.write("#{}   1   NonEn   {}  {}\n".format(c, english_ration, file))
                    continue

                # for word in valid_text:
                #     tag = get_wordnet_tag(word)
                #     word = lemmatizer.lemmatize(word, tag)
                text_len = len(valid_text)
                with open(os.path.join(output_folder_path, file), 'w') as r:
                    print(dict(map(bar,
                                   collections.Counter(map(foo, valid_text)).items())),
                          file=r)

                print("Time: {}".format(time()-t))
                # word_dict = dict(collections.Counter(map(foo, valid_text)))#valid_text))   # count words in text
                #
                # for k, v in word_dict.items():
                #     word_dict[k] = v/len(valid_text)    # calc words' frequency
                #
                # out_file_path = os.path.join(output_folder_path, file)
                # r = open(out_file_path, 'w')
                # r.write(str(word_dict))
                # r.close()
            c += 1


def test():
    lemma = WordNetLemmatizer()
    isEnglish = enchant.Dict('en_US')
    regex = re.compile(",")
    text = """I was thinking I was thinking I was thinking I was thinking"""
    text2 = """the dog has been captured by alians"""

    t = time()
    text = regex.sub(' ', text).lower().split(' ')
    valid_text = [el for el in text if el != '' and isEnglish.check(el)]
    # for word in text:
    #     tag = get_wordnet_tag(word)
    #     get_lemma(word, tag)
    def foo(word):
        return get_lemma(word, get_wordnet_tag(word))
    lemmas = list(map(foo, text))
    print(time()-t)

    t = time()
    text2 = regex.sub(' ', text2).lower().split(' ')
    valid_text = [el for el in text2 if el != '' and isEnglish.check(el)]
    # for word in text2:
    #     tag = get_wordnet_tag(word)
    #     get_lemma(word, tag)
    lemmas2  = list(map(foo, text2))
    print(time()-t)

if __name__ == "__main__":
    make_dict()
    # test()
