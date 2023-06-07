
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

    def listChildren(self, indent=0):
        contentList = []
        for child in self.children:
            contentList.append(" " * indent + "- " + child.content)
            contentList.extend(child.listChildren(indent=indent + 2))
        return contentList

    def createTimeline(self, indent=0):
        timeline = " " * indent + self.content + "\n"
        for child in self.children:
            timeline += child.createTimeline(indent=indent + 2)
        return timeline


root = Entry("17092000080100", "I was born today!")  # Root entry is my birth, representing my whole lifetime
child1 = Entry("01012010120000", "Started school")
child2 = Entry("01072015210000", "Graduated high school")
child3 = Entry("01092020230000", "Started college")
child4 = Entry("01052023220000", "Graduated college")
child5 = Entry("01072023230000", "Started working")

root.addChild(child1)
child1.addChild(child2)
root.addChild(child3)
child3.addChild(child4)
root.addChild(child5)

timeline = root.createTimeline()
print(timeline)