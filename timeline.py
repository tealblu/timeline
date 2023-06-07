from nicegui import ui
import datetime

class Entry:
    def __init__(self):
        self.date = ""
        self.content = ""
        self.children = []

    def __init__(self, date, content):
        self.date = datetime.datetime.strptime(date, "%d%m%Y%H%M%S") #ddMMyyyyhhmmss
        self.content = content
        self.children = []
        
    def addChild(self, child):
        self.children.append(child)
        self.children.sort(key=lambda e: e.date)

    def removeChild(self, date):
        # find the child, remove it
        for child in self.children:
            if child.date == date:
                self.children.remove(child)

    def listChildren(self):
        contentList = []
        for child in self.children:
            contentList.append(child.content)

        return contentList


root = Entry("17092000080100", "I was born today!") # Root entry is my birth, representing my whole lifetime