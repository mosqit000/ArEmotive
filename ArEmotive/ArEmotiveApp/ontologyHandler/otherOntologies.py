from pyfuseki import FusekiUpdate, FusekiQuery, AsyncFuseki, AsyncFusekiResp
from pyfuseki.rdf import rdf_prefix, NameSpace as ns, NameSpace
from rdflib import Graph, OWL, BNode
from pyfuseki.rdf import rdf_property
from rdflib import URIRef as uri, Literal
from rdflib import RDF
import asyncio
import pyfuseki
import requests
import ArEmotiveApp.ontologyHandler.jenaOntologyFunctions as jof
import ArEmotiveApp.ontologyHandler.config as conf

fuseki_query = FusekiQuery('http://localhost:3030', 'secondaryOntology')  # this is the Sync way
async_fuseki = AsyncFuseki('http://localhost:3030', 'secondaryOntology')  # this is the ASync way
jof.getClassesFromOntology("secondaryOntology")
jof.getInstancesFromOntology("secondaryOntology")
jof.getRelationshipsFromOntology("secondaryOntology")
prefix = conf.SECONDARYONTOLOGYURIPREFIX
# jof.checkForMatchInOntology("secondaryOntology",prefix,"احتقار")
# jof.runDeleteQuery("احتقار")
jof.updateGraphWithMatchFromOtherOntology("secondaryOntology", conf.SECONDARYONTOLOGYPREFIX, "تعبان")
