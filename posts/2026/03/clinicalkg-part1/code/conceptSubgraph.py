#

""" Extracting RDF Subgraphs from UMLS with Python
To generate a subgraph from a string name (like "Hypertension" or "Metformin") instead of a CUI, 
we need to add a "Search" step. The script must first resolve your string to the most relevant CUI 
before starting the recursive graph extraction.

This is a common workflow for "Entity Linking" in clinical NLP.

String-to-RDF Subgraph Script
This script adds a search_cui method that uses the UMLS /search endpoint. 
It defaults to an exact match to ensure high precision for your inference engine.
 """

import requests
import time
from rdflib import Graph, Literal, RDF, Namespace
from rdflib.namespace import SKOS

UMLS = Namespace("https://uts.nlm.nih.gov/umls/")
API_KEY = "YOUR_UMLS_API_KEY"
BASE_URL = "https://uts-ws.nlm.nih.gov/rest"

TARGET_SABS = {"SNOMEDCT_US", "ICD10CM", "CPT", "LNC", "MSH"}

class UMLSStringGrapher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.g = Graph()
        self.g.bind("umls", UMLS)
        self.g.bind("skos", SKOS)
        self.visited = set()

    def _call_api(self, endpoint, params=None):
        """Internal helper for rate-limited GET requests."""
        time.sleep(0.1) # 10 requests per second safety
        url = f"{BASE_URL}{endpoint}"
        query_params = {'apiKey': self.api_key}
        if params: query_params.update(params)
        
        response = requests.get(url, params=query_params)
        return response.json().get("result", []) if response.status_code == 200 else []

    def search_cui(self, term):
        """Converts a string term to its best-match UMLS CUI."""
        params = {
            'string': term,
            'searchType': 'exact', # Use 'words' for broader matching
            'returnIdType': 'concept'
        }
        results = self._call_api("/search/current", params)
        if results:
            return results[0].get("ui") # Return the top hit's CUI
        return None

    def build_from_string(self, term, depth=1):
        """Resolves string to CUI and begins recursive extraction."""
        print(f"Searching for term: '{term}'...")
        cui = self.search_cui(term)
        
        if not cui:
            print(f"No CUI found for '{term}'. Try a different term or 'searchType=words'.")
            return
        
        print(f"Found CUI: {cui}. Building subgraph...")
        self._extract_recursive(cui, depth)

    def _extract_recursive(self, cui, depth):
        if cui in self.visited or depth < 0: return
        self.visited.add(cui)
        cui_uri = UMLS[cui]
        self.g.add((cui_uri, RDF.type, SKOS.Concept))

        # Get Atoms (Source Codes)
        atoms = self._call_api(f"/content/current/CUI/{cui}/atoms")
        for atom in atoms:
            sab = atom.get("rootSource")
            if sab in TARGET_SABS:
                code = atom.get("code", "").split("/")[-1]
                self.g.add((cui_uri, SKOS.notation, Literal(f"{sab}:{code}")))
                self.g.add((cui_uri, SKOS.prefLabel, Literal(atom.get("name"), lang="en")))

        # Get Relations
        if depth > 0:
            rels = self._call_api(f"/content/current/CUI/{cui}/relations")
            for rel in rels:
                target_cui = rel.get("relatedId", "").split("/")[-1]
                label = rel.get("additionalRelationLabel", "related_to")
                if target_cui:
                    self.g.add((cui_uri, UMLS[label], UMLS[target_cui]))
                    self._extract_recursive(target_cui, depth - 1)

    def save_ttl(self, filename):
        self.g.serialize(destination=filename, format="turtle")
        print(f"Graph saved to {filename}")

# Usage
engine = UMLSStringGrapher(API_KEY)
engine.build_from_string("Atrial Fibrillation", depth=1)
engine.save_ttl("string_subgraph.ttl")