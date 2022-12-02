# from SPARQLWrapper import QueryResult
import re

from pyfuseki import FusekiUpdate, FusekiQuery, AsyncFuseki, AsyncFusekiResp
from pyfuseki.rdf import rdf_prefix, NameSpace as ns, NameSpace
from rdflib import Graph, OWL, BNode
from pyfuseki.rdf import rdf_property
from rdflib import URIRef as uri, Literal
from rdflib import RDF
import asyncio
import pyfuseki
import requests
import ArEmotiveApp.ontologyHandler.dialectIdentifierThroughTranslation as ditt
import ArEmotiveApp.ontologyHandler.stemmers as stemmers
import ArEmotiveApp.ontologyHandler.config as conf

pyfuseki.register.register_common_prefix('http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#')


# in case of number needed to name a var we can use for example : one = NameSpace()
# http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#


# prefixes done the pyfuseki way
@rdf_prefix()
class RdfPrefix:
    emotionClass: ns
    emotionIndividual: ns
    ArEmotive: ns
    get: ns


# prefixes done manually
loveEmotionClass = NameSpace("http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#حب").to_uri()

rp = RdfPrefix()


# print(rp.ArEmotive['get'])

# define object & data properties
@rdf_property('http://example.org/')
class ObjectProperty:
    lang: uri


@rdf_property('http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#قيمتها')
class DataProperty:
    itsValue: uri


itsValue = NameSpace("http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#قيمتها")
langClass = NameSpace("http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#اللغة")
belongsToLang = NameSpace("http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#ينتمي_للغة")
bordemClass = NameSpace("http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#ملل").to_uri()

# instantiating the graph
g = Graph()

# creating Statements to use -as OWL or TTL-
dp = DataProperty()
# sentiment = rp.emotionClass['pyFusekiTest']
sentiment = NameSpace("http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#pyFusekiTest2").to_uri()
levantineTongue = NameSpace("http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#ينتمي_للغة")
statement = (sentiment, RDF.type, OWL.NamedIndividual)
stmt = (sentiment, RDF.type, bordemClass)
stmt2 = (sentiment, itsValue.to_uri(), Literal('9'))
stmt3 = (levantineTongue.to_uri(), RDF.type, langClass.to_uri())
stmt4 = (sentiment, belongsToLang.to_uri(), levantineTongue.to_uri())

# print(sentiment)
# print(statement)
# print(stmt)
# print(stmt2)
# print(stmt3)
# print(stmt4)

# adding these statements to the graph
g.add(statement)
g.add((sentiment, RDF.type, bordemClass))
g.add((sentiment, itsValue.to_uri(), Literal('9')))
g.add((levantineTongue.to_uri(), RDF.type, langClass.to_uri()))
g.add((sentiment, belongsToLang.to_uri(), levantineTongue.to_uri()))

# update the fuseki DataBase
fuseki = FusekiUpdate('http://localhost:3030', 'ArEmotive')


# fuseki.insert_graph(g)  # uncomment to modify the graph   <----

# to delete


def runDeleteQuery():
    deleteQuery = """
    DELETE WHERE{
    <http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#التقاليد> ?pred ?obj
    } 
    """
    url = "http://localhost:3030/ArEmotive/update"
    queryObject = {'query': 'update',
                   'update': deleteQuery}
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    x = requests.post(url, params=queryObject, headers=headers)
    print(x.text)


# runDeleteQuery()   # uncomment to execute delete
# to query from JENA
fuseki_query = FusekiQuery('http://localhost:3030', 'ArEmotive')  # this is the Sync way
async_fuseki = AsyncFuseki('http://localhost:3030', 'ArEmotive')  # this is the Async way

sparqlQuery = """
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT ?sub
WHERE {

 ?sub <http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#قيمتها> 
"7"^^xsd:int
  
}
"""


def runSyncQuery(query):
    query_result = fuseki_query.run_sparql(query)
    returnedQueryResult = query_result
    query_result.print_results()


# runSyncQuery(sparqlQuery)


def getNumberOfMatches(word):  # ---- should exclude the class "UnRecognizedEntities"
    # and many words throws an error  ------#
    query = """
    prefix untitled-ontology-12: <http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#> 
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix owl: <http://www.w3.org/2002/07/owl#>
 
  SELECT ?cnt 
{ { SELECT (COUNT(*) as ?cnt) { untitled-ontology-12:""" + word + """ a ?class } }
  union {
   untitled-ontology-12:""" + word + """ a ?class }
  
  filter(
?class != <http://www.w3.org/2002/07/owl#Class> &&
 ?class != <http://www.w3.org/2002/07/owl#NamedIndividual> 
)
}
    """
    query_result = fuseki_query.run_sparql(query)
    result = len(query_result.convert()['results']['bindings'])
    # if matchingMode == 1:
    #    testArr = []
    #    word = stemmers.longestWordStemming(twitterHandler.tokenize(testArr.append(word)))
    #    print("new word after mode changed")
    #    print(word)
    #    print("new query is : ")
    #    print(query)
    #    query_result = fuseki_query.run_sparql(query)
    #    result += len(query_result.convert()['results']['bindings'])
    return result


def runAsyncQuery():
    async def selectAllIndividualWithFactor():
        sparql_str = """
         PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    SELECT ?sub
    WHERE {
    
     ?sub <http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#قيمتها> 
    "7"^^xsd:int
      
    }
                """

        return await async_fuseki.query_sparql(sparql_str)

    print("async -----")
    query_resultAsync: AsyncFusekiResp
    query_resultAsync = asyncio.run(selectAllIndividualWithFactor())
    # print(query_resultAsync.resp)
    # print(query_resultAsync.to_bindingItemModels())
    for element in query_resultAsync.to_bindingItemModels():
        print(element['sub'])  # <----------------   # should only show URIs not additional info with it like type:Uri


# runAsyncQuery()

