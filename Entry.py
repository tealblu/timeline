import datetime

DATE_FORMAT = "%d%m%Y%H%M%S"
READABLE_DATE = "%d/%m/%Y %H:%M:%S"

class Entry:
    def __init__(self):
        self.date = ""
        self.content = ""
        self.children = []

    def __init__(self, date, content):
        self.date = datetime.datetime.strptime(date, DATE_FORMAT) #ddMMyyyyhhmmss
        self.content = content
        self.children = []

    def getDatecode(self):
        return self.date.strftime(DATE_FORMAT)
    
    def getReadableDate(self):
        return self.date.strftime(READABLE_DATE)

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
    
    def getChildren(self):
        return self.children
    
    def findParent(self, target_date):
        if any(child.date.strftime(DATE_FORMAT) == target_date for child in self.children):
            return self
        else:
            for child in self.children:
                parent = child.findParent(target_date)
                if parent:
                    return parent
        print("NO PARENT")
        return None

    def timeline(self, indent=0):
        timeline = "    " * indent + self.date.strftime(READABLE_DATE) + ": " + self.content + "\n"
        for child in self.children:
            timeline += child.timeline(indent=indent + 2)
        return timeline
    
# Util for returning datecode of target entry, in parent tree {entry}
def get_entry(entry, datecode):
    if entry.date.strftime(DATE_FORMAT) == datecode:
        return entry
    else:
        for child in entry.children:
            result = get_entry(child, datecode)
            if result:
                return result
    return None