from tkinter import Entry
from tkinter import Tk
from tkinter import Button
from tkinter import END
from tkinter import Label
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
import tkinter.font as font
import tkinter
import pandas
import datetime
import backendUI as backend
import os
import re
from PIL import Image, ImageTk



def input_dive_details():                                                       #define window for inputting dive details
    global root                                                                 #make root global variable so can be accessed by different functions
    root = Tk()                                                                 #make the window
    root.geometry('1000x700')                                                    #size of window
    root.resizable(width=False, height=False)
    root.title('Dive details')
    root.attributes("-fullscreen", True)     #name window title
    root.configure(background = 'black')
    combostyle = ttk.Style()

    combostyle.theme_create('combostyle', parent='alt',
                             settings = {'TCombobox':
                                         {'configure':
                                          {'selectbackground': 'black',
                                           'fieldbackground': 'black',
                                           'background': 'green'
                                           }}}
                             )
    combostyle.theme_use('combostyle')

    rows = 0                                                                    #configure the window into a grid of 10x10
    while rows < 10:
        root.rowconfigure(rows,weight=1)
        root.columnconfigure(rows,weight=1)
        rows += 1

    global helv
    helv = font.Font(family="Helvetica", size=30, weight='bold')

    date_label = input_label('Date:',1)                                         #show the date label,column 1
    date_entry = input_entry(1)                                                 #create entry box for the day
    date_time = datetime.datetime.now().date()                                  #obtain computertime
    date_entry.insert(1,date_time)                                              #pre fill the entrybox with computer date

    gas_label = input_label('Gas used:',2)                                      #show the gas label, column 2
    gas_list = [ "O2","Air",'Heliox','Nitrox']                                  #list of gases used
    gas_entry = input_combo(gas_list,2)                                         #create combobox for gas using gas list

    equip_label = input_label('Equipment used:',3)                              #show the eqipment label,column  3
    equip_list = ['Scuba','Divator','FROGS','AMPHORA']                          #list of equipment
    equip_entry = input_combo(equip_list,3)                                     #create combobox for enquipment using equipment list

    loc_label = input_label('Location:',4)                                      #show the label for location, column 4
    loc_list = ['NDU Dive Pool','NDU training area','Changi Naval Base','Tuas Naval Base']      #list of locations
    loc_entry = input_combo(loc_list,4)                                         #create combobox for location using equipment list

    task_label = input_label('Task:',5)                                         #show the label for task, column 5
    task_list = ['Circular search','Enhanced Beach Clearance','Compass Attack'] #list of tasks
    task_entry = input_combo(task_list,5)                                       #create combobox for task using task list

    submit_dive_details = Button(root)                                          #define button for submittion of dive details
    submit_dive_details.configure(text='Next: Diver details', fg = 'dark green',background = 'black',command = lambda:get_data(date_entry,gas_entry,equip_entry,loc_entry,task_entry))  #show text, run command get_data, pass the entry box
    submit_dive_details['font'] = helv
    submit_dive_details.grid(row=9,column=7)                                    #place the button within the grid

    jump_to_logging = Button(root)
    jump_to_logging.configure(text = 'Skip to logging',fg = 'dark green',background = 'black' ,command = log_entry_skipped)
    jump_to_logging['font']= helv
    jump_to_logging.grid(row = 9,column = 2)

    close_root = Button(root)
    close_root.configure(text = 'Close window', command = closeroot,fg = 'red',background = 'black' )
    close_root['font'] = helv
    close_root.grid(row = 0, column = 7)

    root.mainloop()                                                             #keeps root open

def closeroot():
    root.destroy()

def log_entry_skipped():
    root.destroy()
    log_entry()


def input_label(text,x_coor):                                                   #function for displaying labels in root
    label = Label(root,text = text,background = 'black',foreground = 'white', borderwidth = 0)                                             #create the label using the argument passed in (text)
    label['font'] = helv
    label.grid(row = x_coor,column = 4,sticky = E)                              #Place the label within the grid in root using argument passed in (x_coor)
    return label                                                                #return label to create label

