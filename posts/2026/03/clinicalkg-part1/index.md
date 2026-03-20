---
title: "The Clinical Knowledge Bridge (Part-1): Extracting RDF Subgraphs from UMLS with Python"
date: 2026-03-19
updated: 2026-03-19
categories: 
  - clinical-knowledge
  - knowledge-graphs
  - healthcare-ao
tags: 
  - umls
  - API 
  - clinical nlp
  - knowledge graphs

medium_url: "https://medium.com/@yourhandle/getting-started-markdown"
difficulty: "intermediate"
series: "Healthcare AI Solutions with Knowledge Graphs"
series_part: 1
related: 
  - ""
---

The Clinical Knowledge Bridge (Part 1): Extracting RDF Subgraphs from UMLS with Python
===

***From fragmented clinical codes to structured knowledge graphs for Healthcare AI***

---

Series Overview

Healthcare AI is at an inflection point. Large Language Models (LLMs) are powerful—but ungrounded. Clinical ontologies are precise—but underutilized.

This series explores how to bridge that gap:
	•	Part 1 (this article): Extracting RDF subgraphs from UMLS
	•	Part 2: Storing and querying clinical graphs with GraphDB / SPARQL
	•	Part 3: Integrating Knowledge Graphs with LLMs (Neuro-symbolic AI)

⸻

1. Introduction: The “Tower of Babel” Is Not Just Linguistic

Healthcare systems don’t just speak different “languages”—they encode different worldviews.
	•	ICD-10 → billing-oriented classification
	•	SNOMED CT → clinical ontology
	•	LOINC → lab measurement semantics

The common narrative frames this as a terminology problem. That framing is incomplete.

Critical View

This is not just about vocabulary mismatch—it is about:
	•	Different abstractions of disease
	•	Different granularity of meaning
	•	Different institutional incentives

The Unified Medical Language System (UMLS) attempts to unify these via Concept Unique Identifiers (CUIs) [1].

But UMLS in its raw form is:
	•	Tabular (RRF files)
	•	API-driven (REST endpoints)
	•	Not inherently “reasoning-ready”

To make it useful for modern AI, we need to transform it into a graph of relationships, not just a lookup table.

⸻

2. Why RDF? Representation vs Reality

Neutral View

RDF (Resource Description Framework) models knowledge as triples:

Subject → Predicate → Object

This enables:
	•	Traversable relationships
	•	Schema interoperability
	•	Querying via SPARQL

Example

Instead of:

“Heart Failure = C0012634”

We get:
	•	Heart Failure → is-a → Cardiovascular Disease
	•	Heart Failure → has finding site → Heart Structure

Philosophical Tension

RDF assumes:

Reality can be modeled as discrete, logical relationships.

But clinical reality is:
	•	Probabilistic
	•	Context-dependent
	•	Often ambiguous

Devil’s Advocate
	•	RDF graphs can create a false sense of certainty
	•	They encode consensus knowledge, not necessarily truth
	•	They struggle with uncertainty compared to probabilistic models

Still, they provide something LLMs lack:

Explicit, inspectable reasoning paths

⸻

3. The Practical Constraint: UMLS API Limits

The UMLS REST API allows:

20 requests per second [2]

This is not a minor implementation detail—it fundamentally shapes system design.

What breaks naive approaches?
	•	Recursive traversal explodes quickly
	•	Redundant API calls waste bandwidth
	•	Rate limits trigger HTTP 429 errors

Incorrect Assumption

“We’ll just parallelize.”

You can’t scale past an external bottleneck.

⸻

4. Engineering Strategy: Controlled Knowledge Extraction

To build a stable RDF extraction pipeline, we need:

1. Throttling

Operate below the limit (~10 req/sec) for stability.

2. Caching (Memoization)

Avoid fetching the same CUI multiple times.

3. Breadth-First Search (BFS)

Control graph expansion using depth-limited traversal.

Why BFS?
	•	Prevents runaway recursion
	•	Ensures uniform exploration
	•	Easier to bound computational cost

⸻

5. Python ETL Pipeline: UMLS → RDF

This implementation is designed for:
	•	Robustness under rate limits
	•	Transparency (progress tracking)
	•	Reusability for healthcare pipelines

import requests
import time
from rdflib import Graph, Literal, RDF, Namespace
from rdflib.namespace import SKOS
from tqdm import tqdm

UMLS = Namespace("https://uts.nlm.nih.gov/umls/")
API_KEY = "YOUR_UMLS_API_KEY"
BASE_URL = "https://uts-ws.nlm.nih.gov/rest/content/current/CUI/"

TARGET_SABS = {
    "SNOMEDCT_US": "SNOMED",
    "ICD10CM": "ICD10",
    "CPT": "CPT",
    "LNC": "LOINC",
    "MSH": "MESH"
}

