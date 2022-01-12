import tkinter as tk

from tkinter import TOP
from tkinter import END
from tkinter import BOTTOM
from tkinter import Label
from tkinter import Button
from tkinter import Listbox
from tkinter import Frame
from tkinter import ttk

import MNB_with_word_frequency
import main_word_frequency


if __name__ == '__main__':
    win = tk.Tk()
    win.title('MNB')
    win.geometry('450x500')


    # create tabs
    tab = ttk.Notebook(win)
    tab.pack(pady=3, side=TOP, anchor="w")

    # containers
    frm1 = Frame(tab, width=1000, height=200)
    frm1.pack(fill="both", expand=1, pady=5)
    frm2 = Frame(tab, width=1000, height=200)
    frm2.pack(fill="both", expand=1, pady=5)
    frm3 = Frame(tab,width=1000, height=200)


    # tabs and names
    tab.add(frm1, text="Instructions Page")
    tab.add(frm2, text="Processing Page")
    tab.add(frm3, text="Results")

    # for frm1 = Main Menu
    label01 = Label(frm1, text="Welcome to MNB Sentiment Classifier", font=('Tahoma 16 bold'))
    label02 = Label(frm1, text="Instructions on how to use Classifier:", font=('Tahoma 14 bold'))
    label03 = Label(frm1, text="1. Make sure training and testing set are", font=('Tahoma 13'))
    label04 = Label(frm1, text="in same directory as code files.", font=('Tahoma 13'))
    label05 = Label(frm1, text="2. Program only accepts .csv files and ascii only values,", font=('Tahoma 13'))
    label06 = Label(frm1, text="if a non-ascii value is read by the program an error will", font=('Tahoma 13'))
    label07 = Label(frm1, text="be shown and the program will terminate", font=('Tahoma 13'))
    label08 = Label(frm1, text="3. Click the Execute button on the Processing page", font=('Tahoma 13'))
    label09 = Label(frm1, text="4. Wait for the program to say that it is finish processing", font=('Tahoma 13'))
    label10 = Label(frm1, text="5. Click on the results tab to view overall results.", font=('Tahoma 13'))
    label11 = Label(frm1, text="6. An output named Results.csv will be provided", font=('Tahoma 13'))
    label12 = Label(frm1, text="in the same directory", font=('Tahoma 13'))

    # for frm2 = Processing Page
    def Proceed():
        msg_list.insert(END, "Starting MNB Classifier....")
        msg_list.insert(END, "Reading training data....")
        msg_list.insert(END, "Creating Word Dictionary....")
        msg_list.insert(END, "Reading testing data....")
        MNB_with_word_frequency.main()
        msg_list.insert(END, "Classifying test data....")
        msg_list.insert(END, "Creating output file....")
        msg_list.insert(END, "Results.csv Created")
        msg_list.insert(END, "Classifying Complete")
        msg_list.insert(END, "Please go to Results Page")

    ppg = Label(frm2, text="Data Processing", font=('Tahoma 16 bold'))
    btn = Button(frm2, text="Execute", command= Proceed, font=('Tahoma 16 bold'))
    msg_list = Listbox(frm2, height=10, width=70)

    # for frm3 = Results
    lbl1 = Label(frm3, text="Results", font=('Tahoma 16 bold'))
    rst = Listbox(frm3, height=15, width=70)

    # pack frm1
    label01.pack(pady=5, side= TOP, anchor="w")
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
    label12.pack(pady=5, side=TOP, anchor="w")
    #pack frm2
    ppg.pack(pady=5, side=TOP, anchor="w")
    msg_list.pack(side=TOP, pady=2)
    msg_list.config(font=('Tahoma 16 bold'))
    btn.pack(pady=5, side=BOTTOM, anchor="s")
    #pack frm3
    lbl1.pack(pady=5, side=TOP, anchor="w")
    rst.pack(side=TOP, pady=2)
    rst.config(font=('Tahoma 16 bold'))

    #value for processing

    #value for results
    rst.insert(END, "Total number of Data:", len(main_word_frequency.results))
    rst.insert(END, "Classification Results:")
    for item in main_word_frequency.cnt:
        rst.insert(END,item)
    rst.insert(END, "For classifier ACCURACY")
    rst.insert(END, "User's own classification:")

    win.mainloop()