def input_entry(x_coor):                                                        #function for creating entry box in root
    entry = Entry(root,width = 17,background = 'black',foreground = 'white')                                              #create the entry box within root
    entry['font'] = helv
    entry.grid(row = x_coor,column = 5)                                         #place the box within root using x_coor
    return entry                                                                #return entry to create entry box

def input_combo(list,x_coor):                                                   #function for creating combobox in root
    combo = ttk.Combobox(root,values = list, width = 15,background = 'black' , foreground = 'white')                       #create the combobox using argument list
    combo['font'] = helv
    combo.grid(row = x_coor,column = 5)                                         #place combobox within root using x_coor
    return combo                                                                #return combo to create the combobox

def get_data(date_entry,gas_entry,equip_entry,loc_entry,task_entry):            #function run when button to submit dive details is pushed

    data_date = date_entry.get()                                                #obtain date data
    data_gas = gas_entry.get()                                                  #obtain gas data\
    data_equip = equip_entry.get()                                              #obtain equipment data
    data_loc = loc_entry.get()                                                  #obtain location data
    data_task = task_entry.get()                                                #obtain task data

    print('Date:',str(data_date))
    print('Gas used:',str(data_gas))
    print('Equipment used:',str(data_equip))
    print('Location:',str(data_loc))
    print('Task:',str(data_task))

    root.destroy()                                                              #close root
    diver_details()

name_df = pandas.read_csv("NATO.csv")                                           #obtain namelist from excel
name_list = list(name_df['Name'])

def diver_details():                                                            #function to input diver details
    global window                                                               #delcare window as global to be used later
    window = Tk()                                                               #create window window
    window.geometry('800x700')                                                  #define window size
    window.resizable(width=False, height=False)
    window.title('Diver details')
    window.attributes("-fullscreen", True)                                          #define title of window
    window.configure(background = 'black')

    global helv2
    helv2 = font.Font(family="Helvetica", size=20, weight='bold')

    combostyle = ttk.Style()

    combostyle.theme_create('combostyle', parent='alt',
                             settings = {'TCombobox':
                                         {'configure':
                                          {'selectbackground': 'black',
                                           'fieldbackground': 'black',
                                           'background': 'green'
                                           }}}
                             )
    combostyle.theme_use('combostyle')

    rows = 0                                                                    #create 10x10 grid within window
    while rows < 13:
        window.rowconfigure(rows,weight=1)
        window.columnconfigure(rows,weight=1)
        rows += 1

    for i in range(1,9):
        add_dive_logger(i)                                                      #function to setup dive logger
        add_diver(i)                                                            #function to setup name input

    sup_label = Label(window,text = 'Supervisor:',background= 'black',foreground = 'white')                 #setup sup input
    sup_label['font'] = helv2
    sup_label.grid(row = 1,column = 0)

    sup_entry = ttk.Combobox(window,values = name_list,width = 15,background = 'black',foreground = 'white',postcommand = lambda:search(sup_entry))
    sup_entry['font'] = helv2
    sup_entry.grid(row = 2,column = 0)

    submit_sup = Button(window)
    submit_sup.configure(text = 'Confirm Supervisor',command = lambda:confirm_sup(submit_sup,sup_entry),background = 'black', fg = 'white')
    submit_sup['font'] = helv2
    submit_sup.grid(row = 3,column = 0)


    stdby_d_label = Label(window,text = 'Standby Diver:',background = 'black',foreground = 'white')         #setup standby diver input
    stdby_d_label['font'] = helv2
    stdby_d_label.grid(row = 4,column = 0)

    stdby_d_entry = ttk.Combobox(window,values = name_list,width = 15,background = 'black',foreground = 'white',postcommand = lambda:search(stdby_d_entry))
    stdby_d_entry['font'] = helv2
    stdby_d_entry.grid(row = 5,column = 0)

    stdby_d_submit = Button(window)
    stdby_d_submit.configure(text = 'Confirm Standby Diver',command = lambda:confirm_stdby_d(stdby_d_submit,stdby_d_entry),background = 'black', fg = 'white')
    stdby_d_submit['font'] = helv2
    stdby_d_submit.grid(row = 6,column = 0)


    stdby_a_label = Label(window,text = 'Standby Diver Attendant:',background = 'black',foreground = 'white')       #setup standby diver attendant input
    stdby_a_label['font'] = helv2
    stdby_a_label.grid(row = 7,column = 0)

    stdby_a_entry = ttk.Combobox(window,values = name_list,width = 15,background = 'black',foreground = 'white',postcommand = lambda:search(stdby_a_entry))
    stdby_a_entry['font'] = helv2
    stdby_a_entry.grid(row = 8,column = 0)

    stdby_a_submit = Button(window)
    stdby_a_submit.configure(text = 'Confirm Standby Diver Attendant',command = lambda:confirm_stdby_a(stdby_a_submit,stdby_a_entry),background = 'black', fg = 'white')
    stdby_a_submit['font'] = helv2
    stdby_a_submit.grid(row = 9,column = 0)


    rec_label = Label(window,text = 'Recorder:',background = 'black',foreground = 'white')                      #setup recoder input
    rec_label['font'] = helv2
    rec_label.grid(row = 10,column = 0)

    rec_entry = ttk.Combobox(window,values = name_list,width = 15,background = 'black',foreground = 'white',postcommand = lambda:search(rec_entry))
    rec_entry['font'] = helv2
    rec_entry.grid(row = 11,column = 0)

    rec_submit = Button(window)
    rec_submit.configure(text = 'Confirm Recorder',command = lambda:confirm_rec(rec_submit,rec_entry),background = 'black', fg = 'white')
    rec_submit['font'] = helv2
    rec_submit.grid(row = 12,column = 0)


    end_all_button = Button(window)
    end_all_button.configure(text = 'End of all dives',foreground = 'dark green',background = 'black',command = end_all_dive)
    end_all_button['font']=helv2
    end_all_button.grid(row = 12,column = 8)

    close_window = Button(window)
    close_window.configure(text = 'Close window',command = closewindow,background = 'black' ,fg = 'red')
    close_window['font'] = helv2
    close_window.grid(row = 0, column = 8)

    window.mainloop()

