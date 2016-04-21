from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk import pos_tag
from nltk.corpus import wordnet
import enchant
import collections
import re
import os


stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()
isEnglish = enchant.Dict('en_US')
allowed_ratio = 0.55


regex = re.compile( '(\\n|\?|_|\[|\]|{|}|,|\.|"|-|!|@|#|\$|%|\^|&|\*|\(|\)|~|\||\'|/|\\\\|;|:|<|>)')

input_folder_path = os.path.join(os.getcwd(), "parsed")
output_folder_path = os.path.join(os.getcwd(), "featured")

def get_wordnet_pos(word):
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


def make_dict():
    c = 1
    for root, subdirs, files in os.walk(input_folder_path):
        for file in files:
            try:
                file_path = os.path.join(root, file)
                print("#{}  File: {}".format(c ,file_path))
                with open(file_path) as f:

                    data = f.read()
                    data = regex.sub(' ', data).lower().split(' ')
                    valid_text = [el for el in data if el != '' and isEnglish.check(el)]
                    english_ration = len(valid_text)/len(data)
                    if english_ration > allowed_ratio:     # if english text > allowed_ratio%
                        for word in valid_text:
                            tag = get_wordnet_pos(word)
                            word = lemmatizer.lemmatize(word, tag)


                        word_dict = dict(collections.Counter(valid_text))   # count words in text

                        for k, v in word_dict.items():
                            word_dict[k] = v/len(valid_text)    # calc words' frequency

                        out_file_path = os.path.join(output_folder_path, file)
                        r = open(out_file_path, 'w')
                        r.write(str(word_dict))
                        r.close()

                        er = open('log.txt', 'a')
                        er.write("#{}   0   {}  {}\n".format(c, english_ration, file))
                        er.close()

                    else:
                        er = open('log.txt', 'a')
                        er.write("#{}   1   NonEn   {}  {}\n".format(c, english_ration, file))
                        er.close()

            except:
                er = open('log.txt', 'a')
                er.write("#{}   1   Exc   {}\n".format(c, file))
                er.close()
                continue
            c += 1


def test():

    text = """I was thinking 雷德驤，長安人，太 що я не такий"""

    text = regex.sub(' ', text).lower().split(' ')

    valid_text = [el for el in text if el != '' and isEnglish.check(el)]

    print(str(len(text)) + " vs " + len(valid_text).__str__())
    print(text)
    print(valid_text)

    for word in text:
        lemma = lemmatizer.lemmatize(word, get_wordnet_pos(word))
        print(lemma)


if __name__ == "__main__":
    make_dict()
    # test()
