# ----- IMPORTS -----
from flask import *; app = Flask(__name__)

# ----- CUSTOM LIBRARIES -----
from Entry import * # Defines Entry class and related functions
from root_util import * # Provides persistence utility via pkl, accessed through root variable

# ----- GLOBALS -----
DATE_FORMAT = r"%d%m%Y%H%M%S" # datecode format
READABLE_DATE = r"%d/%m/%Y %H:%M:%S" # format for printing

# ----- VIEWS -----

# redirect to root timeline
@app.route('/')
def main():
    return redirect(url_for('timeline'))

# display the root timeline
@app.route('/timeline')
def timeline():
    root_init()
    entry = root

    return render_template("timeline.html", entry=entry, children=entry.getChildren())

# display entry detail
# <dt> is a datecode of form DATE_FORMAT
@app.route('/timeline/entry/<dt>')
def entry_detail(dt):
    root_init()

    entry = get_entry(root, dt)
    if entry == root: return redirect(url_for("timeline"))
    else: return render_template("entrydetail.html", entry=entry, children=entry.getChildren(), parent=root.findParent(entry.date.strftime(DATE_FORMAT)))

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