def closewindow():
    window.destroy()


appointment_holder = {                                                          #establish appointment holder dictionary to hold appointment holders
'sup':None,
'stdby_d':None,
'stdby_a':None,
'rec':None
}
diver_list = []

def check_diver(name,diver_list = diver_list):
    diver_names = []                                                    #initliase list diver_names to hold all the diver names in diver_list_dict
    for i in range(len(diver_list)):
        diver_names.append(diver_list[i].get('name'))                   #add all the diver names into the list diver_names
    if name in diver_names:                                       #check if the name is already input
        messagebox.showerror('Error','Already a Diver')
        return 1
    else:
        return 0

def check_appt_holder(name,appt_holder = appointment_holder):
    i = 0                                                                       #check if names are already used as appointment holder
    appt_names = []
    for i in appt_holder:
        appt_names.append(appt_holder[i])
    if name in appt_names:
        messagebox.showerror('Error','Already an appointment holder')
        return 1
    else:
        return 0

status = 0
def check_status(status = status):
    if status == 0:
        return 0
    else:
        messagebox.showerror('Error','Dives are still ongoing')
        return 1

sup_name = []
def confirm_sup(submit,entry,sup_name = sup_name, appointment_holder = appointment_holder):
    sup_name.append(entry.get())
    if check_diver(sup_name[0]) == 0:
        if check_appt_holder(sup_name[0]) == 0:
            submit.destroy()
            entry.destroy()
            appointment_holder['sup'] = sup_name[0]

            sup_name_label = Label(window,text = sup_name[0],background = 'black',foreground = 'white')
            sup_name_label['font'] = helv2
            sup_name_label.grid(row = 2,column = 0)

            sup_change = Button(window)
            sup_change.configure(text = 'Change Supervisor',command = lambda:change_sup(sup_name_label,sup_change),background = 'black',fg = 'white')
            sup_change['font'] = helv2
            sup_change.grid(row = 3, column = 0)
    else:
        sup_name.remove(sup_name[0])

