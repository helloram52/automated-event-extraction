import nltk, sys, re
from nltk.corpus import wordnet
from enchant.checker import SpellChecker
from autocorrect import spell
import timex, Utilities
from Event import Event
from nltk.tag import StanfordNERTagger
from Features import Features

KEYWORDS = ['marriage', 'birthday', 'meeting', 'anniversary', 'seminar']
SYNONYMS_FOR_KEYWORDS = {}
PAST_TENSE_TAGS = ['VBD','VBN']
TIMEX_TAG = "</TIMEX2>"
#STANFORD_NER_ROOT = "/Users/vads/Downloads/stanford-ner-2014-06-16/"
STANFORD_NER_ROOT = "/home/ram/Downloads/stanford-ner-2014-06-16/"
STANFORD_NER_PATH = STANFORD_NER_ROOT + 'stanford-ner.jar'
RESULT = []
RESULT_HEADER = ["Event", "When", "Where", "Original Text", "Lexical-Tokens", "Lexical-SpellCorrection", "Syntactic-POS tags", "Syntactic-Temporal tag", "Semantic-Synonym", "Semantic-Location" ]
TIMEX_TAG_REGEX = r'<TIMEX2 .+>.+?</TIMEX2>'

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

    return inputString

#perform spell correction
def performSpellCorrection(featureObj):
    checker = SpellChecker("en_US", featureObj.getText())
    for word in checker:
        word.replace(spell(word.word))

    featureObj.getLexicalFeatures().setSpellCorrection(checker.get_text())

    return featureObj

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

def isRequiredEvent(obj, dict):
    for word in dict:
        for synonym in dict[word]:
            if synonym in obj.getText().lower():
                obj.getSemanticFeatures().setSynonym(str(dict[word]))
                return True, word
    return False, ""

def getCommandLineArgs():
    if len(sys.argv) < 2:
        print "ERROR: Usage: Main.py <input> <output>"
        exit(1)

    return sys.argv[1], sys.argv[2]

def preProcessData(input):
    # read input file
    inputData = parseInputFile(inputFileName)
    # split text into lines based on delimiter
    lines = Utilities.split(inputData, ".")
    featureObjects = []
    for line in lines:
        featureObject = Features()
        featureObject.setText(line)
        # perform spell correction
        featureObjects.append(performSpellCorrection(featureObject))

    return featureObjects

def performTagging(featureObjects):
    taggedLines = []
    for obj in featureObjects:
        taggedLine = ""
        try:
            taggedLine = timex.tag(obj.getLexicalFeatures().getSpellCorrection().lower())
            taggedLine = timex.ground(taggedLine, timex.gmt())
        except:
            taggedLine = ""

        if not Utilities.isEmpty(taggedLine):
            obj.getSyntacticFeatures().setTemporalTag(Utilities.firstMatching(TIMEX_TAG_REGEX, taggedLine))
            taggedLines.append(obj)

    return taggedLines

#check whether event is past
def isEventPast(obj):
    initialTokens = Utilities.split(obj.getText().lower(), " ")

    obj.getLexicalFeatures().setTokens(initialTokens)

    tokens = []
    #remove empty or dummy tokens
    for token in initialTokens:
        if not Utilities.isEmpty(token):
            tokens.append(token)

    taggedWords = nltk.pos_tag(tokens)
    obj.getSyntacticFeatures().setPOSTags(taggedWords)

    for (word, tag) in taggedWords:
        if tag in PAST_TENSE_TAGS:
            return True
    return False

def parseLocation(obj):
    event = re.sub("<TIMEX2>|</TIMEX2>", "", obj.getLexicalFeatures().getSpellCorrection())
    #print "event: {}".format(event)

    entities = []
    try:
        nerTagger = StanfordNERTagger( STANFORD_NER_ROOT + '/classifiers/english.muc.7class.distsim.crf.ser.gz', STANFORD_NER_PATH)
        entities = nerTagger.tag(event.split())
    except:
        print("Unexpected error:", sys.exc_info()[0])

    result = ""
    for entity in entities:
        if entity[1] != 'O':
            result +=  " {}".format( entity[0] )

    #print "location: {}".format(result)
    obj.getSemanticFeatures().setLocation(result)
    return result

def setupEvent(obj, eventType):
    eventDate = Utilities.parseDate(obj.getSyntacticFeatures().getTemporalTag())
    eventLocation = parseLocation(obj)
    return Event(eventType, eventDate, eventLocation)

if __name__ == '__main__':
    #initialize variables
    initialize()

    #read commmand line parameters
    inputFileName, outputFileName = getCommandLineArgs()

    #preprocess input data
    featureObjects = preProcessData(inputFileName)

    #perform temporal expression tagging
    taggedLines = performTagging(featureObjects)

    #select lines which have <TIMEX2> tag
    eventsList = Utilities.filter(taggedLines, TIMEX_TAG)

    #for lines identified as events, check each whether any word matches with synonyms for keywords
    for obj in eventsList:
        #print "event: {}".format(event)
        isRequired, eventType = isRequiredEvent(obj, SYNONYMS_FOR_KEYWORDS)
        if isRequired:
            eventObj = setupEvent(obj, eventType)
            obj.setEvent(eventObj)
            if not isEventPast(obj):
                #["Original Text", "Lexical-Tokens", "Lexical-SpellCorrection", "Syntactic-POS tags", "Syntactic-Temporal tag", "Semantic-Synonym", "Semantic-Location" ]
                RESULT.append([obj.getEvent().type,
                                 obj.getEvent().date,
                                 obj.getEvent().location,
                                 obj.getText(),
                                 str(obj.getLexicalFeatures().getTokens()),
                                 obj.getLexicalFeatures().getSpellCorrection(),
                                 str(obj.getSyntacticFeatures().getPOSTags()),
                                 obj.getSyntacticFeatures().getTemporalTag(),
                                 obj.getSemanticFeatures().getSynonym(),
                                 obj.getSemanticFeatures().getLocation()])
            else:
                if Utilities.isDateInFuture(obj.getSyntacticFeatures().getTemporalTag()):
                    RESULT.append([obj.getEvent().type,
                                     obj.getEvent().date,
                                     obj.getEvent().location,
                                     obj.getText(),
                                     str(obj.getLexicalFeatures().getTokens()),
                                     obj.getLexicalFeatures().getSpellCorrection(),
                                     str(obj.getSyntacticFeatures().getPOSTags()),
                                     obj.getSyntacticFeatures().getTemporalTag(),
                                     obj.getSemanticFeatures().getSynonym(),
                                     obj.getSemanticFeatures().getLocation()])
                else:
                    Utilities.writeLog("INFO: Event Detected but is identified as past event                   :" + obj.getText())
        else:
            Utilities.writeLog("INFO: Event Detected but event type did not match with required events :" + obj.getText())


    Utilities.writeOutput(outputFileName, RESULT_HEADER)
    for feature in RESULT:
        Utilities.writeOutput(outputFileName, feature)