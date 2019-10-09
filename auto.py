import pyautogui as auto
import os
import subprocess
import time
import clipboard
import win32gui
from tkinter import Tk
from win32gui import GetWindowText, GetForegroundWindow

################################## FUNCTIONS ##################################
import_state = list()

def check_window(title):
	result = WindowEnum(title)
	if result:
		window = win32gui.FindWindow(None, result)
		return window
	else:
		return None

def get_visible_windows(hwnd, top_windows):
	if win32gui.IsWindowVisible(hwnd):
		top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

def WindowEnum(title):
	top_windows = []
	win32gui.EnumWindows(get_visible_windows, top_windows)
	for i in top_windows:
		if title in i[1]:
			#print("found:", i[1])
			return i[1]
	return None

def bring_to_front(window):
	#auto.press('alt')
	win32gui.SetForegroundWindow(window)

def start_subsurface():
	#This part is to open subsurface
	# os.system('start cmd')#start command prompt
	# time.sleep(1)#waiting for cmd to open
	# auto.write('start /max C:\\"Program Files (x86)"\\Subsurface\\subsurface.EXE') #command to open subsurface in full screen using cmd
	# auto.press('enter')#executing command\
	os.startfile('C:\\Program Files (x86)\\Subsurface\\subsurface.exe')
	#waiting for Subsurface to open
	window = False
	while not window:
		print("Waiting for Subsurface to launch")
		time.sleep(1)
		window = check_window("Subsurface")
	bring_to_front(window)

def import_device():
	auto.keyDown('ctrl')
	auto.keyDown('d')
	auto.keyUp('ctrl')
	auto.keyUp('d')
	time.sleep(0.1)
	auto.press('tab')
	auto.press('r')
	auto.press('e')
	for i in range(0,3):
		auto.press('tab')
	auto.write('com')
	for i in range(0,5):
		auto.press('tab')
	auto.press('end')
	auto.press('enter')
	time.sleep(2)
	auto.keyDown('shift')
	for i in range(0,15):
		auto.press('tab')
	auto.keyUp('shift')
	auto.press('enter')
	import_state.append(1)
	# # to close error message for now
	# auto.keyDown('alt')
	# auto.keyDown('f4') 
	# auto.keyDown('f4')
	# auto.keyUp('f4')
	# auto.keyUp('alt')
	# time.sleep(1)

def extract_device_id():
	# LOGS > EDIT DEVICE NAMES
	auto.press('alt')
	auto.press('l')
	auto.press('n')
	devID=''
	for i in range(0,2):
		auto.press('tab')
	auto.keyDown('ctrl')
	auto.keyDown('c')
	auto.keyUp('ctrl')
	auto.keyUp('c')
	time.sleep(1)
	auto.press('esc')
	# print(GetWindowText(GetForegroundWindow()))
	# while('Subsurface' not in GetWindowText(GetForegroundWindow())):
	# 	auto.press('esc')
	# 	time.sleep(0.5)
	# 	auto.keyUp('alt')
	devID = clipboard.paste()
	tk=Tk()
	tk.clipboard_clear()			#To clear clipboard of all data
	tk.destroy()
	#print(devID)
	time.sleep(1)
	return devID

	# # '''<Add script to copy device ID onto clipboard>'''#copy device ID into clipboard and make as variable
	# # #This part closes the 'Edit Device Names' tab
	# auto.keyDown('alt')
	# auto.keyDown('f4') #alt+F4 closes the tab
	# auto.keyUp('f4')
	# auto.keyUp('alt')

def export_csv(devID):
	if not os.path.exists('csv_data'): #Checks if 'csv_data' folder is in the main folder
		os.mkdir('csv_data')	#Creating the folder if there isn't one
	dir_name = os.getcwd()
	# # #This part export the dive as a csv
	auto.keyDown('ctrl')
	auto.keyDown('e')#Export tab is opened
	auto.keyUp('e')
	auto.keyUp('ctrl')
	# # #This part scrolls down the "Export Format and export the csv"
	auto.press('tab')
	for i in range(0,4): #scrolling down
		auto.press('down')
	auto.press('enter') #selecting 'CSV dive profile'
	auto.write(dir_name+'\\csv_data\\'+devID+'.csv') #placing the csv into csv_data in the current folder
	auto.press('enter')
	auto.press('tab') #precaution: just rewrite anyways #failsafe
	auto.press('enter')
	time.sleep(1)#waiting for file to be saved

def exit_all():
	if not import_state:
		#This part closes subfurface and cmd
		auto.keyDown('alt')
		auto.press('f4')
		auto.keyUp('alt')
	else:
		auto.keyDown('alt')
		auto.press('f4')
		auto.keyUp('alt')
		auto.press('tab')
		auto.press('enter')
################################## MAIN ##################################


# start_subsurface()
# # test()
# import_device()
# devID = extract_device_id()
# print(devID)
# export_csv(devID)
# exit_all()

################################## REF ##################################
# # file - auto.moveTo(20,25)
# # import - auto.moveTo(130,30)
# # edit device name - auto.moveTo(184,200)
# # This part copy the device ID because the CSV doesnt include the UID
# auto.click(130,30) #Go to "Log"
# auto.click(184,200) #Go to "Edit Device Names"