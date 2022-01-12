import tkinter as tk

from tkinter import TOP
from tkinter import END
from tkinter import BOTTOM

from tkinter import Label
from tkinter import Button
from tkinter import Listbox
from tkinter import Frame
from tkinter import ttk

#function that loads a lexicon of positive words to a set and returns the set
def loadLexicon(fname):
    newLex=set() # about set->no duplicates & fast search
    lex_conn=open(fname)
    #add every word in the file to the set
    for line in lex_conn:
        newLex.add(line.strip())# remember to strip to remove the lin-change character
    lex_conn.close()

    return newLex

def run(path):
    posLex=loadLexicon('positive-words.txt')
    posfreqReview={} #Initialize a new dictionary
    fin=open(path)
    for line in fin: # for every line in the file (1 review per line)
        posList= set()
        words=line.lower().strip().split(' ') # split on the space to get words

        for word in words: #for every word in words
            if word in posLex: # if the word is in the positive lexicon
                posList.add(word) # then add the word in the posList set

        for word in posList: # for every word in the set
            if word in posfreqReview: # if the word is in dictionary
                posfreqReview[word] = posfreqReview[word]+1 # increase the count of the similar word
            else:
                posfreqReview[word]=1 # Set to 1 if it is 1st time.
    fin.close()
    return posfreqReview


# list goes from 0-6 if 7 line
if __name__ == "__main__":

    posfreq = run('textfile')
    print(posfreq)