def getEmotionClassesByWord(word):
    print("the word is :" + word)
    return """
    prefix untitled-ontology-12: <http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#> 
select ?class  where
{
  untitled-ontology-12:""" + word + """ a ?class

FILTER( ?class != <http://www.w3.org/2002/07/owl#Class> &&
?class != <http://www.w3.org/2002/07/owl#NamedIndividual> &&
?class != <http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#UnrecognizedEntities>
) 
}
  
    """


def getEmotionClassesByWordForDisplay(word):
    query = """
    prefix untitled-ontology-12: <http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#> 
select ?class  where
{
  untitled-ontology-12:""" + word + """ a ?class

FILTER( ?class != <http://www.w3.org/2002/07/owl#Class> &&
?class != <http://www.w3.org/2002/07/owl#NamedIndividual> &&
?class != <http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#UnrecognizedEntities>
) 
}

    """
    # formattedQuery = str(query,encodings="UTF-8")
    query_result = fuseki_query.run_sparql(query)

    result = []
    # print(query_result.convert()['results']['bindings'])
    for element in query_result.convert()['results']['bindings']:
        result.append((element['class']['value']).split('#')[1])
    return result


# get details about a word from ontology
def getWordConfidence(word):
    print("the confidence is : ")
    query = """
        prefix owl: <http://www.w3.org/2002/07/owl#>
        prefix untitled-ontology-12: <http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#>
    SELECT   ?obj 
WHERE{ {
  untitled-ontology-12:""" + word + """ a owl:NamedIndividual .
  untitled-ontology-12:""" + word + """ untitled-ontology-12:source ?source.  
  ?source untitled-ontology-12:confidence ?obj
}
UNION {
untitled-ontology-12:""" + word + """
     untitled-ontology-12:confidence ?obj

  }}
    """

    runSyncQuery(query)


def getFullWeightOfWord(word):
    print("the weight is : ")
    query = """
   	prefix owl: <http://www.w3.org/2002/07/owl#>
    prefix untitled-ontology-12: <http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#>
    SELECT   
 ?weight 
WHERE{ {
  untitled-ontology-12:""" + word + """ a owl:NamedIndividual .
  untitled-ontology-12:""" + word + """ untitled-ontology-12:source ?obj.  
  ?obj untitled-ontology-12:قيمتها ?weight.
 
}
UNION  {untitled-ontology-12:""" + word + """
     untitled-ontology-12:قيمتها ?weight}

  }
    """
    runSyncQuery(query)


def getWeightsAndSourcesOfWord(word):
    query = """
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>    
	prefix owl: <http://www.w3.org/2002/07/owl#>
    prefix untitled-ontology-12: <http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#>
    SELECT    ?weight ?type
WHERE{ {
  untitled-ontology-12:""" + word + """ a owl:NamedIndividual .
  untitled-ontology-12:""" + word + """ untitled-ontology-12:source ?obj.  
  ?obj untitled-ontology-12:partialWeight ?pw.
    ?pw a ?type.
    ?pw untitled-ontology-12:قيمتها ?weight. 
}
UNION  {untitled-ontology-12:""" + word + """
     untitled-ontology-12:قيمتها ?obj}

  }
    
    """
    runSyncQuery(query)


def getWordDialect(word):
    print("the dialect is : ")
    query = """
    prefix untitled-ontology-12: <http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#>
       SELECT  ?obj WHERE {untitled-ontology-12:""" + word + """
        untitled-ontology-12:ينتمي_للغة ?obj}
       """
    runSyncQuery(query)


def getWordDialectAndSource(word):
    query = """
    	prefix owl: <http://www.w3.org/2002/07/owl#>
    prefix untitled-ontology-12: <http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#>
    SELECT   
?dialect ?source
WHERE{ {
  untitled-ontology-12:""" + word + """ a owl:NamedIndividual .
  untitled-ontology-12:""" + word + """ untitled-ontology-12:source ?obj.  
  ?obj untitled-ontology-12:ينتمي_للغة ?dialect.
 ?obj untitled-ontology-12:sourceName ?source 
}
UNION  {untitled-ontology-12:""" + word + """
     untitled-ontology-12:ينتمي_للغة ?dialect}

  }
    """
    runSyncQuery(query)


def getMatchedWordDetails(word):
    getWordConfidence(word)  # ########----------# add source name here <--  @@TODO
    getWordDialect(word)
    getFullWeightOfWord(word)

    getWeightsAndSourcesOfWord(word)  # this wont work !! why ? TODO
    print("----------------------")


# -----------search for sentiment in word flow
def updateGraphNoMatch(word, stemmedWord):
    prefix = "http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#"
    newNodeString = prefix + word
    recognizedIndividualClass = NameSpace(newNodeString).to_uri()
    unrecognizedClassString = prefix + "UnrecognizedEntities"
    unrecognizedClass = NameSpace(unrecognizedClassString).to_uri()
    stemmedWordURI = NameSpace(prefix + stemmedWord).to_uri()
    stemRelationShip = NameSpace(prefix + "stem").to_uri()
    graph = Graph()
    graph.add((unrecognizedClass, RDF.type, OWL.Class))
    graph.add((recognizedIndividualClass, RDF.type, OWL.NamedIndividual))
    graph.add((recognizedIndividualClass, RDF.type, unrecognizedClass))
    graph.add((recognizedIndividualClass, stemRelationShip, stemmedWordURI))
    fuseki = FusekiUpdate('http://localhost:3030', 'ArEmotive')
    fuseki.insert_graph(graph)


classificationMode = conf.CLASSIFICATIONMODE


# -----------


