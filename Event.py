
class Event(object):

    def __init__(self, type, date, location):
        self.type = type
        self.date = date
        self.location = location

    def format(self):
        formattedResult = ""
        if self.location != "":
            formattedResult = "Event Type: {}, Date/time: {}, Location: {}".format(self.type, self.date, self.location)
        else:
            formattedResult = "Event Type: {}, Date/time: {}".format(self.type, self.date)

        return formattedResult