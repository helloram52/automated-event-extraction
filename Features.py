from SyntacticFeatures import SyntacticFeatures
from SemanticFeatures import SemanticFeatures
from LexicalFeatures import LexicalFeatures

class Features(object):

    def __init__(self, text, actual):
        self.text = text
        self.syntacticFeatures = SyntacticFeatures()
        self.lexicalFeatures = LexicalFeatures()
        self.semanticFeatures = SemanticFeatures()
        self.event = None
        self.actual = actual
        self.predict = "no"

    def setPredict(self, predict):
        self.predict = predict

    def getPredicted(self):
        return self.predict

    def getActual(self):
        return self.actual

    def setEvent(self, event):
        self.event = event

    def setText(self, text):
        self.text = text

    def getText(self):
        return self.text

    def getEvent(self):
        return self.event

    def getLexicalFeatures(self):
        return self.lexicalFeatures

    def getSyntacticFeatures(self):
        return self.syntacticFeatures

    def getSemanticFeatures(self):
        return self.semanticFeatures