def updateGraphWithMatchFromHugging(word):
    myLabels = ['متعة', 'غضب', 'خوف', 'حب', 'تفهم', 'رضا', 'تطلع', 'اهتمام', 'مفاجآة', 'اشمئزاز', 'محايد', 'لا_مبالاة',
                'حزن']
    prefix = "http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#"
    newClassString = hug.classify(word, myLabels, classificationMode)  # here it returned a single string
    newTrustFactor = tf.getAppropriateTrustFactor(newClassString)
    newNodeString = NameSpace(prefix + word).to_uri()
    newClass = NameSpace(prefix + newClassString).to_uri()
    graph = Graph()
    graph.add((newNodeString, RDF.type, OWL.NamedIndividual))
    graph.add((newNodeString, RDF.type, newClass))
    relationship = "http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#قيمتها"
    relationshipURI = NameSpace(relationship).to_uri()
    confidenceProperty = prefix + "confidence"  # ----- as long as it is from hugging so the conf is 50%
    # ---- may change if update is from other source
    confidencePropertyURI = NameSpace(confidenceProperty).to_uri()
    hFConfLiter = Literal("50", datatype=XSD.int)
    graph.add((newNodeString, confidencePropertyURI, hFConfLiter))
    literal = Literal(newTrustFactor, datatype=XSD.int)
    graph.add((newNodeString, relationshipURI, literal))
    dailect = ditt.checkDialect(word)
    dialectURI = NameSpace(prefix + dailect).to_uri()
    dialectRelationShip = "ينتمي_للغة"
    dialectRelationShipURI = NameSpace(prefix + dialectRelationShip).to_uri()
    graph.add((newNodeString, dialectRelationShipURI, dialectURI))
    fuseki = FusekiUpdate('http://localhost:3030', 'ArEmotive')
    fuseki.insert_graph(graph)


# --------------- multiple classes update test
import ArEmotiveApp.ontologyHandler.createNewProperties as partWeight


def updateGraphWithMatchFromHuggingMulti(word):
    myLabels = ['متعة', 'غضب', 'خوف', 'حب', 'تفهم', 'رضا', 'تطلع', 'اهتمام', 'مفاجآة', 'اشمئزاز', 'محايد', 'لا_مبالاة',
                'حزن']
    prefix = "http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#"
    newClassStringDict = hug.classifyMultiClass(word, myLabels, classificationMode)  # here it returned a dict
    sourceRelationship = NameSpace(prefix + "source")
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
        graph.add((newNodeString, RDF.type, OWL.NamedIndividual))
        graph.add((newNodeString, RDF.type, newClass))
        partWeight.createPartialWeightRelationship(word, obj, int(newTrustFactor))

    relationship = "http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#قيمتها"
    relationshipURI = NameSpace(relationship).to_uri()
    confidenceProperty = prefix + "confidence"  # ----- as long as it is from hugging so the conf is 50%
    # ---- may change if update is from other source
    confidencePropertyURI = NameSpace(confidenceProperty).to_uri()
    hFConfLiter = Literal("50", datatype=XSD.int)
    graph.add((newNodeString, confidencePropertyURI, hFConfLiter))
    newTrustFactor = int(sum(trustFactorList) / len(trustFactorList))
    literal = Literal(newTrustFactor, datatype=XSD.int)  # new trust factor for all classes matched
    graph.add((newNodeString, relationshipURI, literal))
    dialect = ditt.checkDialect(word)
    dialectURI = NameSpace(prefix + dialect).to_uri()
    dialectRelationShip = "ينتمي_للغة"
    dialectRelationShipURI = NameSpace(prefix + dialectRelationShip).to_uri()
    graph.add((newNodeString, dialectRelationShipURI, dialectURI))
    fuseki = FusekiUpdate('http://localhost:3030', 'ArEmotive')
    fuseki.insert_graph(graph)


# --------

def updateGraphWithMatchFromHuggingMultiNew(word, classificationMode=3):
    classificationMode = conf.CLASSIFICATIONMODE
    myLabels = ['متعة', 'غضب', 'خوف', 'حب', 'تفهم', 'رضا', 'تطلع', 'تطلع', 'مفاجآة', 'اشمئزاز', 'محايد', 'لا_مبالاة',
                'امتنان'
        , 'فخر', 'حياد', 'فرح', 'محاولة', 'يأس', 'سعادة', 'حزن', 'فشل', 'غيظ', 'سخط']
    prefix = "http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#"
    relationship = "http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#قيمتها"
    relationshipURI = NameSpace(relationship).to_uri()
    newClassStringDict = hug.classifyMultiClass(word, myLabels, classificationMode)
    weightRelationship = "قيمتها"
    weightRelationshipUri = NameSpace(prefix + weightRelationship).to_uri()
    partialWeightRelationship = NameSpace(
        "http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#partialWeight").to_uri()
    hFConfLiter = Literal("50", datatype=XSD.int)
    emotionClassURI = NameSpace(
        "http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#العاطفة").to_uri()
    confidenceProperty = prefix + "confidence"  # ----- as long as it is from hugging so the conf is 50%
    # ---- may change if update is from other source
    confidencePropertyURI = NameSpace(confidenceProperty).to_uri()
    sourceRelationship = NameSpace(prefix + "source").to_uri()
    SourceNameRelationship = NameSpace(prefix + "sourceName").to_uri()
    huggingFaceLocal = NameSpace(prefix + "hugggingFace-Local").to_uri()
    dataRelationship = NameSpace(prefix + "data").to_uri()
    dialect = ditt.checkDialect(word)
    dialectURI = NameSpace(prefix + dialect).to_uri()
    dialectRelationShip = "ينتمي_للغة"
    dialectRelationShipURI = NameSpace(prefix + dialectRelationShip).to_uri()

    graph = Graph()
    trustFactorList = []
    i = 0
    for obj in newClassStringDict:
        newClassString = obj
        newTrustFactor = tf.getAppropriateTrustFactor(newClassString)
        trustFactorList.append(int(newTrustFactor))
        newNodeString = NameSpace(prefix + word).to_uri()
        newClass = NameSpace(prefix + newClassString).to_uri()
        graph.add((newNodeString, sourceRelationship, BNode(0)))
        graph.add((newNodeString, RDF.type, newClass))
        graph.add((BNode(0), RDF.type, newClass))
        graph.add((BNode(0), SourceNameRelationship, huggingFaceLocal))
        graph.add((BNode(0), confidencePropertyURI, hFConfLiter))
        # graph.add((BNode(i), dataRelationship, BNode(1)))
        graph.add((BNode(0), dialectRelationShipURI, dialectURI))
        graph.add((BNode(0), partialWeightRelationship, BNode(i + 1)))
        graph.add((BNode(i + 1), RDF.type, newClass))
        graph.add((BNode(i + 1), relationshipURI, Literal(int(newTrustFactor), datatype=XSD.int)))
        graph.add((BNode(i + 1), emotionClassURI, NameSpace(prefix + obj).to_uri()))
        i = i + 2
        # graph.add((BNode(1), RDF.type, OWL.NamedIndividual))
        # graph.add((BNode(1), RDF.type, newClass))
        # partWeight.createPartialWeightRelationship(BNode(1), obj, int(newTrustFactor))
        # graph.add((BNode(1), partialWeightRelationship, BNode(2)))
        # graph.add((BNode(2), emotionClassURI, NameSpace(prefix + obj).to_uri()))
        # graph.add((BNode(2), weightRelationshipUri, Literal(newTrustFactor, datatype=XSD.int)))

    newTrustFactor = int(sum(trustFactorList) / len(trustFactorList))
    literal = Literal(newTrustFactor, datatype=XSD.int)  # new trust factor for all classes matched
    graph.add((BNode(0), relationshipURI, literal))

    fuseki = FusekiUpdate('http://localhost:3030', 'ArEmotive')
    fuseki.insert_graph(graph)