def change_sup(name_label,change,sup_name = sup_name,appointment_holder = appointment_holder):
    if check_status() == 0:
        sup_name.remove(sup_name[0])
        appointment_holder['sup'] = None
        name_label.destroy()
        change.destroy()

        sup_entry = ttk.Combobox(window,values = name_list,width = 15,background = 'black',foreground = 'white',postcommand = lambda:search(sup_entry))
        sup_entry['font'] = helv2
        sup_entry.grid(row = 2,column = 0)

        submit_sup = Button(window)
        submit_sup.configure(text = 'Confirm Supervisor',command = lambda:confirm_sup(submit_sup,sup_entry),background = 'black', fg = 'white')
        submit_sup['font'] = helv2
        submit_sup.grid(row = 3,column = 0)

stdby_d_name = []
def confirm_stdby_d(submit,entry,stdby_d_name = stdby_d_name,appointment_holder = appointment_holder):
    stdby_d_name.append(entry.get())
    if check_diver(stdby_d_name[0]) == 0:
        if check_appt_holder(stdby_d_name[0]) == 0:
            submit.destroy()
            entry.destroy()
            appointment_holder['stdby_d'] = stdby_d_name[0]

            stdby_d_name_label = Label(window,text = stdby_d_name[0],background = 'black',foreground = 'white')
            stdby_d_name_label['font'] = helv2
            stdby_d_name_label.grid(row = 5,column = 0)

            stdby_d_change = Button(window)
            stdby_d_change.configure(text = 'Change Standby Diver',command = lambda:change_stdby_d(stdby_d_name_label,stdby_d_change),background = 'black',fg = 'white')
            stdby_d_change['font'] = helv2
            stdby_d_change.grid(row = 6, column = 0)
        else:
            stdby_d_name.remove(stdby_d_name[0])

def change_stdby_d(name_label,change,stdby_d_name = stdby_d_name,appointment_holder = appointment_holder):
    if check_status() == 0:
        stdby_d_name.remove(stdby_d_name[0])
        appointment_holder['stdby_d'] = None
        name_label.destroy()
        change.destroy()

        stdby_d_entry = ttk.Combobox(window,values = name_list,width = 15,background = 'black',foreground = 'white',postcommand = lambda:search(stdby_d_entry))
        stdby_d_entry['font'] = helv2
        stdby_d_entry.grid(row = 5,column = 0)

        stdby_d_submit = Button(window)
        stdby_d_submit.configure(text = 'Confirm Standby Diver',command = lambda:confirm_stdby_d(stdby_d_submit,stdby_d_entry),background = 'black', fg = 'white')
        stdby_d_submit['font'] = helv2
        stdby_d_submit.grid(row = 6,column = 0)

stdby_a_name = []
def confirm_stdby_a(submit,entry,stdby_a_name = stdby_a_name,appointment_holder = appointment_holder):
    stdby_a_name.append(entry.get())
    if check_diver(stdby_a_name) == 0:
        if check_appt_holder(stdyby_a_name) == 0:
            submit.destroy()
            entry.destroy()
            appointment_holder['stdby_a'] = stdby_a_name[0]

            stdby_a_name_label = Label(window,text = stdby_a_name[0],background = 'black',foreground = 'white')
            stdby_a_name_label['font'] = helv2
            stdby_a_name_label.grid(row = 8,column = 0)

            stdby_a_change = Button(window)
            stdby_a_change.configure(text = 'Change Standby Diver Attendant',command = lambda:change_stdby_a(stdby_a_name_label,stdby_a_change),background = 'black',fg = 'white')
            stdby_a_change['font'] = helv2
            stdby_a_change.grid(row = 7, column = 0)
    else:
        stdby_a_name.remove(stdby_a_name[0])

