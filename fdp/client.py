from rdflib import Graph, URIRef, Namespace
from rdflib.namespace import RDF

LDP = Namespace("http://www.w3.org/ns/ldp#")

class Client:
    def __init__(self):
        pass

    def getResources(self, endpoint, resource_filter=None):
        stack = [ endpoint ]

        return self.parseResource(endpoint, stack, resource_filter)

    def parseResource(self, resource, stack, resource_filter):
        g = Graph()
        g.parse(resource)

        resources = []

        if resource_filter and resource_filter(g):
            resources.append(g)

        for s in g.subjects(RDF.type, LDP.DirectContainer):
            for child in g.objects(s, LDP.contains):
                if child not in stack:
                    stack.append(child)
                    resources.extend(self.parseResource(child, stack, resource_filter))
        
        return resources