def updateGraphWithMatchFromHuggingMultiNewWhole(word, classificationMode=3):
    classificationMode = conf.CLASSIFICATIONMODE
    myLabels = ['متعة', 'غضب', 'خوف', 'حب', 'تفهم', 'رضا', 'تطلع', 'تطلع', 'مفاجآة', 'اشمئزاز', 'محايد', 'لا_مبالاة',
                'امتنان'
        , 'فخر', 'حياد', 'فرح', 'محاولة', 'يأس', 'سعادة', 'حزن', 'فشل', 'غيظ', 'سخط']
    prefix = "http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#"
    relationship = "http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#قيمتها"
    relationshipURI = NameSpace(relationship).to_uri()
    newClassStringDict = hug.classifyMortizMulti(word, myLabels, classificationMode)
    weightRelationship = "قيمتها"
    weightRelationshipUri = NameSpace(prefix + weightRelationship).to_uri()
    partialWeightRelationship = NameSpace(
        "http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#partialWeight").to_uri()
    hFConfLiter = Literal("50", datatype=XSD.int)
    emotionClassURI = NameSpace(
        "http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#العاطفة").to_uri()
    confidenceProperty = prefix + "confidence"  # ----- as long as it is from hugging so the conf is 50%
    # ---- may change if update is from other source
    confidencePropertyURI = NameSpace(confidenceProperty).to_uri()
    sourceRelationship = NameSpace(prefix + "source").to_uri()
    SourceNameRelationship = NameSpace(prefix + "sourceName").to_uri()
    huggingFaceLocal = NameSpace(prefix + "hugggingFace-Local").to_uri()
    dataRelationship = NameSpace(prefix + "data").to_uri()
    dialect = ditt.checkDialect(word)
    dialectURI = NameSpace(prefix + dialect).to_uri()
    dialectRelationShip = "ينتمي_للغة"
    dialectRelationShipURI = NameSpace(prefix + dialectRelationShip).to_uri()

    graph = Graph()
    trustFactorList = []
    i = 0
    for obj in newClassStringDict:
        newClassString = obj
        newTrustFactor = tf.getAppropriateTrustFactor(newClassString)
        trustFactorList.append(int(newTrustFactor))
        newNodeString = NameSpace(prefix + word).to_uri()
        newClass = NameSpace(prefix + newClassString).to_uri()
        graph.add((newNodeString, sourceRelationship, BNode(0)))
        graph.add((newNodeString, RDF.type, newClass))
        graph.add((BNode(0), RDF.type, newClass))
        graph.add((BNode(0), SourceNameRelationship, huggingFaceLocal))
        graph.add((BNode(0), confidencePropertyURI, hFConfLiter))
        # graph.add((BNode(i), dataRelationship, BNode(1)))
        graph.add((BNode(0), dialectRelationShipURI, dialectURI))
        graph.add((BNode(0), partialWeightRelationship, BNode(i + 1)))
        graph.add((BNode(i + 1), RDF.type, newClass))
        graph.add((BNode(i + 1), relationshipURI, Literal(int(newTrustFactor), datatype=XSD.int)))
        graph.add((BNode(i + 1), emotionClassURI, NameSpace(prefix + obj).to_uri()))
        i = i + 2
        # graph.add((BNode(1), RDF.type, OWL.NamedIndividual))
        # graph.add((BNode(1), RDF.type, newClass))
        # partWeight.createPartialWeightRelationship(BNode(1), obj, int(newTrustFactor))
        # graph.add((BNode(1), partialWeightRelationship, BNode(2)))
        # graph.add((BNode(2), emotionClassURI, NameSpace(prefix + obj).to_uri()))
        # graph.add((BNode(2), weightRelationshipUri, Literal(newTrustFactor, datatype=XSD.int)))

    newTrustFactor = int(sum(trustFactorList) / len(trustFactorList))
    literal = Literal(newTrustFactor, datatype=XSD.int)  # new trust factor for all classes matched
    graph.add((BNode(0), relationshipURI, literal))

    fuseki = FusekiUpdate('http://localhost:3030', 'ArEmotive')
    fuseki.insert_graph(graph)


# -----------
def getWordFromUri(uri):
    return uri.split('#')[1]


# ---------
from rdflib import Literal, XSD


def updateTrustFactor(newNode, factor):
    relationship = "http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#قيمتها"
    relationshipURI = NameSpace(relationship).to_uri()
    literal = Literal(int(factor), datatype=XSD.int)
    graph = Graph()
    graph.add((newNode, relationshipURI, literal))
    fuseki = FusekiUpdate('http://localhost:3030', 'ArEmotive')
    fuseki.insert_graph(graph)


