from pyfuseki import FusekiUpdate, FusekiQuery, AsyncFuseki, AsyncFusekiResp
from pyfuseki.rdf import rdf_prefix, NameSpace as ns, NameSpace
from rdflib import Graph, OWL, RDFS
from pyfuseki.rdf import rdf_property
from rdflib import URIRef as uri, Literal
from rdflib import RDF, BNode
import asyncio
import pyfuseki
from rdflib.namespace import XSD
import requests


def createConfidenceRelationship():
    confidenceRelationship = NameSpace("http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#confidence").to_uri()
    emotionClassURI = NameSpace("http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#العاطفة").to_uri()
    g = Graph()
    g.add((confidenceRelationship, RDF.type, OWL.DatatypeProperty))
    g.add((confidenceRelationship, RDFS.domain, emotionClassURI))
    g.add((confidenceRelationship, RDFS.range, BNode(1)))
    g.add((BNode(1), RDF.type, RDFS.Datatype))
    g.add((BNode(1), OWL.onDatatype, XSD.int))
    g.add((BNode(1), OWL.withRestrictions, BNode(2)))
    g.add((BNode(3), XSD.minInclusive, Literal('0', datatype=XSD.int)))
    g.add((BNode(2), RDF.first, BNode(3)))
    g.add((BNode(2), RDF.rest, BNode(4)))
    g.add((BNode(5), XSD.maxExclusive, Literal('100', datatype=XSD.int)))
    g.add((BNode(4), RDF.first, BNode(5)))
    g.add((BNode(4), RDF.rest, RDF.nil))
    fuseki = FusekiUpdate('http://localhost:3030', 'ArEmotive')
    fuseki.insert_graph(g)


def createPartialWeightRelationship(node,emotionclass,partialWeight):
    """
<http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#term> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#anger> .
<http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#term> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#love> .
<http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#term> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#hate> .
<http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#term> <http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#p_weight> _:genid1 .
<http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#term> <http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#p_weight> _:genid2 .
_:genid1 <http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#emotion> <http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#Anger> .
_:genid1 <http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#weight> "2" .
_:genid2 <http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#emotion> <http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#Love> .
_:genid2 <http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#weight> "3" .
    """
    partialWeightRelationship = NameSpace(
        "http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#partialWeight").to_uri()
    weightRelationship = "قيمتها"
    emotionClassURI = NameSpace(
        "http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#العاطفة").to_uri()
    prefix = "http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#"
    weightRelationshipUri = NameSpace(prefix + weightRelationship).to_uri()
    #wordUri = NameSpace(prefix+word).to_uri()
    newEmotionUri = NameSpace(prefix+emotionclass).to_uri()
    g = Graph()
    g.add((node,partialWeightRelationship,BNode(1)))
    g.add((BNode(1),emotionClassURI,newEmotionUri))
    g.add((BNode(1),weightRelationshipUri, Literal(partialWeight, datatype=XSD.int)))
    fuseki = FusekiUpdate('http://localhost:3030', 'ArEmotive')
    fuseki.insert_graph(g)


def createSecondaryOntologyTestProps():
    prefix = "http://www.semanticweb.org/asus/ontologies/2022/5/untitled-ontology-22#"
    newProps = ['ينتمي','القيمة','الثقة']
    g = Graph()
    g.add((NameSpace(prefix+newProps[0]).to_uri(),RDF.type,OWL.ObjectProperty))
    g.add((NameSpace(prefix + newProps[1]).to_uri(), RDF.type, OWL.DatatypeProperty))
    g.add((NameSpace(prefix + newProps[2]).to_uri(), RDF.type, OWL.DatatypeProperty))
    fuseki = FusekiUpdate('http://localhost:3030', 'secondaryOntology')
    fuseki.insert_graph(g)


#createSecondaryOntologyTestProps()

prefix = "http://www.semanticweb.org/asus/ontologies/2022/5/untitled-ontology-22#"
yantamiRelation = NameSpace(prefix+"ينتمي").to_uri()
levantineDialect = NameSpace(prefix+"levantine").to_uri()
weightProp = NameSpace(prefix+"القيمة").to_uri()
confProp = NameSpace(prefix+"الثقة").to_uri()
newWord = NameSpace(prefix+"أزعر").to_uri()
alshddeProp = NameSpace(prefix+"الشدة").to_uri()
alshdde = NameSpace(prefix+"سلبية_منخفضة").to_uri()
g = Graph()
g.add((newWord,RDF.type,OWL.NamedIndividual))
g.add((newWord,RDF.type,NameSpace(prefix+"أذية").to_uri()))
g.add((newWord,yantamiRelation,levantineDialect))
#g.add((newWord, confProp, OWL.DatatypeProperty)) # TODO should be replaced with شدة عاطفية
g.add((newWord, weightProp, Literal("-6", datatype=XSD.int)))
g.add((newWord,alshddeProp,alshdde))
g.add((newWord,confProp,Literal("60", datatype=XSD.int)))
fuseki = FusekiUpdate('http://localhost:3030', 'secondaryOntology')
fuseki.insert_graph(g)




def runDeleteQuery():
    deleteQuery = """
    DELETE WHERE{
    <http://www.semanticweb.org/asus/ontologies/2022/5/untitled-ontology-22#بنتمي> ?pred ?obj
    } 
    """
    url = "http://localhost:3030/secondaryOntology/update"
    queryObject = {'query': 'update',
                   'update': deleteQuery}
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    x = requests.post(url, params=queryObject, headers=headers)
    print(x.text)

#runDeleteQuery()