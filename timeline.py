import os
import datetime
import pickle as pickle
import sys
from flask import *

app = Flask(__name__)

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
        timeline = " " * indent + self.date.strftime(READABLE_DATE) + ": " + self.content + "\n"
        for child in self.children:
            timeline += child.timeline(indent=indent + 2)
        return timeline

def write_data(data):
    with open(data_filepath, 'wb') as outfile:
        pickle.dump(data, outfile)

def read_data():
    with open(data_filepath, "rb") as infile:
        return pickle.load(infile)

def root_init():
    global root
    root = read_data()

def root_save():
    write_data(root)

def get_entry(entry, datecode):
    if entry.date.strftime(DATE_FORMAT) == datecode:
        return entry
    else:
        for child in entry.children:
            result = get_entry(child, datecode)
            if result:
                return result
    print("no entry found!")
    return None

# UI
def load_ui():
    print("test")

# Globals
data_filepath = os.path.dirname(os.path.realpath(__file__)) + "\pickled_data.pkl"
root = None
DATE_FORMAT = "%d%m%Y%H%M%S"
READABLE_DATE = "%d/%m/%Y %H:%M:%S"

# redirect to root timeline
@app.route('/')
def main():
    return redirect(url_for('timeline'))

# display the root timeline
@app.route('/timeline')
def timeline():
    root_init()
    entry = root

    return render_template("timeline.html", content=entry.timeline())

# display entry detail
# <dt> is a datecode of form DATE_FORMAT
@app.route('/timeline/entry/<dt>')
def entry_detail(dt):
    root_init()
    entry = get_entry(root, dt)
    return render_template("entrydetail.html", entry=entry)

# add entry to parent specified by <datecode>
@app.route('/addentry/<datecode>', methods = ['POST', 'GET'])
def add_entry(datecode):
    root_init()
    parent = get_entry(root, datecode) # get the parent from the url parameter

    if request.method == 'POST': # on form submit
        result = request.form

        # Create the child from form elements
        child = Entry(result["datecode"], result["content"])
        parent.addChild(child)

        root_save()
        return render_template("timeline.html", content=root.timeline())
    else:
        return render_template("addentry.html", parent=datecode)

# run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)