class UMLSRDFBuilder:
    def __init__(self, api_key):
        self.api_key = api_key
        self.g = Graph()
        self.g.bind("umls", UMLS)
        self.g.bind("skos", SKOS)
        self.visited = set()
        self.last_request_time = 0
        self.min_interval = 0.1

    def _throttle(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_request_time = time.time()

    def fetch_data(self, endpoint):
        self._throttle()
        url = f"{BASE_URL}{endpoint}apiKey={self.api_key}"
        try:
            response = requests.get(url)
            if response.status_code == 429:
                print("Rate limit hit! Sleeping...")
                time.sleep(5)
                return self.fetch_data(endpoint)
            return response.json().get("result", [])
        except Exception as e:
            print(f"Error: {e}")
            return []

    def build_subgraph(self, seed_cuis, depth=1):
        queue = [(cui, depth) for cui in seed_cuis]
        pbar = tqdm(total=len(queue), desc="Building Graph")

        while queue:
            cui, current_depth = queue.pop(0)

            if cui in self.visited:
                pbar.update(1)
                continue

            self.visited.add(cui)
            cui_uri = UMLS[cui]
            self.g.add((cui_uri, RDF.type, SKOS.Concept))

            atoms = self.fetch_data(f"{cui}/atoms?")
            for atom in atoms:
                sab = atom.get("rootSource")
                if sab in TARGET_SABS:
                    code = atom.get("code", "").split("/")[-1]
                    name = atom.get("name")
                    self.g.add((cui_uri, SKOS.notation, Literal(f"{sab}:{code}")))
                    self.g.add((cui_uri, SKOS.prefLabel, Literal(name, lang="en")))

            if current_depth > 0:
                rels = self.fetch_data(f"{cui}/relations?")
                for rel in rels:
                    target_cui = rel.get("relatedId", "").split("/")[-1]
                    rel_label = rel.get("additionalRelationLabel", "related_to")

                    target_uri = UMLS[target_cui]
                    self.g.add((cui_uri, UMLS[rel_label], target_uri))

                    if target_cui not in self.visited:
                        queue.append((target_cui, current_depth - 1))
                        pbar.total += 1

            pbar.update(1)

        pbar.close()
        return self.g


builder = UMLSRDFBuilder(API_KEY)
rdf_graph = builder.build_subgraph(["C0012634"], depth=1)

with open("umls_subgraph.ttl", "wb") as f:
    f.write(rdf_graph.serialize(format="turtle").encode("utf-8"))


⸻

6. Output: From Codes to Context

The result is a Turtle (.ttl) file representing a semantic subgraph.

Example:
	•	umls:C0012634 → Heart Failure
	•	Relationships → anatomy, hierarchy, associations
	•	Mappings → SNOMED, ICD-10, MeSH

This transforms:

Static codes → Dynamic clinical knowledge

⸻

7. Performance Reality Check

A critical (often ignored) constraint:
	•	Depth = 1 → manageable
	•	Depth = 2 → hundreds of nodes
	•	Depth ≥ 3 → impractical via API

Recommendation

For production systems:
	•	Download UMLS RRF files
	•	Load into PostgreSQL
	•	Perform local graph extraction

Contrarian View

If you’re doing this at scale:

The REST API approach may be the wrong abstraction entirely.

⸻

8. What This Enables (and What It Doesn’t)

What it enables
	•	Structured clinical reasoning
	•	Cross-ontology mapping
	•	Explainable AI pipelines

What it does NOT solve
	•	Clinical uncertainty
	•	Missing or biased knowledge
	•	Real-time inference at scale

⸻

9. Toward Neuro-Symbolic Healthcare AI

This pipeline is a stepping stone toward:

Hybrid systems combining symbolic graphs + LLMs

Why this matters
	•	LLMs → fluent but unreliable
	•	Knowledge graphs → precise but rigid

Together:

Potentially accurate AND explainable AI

Skeptical Note

Neuro-symbolic AI is still:
	•	Experimentally promising
	•	Not widely validated in production healthcare

⸻

10. Conclusion: Building the Bridge

Extracting RDF subgraphs from UMLS is not just a data transformation task—it is an architectural shift:
	•	From lookup → relationships
	•	From data → meaning
	•	From generation → reasoning

But it comes with trade-offs:
	•	Complexity
	•	Performance constraints
	•	Modeling assumptions

The real question is not:

“Can we build knowledge graphs?”

But:

“Where do they genuinely outperform simpler systems?”

⸻

References (IEEE Style)

[1] O. Bodenreider, “The Unified Medical Language System (UMLS): integrating biomedical terminology,” Nucleic Acids Research, vol. 32, pp. D267–D270, 2004.

[2] U.S. National Library of Medicine, “UMLS REST API Documentation,” 2024.

[3] G. Besold et al., “Neural-Symbolic Learning and Reasoning: A Survey and Interpretation,” arXiv preprint arXiv:1711.03902, 2017.

⸻

Author’s Note: 

If you’re working on healthcare AI, semantic layers, or knowledge graphs, I’d be interested in what you think:
_Where in Symbolic systems still outperform purely statistical AI - and where they don’t._

⸻


[Back to 2026](../README.md) | [← February 2026](../02) | [April 2026 →](../04)