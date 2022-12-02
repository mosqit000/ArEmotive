from SPARQLWrapper import QueryResult
from pyfuseki import FusekiUpdate, FusekiQuery, AsyncFuseki, AsyncFusekiResp
from pyfuseki.rdf import rdf_prefix, NameSpace as ns, NameSpace
from rdflib import Graph, OWL, BNode, XSD
from pyfuseki.rdf import rdf_property
from rdflib import URIRef as uri, Literal
from rdflib import RDF
import asyncio
import pyfuseki
import requests
import ArEmotiveApp.ontologyHandler.Utils as util
import ArEmotiveApp.ontologyHandler.config as conf
import ArEmotiveApp.ontologyHandler.rdfProperties as prop
import ArEmotiveApp.ontologyHandler.huggingFace as hf


def getClassesFromOntology(ontologyName):
    fuseki_query = FusekiQuery('http://localhost:3030', ontologyName)
    query = """
    prefix owl: <http://www.w3.org/2002/07/owl#>
    SELECT  ?s  where {?s ?p owl:Class}
    """
    query_result = fuseki_query.run_sparql(query)
    print("classes :")
    print(util.getWordsFromURI(query_result))


def getRelationshipsFromOntology(ontologyName):
    fuseki_query = FusekiQuery('http://localhost:3030', ontologyName)
    query = """
       prefix owl: <http://www.w3.org/2002/07/owl#>
       SELECT  ?s  where {{?s ?p owl:ObjectProperty} UNION  {?s ?p owl:DatatypeProperty}}
       """
    query_result = fuseki_query.run_sparql(query)
    print("properties :")
    print(util.getWordsFromURI(query_result))


def getInstancesFromOntology(ontologyName):
    fuseki_query = FusekiQuery('http://localhost:3030', ontologyName)
    query = """
           prefix owl: <http://www.w3.org/2002/07/owl#>
           SELECT  ?s  where {?s ?p owl:NamedIndividual}
           """
    query_result = fuseki_query.run_sparql(query)
    print("instances :")
    print(util.getWordsFromURI(query_result))


def checkForMatchInOntology(ontologyName, ontologyPrefix, word):
    fuseki_query = FusekiQuery('http://localhost:3030', ontologyName)

    query = """
               prefix DynamOnto: """ + ontologyPrefix + """
               prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        SELECT  ?s  where {
          DynamOnto:""" + word + """ DynamOnto:نوع_العاطفة ?s;
         FILTER (
        ?s != <http://www.w3.org/2002/07/owl#Class> &&
         ?s != <http://www.w3.org/2002/07/owl#NamedIndividual>
)}
               """
    query_result = fuseki_query.run_sparql(query)
    # query_result.print_results()
    # print(util.getWordsFromURI(query_result))
    return util.getWordsFromURI(query_result)


def runDeleteQuery(word):
    deleteQuery = """
    DELETE WHERE{
    <http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#""" + word + """> ?pred ?obj
    } 
    """
    url = "http://localhost:3030/ArEmotive/update"
    queryObject = {'query': 'update',
                   'update': deleteQuery}
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    x = requests.post(url, params=queryObject, headers=headers)
    print(x.text)


def updateGraphWithMatchFromOtherOntology(ontologyName, ontologyPrefix, word):
    result = checkForMatchInOntology(ontologyName, "<" + ontologyPrefix + ">", word)
    wordNode = NameSpace(conf.AREMOTIVEPREFIX + word).to_uri()
    classesAsURIs = []
    for item in result:
        classesAsURIs.append(NameSpace(conf.AREMOTIVEPREFIX + item).to_uri())
    graph = Graph()
    for item in classesAsURIs:
        graph.add((wordNode, RDF.type, item))
    graph.add((wordNode, RDF.type, NameSpace(prop.unrecognized).to_uri()))
    graph.add((wordNode, RDF.type, OWL.NamedIndividual))
    graph.add((wordNode, NameSpace(prop.source).to_uri(), BNode(0)))
    i = 0
    for item in classesAsURIs:
        graph.add((BNode(0), RDF.type, item))
        graph.add(
            (BNode(0), NameSpace(prop.sourceName).to_uri(), NameSpace(conf.AREMOTIVEPREFIX + ontologyName).to_uri()))
        graph.add((BNode(0), NameSpace(prop.confidence).to_uri(), Literal("80", datatype=XSD.int)))
        graph.add((BNode(0), NameSpace(prop.partialWeight).to_uri(), BNode(i + 1)))
        graph.add((BNode(i + 1), RDF.type, item))
        graph.add((BNode(i + 1), NameSpace(prop.emotion).to_uri(), item))
        i = i + 2
    fuseki = FusekiUpdate('http://localhost:3030', 'ArEmotive')
    fuseki.insert_graph(graph)


def getOntologyProperties(ontologyName):
    query = """
    prefix owl: <http://www.w3.org/2002/07/owl#>
    select ?s where{
{?s a owl:ObjectProperty}
union
  {?s a owl:DatatypeProperty}}
    """
    fuseki_query = FusekiQuery('http://localhost:3030', ontologyName)
    query_result = fuseki_query.run_sparql(query)
    return util.getWordsFromURI(query_result)


def mapNewPropertiesWithMyProperties(primaryOntology, secondaryOntology):
    primaryOntologyProps = getOntologyProperties(primaryOntology)
    secondaryOntologyProps = getOntologyProperties(secondaryOntology)
    newProps = []
    for prop in secondaryOntologyProps:
        newProps.append([hf.classifyMortiz(prop, primaryOntologyProps, 1), prop])
    print(newProps)

    return newProps


