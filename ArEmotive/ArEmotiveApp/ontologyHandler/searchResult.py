class SearchResult:
    originalSentence = "",
    classificationResults = [],
    classes = [],
    sources = []

    def __init__(self, originalSentence, classificationResults=[], classes=[], sources=[]):
        self.originalSentence = originalSentence
        self.classificationResults = classificationResults
        self.classes = classes
        self.sources = sources


class Source:
    emotion = "",
    confidence = "",
    partialWeight = [],
    sourceName = "",
    dialect = "",
    weight = ""

    def __init__(self,emotion, confidence,partialWeight, sourceName, dialect, weight):
        self.emotion = emotion
        self.confidence = confidence
        self.partialWeight = partialWeight
        self.sourceName = sourceName
        self.dialect = dialect
        self.weight = weight


class PartialWeight:
    emotion = "",
    weight = ""

    def __init__(self, emotion, weight):
        self.emotion = emotion
        self.weight = weight