def change_stdby_a(name_label,change,stdby_a_name = stdby_a_name,appointment_holder = appointment_holder):
    if check_status() == 0:
        stdby_a_name.remove(stdby_a_name[0])
        appointment_holder['stdby_a'] = None
        name_label.destroy()
        change.destroy()

        stdby_a_entry = ttk.Combobox(window,values = name_list,width = 15,background = 'black',foreground = 'white',postcommand = lambda:search(stdby_a_entry))
        stdby_a_entry['font'] = helv2
        stdby_a_entry.grid(row = 8,column = 0)

        stdby_a_submit = Button(window)
        stdby_a_submit.configure(text = 'Confirm Standby Diver Attendant',command = lambda:confirm_stdby_a(stdby_a_submit,stdby_a_entry),background = 'black', fg = 'white')
        stdby_a_submit['font'] = helv2
        stdby_a_submit.grid(row = 9,column = 0)

rec_name = []
def confirm_rec(submit,entry,rec_name = rec_name,appointment_holder = appointment_holder):
    rec_name.append(entry.get())
    if check_diver(rec_name[0]) == 0:
        if check_appt_holder(rec_name[0]) == 0:
            submit.destroy()
            entry.destroy()
            appointment_holder['rec'] = rec_name[0]

            rec_name_label = Label(window,text = rec_name[0],background = 'black',foreground = 'white')
            rec_name_label['font'] = helv2
            rec_name_label.grid(row = 11,column = 0)

            rec_change = Button(window)
            rec_change.configure(text = 'Change Recorder',command = lambda:change_rec(rec_name_label,rec_change),background = 'black',fg = 'white')
            rec_change['font'] = helv2
            rec_change.grid(row = 12, column = 0)
        else:
            rec_name.remove(rec_name[0])

def change_rec(name_label,change,rec_name = rec_name,appointment_holder = appointment_holder):
    if check_status() == 0:
        rec_name.remove(rec_name[0])
        appointment_holder['rec_name'] = None
        name_label.destroy()
        change.destroy()

        rec_entry = ttk.Combobox(window,values = name_list,width = 15,background = 'black',foreground = 'white',postcommand = lambda:search(rec_entry))
        rec_entry['font'] = helv2
        rec_entry.grid(row = 11,column = 0)

        rec_submit = Button(window)
        rec_submit.configure(text = 'Confirm Recorder',command = lambda:confirm_rec(rec_submit,rec_entry),background = 'black', fg = 'white')
        rec_submit['font'] = helv2
        rec_submit.grid(row = 12,column = 0)

dive_logger_list = []                                                          #list that hold current dive logger list

def add_dive_logger(x_coor, sup_name = sup_name):                                                    #create button to add dive logger
    setup_logger_button = Button(window)
    setup_logger_button.configure(text = 'Add dive logger',background = 'black' ,fg = 'white',command = lambda:confirm_setup(setup_logger_button,x_coor, sup_name))
    setup_logger_button['font'] = helv2
    setup_logger_button.grid(row = x_coor,column = 4, sticky=W)

def confirm_setup(setup_logger_button,x_coor,sup_name):
    if sup_name == []:                              #function run when pair diver button is pressed, takes diver number(x_coor) and the button that pairs dive logger(button_pair) as arguments
        messagebox.showerror('Error','Input Supervisor name')
    else:
        window.withdraw()

        confirm_pair = Tk()                                                         #create confirm_pair
        confirm_pair.title('Confirm')                                                      #define confirm pair title
        confirm_pair.geometry('300x300')                                            #define size of confirm pair
        confirm_pair.resizable(width=False, height=False)
        confirm_pair.attributes("-fullscreen",True)
        confirm_pair.configure(background = 'black')

        global helv
        helv = font.Font(family="Helvetica", size=30, weight='bold')

        rows = 0                                                                    #define grid within confirm pair as a 4x3
        while rows < 4:
            confirm_pair.rowconfigure(rows,weight=1)
            rows += 1
        column = 0
        while column < 3:
            confirm_pair.columnconfigure(column,weight=1)
            column += 1

        label = Label(confirm_pair)
        label.configure(text = 'Place dive logger',background = 'black',fg = 'white')
        label['font'] = helv
        label.grid(row = 1,column = 1)     #create label asking user to place diver logger

        pair_label = Button(confirm_pair,text = 'Pair',background = 'black',fg = 'white',command = lambda: get_serial(setup_logger_button,confirm_pair,x_coor))
        pair_label['font'] = helv
        pair_label.grid(row = 3,column = 2)     #button to run function pair_logger to pair dive logger

        cancel = Button(confirm_pair,text = 'Cancel',background = 'black',fg = 'white',command = lambda:cancel_setup(confirm_pair))
        cancel['font'] = helv
        cancel.grid(row = 3,column = 0)       #button to cancel pairing, runs cancel_pairing function