# mapNewPropertiesWithMyProperties("ArEmotive", "secondaryOntology")


def findMatchingWord(array, word):
    for elem in array:
        if elem[0] == word:
            return elem[1]
    return "not Found"


def getWordWeightFromOntology(word, ontologyName,mappedProps):
    print("searched word from new Ontology")
    print(word)
    if ontologyName == "DynamOnto":
        relation = "شدة_العاطفة"
    else:
        relation = findMatchingWord(mappedProps, "قيمتها")
    queryWeight = """
   prefix DynamOnto:  <http://www.semanticweb.org/asus/ontologies/2022/8/untitled-ontology-27#>
    select ?s where
{DynamOnto:""" + word + """ DynamOnto:""" + relation + """ ?s}
    """
    fuseki_query = FusekiQuery('http://localhost:3030', ontologyName)
    query_result = fuseki_query.run_sparql(queryWeight)
    return util.getWordsFromURI(query_result)


def getWordDialectFromOntology(word, ontologyName,mappedProps):
    if ontologyName == "DynamOnto":
        relation = "اللغة"
    else:
        relation = findMatchingWord(mappedProps, "ينتمي_للغة")
    queryDialect = """
    prefix DynamOnto:  <http://www.semanticweb.org/asus/ontologies/2022/8/untitled-ontology-27#> 
        select ?s where
    {DynamOnto:""" + word + """ DynamOnto:""" + relation + """ ?s}
        """
    print(queryDialect)

    fuseki_query = FusekiQuery('http://localhost:3030', ontologyName)
    query_result2 = fuseki_query.run_sparql(queryDialect)
    return util.getWordsFromURI(query_result2)


def getWordConfidenceFromOntology(word, ontologyName,mappedProps):
    if ontologyName == "DynamOnto":
        relation = "ثقة_المصدر"
    else:
        relation = findMatchingWord(mappedProps, "confidence")
    queryConfidence = """
   prefix DynamOnto:  <http://www.semanticweb.org/asus/ontologies/2022/8/untitled-ontology-27#>
       select ?s where
   {DynamOnto:""" + word + """ DynamOnto:""" + relation + """ ?s}
       """
    fuseki_query = FusekiQuery('http://localhost:3030', ontologyName)
    query_result3 = fuseki_query.run_sparql(queryConfidence)
    return util.getWordsFromURI(query_result3)


def dynamicUpdateGraphWithMatchFromOtherOntology(ontologyName, ontologyPrefix, word):
    # mappedProps = mapNewPropertiesWithMyProperties("ArEmotive", "DynamOnto")
    mappedProps = []
    # mappedProps = {
    #     'نوع_العاطفة':'العاطفة',
    #     'ثقة_المصدر':'confidence',
    #     'اللغة': 'ينتمي_للغة',
    #     'شدة_العاطفة': 'قيمتها',
    # }
    result = checkForMatchInOntology(ontologyName, "<" + ontologyPrefix + ">", word)
    print("after check for match in new ontology")
    print(result)
    wordNode = NameSpace(conf.AREMOTIVEPREFIX + word).to_uri()
    classesAsURIs = []
    if result is None:
        return "didn't find any matches"
    for item in result:
        if item ==  "لا مبالاة":
            item = "لا_مبالاة"
        classesAsURIs.append(NameSpace(conf.AREMOTIVEPREFIX + item).to_uri())
    graph = Graph()
    for item in classesAsURIs:
        graph.add((wordNode, RDF.type, item))
    graph.add((wordNode, RDF.type, NameSpace(prop.unrecognized).to_uri()))
    graph.add((wordNode, RDF.type, OWL.NamedIndividual))
    graph.add((wordNode, NameSpace(prop.source).to_uri(), BNode(0)))
    i = 0
    for item in classesAsURIs:
        print("items in classes as URIs: "+item)
        graph.add((BNode(0), RDF.type, item))  # TODO make this susiptable to arrays getWordDialectFromOntology(word,ontologyName,mappedProps)[0]
        graph.add(
            (BNode(0), NameSpace(prop.sourceName).to_uri(), NameSpace(conf.AREMOTIVEPREFIX + ontologyName).to_uri()))
        graph.add((BNode(0), NameSpace(prop.dialect).to_uri(),
                   NameSpace(conf.AREMOTIVEPREFIX + str(getWordDialectFromOntology(word, ontologyName, mappedProps)[0])).to_uri()))
        graph.add((BNode(0), NameSpace(prop.confidence).to_uri(),
                   NameSpace(conf.AREMOTIVEPREFIX + str(getWordConfidenceFromOntology(word, ontologyName, mappedProps)[0])).to_uri()))
        graph.add((BNode(0), NameSpace(prop.confidence).to_uri(), Literal("80", datatype=XSD.int)))
        graph.add((BNode(0), NameSpace(prop.partialWeight).to_uri(), BNode(i + 1)))
        graph.add((BNode(i + 1), RDF.type, item))
        graph.add((BNode(i + 1), NameSpace(prop.emotion).to_uri(), item))
        graph.add((BNode(i + 1), NameSpace(prop.weight).to_uri(),
                   NameSpace(conf.AREMOTIVEPREFIX).to_uri() + Literal(
                      getWordWeightFromOntology(word, ontologyName, mappedProps)[0], datatype=XSD.int)))
        i = i + 2
    fuseki = FusekiUpdate('http://localhost:3030', 'ArEmotive')
    fuseki.insert_graph(graph)


#runDeleteQuery("أزعر")
#dynamicUpdateGraphWithMatchFromOtherOntology("secondaryOntology", conf.SECONDARYONTOLOGYPREFIX, "أزعر")
