
class SyntacticFeatures(object):

    def __init__(self):
        self.POSTags = []
        self.temporalTag = ""

    def setPOSTags(self, tags):
        self.POSTags = tags

    def setTemporalTag(self, tag):
        self.temporalTag = tag

    def getTemporalTag(self):
        return self.temporalTag

    def getPOSTags(self):
        return self.POSTags