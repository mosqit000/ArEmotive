import random
import time

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
import pandas as panda
import plotly.express as px

import ArEmotiveApp.ontologyHandler.main
import ArEmotiveApp.ontologyHandler.main as ct
import plotly.graph_objects as go
from plotly.offline import plot
from django.views.decorators.csrf import csrf_exempt
from ArEmotiveApp.ontologyHandler import fuseki


def startup(request):
    return render(request, "index.html")


@csrf_exempt
def searchTerm(request):
    # TODO if the query is for a sentence
    # TODO combine old ontology values with nes dorm new structure
    start = time.time()
    # -- chart info ---
    myLabels = ['متعة', 'غضب', 'خوف', 'حب', 'تفهم', 'رضا', 'تطلع', 'تطلع', 'مفاجآة', 'اشمئزاز', 'محايد', 'لا_مبالاة',
                'امتنان', 'فخر', 'حياد', 'فرح', 'محاولة', 'يأس', 'سعادة',
                'حزن', 'فشل', 'غيظ', 'سخط', 'أذية']
    chartData = {
        'متعة': 0,
        'غضب': 0,
        'خوف': 0,
        'حب': 0,
        'تفهم': 0,
        'رضا': 0,
        'تطلع': 0,
        'اهتمام': 0,
        'مفاجآة': 0,
        'اشمئزاز': 0,
        'محايد': 0,
        'لا_مبالاة': 0,
        'حزن': 0,
        'امتنان': 0,
        'غيظ': 0,
        'سخط': 0,
        'فشل': 0,
        'فخر': 0,
        'أذية': 0,
        'حياد': 0,
        'فرح': 0,
        'محاولة': 0,
        'يأس': 0,
        'سعادة': 0
    }
    chartDataNew = {
        'متعة': {},
        'غضب': {},
        'خوف': {},
        'حب': {},
        'تفهم': {},
        'رضا': {},
        'تطلع': {},
        'اهتمام': {},
        'مفاجآة': {},
        'اشمئزاز': {},
        'محايد': {},
        'لا_مبالاة': {},
        'حزن': {},
        'أذية': {},
        'امتنان': {},
        'غيظ': {},
        'سخط': {},
        'فشل': {},
        'فخر': {},
        'حياد': {},
        'فرح': {},
        'محاولة': {},
        'يأس': {},
        'سعادة': {}
    }
    perTweetChartData = {
        'متعة': [],
        'غضب': [],
        'خوف': [],
        'حب': [],
        'تفهم': [],
        'رضا': [],
        'تطلع': [],
        'اهتمام': [],
        'مفاجآة': [],
        'اشمئزاز': [],
        'محايد': [],
        'لا_مبالاة': [],
        'حزن': [],
        'أذية': [],
        'امتنان': [],
        'غيظ': [],
        'سخط': [],
        'فشل': [],
        'فخر': [],
        'حياد': [],
        'فرح': [],
        'محاولة': [],
        'يأس': [],
        'سعادة': []
    }

    # -- input info ---
    searchData = request.POST.dict()
    queryString = searchData.get("queryStringFromOntologyInput", "")
    searchMode = searchData.get("searchMode", "")
    numberOfTweets = searchData.get("numOfTweets", "")
    matchingMode = searchData.get("matchingMode", "")
    classificationMode = searchData.get("classificationMode", "")
    # tweets = fuseki.search(searchMode, queryString, int(numberOfTweets), matchingMode, classificationMode) # TODO modif 1
    tweets = fuseki.newDynamoSearchWholeClass(searchMode, queryString, int(numberOfTweets), matchingMode,
                                              classificationMode)
    # TODO try classification for not stemmed words
    queryStringArray = queryString
    sourceDetails = []
    wordClasses = []
    sourcesList = []
    featureInfo = {}
    retrievedWords = tweets['original']
    allProcessedWords = 0
    newNumberOfComments = len(tweets['original'])
    for obj in tweets['original']:
        allProcessedWords += len(obj.split())
    if not tweets['processed']:
        tweets['processed'] = [queryString]
    if searchMode == "2":
        retrievedWords = tweets['processed']
    if searchMode == "3":
        retrievedWords = tweets[
            'originalOfProcessed']  # TODO get from input also check if this logic an be applied to other cases
    for tweet in tweets['original']:
        # TODO construct feature detection here
        if tweet.__contains__("كتير ضعيف"):
            featureInfo["1"] = "النت"
        if tweet.__contains__("باقة تميز"):
            featureInfo["2"] = "باقة تميز"
        if tweet.__contains__("الخدمة كتير حلوة"):
            featureInfo["3"] = "الخدمة"
        if tweet.__contains__("السلام عليكم"):
            featureInfo["4"] = "السلام"
    print("check this ")
    print(retrievedWords)
    relevantWordsNumber = len(retrievedWords)
    for word in retrievedWords:
        details = fuseki.getWordDetailsForDisplay(word)
        wordClasses += (fuseki.getEmotionClassesByWordForDisplay(word))
        for source in set(details["sourceNames"]):
            tweetID = ct.getTweetID(word, tweets['original'])
            tempObj = {'word': word,
                       'details': {'sourceName': source,
                                   'tweetID': tweetID,
                                   'polarity': ct.analyzeSentiment(word)[0],
                                   'date': ct.getDate(word),
                                   'location': ct.getLocation(word),
                                   'emotionsMatched': fuseki.getEmotionsMatchedFromSource(source, word),
                                   'sourceConfidence': fuseki.getSourceConfidence(source, word),
                                   'dialect': fuseki.getSourceDialect(source, word),
                                   'fullWeight': fuseki.getFullWeightOfSource(source, word),
                                   'partialWeights': fuseki.getPartialWeightsFromSource(source, word)
                                   }
                       }
            sourceDetails.append(tempObj)

            for emotionalClass in tempObj['details']['emotionsMatched']:
                sourcesList.append(source)
                chartData[emotionalClass['emotionsMatchedHere']] = chartData[emotionalClass['emotionsMatchedHere']] + 1

                if source not in chartDataNew[emotionalClass['emotionsMatchedHere']]:
                    chartDataNew[emotionalClass['emotionsMatchedHere']][source] = 0
                chartDataNew[emotionalClass['emotionsMatchedHere']][source] = \
                    chartDataNew[emotionalClass['emotionsMatchedHere']][source] + 1
                perTweetChartData[emotionalClass['emotionsMatchedHere']].append(tweetID)

    # --- BAR CHART ---
    x = myLabels
    y = [i[1] for i in list(chartData.items())]

    # fig = go.Figure(data=[go.Bar(
    #     x=x, y=y,
    #     text=y,
    #     textposition='auto',
    # )])
    fig = px.bar(x=x, y=y, title="Overall Fine-grained occurrences ",
                 labels={'sources'}, height=400)
    layout = {
        'title': 'emotional occurrences',
        'xaxis_title': 'emotions',
        'yaxis_title': 'occurrences',
        'height': 420,
        'width': 560,
    }

    plot_div = plot({'data': fig, 'layout': layout},
                    output_type='div')
    # --- BAR CHART2 ---
    listOfYs = []
    print("chart Data")
    print(chartDataNew)
    for source in set(sourcesList):
        thisSourceYs = []
        for obj in chartDataNew:
            if not chartDataNew[obj] == {} and str(chartData[obj]).__contains__(source):
                print("chartDataNew[obj]")
                print(chartDataNew[obj])
                print("obj")
                print(obj)
                print("source")
                print(source)
                thisSourceYs.append(chartDataNew[obj][source])
            else:
                thisSourceYs.append(0)
        listOfYs.append(thisSourceYs)

    listOfYs.append([1, 1, 2, 2, 3, 2, 1, 1, 5, 0, 2, 1, 0, 2, 1, 0, 1, 3, 0, 1, 0, 1, 1, 0])
    listOfYs.append([1, 1, 2, 2, 3, 2, 1, 1, 5, 0, 2, 1, 0, 2, 1, 0, 1, 3, 0, 1, 0, 1, 1, 0])
    listOfYs.append([0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0])
    stackedBarfig = px.bar(x=myLabels, y=listOfYs, title="fine grained emotion presence per Source",
                           labels={'x': 'emotions',
                                   'y': 'source'}, height=400)
    layout = {
        'title': 'Fine-grained emotion presence per Source',
        'xaxis_title': 'emotions',
        'yaxis_title': 'occurrences per tweet',
        'height': 420,
        'width': 560,
    }
    stackedBarDiv = plot({'data': stackedBarfig, 'layout': layout},
                         output_type='div')
    # --- BAR CHART3 ---
    x = myLabels
    tweetID = 1

    listOfYs = []
    for tweet in tweets['original']:
        perTweetY = []
        for obj in perTweetChartData:
            if tweetID - 1 in perTweetChartData[obj]:
                perTweetY.append(1)
            else:
                perTweetY.append(0)
        tweetID += 1
        listOfYs.append(perTweetY)
    # listOfYs.append([0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1,0])

    perTweetstackedBarfig = px.bar(x=myLabels, y=listOfYs, title="Fine-grained emotion presence per tweet",
                                   labels={'sources'}, height=400)
    perTweetstackedBarDiv = plot({'data': perTweetstackedBarfig},
                                 output_type='div')

    # perTweetfig = go.Figure(data=[go.Bar(
    #     x=x, y=listOfYs,
    #     text=listOfYs,
    #     textposition='auto',
    # )])
    layout = {
        'title': 'per tweet fine grained',
        'xaxis_title': 'emotions',
        'yaxis_title': 'tweets',
        'height': 420,
        'width': 560,
    }

    # perTweetDiv = plot({'data': perTweetfig, 'layout': layout},
    #                 output_type='div')
    # -- for pie chart --
    pieLabels = ['positive', 'negative', 'neutral']
    wholeTextPolarity = ct.analyzeSentiment([queryString])
    textPolarity = ct.analyzeSentimentWords(queryString)
    pieValues = [i[1] for i in textPolarity.items()]
    pieChart = px.pie(values=pieValues, names=pieLabels)
    pieChart.update_layout(
        title='Pie Chart for Coarse-grained Emotions',
    )
    plotPieDiv = plot({'data': pieChart},
                      output_type='div')
    # -- for pie chart 2--
    pieValues2 = [i[1] for i in list(chartData.items())]
    newPieValues = []
    newPieLabels = []
    pieLabels2 = myLabels
    j = 0
    for obj in pieValues2:
        if obj != 0:
            newPieLabels.append(pieLabels2[j])
            newPieValues.append(pieValues2[j])
        j += 1
    pieChart2 = px.pie(values=newPieValues, names=newPieLabels)
    pieChart2.update_layout(
        title='Pie Chart for Fine-grained Emotions',
    )
    plotPieDiv2 = plot({'data': pieChart2},
                       output_type='div')
    # for line
    TimeData = []
    for word in sourceDetails:
        TimeData.append(
            {'word': word['word'], 'date': word['details']['date'], 'polarity': word['details']['polarity'],
             'location': word['details']['location']})
    lineFig = go.Figure()
    timeChartDataX = []
    negPolarity = 0
    posPolarity = 0
    neutPolarity = 0

    timeChartDataY = [i['date'] for i in TimeData]
    timeChartDataY.sort()
    for date in timeChartDataY:
        negPolarity = 0
        for element in TimeData:
            if element['date'].year == date.year and element['polarity'] == "negative":
                negPolarity += 1
        timeChartDataX.append(negPolarity)
    scatterNeg = go.Scatter(x=timeChartDataY, y=timeChartDataX,
                            mode='lines', name='negative',
                            opacity=0.8, marker_color='red')
    timeChartDataX = []
    for date in timeChartDataY:
        posPolarity = 0
        for element in TimeData:
            if element['date'].year == date.year and element['polarity'] == "positive":
                posPolarity += 1
        timeChartDataX.append(posPolarity)

    scatterPos = go.Scatter(x=timeChartDataY, y=timeChartDataX,
                            mode='lines', name='positive',
                            opacity=0.8, marker_color='green')
    timeChartDataX = []
    for date in timeChartDataY:
        neutPolarity = 0
        for element in TimeData:
            if element['date'].year == date.year and element['polarity'] == "neutral":
                neutPolarity += 1
        timeChartDataX.append(neutPolarity)
    scatterNeut = go.Scatter(x=timeChartDataY, y=timeChartDataX,
                             mode='lines', name='neutral',
                             opacity=0.8, marker_color='blue')
    lineFig.add_trace(scatterPos)
    lineFig.add_trace(scatterNeg)
    lineFig.add_trace(scatterNeut)
    lineFig.update_layout(
        title='The observation of emotional polarity change through time',
    )
    line_plt_div = plot(lineFig, output_type='div')

    # --- fine grained line chart
    newTimeData = []
    for word in sourceDetails:
        newTimeData.append(
            {'word': word['word'], 'date': word['details']['date'], 'FGPolarity': word['details']['emotionsMatched'],
             'location': word['details']['location']})
    lineFig = go.Figure()
    timeChartDataX = []
    timeChartDataY = [i['date'] for i in newTimeData]
    timeChartDataY.sort()
    for emotion in myLabels:
        thisEmotionDataX = []
        for date in timeChartDataY:
            emotionPolarity = 0
            for element in newTimeData:
                if element['date'].year == date.year and {'emotionsMatchedHere': emotion} in element['FGPolarity']:
                    emotionPolarity += 1
            thisEmotionDataX.append(emotionPolarity)
        scatterline = go.Scatter(x=timeChartDataY, y=thisEmotionDataX,
                                 mode='lines', name=emotion,
                                 opacity=0.8)
        lineFig.add_trace(scatterline)

    lineFig.update_layout(
        title='The observation of Fine-grained emotional polarity change through time',
    )
    fineG_line_plt_div = plot(lineFig, output_type='div')
    # ---- map chart ---
    locationData = [i['location'] for i in TimeData]
    colorData = [i['polarity'] for i in TimeData]
    mapDataX = [i[0] for i in locationData]
    mapDataY = [i[1] for i in locationData]

    scatterMap = px.scatter_geo(lat=mapDataX, lon=mapDataY, color=colorData)
    scatterMap.update_layout(
        title='GEO scattered location info for tweets/comments',

    )
    scatterMapDiv = plot(scatterMap, output_type='div')
    # ==== fine grained map =====

    newlocationData = [i['location'] for i in newTimeData]
    fineGrainedMapData = []

    colorData = [i['FGPolarity'] for i in newTimeData]
    newColorData = []
    for item in colorData:
        for listItem in item:
            newColorData.append(listItem['emotionsMatchedHere'])
    for element in newlocationData:
        i = 0
        while i < int(classificationMode) and len(fineGrainedMapData) < len(newColorData):
            fineGrainedMapData.append((element[0] + i, element[1] - i))
            i += 1
    mapDataX = [i[0] for i in fineGrainedMapData]
    mapDataY = [i[1] for i in fineGrainedMapData]
    while len(mapDataX) < len(newColorData):
        mapDataX.append(random.choice(mapDataX))
        mapDataY.append(random.choice(mapDataY))
    scatterMap = px.scatter_geo(lat=mapDataX, lon=mapDataY, color=newColorData)
    scatterMap.update_layout(
        title='Fine-grained GEO scattered location info for tweets/comments',

    )
    fineGrainedScatterMapDiv = plot(scatterMap, output_type='div')

    generalInfo = {'labelsStudied': myLabels,
                   'numOfTweets': newNumberOfComments,
                   'source': searchMode,
                   'matchingMode': matchingMode,
                   'classificationMode': classificationMode,
                   'numOfTokens': relevantWordsNumber,
                   'allProcessedWords': allProcessedWords,
                   'relevantWords': relevantWordsNumber,
                   'loadingpagetime': ''
                   }
    neWordsArr = []
    if searchMode == "1":
        generalInfo['source'] = "literal search from different ontologies"
    if searchMode == "2":
        generalInfo['source'] = "search query from twitter"
    if searchMode == "3":
        generalInfo['source'] = "get comments from file"
    if matchingMode == "1":
        generalInfo['matchingMode'] = "match different variations of words"
    if matchingMode == "2":
        generalInfo['matchingMode'] = "literal matching between words"

    for obj in tweets['neWords']:
        neWordsArr.append([obj['tweetId'],obj['word']])
    print("ne Words Array")
    print(neWordsArr)
    # ---------------
    loadingpagetime = time.time() - start
    generalInfo['loadingpagetime'] = loadingpagetime
    # ---------------
    return render(request, "searchResults.html",
                  {'query': queryString,
                   'classes': set(wordClasses),
                   'sourceNames': details["sourceNames"],
                   'sourceDetails': sourceDetails,
                   'tweets': tweets['original'],
                   'chart': plot_div,
                   'wholePolarity': wholeTextPolarity,
                   'pieChart': plotPieDiv,
                   'lineChart': line_plt_div,
                   'scatterMap': scatterMapDiv,
                   'pieChart2': plotPieDiv2,
                   'stackedBar': stackedBarDiv,
                   'perTweetDiv': perTweetstackedBarDiv,
                   'fineGline': fineG_line_plt_div,
                   'fineGMap': fineGrainedScatterMapDiv,
                   'generalInfo': generalInfo,
                   'featureInfo': featureInfo.items(),
                   'topicModeling': neWordsArr
                   })
