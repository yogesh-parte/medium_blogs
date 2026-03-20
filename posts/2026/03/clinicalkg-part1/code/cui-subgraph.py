import requests
import time
from rdflib import Graph, Literal, RDF, Namespace, URIRef
from rdflib.namespace import SKOS, RDFS

# Official UMLS Base URI and Namespaces
UMLS = Namespace("https://uts.nlm.nih.gov/umls/")
API_KEY = "YOUR_UMLS_API_KEY"
BASE_URL = "https://uts-ws.nlm.nih.gov/rest"

# The specific vocabularies you requested
TARGET_SABS = {
    "SNOMEDCT_US": "SNOMED",
    "ICD10CM": "ICD10",
    "CPT": "CPT",
    "LNC": "LOINC",
    "MSH": "MESH"
}

class UMLSSubgraphExtractor:
    def __init__(self, api_key):
        self.api_key = api_key
        self.g = Graph()
        self.g.bind("umls", UMLS)
        self.g.bind("skos", SKOS)
        self.visited = set()

    def get_data(self, endpoint):
        """Standard GET request with rate-limiting and API Key."""
        # Rate limiting: UMLS allows 20 req/sec; we stay safe at 10
        time.sleep(0.1) 
        url = f"{BASE_URL}{endpoint}"
        params = {'apiKey': self.api_key}
        
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json().get("result", [])
            elif response.status_code == 429:
                time.sleep(2) # Back off if rate-limited
                return self.get_data(endpoint)
            return []
        except Exception as e:
            print(f"Connection error: {e}")
            return []

    def extract(self, cui, depth=1):
        if cui in self.visited or depth < 0:
            return
        
        self.visited.add(cui)
        cui_uri = UMLS[cui]
        self.g.add((cui_uri, RDF.type, SKOS.Concept))

        # 1. Official 'Atoms' Logic: Get Source Codes (SNOMED, ICD, LOINC, etc.)
        atoms = self.get_data(f"/content/current/CUI/{cui}/atoms")
        for atom in atoms:
            sab = atom.get("rootSource")
            if sab in TARGET_SABS:
                # Store the code as a notation and the name as a label
                code = atom.get("code", "").split("/")[-1]
                name = atom.get("name")
                self.g.add((cui_uri, SKOS.notation, Literal(f"{sab}:{code}")))
                self.g.add((cui_uri, SKOS.prefLabel, Literal(name, lang="en")))

        # 2. Official 'Relations' Logic: Build the Graph Edges
        if depth > 0:
            relations = self.get_data(f"/content/current/CUI/{cui}/relations")
            for rel in relations:
                # Filter for meaningful relationships
                target_uri_str = rel.get("relatedId", "")
                target_cui = target_uri_str.split("/")[-1]
                rel_label = rel.get("additionalRelationLabel", "related_to")
                
                if target_cui and rel_label:
                    target_node = UMLS[target_cui]
                    # Create the edge
                    self.g.add((cui_uri, UMLS[rel_label], target_node))
                    # Recurse
                    self.extract(target_cui, depth - 1)

    def save(self, filename="subgraph.ttl"):
        self.g.serialize(destination=filename, format="turtle")
        print(f"Success! RDF subgraph saved to {filename}")

# Usage for your Article
extractor = UMLSSubgraphExtractor(API_KEY)
extractor.extract("C0012634", depth=1) # Example: Heart Failure
extractor.save("umls_clinical_graph.ttl")