def cancel_setup(confirm_pair):                                                             #run when user presses cancel within confirm_pair
    confirm_pair.destroy()
    window.update()
    window.deiconify()

def get_serial(setup_logger_button,confirm_pair,x_coor,sup_name = sup_name):
    #get serial number of dive logger here
    serial = backend.get_device_id()
    regex = re.compile(r'\d\w\d{7}\w')
    if regex.match(serial) is not None and serial not in dive_logger_list:
        setup_logger_button.destroy()                                               #destroy irrelevant windows and button
        confirm_pair.destroy()

        window.update()
        window.deiconify()
        logger_no_label = Label(window,text = 'Serial:',background = 'black',fg = 'white')                            #display the serial number of the dive logger
        logger_no_label['font']= helv2
        logger_no_label.grid(row = x_coor, column = 3,sticky=E)

        serial_logger_label = Label(window,text = serial,background = 'black',fg = 'white')
        serial_logger_label['font'] = helv2
        serial_logger_label.grid(row = x_coor,column = 4,sticky=W)

        diver_dict = {}                                                             #initialise dictionary diver_dict
        diver_dict['number'] = x_coor                                               #define key -> number as x_coor
        diver_dict['serial'] = serial                                               #define variable - > serial as serial number of dive logger
        diver_dict['sup'] = sup_name[0]
        diver_list.append(diver_dict)                                               #add dictionary to diver_list
        dive_logger_list.append(serial)
    elif serial in dive_logger_list:
        cancel_setup(confirm_pair)
        messagebox.showerror('Error','Dive Logger already added!')
    else:
        cancel_setup(confirm_pair)
        messagebox.showerror('Error','Dive Logger not detected!')

def search(cb3,nl = name_list):                                                 #function to do search function for entrybox
	rl = list()
	typed = cb3.get()
	for i in nl:
		if typed.lower() in i.lower():
			rl.append(i)

	if typed:
		cb3.config(value = rl)

	elif not typed:
		cb3.config(value = nl)

def add_diver(x_coor,nl = name_list):                                           #function for diver name input
    diver_label = Label(window,text = 'Diver name:',background = 'black',foreground = 'white')
    diver_label['font'] = helv2
    diver_label.grid(row = x_coor,column = 6,sticky = E)

    diver_name_entrybox = ttk.Combobox(window,background = 'black',foreground = 'white')
    diver_name_entrybox.configure(values = name_list,width = 15,postcommand = lambda:search(diver_name_entrybox))
    diver_name_entrybox['font'] = helv2
    diver_name_entrybox.grid(row = x_coor, column = 7,sticky = W)

    diver_name_enter_button = Button(window)
    diver_name_enter_button['font'] = helv2
    diver_name_enter_button.configure(text = 'Submit',background = 'black',fg = 'white' ,command = lambda:start_dive(diver_name_enter_button,diver_label,diver_name_entrybox,x_coor))
    diver_name_enter_button.grid(row = x_coor,column = 8)

