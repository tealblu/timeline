import os
import datetime
import pickle

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
        timeline = " " * indent + self.date.strftime("%d/%m/%Y %H:%M:%S") + ": " + self.content + "\n"
        for child in self.children:
            timeline += child.createTimeline(indent=indent + 2)
        return timeline

# Globals
data_filepath = os.path.dirname(os.path.realpath(__file__)) + "\pickled_data.pkl"

def write_data(data):
    with open(data_filepath, 'wb') as outfile:
        pickle.dump(data, outfile, pickle.HIGHEST_PROTOCOL)

def read_data():
    with open(data_filepath, "rb") as infile:
        return pickle.load(infile)

def test():
    root = read_data()
    if root:
        print(root.children)

test()