# ---------- check words that are not recognized from other sources
# from camel_tools.disambig.mle import MLEDisambiguator
# from camel_tools.tokenizers.morphological import MorphologicalTokenizer

sentence_msa = []
sentence_msa.append("لعّيب")

# import main as tokenizer

# tokenizer.tokenize(sentence_msa)

# mle_msa = MLEDisambiguator.pretrained('calima-msa-r13')

# msa_bw_tokenizer = MorphologicalTokenizer(disambiguator=mle_msa, scheme='bwtok')
# msa_bw_tok = msa_bw_tokenizer.tokenize(sentence_msa)
# print("tokenization")
# print(sentence_msa)
# print(msa_bw_tok)

# --------- check sentiment output class from previous step form # camel tools #

# from camel_tools.sentiment import SentimentAnalyzer
# sa = SentimentAnalyzer.pretrained()
sentences = [
    'لعّيب'
]
# sentiments = sa.predict(sentences)
# print(sentiments)
# -----------

# --------- check sentiment output class from previous step form # hugging face #

import ArEmotiveApp.ontologyHandler.huggingFace as hug
import ArEmotiveApp.ontologyHandler.trustFactor as tf


def checkMatchWithClassesAndUpdate(word):
    myLabels = ['متعة', 'غضب', 'خوف', 'حب', 'تفهم', 'رضا', 'تطلع', 'اهتمام', 'مفاجآة', 'اشمئزاز', 'محايد', 'لا_مبالاة',
                'حزن']
    newClassString = hug.classify(word, myLabels, classificationMode)
    newTrustFactor = tf.getAppropriateTrustFactor(newClassString)
    updateGraphWithMatchFromHugging(word, newClassString)
    prefix = "http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#"
    newNode = NameSpace(prefix + newClassString).to_uri()
    # updateTrustFactor(newNode, newTrustFactor)


# ------------------------------------------ main flow

import ArEmotiveApp.ontologyHandler.main as twitterHandler
import ArEmotiveApp.ontologyHandler.Utils as utils

# runDeleteQuery()
# result = twitterHandler.getTweetsLocal("اوكرانيا", 1)
# tweetsAsText = utils.getTweetsAsText(result)
# tweetsAsText = ["يقال أن التقاليد رجعية أزعر"]
# oldNewWordMap = {}
# for tweet in tweetsAsText:  # <-------------------------------- here check for original
#     # twitterHandler.tokenize(tweet)
#     recognizedTweet = utils.removeNERRecognizedWords(tweet.split())
#     newTweet = []
#     newTokenizedTweet = ""
#     newStringifiedTweet = ""
#     for word in recognizedTweet:
#         newTweet.append(word[0])
#         newTokenizedTweet += stemmers.longestWordStemming(word[0]) + " "  # why stem here ????
#         newStringifiedTweet += word[0] + " "
#         # newTokenizedTweet += stemmers.ISRIStem(word[0]) # needs work
#
#     newTokenizedTweetlist = newTokenizedTweet.split(" ")
#
#     # ------- try another stemmer
#     # for item in newTokenizedTweetlist:
#     #    newTokenizedTweetlist.remove(item)
#     #    newTokenizedTweetlist.append(max(item.split("+")))
#     # print("final")
#     # print(newTokenizedTweetlist)
#     # tokenizedTweet = twitterHandler.tokenize(newTweet)
#     # ---------
#     print("new Tokeinzed tweet List : ")
#     print(newTokenizedTweetlist)  # < --- original words here
#     tokenizedTweet = twitterHandler.tokenize(newTokenizedTweetlist)  # < ---- new words here
#     oldNewWordMap = utils.generateNewOldWordMap(tokenizedTweet, newTokenizedTweetlist)
#     newTweetList = []
#     for item in tokenizedTweet:
#         print("word : " + item)
#         item2 = stemmers.longestWordStemming(item)
#         print("stemmed : " + item2)  # ----------- needs work
#         print(item)
#         item = item2
#         newTweetList.append(item)
#     print("tokenization : ")
#     stemmedTweet = " ".join(newTweetList)
#     print(stemmedTweet)  # ------- after stemming
# # ---------------
# print("new tweet list check")
# print(newTweetList)
# import arabicstopwords.arabicstopwords as stp
#
# processedTweet = stemmedTweet.split(" ")  # --- stop word removal
# processedTweet.remove(processedTweet[0])
# for word in processedTweet:
#     if stp.is_stop(word) or len(word) == 0 or len(word) == 1:
#         processedTweet.remove(word)
# print("processedTweet : ")
# print(processedTweet)
#
# matchingMode = conf.MATCHINGMODE
#
# # getWeightsAndSourcesOfWord(word)
# # ---- apply main logic to each word in the processed tweet
# for word in processedTweet:  # should look at main tweet first not processed <------------??????
#     #  ## make sure that flow is correct   # ////// ?????????????????????????????????????????
#     originalWord = oldNewWordMap[word].strip('+_[]')  # should check processed tweet or main tweet
#     print("the original word is : " + originalWord)
#     print("the processed word is : " + word)
#     if matchingMode == 1:  # if matching mode is literal
#         if getNumberOfMatches(originalWord) == 0:  # if not found in my ontology
#             if getNumberOfMatches(word) == 0:  # if stemmed word also not found
#                 updateGraphNoMatch(originalWord)
#                 # updateGraphWithMatchFromHugging(originalWord)
#                 updateGraphWithMatchFromHuggingMultiNew(originalWord)
#             else:
#                 runSyncQuery(getEmotionClassesByWord(word))
#                 getMatchedWordDetails(word)
#                 # getWeightsAndSourcesOfWord(word)
#
#         else:
#             runSyncQuery(getEmotionClassesByWord(originalWord))
#             getMatchedWordDetails(originalWord)
#             # getWeightsAndSourcesOfWord(originalWord)
#     else:
#         if getNumberOfMatches(originalWord) == 0:
#             updateGraphNoMatch(originalWord)
#             updateGraphWithMatchFromHugging(originalWord)
#         else:
#             runSyncQuery(getEmotionClassesByWord(originalWord))
#             getMatchedWordDetails(originalWord)