def start_dive(diver_name_enter_button,diver_label,diver_name_entrybox,x_coor,diver_list=diver_list,appointment_holder = appointment_holder,check_dive_status = status):
    diver_name = diver_name_entrybox.get()                                      #obtain input from entrybox

    a = 0
    if diver_name == '':                                                        #check if field is empty
        messagebox.showerror('Error','Empty input field')
        a = 1
    else:
        i = 0
        number_no = []                                                          #initliase list number_no to hold all the diver numbers in diver_list_dict
        for i in range(len(diver_list)):
            number_no.append(diver_list[i].get('number'))                       #add all the diver_nos into the list number_no
        if x_coor not in number_no:                                             #check if dive logger has been setup
            messagebox.showerror('Error','No dive logger setup')
            a = 1
        else:
            if check_diver(diver_name) != 0:
                a = 1
            if check_appt_holder(diver_name) != 0:
                a = 1
            i = 0
            appt_names = []
            for i in appointment_holder:
                appt_names.append(appointment_holder[i])
            if None in appt_names:
                messagebox.showerror('Error','Input appointment holders')
                a = 1

    if a == 0:                                                                  #if no errors
        diver_name_entrybox.destroy()                                           #destroy entryboxes and submit button
        diver_name_enter_button.destroy()

        time_start = datetime.datetime.now()                                    #record datetime
        status += 1

        i = 0
        for i in range(len(diver_list)):
            if (diver_list[i].get('number')) == x_coor:                         #when the diver_no thats in diver_list is equal to the input x_coor
                diver_list[i]['name'] = diver_name                              #add key -> name to be diver_name in the same list index
                diver_list[i]['time start'] = time_start                        #add key - > time start to record start time

                diver_name_label = Label(window,text = diver_name,background = 'black',foreground = 'white')              #display diver name
                diver_name_label['font'] = helv2
                diver_name_label.grid(row = x_coor, column = 7, sticky = W)

                end_dive_button = Button(window)                                #create button to end dive
                end_dive_button['font']= helv2
                end_dive_button.configure(text = 'End dive',background = 'black' ,fg = 'white',command = lambda:end_dive(diver_label,diver_name_label,end_dive_button,x_coor))
                end_dive_button.grid(row = x_coor,column = 8)

def end_dive(diver_label,diver_name_label,end_dive_button,x_coor,diver_list = diver_list, check_dive_status = status):
    end_dive_button.destroy()                                                   #destroy irrelevant labes and buttons
    diver_name_label.destroy()
    diver_label.destroy()

    time_end = datetime.datetime.now()                                          #record end time of dive
    status -= 1
    i = 0
    for i in range(len(diver_list)):
        if (diver_list[i].get('number')) == x_coor:                             #when the diver_no thats in diver_list is equal to the input x_coor
            diver_list[i]['time end'] = time_end                                #add key -> time end to record end time
            #diver_list[i] passes into backend code here to be saved
            backend.record_dive(device_id = diver_list[i]['serial'],sup = diver_list[i]['sup'],name = diver_list[i]['name'], start_time = diver_list[i]['time start'], end_time = diver_list[i]['time end'])
            del diver_list[i]['name']                                           #destroy name and times so that a new dive can be recorded
            del diver_list[i]['time start']
            del diver_list[i]['time end']
            messagebox.showinfo('Success','Dive saved!')


    add_diver(x_coor)                                                           #run add diver again for new diver

def end_all_dive(diver_list = diver_list):
    a = 0
    for i in range(len(diver_list)):
        if len(diver_list[i]) > 3:
            a=1
    if a==1:
        messagebox.showerror('Error','Dives are still ongoing')
    else:
        prompt_end_dive()

def prompt_end_dive():
    window.withdraw()


    confirm_end = Tk()
    confirm_end.geometry('300x300')
    confirm_end.title('')
    confirm_end.attributes("-fullscreen",True)
    confirm_end.configure(background = 'black')

    global helv
    helv = font.Font(family="Helvetica", size=30, weight='bold')

    rows = 0                                                                    #create a 4x3 grid
    while rows < 2:
        confirm_end.rowconfigure(rows,weight=1)
        rows += 1
    column = 0
    while column < 3:
        confirm_end.columnconfigure(column,weight=1)
        column += 1

    confirm = Label(confirm_end,text = 'Confirm end all dives?',background = 'black',fg = 'white')
    confirm['font'] = helv
    confirm.grid(row = 0 ,column = 1)
    end = Button(confirm_end)
    end.configure(text = 'End',command = lambda:end_cmd(confirm_end),background = 'black',fg = 'white')
    end['font'] = helv
    end.grid(row = 1,column = 2)
    cancel = Button(confirm_end)
    cancel.configure(text = 'Cancel',command = lambda:cancel_cmd(confirm_end),background = 'black',fg = 'white')
    cancel['font']=helv
    cancel.grid(row = 1,column = 0)

