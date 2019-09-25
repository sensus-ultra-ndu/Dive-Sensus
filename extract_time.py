import csv
import sys
import datetime
from datetime import timedelta
import pandas as pd

def extract_time(df):
    if df is None:                                                              #check for nonetype
        print('Error: No dive data')
        return
    else:
        for row in df.iterrows():                                                   #search rows for start time
            if row[1][3]=='0:10':                                                   #when time == 0:10 (getting first line)
                left_surface_str = row[1]['date']+' '+row[1]['time']                          #add date and time tgt to obtain start datetime
                format = "%Y-%m-%d %H:%M:%S"                                        #define format to make datetime object
                left_surface = datetime.datetime.strptime(left_surface_str, format) #make left_surface into a datetime object
                break

        depth = []                                                                  #create list to hold all depth variables
        for row in df.iloc[::-1].iterrows():                                        #search df from bottom up
            depth.append(row[1]['sample depth (m)'])                                                 #add all depth values into the list
        counter = 0
        for i in range(len(depth)-1,-1,-1):                                        #search list depth
            while depth[i]-depth[i-1]< 0:                                           #when depth getting deeper
                counter += 1                                                    #add counter
                i-=1
            else:
                break                                                               #once not getting deeper, stop loop
        if counter == 0:
            left_bottom = reach_surface                                             #if prog cant find left bottom, then equate it to reach surface
        else:
            time_left_str =df.iloc[counter]['sample time (min)']                   #obtain duration at left bottom index
            lb_dive_min = int(time_left_str[:-3])
            if lb_dive_min < 60:                                                  #obtain left bottom duration (check if min >60, if it is use diff format)
                format = "%M:%S"
                time_left = datetime.datetime.strptime(time_left_str, format)
            else:
                lb_hour = round(lb_dive_min/60)
                lb_min = lb_dive_min - (end_hour*60)
                format = "%H:%M:%S"
                dive_duration = str(lb_hour) + ':' + str(lb_min) +':'+ lb_dive_min[-2:]
                time_left = datetime.datetime.strptime(dive_duration, format)
            hourl = time_left.hour                                              #obtain hr min sec from time_left
            minl = time_left.minute
            secl = time_left.second
            left_bottom = left_surface + timedelta(hours = hourl,minutes = minl, seconds = secl)        #add to left surface time to obtain left bottom                                     #search df bottom up


        for row in df.iloc[::-1].iterrows():                                       #iterate through df in reverse
            if row[1]['sample depth (m)'] >0.110:                               #once dive logger is deeper than 0.1m
                dive_duration_str = row[1]['sample time (min)']                   #obtain dive duration
                end_dive_min = int(dive_duration_str[:-3])
                if end_dive_min < 60:                                           #make into datetime object
                    format = "%M:%S"
                    dive_duration = datetime.datetime.strptime(dive_duration_str, format)
                else:
                    end_hour = round(end_dive_min/60)
                    end_min = end_dive_min - (end_hour*60)
                    format = "%H:%M:%S"
                    dive_duration = str(end_hour) + ':' + str(end_min) +':'+ dive_duration_str[-2:]
                    dive_duration = datetime.datetime.strptime(dive_duration, format)
                hour = dive_duration.hour
                min = dive_duration.minute
                sec = dive_duration.second
                reach_surface = left_surface + timedelta(hours = hour,minutes = min, seconds = sec)             #add to left surface to obtain reach surface
                break

        name = df['Diver Name'][1]
        sup = df['Supervisor'][1]
        data = [name,sup,left_surface,left_bottom,reach_surface]
    return data