import ArEmotiveApp.ontologyHandler.searchResult as SRClasses


def search(mode,
           sentence, numberOfTweets: 1, matchingMode, classificationMode):  # here mode determines if the search is from
    # TODO search if word exists before stemming bcz stemming might deform the word
    if mode == "2":
        result = twitterHandler.getTweetsLocal(sentence, numberOfTweets)
        tweetsAsText = utils.getTweetsAsText(result)
    if mode == "3":
        dataFromFile = twitterHandler.getCommentsFromFile("ArEmotiveApp/ontologyHandler/Comments.txt", 0, 2)
        # tweetsAsText = twitterHandler.getCommentsFromFile("ArEmotiveApp/ontologyHandler/FBcomments.txt", 0, 2)
        tweetsAsText = []
        for obj in dataFromFile:
            tweetsAsText.append(obj['comment'])
    else:
        tweetsAsText = [sentence]
    oldNewWordMap = {}
    tweetID = 0
    for tweet in tweetsAsText:  # <-------------------------------- here check for original
        # twitterHandler.tokenize(tweet)
        recognizedTweet = utils.removeNERRecognizedWords(tweet.split())
        newTweet = []
        newTokenizedTweet = ""
        newStringifiedTweet = ""
        for word in recognizedTweet:
            newTweet.append(word[0])
            newTokenizedTweet += stemmers.longestWordStemming(word[0]) + " "
            newStringifiedTweet += word[0] + " "

        newTokenizedTweetlist = newTokenizedTweet.split(" ")

        # ------- try another stemmer
        tokenizedTweet = twitterHandler.tokenize(newTokenizedTweetlist)  # < ---- new words here
        oldNewWordMap = utils.generateNewOldWordMap(tokenizedTweet, newTokenizedTweetlist)
        newTweetList = []
        for item in tokenizedTweet:
            item2 = stemmers.longestWordStemming(item)
            item = item2
            newTweetList.append(item)
        stemmedTweet = " ".join(newTweetList)
        tweetID += 1
    # ---------------
    import arabicstopwords.arabicstopwords as stp
    processedTweet = stemmedTweet.split(" ")  # --- stop word removal
    processedTweet = list(filter(None, processedTweet))
    for word in processedTweet:
        if stp.is_stop(word) or len(word) == 0 or len(word) == 1:
            processedTweet.remove(word)
    for word in processedTweet:
        originalWord = oldNewWordMap[word].strip('+_[]')  # should check processed tweet or main tweet
        if matchingMode == "2":  # if matching mode is not literal
            if getNumberOfMatches(originalWord) == 0:  # if not found in my ontology
                if getNumberOfMatches(word) == 0:  # if stemmed word also not found
                    updateGraphNoMatch(originalWord, word)
                    # updateGraphWithMatchFromHugging(originalWord)
                    updateGraphWithMatchFromHuggingMultiNew(originalWord, classificationMode=3)
                else:
                    runSyncQuery(getEmotionClassesByWord(word))
                    getMatchedWordDetails(word)  # TODO if i'm searching in view should i search here for details
                    # getWeightsAndSourcesOfWord(word)

            else:
                runSyncQuery(getEmotionClassesByWord(originalWord))
                getMatchedWordDetails(originalWord)
                # getWeightsAndSourcesOfWord(originalWord)
        else:
            if getNumberOfMatches(originalWord) == 0:
                updateGraphNoMatch(originalWord, word)
                updateGraphWithMatchFromHuggingMultiNew(originalWord, classificationMode=3)
                # TODO should add other ontologies
            else:
                runSyncQuery(getEmotionClassesByWord(originalWord))
                getMatchedWordDetails(originalWord)
    originalOfProcessed = []
    for word in processedTweet:
        originalOfProcessed.append(oldNewWordMap[word].strip('[]/-_+'))
    return {
        'original': tweetsAsText,
        'processed': processedTweet,
        'originalOfProcessed': originalOfProcessed
    }


