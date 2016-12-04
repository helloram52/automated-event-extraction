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
rel_day = "(today|yesterday|tomorrow|tonight|tonite)"
exp1 = "(before|after|earlier|later|ago)"
exp2 = "(this|next|last)"
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
  inputData = Utilities.parseInputFile(inputFileName)

  # Split text into lines based on delimiter
  lines = Utilities.split(inputData, ".")

  # Get rid of empty lines.
  lines = filter(None, lines)

  print "lines: {}".format(lines)

  return lines

def extractDate(text):
    # Initialization
    timex_found = []

    # re.findall() finds all the substring matches, keep only the full
    # matching string. Captures expressions such as 'number of days' ago, etc.
    found = reg1.findall(text)
    found = [a[0] for a in found if len(a) > 1]
    for timex in found:
      timex_found.append(timex)

    # Variations of this thursday, next year, etc
    found = reg2.findall(text)
    found = [a[0] for a in found if len(a) > 1]
    for timex in found:
      timex_found.append(timex)

    # today, tomorrow, etc
    found = reg3.findall(text)
    for timex in found:
      timex_found.append(timex)

    # ISO
    found = reg4.findall(text)
    for timex in found:
      timex_found.append(timex)

    # Year
    found = reg5.findall(text)
    for timex in found:
      timex_found.append(timex)

    print "temporal expressions: {}".format(timex_found)
    if timex_found:
      return ",".join(timex_found)
    else:
      return ""

    # result = ""
    # result
    #   # Tag only temporal expressions which haven't been tagged.
    # for timex in timex_found:
    #   text = re.sub(timex + '(?!</TIMEX2>)', '<TIMEX2>' + timex + '</TIMEX2>', text)
    #
    # return

if __name__ == '__main__':
  # initialize variables
  # initialize()

  # read commmand line parameters
  inputFileName, outputFileName = getCommandLineArgs()

  # Preprocess input data
  lines = preProcessData(inputFileName)

  result = []
  for line in lines:
    isRequired, eventType = isRequiredEvent(line)
    if isRequired:
      # print "line : {}".format(line)
      eventDate = extractDate(line)
      print "eventdate: ".format(eventDate)
      result.append([eventType, eventDate, "", line])

  Utilities.writeOutput(outputFileName, tabulate(result, headers=["Event", "When", "Where", "Text"], tablefmt="grid"))

# Steps:
#   - isRequiredEvent()
#   - isDatePresent()
#     - keyword matching Mon-Sun, Jan - Dec, regex for date
#   - If the above are true:
#     -
