
class LexicalFeatures(object):

    def __init__(self):
        self.tokens = []
        self.spellCorrection = ""

    def setTokens(self, tokens):
        self.tokens = tokens

    def setSpellCorrection(self, sentence):
        self.spellCorrection = sentence

    def getSpellCorrection(self):
        return self.spellCorrection

    def getTokens(self):
        return self.tokens