def newDynamoSearch(mode,
                    sentence, numberOfTweets: 1, matchingMode,
                    classificationMode):  # here mode determines if the search is from
    # TODO search if word exists before stemming bcz stemming might deform the word
    print("mode : " + mode)
    if mode == "2":
        result = twitterHandler.getTweetsLocal(sentence, numberOfTweets)
        tweetsAsText = utils.getTweetsAsText(result)
    if mode == "3":
        dataFromFile = twitterHandler.getCommentsFromFile("ArEmotiveApp/ontologyHandler/Comments.txt", 0, 4)
        # tweetsAsText = twitterHandler.getCommentsFromFile("ArEmotiveApp/ontologyHandler/FBcomments.txt", 0, 2)
        tweetsAsText = []
        for obj in dataFromFile:
            tweetsAsText.append(obj['comment'])
        print("tweets As text")
        print(tweetsAsText)
    else:
        tweetsAsText = [sentence]
    oldNewWordMap = {}

    tweetID = 0
    newListOfTweets = []
    for tweet in tweetsAsText:  # <-------------------------------- here check for original
        # twitterHandler.tokenize(tweet)
        recognizedTweet = utils.removeNERRecognizedWords(tweet.split())
        newTweet = []
        newTokenizedTweet = ""
        newStringifiedTweet = ""
        for word in recognizedTweet:
            newTweet.append(word[0])
            newTokenizedTweet += stemmers.longestWordStemming(word[0]) + " "
            newStringifiedTweet += word[0] + " "

        newTokenizedTweetlist = newTokenizedTweet.split(" ")
        print("newTokenizedTweetlist")
        print(newTokenizedTweetlist)

        # ------- try another stemmer
        tokenizedTweet = twitterHandler.tokenize(newTokenizedTweetlist)  # < ---- new words here
        print("tokenizedTweet")
        print(tokenizedTweet)
        oldNewWordMap.update(utils.generateNewOldWordMap(tokenizedTweet, newTokenizedTweetlist))

        newTweetList = []
        for item in tokenizedTweet:
            item2 = stemmers.longestWordStemming(item)
            item = item2
            newTweetList.append(item)
        newListOfTweets = newListOfTweets + newTweetList
        stemmedTweet = " ".join(newTweetList)
        tweetID += 1
    # ---------------
    import ArEmotiveApp.ontologyHandler.jenaOntologyFunctions as jof
    import arabicstopwords.arabicstopwords as stp
    print("stemmed tweet")
    print(stemmedTweet)
    processedTweet = stemmedTweet.split(" ")  # --- stop word removal
    print("first processed tweet")
    print(processedTweet)
    # processedTweet = list(filter(None, processedTweet))
    processedTweet = list(filter(None, newListOfTweets))
    print("second processed tweet")
    print(processedTweet)
    for word in processedTweet:
        if stp.is_stop(word) or len(word) == 0 or len(word) == 1:
            processedTweet.remove(word)
    for word in processedTweet:  ## TODO here is the problem and up
        print("before if checked words")
        print(word)
        originalWord = oldNewWordMap[word].strip('+_[]')  # should check processed tweet or main tweet
        if getNumberOfMatches(originalWord) == 0:
            print("words checked ")
            print(originalWord)
            jof.dynamicUpdateGraphWithMatchFromOtherOntology("DynamOnto", conf.DYNAMONTOPREFIX, originalWord)
        # if matchingMode == "2":  # if matching mode is not literal
        #     if getNumberOfMatches(originalWord) == 0:  # if not found in my ontology
        #         if getNumberOfMatches(word) == 0:  # if stemmed word also not found
        #             updateGraphNoMatch(originalWord, word)
        #             # updateGraphWithMatchFromHugging(originalWord)
        #             updateGraphWithMatchFromHuggingMultiNew(originalWord, classificationMode=3)
        #         else:
        #             runSyncQuery(getEmotionClassesByWord(word))
        #             getMatchedWordDetails(word)  # TODO if i'm searching in view should i search here for details
        #             # getWeightsAndSourcesOfWord(word)
        #
        #     else:
        #         runSyncQuery(getEmotionClassesByWord(originalWord))
        #         getMatchedWordDetails(originalWord)
        #         # getWeightsAndSourcesOfWord(originalWord)
        # else:
        #     if getNumberOfMatches(originalWord) == 0:
        #         updateGraphNoMatch(originalWord, word)
        #         updateGraphWithMatchFromHuggingMultiNew(originalWord, classificationMode=3)
        #         # TODO should add other ontologies
        #     else:
        #         runSyncQuery(getEmotionClassesByWord(originalWord))
        #         getMatchedWordDetails(originalWord)
    originalOfProcessed = []
    for word in processedTweet:
        originalOfProcessed.append(oldNewWordMap[word].strip('[]/-_+'))
    print("returned by dynaSearch")
    print({
        'original': tweetsAsText,
        'processed': processedTweet,
        'originalOfProcessed': originalOfProcessed
    })
    return {
        'original': tweetsAsText,
        'processed': processedTweet,
        'originalOfProcessed': originalOfProcessed
    }


def newDynamoSearchWholeClass(mode,
                              sentence, numberOfTweets: 1, matchingMode,
                              classificationMode):  # here mode determines if the search is from
    if mode == "2":
        result = twitterHandler.getTweetsLocal(sentence, numberOfTweets)
        tweetsAsText = utils.getTweetsAsText(result)
    if mode == "3":
        dataFromFile = twitterHandler.getCommentsFromFile("ArEmotiveApp/ontologyHandler/Comments.txt", 0, 4)
        # tweetsAsText = twitterHandler.getCommentsFromFile("ArEmotiveApp/ontologyHandler/FBcomments.txt", 0, 2)
        tweetsAsText = []
        for obj in dataFromFile:
            tweetsAsText.append(obj['comment'])
    else:
        tweetsAsText = [sentence]
    nEWords = []
    stopWordsDetected = []
    processedTweet = []
    tweetID = 0
    for tweet in tweetsAsText:
        tweetID += 1
        words = list(filter(None, tweet.split(" ")))
        for word in words:
            if (str(twitterHandler.NERRecognize([word])[0][1])) != "O":
                nEWords.append({'tweetId': tweetID,
                                'word': word})
                continue
            if len(word) <= 2:
                stopWordsDetected.append(word)
                continue
            # originalWord = oldNewWordMap[word].strip('+_[]')  # should check processed tweet or main tweet
            # if getNumberOfMatches(originalWord) == 0:
            if not re.search("[^\u0621-\u064A]", word):
                print("matched expression : " + word)
                processedTweet.append(word)
                if getNumberOfMatches(word) == 0:
                    updateGraphWithMatchFromHuggingMultiNewWhole(word, classificationMode=3)
        # jof.dynamicUpdateGraphWithMatchFromOtherOntology("DynamOnto", conf.DYNAMONTOPREFIX, originalWord)
    # ---------------
    import ArEmotiveApp.ontologyHandler.jenaOntologyFunctions as jof
    import arabicstopwords.arabicstopwords as stp

    # if matchingMode == "2":  # if matching mode is not literal
    #     if getNumberOfMatches(originalWord) == 0:  # if not found in my ontology
    #         if getNumberOfMatches(word) == 0:  # if stemmed word also not found
    #             updateGraphNoMatch(originalWord, word)
    #             # updateGraphWithMatchFromHugging(originalWord)
    #             updateGraphWithMatchFromHuggingMultiNew(originalWord, classificationMode=3)
    #         else:
    #             runSyncQuery(getEmotionClassesByWord(word))
    #             getMatchedWordDetails(word)  # TODO if i'm searching in view should i search here for details
    #             # getWeightsAndSourcesOfWord(word)
    #
    #     else:
    #         runSyncQuery(getEmotionClassesByWord(originalWord))
    #         getMatchedWordDetails(originalWord)
    #         # getWeightsAndSourcesOfWord(originalWord)
    # else:
    #     if getNumberOfMatches(originalWord) == 0:
    #         updateGraphNoMatch(originalWord, word)
    #         updateGraphWithMatchFromHuggingMultiNew(originalWord, classificationMode=3)
    #         # TODO should add other ontologies
    #     else:
    #         runSyncQuery(getEmotionClassesByWord(originalWord))
    #         getMatchedWordDetails(originalWord)
    originalOfProcessed = processedTweet
    print({
        'original': tweetsAsText,
        'processed': processedTweet,
        'originalOfProcessed': originalOfProcessed,
        'neWords': nEWords,
        'stopWords': stopWordsDetected
    })
    return {
        'original': tweetsAsText,
        'processed': processedTweet,
        'originalOfProcessed': originalOfProcessed,
        'neWords': nEWords,
        'stopWords': stopWordsDetected
    }


