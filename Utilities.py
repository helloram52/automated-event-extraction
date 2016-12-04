from datetime import datetime
import logging, random, copy, re
import logging.config

TIMEX_TAG = "</TIMEX2>"
TIMEX_TAG_REGEX = r'<TIMEX2 .+>.+?</TIMEX2>'

def days(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d1 - d2).days)

def split(sentence, delimiter):
    return sentence.split(delimiter)

def isEmpty(string):
    return string == '' or string == None

def setupLog():
    logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
        filename='eventDetector.log',
        filemode='w')

def parseDate(line):
    if TIMEX_TAG in line:
        r = re.compile(TIMEX_TAG_REGEX)
        dates = r.findall(line)
        return re.sub("<\/?TIMEX2([^<.]+)?>", "", dates[0])

    return ""

def filter(taggedLines, searchString):
    events = []
    for (line, taggedLine) in taggedLines:
        if searchString in taggedLine:
            events.append((line, taggedLine))

    return events

def firstMatching(pattern, string):
    expression = re.compile(pattern)
    results = expression.findall(string)
    return results[0]

def remove(pattern, string):
    return re.sub(pattern, "", string)

#check whether date is in future
def isDateInFuture(event):
    date = firstMatching(r'val=.+>', event)
    date = remove(r"(>.+\/?TIMEX2>)|(val=)|'|\"", date)
    #remove token 'val='
    #date = remove(r'val=', date)
    #remove single quote
    #date = remove(r"'|\"", date)

    #Based on length check whether it is past or future event
    if len(date) == 4:
        return int(datetime.now().year) < int(date)
    elif len(date) == 10:
        return days(date, datetime.now().strftime("%Y-%m-%d")) > 0
    elif len(date) == 7 and 'W' in date:
        return datetime.now().isocalendar()[1] <= int(date[5:])
    else:
        return False

#write log message
def writeLog(line):
    #print line
    logging.warn(line)

#write data to output
def writeOutput(outputFileName, line):
    with open(outputFileName, 'a') as outputFile:
        outputFile.write(line+"\n")
