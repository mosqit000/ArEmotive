import requests

import ArEmotiveApp.ontologyHandler.stemmers as stemmers


def getTweetsAsText(list, mode="Truncfalse"):
    result = []
    for tweet in list:
        tweetString = str(tweet)
        if mode == "TruncTrue":
            start = tweetString.find(", 'text':") + len(", 'text':")
            end = tweetString.find(", 'truncated':")
        else:
            start = tweetString.find("'full_text':") + len("'full_text':")
            end = tweetString.find(", 'truncated':")
        substring = tweetString[start:end]
        result.append(substring)
    return result


def getTweetText(tweets):
    result = []
    for tweet in tweets:
        for element in tweet:

            if element['truncated'] == "true":
                result.append(element['text'])
            else:
                result.append(element['full_text'])


import ArEmotiveApp.ontologyHandler.main as twitterHandler


def removeNERRecognizedWords(sentence):
    recognizedWords = twitterHandler.NERRecognize(sentence)
    for word in recognizedWords:
        if word[1] != 'O':
            recognizedWords.remove(word)
            print("Named Entity Word found : "+str(word))
    return recognizedWords


# to delete
deleteQuery = """
DELETE WHERE{
<http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#confidence> ?pred ?obj
} 
"""


def runDeleteQuery():
    url = "http://localhost:3030/ArEmotive/update"
    queryObject = {'query': 'update',
                   'update': deleteQuery}
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    x = requests.post(url, params=queryObject, headers=headers)
    print(x.text)


def getOriginalWord(list, word):
    for item in list:
        if stemmers.longestWordStemming(item) == word:
            print("get original :")
            print(stemmers.longestWordStemming(item))
            return item


def generateNewOldWordMap(list1, list2):
    map = {}
    i = 0
    for item in list1:
        map[stemmers.longestWordStemming(item)] = list2[i]
        i += 1
    return map


def getWordsFromURI(queryResult):
    words = []

    for obj in queryResult.convert()['results']['bindings']:
        print(obj)
        if obj['s']['type'] == "literal":
            words.append(obj['s']['value'])
        else:
            if obj['s']['type'] == "uri":  # keep in mind that this 's' here represents the variable in the sparql query
                # if the query is changed this parameter should be changed
                words.append(((obj['s']['value']).split("#"))[1])

        # if str(obj['s']['value']).__contains__("#"):
        #    words.append(((obj['s']['value']).split("#"))[1])
    return words
