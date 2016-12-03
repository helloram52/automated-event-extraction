import nltk, sys, re
from nltk.corpus import wordnet
from enchant.checker import SpellChecker
from autocorrect import spell
import timex, Utilities
from Event import Event
from nltk.tag import StanfordNERTagger


ENFORCE_LOWER_CASE = True
KEYWORDS = ['marriage', 'birthday', 'meeting', 'anniversary', 'seminar']
SYNONYMS_FOR_KEYWORDS = {}
PAST_TENSE_TAGS = ['VBD','VBN']
TIMEX_TAG = "<TIMEX2>"
STANFORD_NER_PATH = '/Users/vads/Downloads/stanford-ner-2014-06-16/stanford-ner.jar'

def initialize():
    setupKeywords()
    SYNONYMS_FOR_KEYWORDS['seminar'].append('lecture')
    Utilities.setupLog()

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

#get synonyms for given word
def getSynonyms(word):
    lemmas = []
    synsets = wordnet.synsets(word)
    for sense in synsets:
        lemmas += [re.sub("_", " ", lemma.name()) for lemma in sense.lemmas()]
    return list(set(lemmas))

def setupKeywords():
    # get all synonyms for given keywords
    global SYNONYMS_FOR_KEYWORDS
    for word in KEYWORDS:
        SYNONYMS_FOR_KEYWORDS[word] = getSynonyms(word)

def isRequiredEvent(line, dict):
    for word in dict:
        for synonym in dict[word]:
            if synonym in line:
                return True, word
    return False, ""

def getCommandLineArgs():
    return sys.argv[1], sys.argv[2]

def preProcessData(input):
    # read input file
    inputData = parseInputFile(inputFileName)
    # perform spell correction
    correctSentence = performSpellCorrection(inputData)
    # split text into lines based on delimiter
    lines = Utilities.split(correctSentence, ".")

    return lines

def performTagging(lines):
    taggedLines = []
    for line in lines:
        taggedLine = ""
        try:
            taggedLine = timex.tag(line)
            taggedLine = timex.ground(taggedLine, timex.gmt())
        except:
            taggedLine = ""

        if not Utilities.isEmpty(taggedLine):
            taggedLines.append(taggedLine)

    return taggedLines

    
#check whether event is past
def isEventPast(line):
    initialTokens = Utilities.split(line, " ")
    tokens = []
    #remove empty or dummy tokens
    for token in initialTokens:
        if not Utilities.isEmpty(token):
            tokens.append(token)

    taggedWords = nltk.pos_tag(tokens)

    for (word, tag) in taggedWords:
        if tag in PAST_TENSE_TAGS:
            return True
    return False

def parseLocation(event):
    event = re.sub("<TIMEX2>|</TIMEX2>", "", event)
    print "event: {}".format(event)

    entities = []
    try:
        nerTagger = StanfordNERTagger('/Users/vads/Downloads/stanford-ner-2014-06-16/classifiers/english.muc.7class.distsim.crf.ser.gz', STANFORD_NER_PATH)
        entities = nerTagger.tag(event.split())
    except:
        print("Unexpected error:", sys.exc_info()[0])

    result = ""
    for entity in entities:
        print "entity: {}".format(entity)
        if entity[1] != 'O':
            result += entity[0]

    print "location: {}".format(result)
    return result

def setupEvent(event):
    eventDate = Utilities.parseDate(event)
    eventLocation = parseLocation(event)
    return Event(eventType, eventDate, eventLocation)

if __name__ == '__main__':
    #initialize variables
    initialize()

    #read commmand line parameters
    inputFileName, outputFileName = getCommandLineArgs()

    #preprocess input data
    lines = preProcessData(inputFileName)

    #perform temporal expression tagging
    taggedLines = performTagging(lines)

    #select lines which have <TIMEX2> tag
    events = Utilities.filter(taggedLines, TIMEX_TAG)

    #for lines identified as events, check each whether any word matches with synonyms for keywords
    for event in events:
        isRequired, eventType = isRequiredEvent(event, SYNONYMS_FOR_KEYWORDS)
        if isRequired:
            eventObj = setupEvent(event)
            if not isEventPast(event):
                Utilities.writeOutput(outputFileName, eventObj.format())
            else:
                if Utilities.isDateInFuture(event):
                    Utilities.writeOutput(outputFileName, eventObj.format())
                else:
                    Utilities.writeLog("INFO: Event Detected but is identified as past event                   :" + event)
        else:
            Utilities.writeLog("INFO: Event Detected but event type did not match with required events :" + event)

