from SyntacticFeatures import SyntacticFeatures
from SemanticFeatures import SemanticFeatures
from LexicalFeatures import LexicalFeatures

class Features(object):

    def __init__(self):
        self.text = ""
        self.syntacticFeatures = SyntacticFeatures()
        self.lexicalFeatures = LexicalFeatures()
        self.semanticFeatures = SemanticFeatures()
        self.event = None

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