import fdp
from rdflib import Namespace, URIRef, Literal
from rdflib.namespace import RDF
from SPARQLWrapper import SPARQLWrapper2

DCAT = Namespace("http://www.w3.org/ns/dcat#")

with open("queries/dexamethasone.sparql") as file:
    query = file.read()

client = fdp.Client()
distFilter = lambda g: (None, RDF.type, DCAT.Distribution) in g

for dist in client.getResources("https://twoc.fair-dtls.surf-hosted.nl", distFilter):
    for s in dist.subjects(RDF.type, DCAT.Distribution):
        if (s, DCAT.mediaType, Literal("application/sparql-results+json")) not in dist:
            continue

        accessURL = dist.value(s, DCAT.accessURL)

        print(f"found sparql endpoint {accessURL}")

        sparql = SPARQLWrapper2(accessURL)
        sparql.setQuery(query)

        for result in sparql.query().bindings:
            for x in result.items():
                print(x)