def end_cmd(confirm_end):
    confirm_end.destroy()
    window.destroy()
    log_entry()

def cancel_cmd(confirm_end):
    confirm_end.destroy()
    window.update()
    window.deiconify()

def log_entry():                                                                #creates window to log dives
    global log
    log = Tk()                                                                  #define log
    log.geometry('300x300')
    log.resizable(width=False, height=False)
    log.title('Log dive time')
    log.attributes("-fullscreen", True)
    log.configure(background = 'black')
    rows = 0                                                                    #create 10x10 grid
    while rows < 9:
        log.rowconfigure(rows,weight=1)
        log.columnconfigure(rows,weight=1)
        rows += 1
    global helv
    helv = font.Font(family="Helvetica", size=30, weight='bold')

    log_dive_button = Button(log)                                           #create button to log dives
    log_dive_button['font'] = helv
    log_dive_button.configure(width = 20,foreground = 'dark green',text = 'Log all dives', command = lambda: log_dives(log_dive_button))
    log_dive_button.grid(row = 4, column = 4)

    log.mainloop()

def log_dives(log_dive_button):                               #runs when log all dives button is pressed
    log.withdraw()


    global place                                                              #create widnow named place
    place = Tk()
    place.geometry('300x300')
    place.resizable(width=False, height=False)
    place.title('')
    place.configure(background = 'black')
    place.attributes('-fullscreen',True)

    global helv
    helv = font.Font(family="Helvetica", size=30, weight='bold')

    rows = 0                                                                    #create a 4x3 grid
    while rows < 4:
        place.rowconfigure(rows,weight=1)
        rows += 1
    column = 0
    while column < 3:
        place.columnconfigure(column,weight=1)
        column += 1

    if os.path.exists('pkl_data'):
        diver_logger_length = 0
        for i in os.listdir('pkl_data'):
            if '.pkl' in i:
                diver_logger_length+=1
    else:
        diver_logger_length = 0
    prompt_user(log_dive_button,diver_logger_length)

def prompt_user(log_dive_button,diver_logger_length):
    if diver_logger_length == 0:                                                #if there are no more dive loggers to be logged
        log.update()
        log.deiconify()
        blank.destroy()
        place.destroy()                                                         #close place
        log_dive_button.destroy()                                               #destroy the 'log all dives' button
        submit_all_dive_data()
    else:
        message = Label(place,text = 'Place dive logger',background = 'black',fg ='white').grid(row = 0,column = 1)                              #create label
        label_number_left = Label(place,text = 'Dive loggers remaining:',background = 'black',fg = 'white').grid(row = 1,column = 1)              #create label
        number_left = Label(place,text = diver_logger_length,background = 'black',fg = 'white').grid(row = 1,column = 2,sticky = W)                 #show number of dive loggers left

        log_next_button = Button(place)                                                                         #button to extract dive data from dive logger
        log_next_button.configure(text = 'OK',command = lambda:extract_data(log_dive_button,diver_logger_length),background = 'black',fg = 'white')
        log_next_button.grid(row = 3, column = 1)

def extract_data(log_dive_button,diver_logger_length):
    extract_status = backend.extract_dive()
    if extract_status != []:
        diver_logger_length -= 1
        prompt_user(log_dive_button,diver_logger_length)
        return
    messagebox.showerror('Error','Please place Dive Logger on Reader')
    prompt_user(log_dive_button,diver_logger_length)

def submit_all_dive_data():
    submit_all = Button(log)
    submit_all['font'] = helv
    submit_all.configure(width = 20,foreground = 'dark red',text = 'Submit dives', command = excel_output)
    submit_all.grid(row = 4, column = 4)

def excel_output():
    #richies code here
    log.destroy()

input_dive_details()
