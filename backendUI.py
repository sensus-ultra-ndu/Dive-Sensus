import auto
import win32gui
import time
import pandas as pd
from datetime import datetime
import os
import pickle
import extract_time
import re

def get_device_id(exitoption=True):
	window=auto.check_window('Subsurface')	#Checking if Subsurface is opened
	if(window!=None):
		auto.bring_to_front(window) #If it is open bring the window to foreground
	else:
		auto.start_subsurface()	#Else if it is not open, open Subsurface
	auto.import_device()	#Registering the device into Subsurface
	devID = auto.extract_device_id() #Returning the Device ID
	if exitoption:
		auto.exit_all()
	return devID

def record_dive(device_id, sup, name, start_time, end_time):
	dive_record = [device_id, sup, name, start_time, end_time] #Create a list storing the respective information
	if os.path.exists(str('pkl_data/'+device_id+'.pkl')):	#Checking is the pickle file exist
		obj=[]	#Creating a list to store potential data in pickle
		pickle_data=open(str('pkl_data/'+device_id+'.pkl'), 'rb')	#Opening the existing pickle file in read-only
		while True:
			try:
				obj.append(pickle.load(pickle_data))	#Loading the data in the pickle file into 'obj'
			except EOFError:
				break 	#Breaks the loop if there are no more data to load
		pickle_data.close() #Close the pickle file
		obj.append(dive_record) #Adding the latest dive record into the pickle file
		pickle_data=open(str('pkl_data/'+device_id+'.pkl'), 'wb') #opening the existing pickle file in write
		for i in obj:
			pickle.dump(i,pickle_data) #Adding the updated list back to the pickle file (ascending)
		pickle_data.close()	#Close the pickle file
	else:	#if the pkl file do not exist
		pickle_data=open(str('pkl_data/'+device_id+'.pkl'), 'wb') #Create a new pkl
		pickle.dump(dive_record,pickle_data) #dumping the data into the pickle file
		pickle_data.close()	#Closing the Pickle file


def date_filtering(diver_name,sup,ui_startdive,ui_enddive,fileName):
	try:	#Checking if the file exist
		csv = pd.read_csv('csv_data/'+fileName)  #Putting CSV into DataFrame
	except FileNotFoundError as error:
		print('Error: '+ str(error))
		return #Return NoneType
	index = 0 #index used to select objects from the DataFrame
	temp_df = pd.DataFrame( #creating an empty temporary Dataframe to store relevant dives
		columns=['dive number', 'date', 'time', 'sample time (min)', 'sample depth (m)','sample temperature (C)', 'sample pressure (bar)', 'sample heartrate'])
	for i in csv['date']: #For loop to iterate through all the rows of the 'Date' column in the DataFrame
		#This condition statement picks out the dives that falls between 2 datetime variables
		if(ui_startdive<=datetime.strptime(str(i+' '+csv.iloc[index]['time']),'%Y-%m-%d %H:%M:%S') #Part 1 of the statement
		and ui_enddive>=(datetime.strptime(str(i+' '+csv.iloc[index]['time']),'%Y-%m-%d %H:%M:%S')+timedelta(hours=1))):#Part 2 of the statement
			temp_df = temp_df.append(csv.iloc[index]) #Appending the current object into the temp DataFrame
		index+=1 #Increaing Index by 1
	temp_df['Diver Name'] = diver_name
	temp_df['Supervisor'] = sup
	return(temp_df)

def extract_dive():
	devid = get_device_id(False)	#Get Device ID
	regex = re.compile(r'\d\w[a-zA-Z0-9]{8}')
	if regex.match(devid) is None:
		auto.exit_all()
		return []
	#get pickle file by serial into list
	dives=[]	#Create a list to store the lists in the pickle
	if os.path.exists(str('pkl_data/'+devid+'.pkl')):	#Checking if the pickle file exists
		pickle_data=open(str('pkl_data/'+devid+'.pkl'), 'rb')	#Open the Pickle file that belongs to the specific device
		while True:
			try:
				dives.append(pickle.load(pickle_data))	#Adding in ascending chronological order
			except EOFError:
				break	#Breaks the loop when there are no more list to load
		pickle_data.close()	#Close the Pickle file
		auto.export_csv(devid) #Export all the dives in the device
		auto.exit_all()
		#for loop iterate through dictionary to enter Start Time & End Time into date_filtering()
		total_dive = []
		for i in dives:
			temp_df = date_filtering(diver_name=i[1],sup=i[2],ui_startdive=i[3],ui_enddive=i[4],fileName=str(devid+'.csv')) #Storing date_filtering() return variable into 'temp_df'
			if temp_df.empty:
				print('No dives filtered')
				return
			total_dive.append(extract_time.extract_time(temp_df))
			return total_dive
	else:
		print('Pickle File not found')
		return dives #Returning an empty list if the pickle file do not exists
