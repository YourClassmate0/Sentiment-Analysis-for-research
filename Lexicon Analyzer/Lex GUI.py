import tkinter as tk

from tkinter import TOP
from tkinter import END
from tkinter import BOTTOM

from tkinter import Label
from tkinter import Button
from tkinter import Listbox
from tkinter import Frame
from tkinter import ttk

import PositiveNegative
import senticounter


if __name__ == '__main__':
    main = tk.Tk()
    main.title("Lexicon Sentiment Analyzer")
    main.geometry("515x500")

    #for tabs
    tab = ttk.Notebook(main)
    tab.pack(pady=3, side=TOP, anchor="w")

    #containers
    frm1 = Frame(tab, width=1000, height=200)
    frm1.pack(fill="both", expand=1, pady=5)
    frm2 = Frame(tab, width=1000, height=200)
    frm2.pack(fill="both", expand=1, pady=5)
    frm3 = Frame(tab, width=1000, height=200)

    # tab name
    tab.add(frm1, text="Instructions Page")
    tab.add(frm2, text="Processing Page")
    tab.add(frm3, text="Results")

    # Instruction page content
    label01 = Label(frm1, text="Welcome to Lexicon-Based Sentiment Classifier", font=('Tahoma 16 bold'))
    label02 = Label(frm1, text="Instructions on how to use Classifier:", font=('Tahoma 14 bold'))
    label03 = Label(frm1, text="1. Make sure testing data is in same folder as code files", font=('Tahoma 13'))
    label04 = Label(frm1, text="2. Testing data MUST be cleaned of non-ASCII characters", font=('Tahoma 13'))
    label05 = Label(frm1, text="and symbols", font=('Tahoma 13'))
    label06 = Label(frm1, text="3. To use Lexicon Classifier proceed to Processing Page", font=('Tahoma 13'))
    label07 = Label(frm1, text="4. Press the <<Execute>> button to start the classifier", font=('Tahoma 13'))
    label08 = Label(frm1, text="5. Wait for the program to notify if the classification", font=('Tahoma 13'))
    label09 = Label(frm1, text="6. The program will produce an output file in the same", font=('Tahoma 13'))
    label10 = Label(frm1, text="directory", font=('Tahoma 13'))

    # processing page content
    label11 = Label(frm2, text="Data Processing", font=('Tahoma 16 bold'))
    def Proceed():
        msg_list.insert(END, "Starting Lexicon Classifier")
        PositiveNegative.run('textfile')
        msg_list.insert(END, "Classification Done")
        reviews, decisions = PositiveNegative.run('textfile')
        for i in range(len(reviews)):
            print(reviews[i], decisions[i])

    btn = Button(frm2, text="Execute", command=Proceed, font=('Tahoma 16 bold'))
    msg_list = Listbox(frm2, height=10, width=70)

    #pack
    label01.pack(pady=5, side=TOP, anchor="w")
    label02.pack(pady=5, side=TOP, anchor="w")
    label03.pack(pady=5, side=TOP, anchor="w")
    label04.pack(pady=5, side=TOP, anchor="w")
    label05.pack(pady=5, side=TOP, anchor="w")
    label06.pack(pady=5, side=TOP, anchor="w")
    label07.pack(pady=5, side=TOP, anchor="w")
    label08.pack(pady=5, side=TOP, anchor="w")
    label09.pack(pady=5, side=TOP, anchor="w")
    label10.pack(pady=5, side=TOP, anchor="w")
    label11.pack(pady=5, side=TOP, anchor="w")
    msg_list.pack(side=TOP, pady=2)
    msg_list.config(font=('Tahoma 16 bold'))
    btn.pack(pady=5, side=BOTTOM, anchor="s")

    main.mainloop()