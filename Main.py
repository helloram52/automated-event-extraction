import nltk, sys, re
from nltk.corpus import wordnet
from enchant.checker import SpellChecker
from autocorrect import spell

ENFORCE_LOWER_CASE = True
KEYWORDS = ['marriage', 'birthday', 'meeting', 'anniversary', 'seminar']

#parse input file - read all the input lines
def parseInputFile(inputFileName):
    inputString = ""
    with open(inputFileName, 'r') as inputFile:
        for line in inputFile:
            inputString = inputString.join(line)

    return inputString.lower() if ENFORCE_LOWER_CASE else inputString

#perform spell correction
def performSpellCorrection(line):
    checker = SpellChecker("en_US", line)
    for word in checker:
        word.replace(spell(word.word))

    return checker.get_text()

def getSynonyms(words):
    lemmas = []
    for word in words:
        synsets = wordnet.synsets(word)
        for sense in synsets:
            lemmas += [re.sub("_", " ", lemma.name()) for lemma in sense.lemmas()]
    return list(set(lemmas))

def isRequiredEvent(line, dict):
    for word in dict:
        if word in line:
            return True
    return False

if __name__ == '__main__':
    #read commmand line params
    inputFileName = sys.argv[1]
    outputFileName = sys.argv[2]

    #read input file
    inputData = parseInputFile(inputFileName)

    #perform spell correction
    correctSentence = performSpellCorrection(inputData)

    #get all synonyms for given keywords
    synonymsForKeywords = getSynonyms(KEYWORDS)

    #for lines identified as events, check each whether any word matches with synonyms for keywords
    if isRequiredEvent(correctSentence, synonymsForKeywords):
        print "Required Event:" + correctSentence

    pass