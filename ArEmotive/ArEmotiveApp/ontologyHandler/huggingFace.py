from _testcapi import sequence_getitem

from transformers import pipeline
from transformers import AutoTokenizer, AutoModel

labels = ['حب', 'كره', 'سعادة', 'أمل', 'لا_مبالاة', 'حزن', 'غضب', 'حقد']
sequence = "الحياة ليست دائما صعبة"


def classify(sequence, labels, classificationMode):
    model_name = "joeddav/xlm-roberta-large-xnli"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    classifier = pipeline("zero-shot-classification", model=model_name, tokenizer=tokenizer,
                          use_fast=True)

    result = classifier(sequence, labels, multi_label=True)
    print(result)
    print("the sequence is : " + sequence)
    i = 0
    biggest_percentage = 0  # result["scores"][i]
    highest_match_label = 0  # result["labels"][i]
    resultMap = {}
    for label in result["labels"]:
        resultMap[label] = result["scores"][i]
        print(label + "percentage is :" + str(result["scores"][i]))
        if result["scores"][i] > biggest_percentage:
            biggest_percentage = result["scores"][i]
            highest_match_label = label
        i = i + 1
    print("dictionary is :")
    print(resultMap)
    sortedResultMap = sorted(resultMap.items(), key=lambda x: x[1])
    print("ordered dict :")
    print(sortedResultMap)
    print("top " + str(classificationMode) + " hits :")
    j = 0
    for i in reversed(sortedResultMap):
        print(i[0] + " , " + str(i[1]))
        j += 1
        if j >= classificationMode:
            break

    print("highest match is for label " + highest_match_label + " with percentage : " + str(biggest_percentage))
    return highest_match_label


# ----------------------#


def classifyMultiClass(sequence, labels, classificationMode):
    model_name = "joeddav/xlm-roberta-large-xnli"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    classifier = pipeline("zero-shot-classification", model=model_name, tokenizer=tokenizer,
                          use_fast=True)

    result = classifier(sequence, labels, multi_label=True)
    print(result)
    print("the sequence is : " + sequence)
    i = 0
    biggest_percentage = 0  # result["scores"][i]
    highest_match_label = 0  # result["labels"][i]
    resultMap = {}
    for label in result["labels"]:
        resultMap[label] = result["scores"][i]
        print(label + "percentage is :" + str(result["scores"][i]))
        if result["scores"][i] > biggest_percentage:
            biggest_percentage = result["scores"][i]
            highest_match_label = label
        i = i + 1
    print("dictionary is :")
    print(resultMap)
    sortedResultMap = sorted(resultMap.items(), key=lambda x: x[1])
    print("ordered dict :")
    print(sortedResultMap)
    topHits = {}
    print("top " + str(classificationMode) + " hits :")
    j = 0
    for i in reversed(sortedResultMap):
        j += 1
        topHits[i[0]] = "{:.2f}".format(i[1])
        if j >= classificationMode:
            break

    print("highest match is for label " + highest_match_label + " with percentage : " + str(biggest_percentage))
    print("top hits : from classifyMultiClass :")
    print(topHits)
    return topHits


def classifyMortiz(sequence, labels, classificationMode):
    model_name = "MoritzLaurer/mDeBERTa-v3-base-mnli-xnli"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    classifier = pipeline("zero-shot-classification", model=model_name, tokenizer=tokenizer,
                          use_fast=True)

    result = classifier(sequence, labels, multi_label=True)
    print(result)
    print("the sequence is : " + sequence)
    i = 0
    biggest_percentage = 0  # result["scores"][i]
    highest_match_label = 0  # result["labels"][i]
    resultMap = {}
    for label in result["labels"]:
        resultMap[label] = result["scores"][i]
        print(label + "percentage is :" + str(result["scores"][i]))
        if result["scores"][i] > biggest_percentage:
            biggest_percentage = result["scores"][i]
            highest_match_label = label
        i = i + 1
    print("dictionary is :")
    print(resultMap)
    sortedResultMap = sorted(resultMap.items(), key=lambda x: x[1])
    print("ordered dict :")
    print(sortedResultMap)
    print("top " + str(classificationMode) + " hits :")
    j = 0
    for i in reversed(sortedResultMap):
        print(i[0] + " , " + str(i[1]))
        j += 1
        if j >= classificationMode:
            break
    returnedDict = {}
    print("highest match is for label " + highest_match_label + " with percentage : " + str(biggest_percentage))
    # for obj in reversed(sortedResultMap):
    #     returnedDict[obj] = obj[1]
    return highest_match_label
    # sortedResultMap = sorted(resultMap.items(), key=lambda x: x[1])
    # print("ordered dict :")
    # print(sortedResultMap)
    # topHits = {}
    # print("top "+str(classificationMode)+" hits :")
    # j = 0
    # for i in reversed(sortedResultMap):
    #    j += 1
    #    topHits[i[0]] = "{:.2f}".format(i[1])
    #    if j >= classificationMode:
    #        break

    # print("highest match is for label " + highest_match_label + " with percentage : " + str(biggest_percentage))
    # print("top hits : from classifyMultiClass :")
    # print(topHits)
    # return topHits


# classifyMultiClass("مؤذي",labels,3)

# ---------------------#
# from transformers import AutoTokenizer, AutoModel

# model_name = "joeddav/xlm-roberta-large-xnli"
# "MoritzLaurer/mDeBERTa-v3-base-mnli-xnli"#"joeddav/xlm-roberta-large-xnli"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModel.from_pretrained(model_name)
# from transformers import pipeline

# classifier = pipeline("zero-shot-classification", model=model_name, tokenizer=tokenizer, use_fast=True)

# from os import name
# from transformers.models.auto.auto_factory import FROM_PRETRAINED_TORCH_DOCSTRING

# sequence_to_classify = "الحياة ليست دائما صعبة"
# candidate_labels = ["حب", "كره"]
# results = classifier(sequence_to_classify, candidate_labels, multi_label=True)
# i = 0
# for label in results['labels']:
#    print(label + " has score")
#    print(results["scores"][i])
#    i = i + 1


def classifyMortizMulti(sequence, labels, classificationMode):
    model_name = "MoritzLaurer/mDeBERTa-v3-base-mnli-xnli"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    classifier = pipeline("zero-shot-classification", model=model_name, tokenizer=tokenizer,
                          use_fast=True)

    result = classifier(sequence, labels, multi_label=True)
    i = 0
    biggest_percentage = 0  # result["scores"][i]
    highest_match_label = 0  # result["labels"][i]
    resultMap = {}
    for label in result["labels"]:
        resultMap[label] = result["scores"][i]
        if result["scores"][i] > biggest_percentage:
            biggest_percentage = result["scores"][i]
            highest_match_label = label
        i = i + 1
    sortedResultMap = sorted(resultMap.items(), key=lambda x: x[1])
    topHits = {}
    j = 0
    for i in reversed(sortedResultMap):
        j += 1
        topHits[i[0]] = "{:.2f}".format(i[1])
        if j >= classificationMode:
            break


    print("top hits for : "+ sequence)
    print(topHits)
    return topHits
