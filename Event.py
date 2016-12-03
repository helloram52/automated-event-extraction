
class Event(object):

    def __init__(self, type, date, location):
        self.type = type
        self.date = date
        self.location = location

    def format(self):
        formattedResult = ""
        if self.location != "":
            formattedResult = "Event : {}, when: {}, where: {}".format(self.type, self.date, self.location)
        else:
            formattedResult = "Event : {}, when: {}".format(self.type, self.date)

        return formattedResult