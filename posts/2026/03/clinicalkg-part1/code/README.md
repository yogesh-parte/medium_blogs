# Code Samples - UMLS RDF Subgraph Extraction

This folder contains the complete Python implementation for extracting RDF subgraphs from the UMLS REST API, as described in the blog post.

## Files

- `cui-subgraph.py` - Complete ETL pipeline for UMLS → RDF transformation

## Prerequisites

### Required Libraries
- `requests` - HTTP client for UMLS API
- `rdflib` - RDF graph manipulation and serialization
- `time` - Rate limiting and delays

### Installation
```bash
pip install requests rdflib
```

### UMLS API Key
You need a free API key from the U.S. National Library of Medicine:

1. Register at: https://uts.nlm.nih.gov/uts/signup-login
2. Get your API key from the UTS profile
3. Replace `YOUR_UMLS_API_KEY` in the code

## Running the Code

### Basic Usage
```python
from cui_subgraph import UMLSSubgraphExtractor

# Initialize with your API key
extractor = UMLSSubgraphExtractor("your_api_key_here")

# Extract subgraph for Heart Failure (C0012634)
extractor.extract("C0012634", depth=1)

# Save as Turtle RDF file
extractor.save("umls_clinical_graph.ttl")
```

### Command Line Execution
```bash
python cui-subgraph.py
```

### Output
- Generates `umls_clinical_graph.ttl` - RDF graph in Turtle format
- Contains clinical concepts with relationships and cross-references
- Ready for loading into GraphDB, Neo4j, or other graph databases

## Key Features

### 1. Rate Limiting & Error Handling
- Respects UMLS API limits (20 req/sec)
- Automatic backoff on rate limit errors (HTTP 429)
- Connection error recovery

### 2. Controlled Graph Expansion
- Breadth-first search (BFS) for predictable growth
- Configurable depth limits
- Caching to avoid redundant API calls

### 3. Multi-Vocabulary Support
Extracts codes from:
- SNOMED CT (SNOMEDCT_US)
- ICD-10-CM (ICD10CM)
- CPT (CPT)
- LOINC (LNC)
- MeSH (MSH)

### 4. RDF Standards Compliance
- Uses SKOS vocabulary for concept modeling
- Proper URI namespaces
- Turtle serialization format

## Configuration

### Depth Control
```python
# Shallow extraction (recommended for testing)
extractor.extract("C0012634", depth=1)

# Deeper relationships (may hit API limits)
extractor.extract("C0012634", depth=2)
```

### Custom Vocabularies
Modify `TARGET_SABS` dictionary to include/exclude specific source vocabularies.

## Performance Notes

- **Depth 1**: ~10-20 API calls, fast
- **Depth 2**: ~100-200 API calls, moderate
- **Depth 3+**: Thousands of calls, may timeout

For production use, consider downloading UMLS RRF files and using local databases.

## Output Format

The generated Turtle file contains:
- Concept nodes with UMLS URIs
- SKOS labels and notations
- Relationship edges between concepts
- Cross-references to source vocabularies

## Example Output Structure

```turtle
@prefix umls: <https://uts.nlm.nih.gov/umls/> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .

umls:C0012634 a skos:Concept ;
    skos:prefLabel "Heart Failure"@en ;
    skos:notation "SNOMEDCT_US:84114007" ;
    skos:notation "ICD10CM:I50.9" ;
    umls:isa umls:C0018799 .  # Relationship to Cardiovascular Disease
```

## Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure your UMLS API key is valid and active
2. **Rate Limiting**: Reduce depth or add longer delays between calls
3. **Empty Results**: Check CUI validity and network connectivity
4. **Import Errors**: Install required packages with `pip install requests rdflib`

### Debug Mode
Add print statements to track API calls and graph construction.

## License & Usage

This code is provided as-is for educational and research purposes. Ensure compliance with UMLS license terms when using extracted data.

## Related Resources

- [UMLS REST API Documentation](https://documentation.uts.nlm.nih.gov/rest/home.html)
- [RDFLib Documentation](https://rdflib.readthedocs.io/)
- [SKOS Vocabulary](https://www.w3.org/2009/08/skos-reference/skos.html)
