
class SemanticFeatures(object):

    def __init__(self):
        self.synonym = ""
        self.location = ""

    def setSynonym(self, word):
        self.synonym = word

    def setLocation(self, location):
        self.location = location

    def getSynonym(self):
        return self.synonym

    def getLocation(self):
        return self.location