def getSourceNamesFromOntology(sentence):
    query = """
       prefix untitled-ontology-12: <http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#> 
select distinct ?type  where
{
  untitled-ontology-12:""" + sentence + """ untitled-ontology-12:source ?class.
    ?class   untitled-ontology-12:sourceName ?type}
    """
    query_result = fuseki_query.run_sparql(query)
    result = []
    for element in query_result.convert()['results']['bindings']:
        result.append((element['type']['value']).split('#')[1])
    return result


def getEmotionsMatchedFromSource(sourceName, sentence):
    query = """
        prefix untitled-ontology-12: <http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#> 
select distinct ?emotionsMatchedHere  where
{
  untitled-ontology-12:""" + sentence + """ untitled-ontology-12:source ?node.
  ?node untitled-ontology-12:sourceName untitled-ontology-12:""" + sourceName + """.
      ?node   a ?emotionsMatchedHere.}
  		"""
    query_result = fuseki_query.run_sparql(query)
    result = []
    for element in query_result.convert()['results']['bindings']:
        result.append({'emotionsMatchedHere': element['emotionsMatchedHere']['value'].split('#')[1]
                       })
    return result


def getSourceConfidence(sourceName, sentence):
    query = """
     prefix untitled-ontology-12: <http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#> 
select distinct  ?confidence  where
{
  untitled-ontology-12:""" + sentence + """ untitled-ontology-12:source ?node.
  ?node untitled-ontology-12:sourceName untitled-ontology-12:""" + sourceName + """.
  		?node untitled-ontology-12:confidence ?confidence.}
    """
    query_result = fuseki_query.run_sparql(query)
    result = []
    for element in query_result.convert()['results']['bindings']:
        if element['confidence']['type'] == "literal":
            result.append({'confidence': element['confidence']['value']})
        else:
            result.append({'confidence': element['confidence']['value'].split('#')[1]})
    return result


def getSourceDialect(sourceName, sentence):
    query = """
      prefix untitled-ontology-12: <http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#> 
select distinct  ?dialect  where
{
  untitled-ontology-12:""" + sentence + """ untitled-ontology-12:source ?node.
  ?node untitled-ontology-12:sourceName untitled-ontology-12:""" + sourceName + """.
  		?node untitled-ontology-12:ينتمي_للغة ?dialect.}
    """
    query_result = fuseki_query.run_sparql(query)
    result = []
    for element in query_result.convert()['results']['bindings']:
        result.append({'dialectNode': element['dialect']['value'].split('#')[1]})
    return result


def getFullWeightOfSource(sourceNAme, sentence):
    query = """
    
    prefix untitled-ontology-12: <http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#> 
select   (AVG(?weight) as ?avgWeight)    where
{

  untitled-ontology-12:""" + sentence + """ untitled-ontology-12:source ?node.
  ?node untitled-ontology-12:sourceName untitled-ontology-12:""" + sourceNAme + """.
   
  		?node untitled-ontology-12:partialWeight ?pnode. 
  		optional{?pnode untitled-ontology-12:قيمتها ?weight}
  }
    """
    query_result = fuseki_query.run_sparql(query)
    result = []
    for element in query_result.convert()['results']['bindings']:
        if not element:
            result.append({'fullWeight': "not found"})
            break
        result.append({'fullWeight': int(float(element['avgWeight']['value']))})

    if not result:
        return result.append('0')
    return result


def getPartialWeightsFromSource(sourceName, sentence):
    query = """
        prefix untitled-ontology-12: <http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#> 
select  distinct ?emotion ?weight  where
{

  untitled-ontology-12:""" + sentence + """ untitled-ontology-12:source ?node.
  ?node untitled-ontology-12:sourceName untitled-ontology-12:""" + sourceName + """.
   
  		?node untitled-ontology-12:partialWeight ?pnode. 
  		?pnode untitled-ontology-12:العاطفة ?emotion.
  		?pnode untitled-ontology-12:قيمتها ?weight}
    """
    query_result = fuseki_query.run_sparql(query)
    result = []
    for element in query_result.convert()['results']['bindings']:
        if element['weight']['type'] == "literal":
            result.append({'pWeightEmotion': element['emotion']['value'].split('#')[1],
                           'pWeightWeight': element['weight']['value']
                           })
        else:
            result.append({'pWeightEmotion': element['emotion']['value'].split('#')[1],
                           'pWeightWeight': element['weight']['value'].split('#')[1]
                           })

    return result


def getWordDetailsForDisplay(sentence):
    sourceNames = getSourceNamesFromOntology(sentence)
    return {
        'sourceNames': sourceNames
    }


def Convert(a):
    it = iter(a)
    res_dct = dict(zip(it, it))
    return res_dct

# runDeleteQuery()
# search(1, "يقال أن التقاليد رجعية أزعر")
# ---- to do :  TODO
# delete multiple ranges for confidence property
# check if labels returned from Hugging are true (ordered correctly)
# some words clearly differ from expected output
# see postman for reference
# to try and upgrade the result maybe classify the word on camel tools
# then a set of corresponding classes not all classes
# determine how u want to see multiple classes as a result
# also when checking a sentence do u want to check the whole sentence or one word at a time
# problems with stemming and tokenization
# ....
# updateGraphWithMatchFromHuggingMultiNew("أزعر")
