# when u start with a sentence u first look for matches between words from the given sentence and the ontology
# now : this matching is exclusively literal and if we want to include a second way of matching
# which is search for literal matches and stem of the original word match
# ex: newWord = oldWord => match
# ex: stem(newWord) = word from ontology => also match
# we should set this constant to 1

MATCHINGMODE = 1

# classification mode refers to how macy classes do u want the hugging face classification process to return
# for example 3 would mean the highest 3 matching sentimental classes

CLASSIFICATIONMODE = 3

# huggingFace allows the classification process to have a full sentence as input
# if we wish to enable this method we can change this value to 1

WHOLESENTENCECLASSIFICATION = 1

# KIM that these prefixes are formatted as URIs for sparql queries and ad strings for other purposes
# sencodaryOntology Prefix

SECONDARYONTOLOGYPREFIX = "http://www.semanticweb.org/asus/ontologies/2022/5/untitled-ontology-22#"
SECONDARYONTOLOGYURIPREFIX = "<http://www.semanticweb.org/asus/ontologies/2022/5/untitled-ontology-22#>"

# ArEmotive Prefix
AREMOTIVEPREFIX = "http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#"
AREMOTIVEURIPREFIX = "<http://www.semanticweb.org/asus/ontologies/2022/2/untitled-ontology-12#>"

# DynamOnto Prefixes
DYNAMONTOPREFIX = "http://www.semanticweb.org/asus/ontologies/2022/8/untitled-ontology-27#"
DYNAMONTOURIPREFIX = "<http://www.semanticweb.org/asus/ontologies/2022/8/untitled-ontology-27#>"
