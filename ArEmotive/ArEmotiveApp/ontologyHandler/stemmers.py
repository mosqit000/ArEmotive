from snowballstemmer import stemmer
import re

def stem(word):  # snowball
    ar_stemmer = stemmer("arabic")
    result = ar_stemmer.stemWord(word)
    return result


# utilities

# import seaborn as sns #text processing & sentiment analysis
# from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
# from afinn import Afinn
import unicodedata as ud
import camel_tools as ct
from nltk.stem.isri import ISRIStemmer


# from ar_wordcloud import ArabicWordCloud
# from sklearn.metrics import classification_report, accuracy_score

def ISRIStem(text):  # ISRI needs work
    processedText = []
    st = ISRIStemmer()
    for t in text:
        t = ''.join(c for c in t if ud.category(c) == 'Lo' or ud.category(c) == 'Nd' or c == ' ')
        commentwords = ''
        for word in t.split():
            # Checking if the word is a stopword.
            if word not in stopwords:
                if len(word) > 1:
                    # Lemmatizing the word.
                    word = st.suf32(word)
                    commentwords += (word + ' ')
                    processedText.append(commentwords)

    return processedText


def longestWordStemming(word): # TODO why remove english here
    testString = max((str(word)).split("+"), key=len).strip(')[](#\\n_.:"@rRtT,'
                                                      ';123456780'
                                                      '-9azxcvbnmsdfghjklqwertyuiopABCDEFGHIJKLMNOPQRSTUVWXYZ!%^&*')\
        .replace(
        "'",
        "").replace(
        '"', "")
    return re.sub("[^\u0621-\u064A]", "", testString)
