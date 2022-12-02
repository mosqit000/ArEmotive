from pyfuseki import FusekiUpdate
from pyfuseki.rdf import NameSpace
from rdflib import Graph, BNode, OWL, RDF, XSD, Literal

import ArEmotiveApp.ontologyHandler.Utils as utils
import ArEmotiveApp.ontologyHandler.main as twitterH
import  ArEmotiveApp.ontologyHandler.createNewProperties as partWeight
import ArEmotiveApp.ontologyHandler.huggingFace as hug
import ArEmotiveApp.ontologyHandler.stemmers as stm
import  ArEmotiveApp.ontologyHandler.trustFactor as tf
import ArEmotiveApp.ontologyHandler.config as conf
import ArEmotiveApp.ontologyHandler.dialectIdentifierThroughTranslation as ditt


def getoriginalWordTest():
    original = "يقال أن الاحتباس الحراري موجع للطبيعة و مضر بالمجتمع و مو منيح"
    stemmed = ["ٱحتباس", "حراري", "مضر", "طبيع"]
    originalArray = original.split()
    tokenized = twitterH.tokenize(originalArray)
    print(tokenized)
    for item in tokenized:
        print(stm.longestWordStemming(item))
    for word in stemmed:
         for oldWord in originalArray:
            testArray = []
            testArray.append(oldWord)
            tokenized = twitterH.tokenize(testArray)
            print("word is : "+ word)
            print("tokenized : "+ stm.longestWordStemming(tokenized))
            if word == oldWord or word == stm.longestWordStemming(oldWord) or word == stm.longestWordStemming(tokenized):
                print("new word is : " + word)
                print("original is : " + oldWord)
                break




def updateGraphWithMatchFromHuggingMultiNew(word):
    classificationMode = conf.CLASSIFICATIONMODE
    myLabels = ['متعة', 'غضب', 'خوف', 'حب', 'تفهم', 'رضا', 'تطلع', 'اهتمام', 'مفاجآة', 'اشمئزاز', 'محايد', 'لا_مبالاة',
                'حزن']
    prefix = "http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#"
    newClassStringDict = hug.classifyMultiClass(word, myLabels,classificationMode) # here it returned a dict
    weightRelationship = "قيمتها"
    weightRelationshipUri = NameSpace(prefix + weightRelationship).to_uri()
    partialWeightRelationship = NameSpace(
        "http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#partialWeight").to_uri()
    emotionClassURI = NameSpace(
        "http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#العاطفة").to_uri()
    sourceRelationship = NameSpace(prefix+"source").to_uri()
    SourceNameRelationship = NameSpace(prefix+"sourceName").to_uri()
    huggingFaceLocal = NameSpace(prefix+"hugggingFace-Local").to_uri()
    dataRelationship = NameSpace(prefix+"data").to_uri()
    graph = Graph()
    trustFactorList = []
    for obj in newClassStringDict:
        newClassString = obj
        print("_+_+_++_+_+_+_+_++_+_++_+")
        print(newClassString)
        newTrustFactor = tf.getAppropriateTrustFactor(newClassString)
        trustFactorList.append(int(newTrustFactor))
        newNodeString = NameSpace(prefix + word).to_uri()
        newClass = NameSpace(prefix + newClassString).to_uri()
        graph.add((newNodeString,sourceRelationship,BNode(0)))
        graph.add((BNode(0),SourceNameRelationship,huggingFaceLocal))
        graph.add((BNode(0), dataRelationship, BNode(1)))
        graph.add((BNode(1), RDF.type, OWL.NamedIndividual))
        graph.add((BNode(1), RDF.type, newClass))
        partWeight.createPartialWeightRelationship(word,obj,int(newTrustFactor))
        graph.add((BNode(1),partialWeightRelationship,BNode(2)))
        graph.add((BNode(2),emotionClassURI,NameSpace(prefix+obj).to_uri()))
        graph.add((BNode(2),weightRelationshipUri, Literal(newTrustFactor, datatype=XSD.int)))

    relationship = "http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#قيمتها"
    relationshipURI = NameSpace(relationship).to_uri()
    confidenceProperty = prefix + "confidence"  # ----- as long as it is from hugging so the conf is 50%
    # ---- may change if update is from other source
    confidencePropertyURI = NameSpace(confidenceProperty).to_uri()
    hFConfLiter = Literal("50", datatype=XSD.int)
    graph.add((BNode(1), confidencePropertyURI, hFConfLiter))
    newTrustFactor = int(sum(trustFactorList)/len(trustFactorList))
    literal = Literal(newTrustFactor, datatype=XSD.int) # new trust factor for all classes matched
    graph.add((BNode(1), relationshipURI, literal))
    dialect = ditt.checkDialect(word)
    dialectURI = NameSpace(prefix + dialect).to_uri()
    dialectRelationShip = "ينتمي_للغة"
    dialectRelationShipURI = NameSpace(prefix + dialectRelationShip).to_uri()
    graph.add((BNode(1), dialectRelationShipURI, dialectURI))
    fuseki = FusekiUpdate('http://localhost:3030', 'ArEmotive')
    fuseki.insert_graph(graph)

import arabicstopwords.arabicstopwords as stp
