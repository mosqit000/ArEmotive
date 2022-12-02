import tweepy
import json
import csv
from datetime import date
from camel_tools.utils.charsets import AR_LETTERS_CHARSET
import io
import datetime
import pandas as pd
import random

auth = tweepy.AppAuthHandler("0YmjN1VQdBQZCSHCe3WuJEJnq", "6H1L65TvwefrJs14hDq2lmfVDify6dgJCH0ICCvePRWr7HVVuS")
api = tweepy.API(auth)


def getTweetsToText(fileName, query, numberOfTweets):
    myfile = open(fileName, "a", encoding="UTF-8")
    for tweet in tweepy.Cursor(api.search_tweets, q=query).items(numberOfTweets):
        myfile.write(tweet.text)
    myfile.close()
    print("done!")


# getTweetsToText("myTweets.txt","shiba inu",10)

def getTweetsToJSON(fileName, query, numberOfTweets):
    myjson = []
    with open(fileName, 'r', encoding="UTF-8") as outfile:
        try:
            data = json.load(outfile)
        except:
            # json.dump({[]},outfile)
            data = []
        # myjson.append(data)
        myjson = [*data]
    for tweet in tweepy.Cursor(api.search_tweets, q=query).items(numberOfTweets):
        myjson.append(tweet._json)
    with open(fileName, 'w', encoding="UTF-8") as outfile:
        json.dump(myjson, outfile)
    print("done!")
    # open('myTweets.jsonl')
    # with open('myTweets.jsonl', 'r') as json_file:
    #     json_list = list(json_file)

    #     for json_str in json_list:
    #         result = json.loads(json_str)
    #         print(f"result: {result}")
    #         print(isinstance(result, dict))
    #     json_file.close()
    # print("done!")


# getTweetsToJSON('myTweets.json',"Possible",5)

def getTweetsToCSV(fileName, query, numberOfTweets):
    csvFile = open(fileName, 'a', encoding="utf-8")
    csvWriter = csv.writer(csvFile)
    for tweet in tweepy.Cursor(api.search_tweets, query).items(numberOfTweets):
        csvWriter.writerow(['{}\t{}\t{}'.format(tweet.created_at, tweet.user.screen_name, tweet.text)])
        # print('{}\t{}\t{}'.format(tweet.created_at,tweet.user.screen_name,tweet.text))
    csvFile.close()


# getTweetsToCSV("result1.csv","اوكرانيا",15)

def getTweetsLocal(query, numberOfTweets):
    tweets = []
    for tweet in tweepy.Cursor(api.search_tweets, q=query, lang="ar", tweet_mode="extended") \
            .items(numberOfTweets):
        tweets.append(tweet)
    return tweets


def readTweetsFromText(fileName):
    tweets = open(fileName, 'r', encoding="utf-8")
    for tweet in tweets:
        print(tweet)


def getCommentsFromFile(fileName, start: 0, end):
    commentsfile = open(fileName, 'r', encoding="utf-8")
    index = 0
    requiredComments = []
    for comment in commentsfile:
        if index in range(start, end):
            requiredComments.append({'comment': comment[comment.find("<text>") + 6:comment.find("</text>")],
                                     'date': comment[comment.find("<date>") + 6:comment.find("</date>")],
                                     'location': comment[comment.find("<location>") + 6:comment.find("</location>")]})
        index = index + 1
    return requiredComments


query = "جريمة"


# getTweetsToText("myTweets.txt",query,10)
# readTweetsFromText("myTweets.txt")

# def readTweetsFromJSON():
#    with open("myTweets.json", encoding="UTF-8") as json_file:
#        cursor = 0
#        for line_number, line in enumerate(json_file):
#            print ("Processing line", line_number + 1,"at cursor index:", cursor)
#            line_as_file = io.StringIO(line)
#            # Use a new parser for each line
#            json_parser = ijson.parse(line_as_file)
#            for prefix, type, value in json_parser:
#                print ("prefix=",prefix, "type=",type, "value=",value)
#            cursor += len(line)
# readTweetsFromJSON();

def readTweetsFromCSV(numberOfTweetsToOutput):
    f = open("result1.csv", newline='')
    csv_reader = csv.reader(f)
    for item in range(0, 2 * numberOfTweetsToOutput):
        print(next(csv_reader))


# readTweetsFromCSV(5)


