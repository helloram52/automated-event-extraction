import Utilities
import re, sys
from tabulate import tabulate


# Predefined strings.
numbers = "(^a(?=\s)|one|two|three|four|five|six|seven|eight|nine|ten| \
          eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen| \
          eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty| \
          ninety|hundred|thousand)"
day = "(monday|tuesday|wednesday|thursday|friday|saturday|sunday)"
week_day = "(monday|tuesday|wednesday|thursday|friday|saturday|sunday)"
month = "(january|february|march|april|may|june|july|august|september| \
          october|november|december)"
dmy = "(year|day|week|month)"
rel_day = "(today|tomorrow|tonight|tonite)"
exp1 = "(after)"
exp2 = "(this)"
iso = "\d+[/-]\d+[/-]\d+ \d+:\d+:\d+\.\d+"
year = "((?<=\s)\d{4}|^\d{4})"
regxp1 = "((\d+|(" + numbers + "[-\s]?)+) " + dmy + "s? " + exp1 + ")"
regxp2 = "(" + exp2 + " (" + dmy + "|" + week_day + "|" + month + "))"

reg1 = re.compile(regxp1, re.IGNORECASE)
reg2 = re.compile(regxp2, re.IGNORECASE)
reg3 = re.compile(rel_day, re.IGNORECASE)
reg4 = re.compile(iso)
reg5 = re.compile(year)

def getCommandLineArgs():
  return sys.argv[1], sys.argv[2]

def isRequiredEvent(line):
  for word in ['marriage', 'birthday', 'meeting', 'anniversary', 'seminar']:
    if word in line.lower():
      return True, word

  return False, ""

def preProcessData(input):

  # Read input file
  objects = Utilities.parseInputFile(inputFileName)

  # Split text into lines based on delimiter
  #lines = Utilities.split(inputData, ".")

  # Get rid of empty lines.
  #lines = filter(None, lines)

  #print "lines: {}".format(lines)

  return objects

def extractDate(text):
  # Initialization
  temporalExpressionFound = []

  # re.findall() finds all the substring matches, keep only the full
  # matching string. Captures expressions such as 'number of days' ago, etc.
  found = reg1.findall(text)
  found = [a[0] for a in found if len(a) > 1]
  for timex in found:
    temporalExpressionFound.append(timex)

  # Variations of this thursday, next year, etc
  found = reg2.findall(text)
  found = [a[0] for a in found if len(a) > 1]
  for timex in found:
    temporalExpressionFound.append(timex)

  # today, tomorrow, etc
  found = reg3.findall(text)
  for timex in found:
    temporalExpressionFound.append(timex)

  # ISO
  found = reg4.findall(text)
  for timex in found:
    temporalExpressionFound.append(timex)

  # Year
  found = reg5.findall(text)
  for timex in found:
    temporalExpressionFound.append(timex)

  # print "temporal expressions: {}".format(temporalExpressionFound)
  if temporalExpressionFound:
    return ",".join(temporalExpressionFound)
  else:
    return ""



def initialize():
  Utilities.setupLog()

if __name__ == '__main__':
  initialize()

  # read commmand line parameters
  inputFileName, outputFileName = getCommandLineArgs()

  # Preprocess input data
  lines = preProcessData(inputFileName)

  result = []
  for line in lines:
    isRequired, eventType = isRequiredEvent(line.getText())
    if isRequired:
      # print "line : {}".format(line)
      eventDate = extractDate(line.getText())
      if eventDate:
        # print "eventdate: ".format(eventDate)
        if line.getActual() == "yes":
            Utilities.incrementTP()

        line.setPredict("yes")
        result.append([eventType, eventDate, "", line.getText()])
      else:
        Utilities.writeLog("INFO [NAIVE APPROACH]: Event Detected but is identified as past event                   :" + line.getText())
    else:
      Utilities.writeLog("INFO [NAIVE APPROACH]: Event Detected but event type did not match with required events :" + line.getText())

  Utilities.writeOutput(outputFileName, ["Event", "When", "Where", "Text"])
  [ Utilities.writeOutput(outputFileName, x) for x in result ]
  # Utilities.writeOutput(outputFileName, tabulate(result, headers=["Event", "When", "Where", "Text"], tablefmt="grid"))

  Utilities.computeRecall(lines)
  Utilities.printMetrics()