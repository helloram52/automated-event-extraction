import Utilities

day = "(monday|tuesday|wednesday|thursday|friday|saturday|sunday)"
week_day = "(monday|tuesday|wednesday|thursday|friday|saturday|sunday)"
month = "(january|february|march|april|may|june|july|august|september| \
          october|november|december)"

def getCommandLineArgs():
  return sys.argv[1], sys.argv[2]

def isRequiredEvent(line, dict):
  for word in ['marriage', 'birthday', 'meeting', 'anniversary', 'seminar']:
    if word in line.lower():
      return True, word

  return False, ""

def preProcessData(input):
  # Read input file
  inputData = parseInputFile(inputFileName)

  # Split text into lines based on delimiter
  lines = Utilities.split(inputData, ".")

  return lines

def isDatePresent():
  if


if __name__ == '__main__':
  # initialize variables
  # initialize()

  # read commmand line parameters
  inputFileName, outputFileName = getCommandLineArgs()

  # Preprocess input data
  lines = preProcessData(inputFileName)

  for line in lines:
    (isEventRequired, ) = isRequiredEvent(line):
    if isDatePresent()

# Steps:
#   - isRequiredEvent()
#   - isDatePresent()
#     - keyword matching Mon-Sun, Jan - Dec, regex for date
#   - If the above are true:
#     -
