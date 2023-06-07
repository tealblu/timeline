import os
import datetime
import pickle
import sys
import kivy


class Entry:
    def __init__(self):
        self.date = ""
        self.content = ""
        self.children = []

    def __init__(self, date, content):
        self.date = datetime.datetime.strptime(date, DATE_FORMAT) #ddMMyyyyhhmmss
        self.content = content
        self.children = []
        
    def addChild(self, child):
        if child.date in (d.date for d in self.children): # check if error already exists as child at same time
            print("ERROR: ENTRY ALREADY EXISTS")
            return

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

    def timeline(self, indent=0):
        timeline = " " * indent + self.date.strftime("%d/%m/%Y %H:%M:%S") + ": " + self.content + "\n"
        for child in self.children:
            timeline += child.timeline(indent=indent + 2)
        return timeline

def write_data(data):
    with open(data_filepath, 'wb') as outfile:
        pickle.dump(data, outfile, pickle.HIGHEST_PROTOCOL)

def read_data():
    with open(data_filepath, "rb") as infile:
        return pickle.load(infile)

def root_init():
    global root
    root = read_data()

def root_save():
    write_data(root)

# UI
def load_ui():
    print("test")

# Globals
data_filepath = os.path.dirname(os.path.realpath(__file__)) + "\pickled_data.pkl"
root = None
DATE_FORMAT = "%d%m%Y%H%M%S"

def main():
    root_init()
    load_ui()

main()