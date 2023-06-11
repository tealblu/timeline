import os
import pickle as pickle
from Entry import Entry

data_filepath = os.path.dirname(os.path.realpath(__file__)) + r"\root.pkl"
root = Entry

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

# ON LOAD:
root_init()