def readTweetsFromJSON():
    myjson = []
    with open("myTweets.json", 'r', encoding="UTF-8") as outfile:
        try:
            data = json.load(outfile)
        except:
            data = []
    myjson = [*data]
    print(myjson[1])


# readTweetsFromJSON()

from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer


def analyze(word):
    db = MorphologyDB.builtin_db()
    analyzer = Analyzer(db, 'NOAN_PROP')
    analyses = analyzer.analyze(word)
    print('morphology analyzer started')
    print('for word : ' + word)
    print(analyses)
    print('----------------')


from camel_tools.sentiment import SentimentAnalyzer

sentences = [
    'تعبان',
    'الحياة ليست دائما صعبة',
    'لعّيب'
]


def getDate(word):
    # TODO if tweet or comment has date the date should be from them
    start = datetime.datetime.strptime("01-01-2021", "%d-%m-%Y")
    end = date.today().strftime("%d-%m-%Y")
    date_generated = pd.date_range(start, end)
    date_generated.strftime("%Y-%m-%d")
    newDateDay = random.randint(1, 28)
    newDateMonth = random.randint(1, 12)
    newDateYear = random.randint(2020, date.today().year)
    newDate = str(newDateDay) + "-" + str(newDateMonth) + "-" + str(newDateYear)
    # formattedDate = newDate.strftime("%d-%m-%Y")
    newDate = datetime.datetime.strptime(newDate, "%d-%m-%Y")
    newDate.strftime("%Y-%m-%d")
    return newDate


def getTweetID(word, tweetList):
    tweetID = 0
    for tweet in tweetList:
        if word in tweet.split():
            return tweetID
        tweetID += 1


def getTimeChartData():
    pass


def getLocation(word):
    coordinates = []
    coordinates.append((34.8149145, 39.0464523))
    x = round(random.uniform(-5, 5), 5)
    y = round(random.uniform(-5, 5), 5)
    location = (34.8149145 + x,
                39.0464523 + y)
    return location


def analyzeSentimentWords(sentence):
    sentenceList = sentence.split(" ")
    sa = SentimentAnalyzer.pretrained()
    positivePolarity = 0
    negativePolarity = 0
    neutralPolarity = 0
    for word in sentenceList:
        print(word)
        result = sa.predict(word)
        print(result)
        if result[0] == "positive":
            positivePolarity = positivePolarity + 1
        if result[0] == "negative":
            negativePolarity = negativePolarity + 1
        else:
            neutralPolarity = neutralPolarity + 1
    return {
        'positivePolarity': positivePolarity,
        'negativePolarity': negativePolarity,
        'neutralPolarity': neutralPolarity
    }


def analyzeSentiment(sentences):
    sa = SentimentAnalyzer.pretrained()
    sentiments = sa.predict(sentences)
    return sentiments


from camel_tools.ner import NERecognizer

sentence = 'إمارة أبوظبي هي إحدى إمارات دولة الإمارات العربية المتحدة السبع .'.split()


def NERRecognize(sentence):
    ner = NERecognizer.pretrained()
    labels = ner.predict_sentence(sentence)
    print(list(zip(sentence, labels)))
    return list(zip(sentence, labels))


from camel_tools.disambig.mle import MLEDisambiguator

sentence = ['سوف', 'نقرأ', 'الكتب']


def disambiguate(sentence):
    mle = MLEDisambiguator.pretrained()
    disambig = mle.disambiguate(sentence)
    diacritized = [d.analyses[0].analysis['diac'] for d in disambig]
    print('MLEDisambiguator started : diacritization')
    print('original : سوف نقرأ الكتب')
    print(' '.join(diacritized))
    print('--------------')


from camel_tools.disambig.mle import MLEDisambiguator
from camel_tools.tokenizers.morphological import MorphologicalTokenizer

sentence_msa = ['فتنفست', 'الصعداء']


def tokenize(sentence_msa):
    mle_msa = MLEDisambiguator.pretrained('calima-msa-r13')
    msa_bw_tokenizer = MorphologicalTokenizer(disambiguator=mle_msa, scheme='bwtok')
    msa_bw_tok = msa_bw_tokenizer.tokenize(sentence_msa)
    print('BW tokenization (MSA):', msa_bw_tok)
    print('----------------')
    return msa_bw_tok
