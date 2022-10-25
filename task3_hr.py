'''
Ques 1 : To open and read contents from json file
'''
import json
all_files = ['Elga.json','mayukha.json','Prathibha.json','Sharika.json','Vishakh.json']
for file in all_files:
    with open(file) as json_file:
      main_file = json.load(json_file)

# print(main_file)
# # https://stackoverflow.com/questions/58396329/opening-multiple-json-files-inside-a-for-loop

print(main_file['captured_data'].keys())
print(main_file['captured_data']['hr'].keys())
print(main_file['captured_data']['slp'].keys())
print(main_file['captured_data']['act'].keys())
print(main_file['captured_data']['bat'].keys())
print(main_file['captured_data']['err'].keys())


'''
Ques 2 : Access the time information and convert the appropriate time form to IST
'''

from datetime import datetime, timedelta
from pytz import timezone
import pytz
start_date_time = main_file['Start_date_time']
str(start_date_time).replace('+00:00', 'Z')
time_object = datetime.strptime(start_date_time, '%Y-%m-%dT%H:%M:%SZ')
time = pytz.timezone("UTC")
loc_time = time.localize(time_object, is_dst=None) #https://stackoverflow.com/questions/25264811/pytz-converting-utc-and-timezone-to-local-time
time_utc = loc_time.astimezone(pytz.utc)
time_ist = loc_time.astimezone(pytz.timezone('Asia/Kolkata'))
print(time_utc,time_ist)


'''
Ques 3 : Plot the converted time in x axis and heart rate in y axis
'''
hr_in_bpm=main_file['captured_data']['hr']['HR in BPM']
# print(hr_in_bpm)
rr_in_ms = main_file['captured_data']['hr']['RR in ms']

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

heart_rate = np.array(main_file['captured_data']['hr']['HR in BPM'])

# finding cumulative sum of the "RR in ms" column
cumsum_arr = np.array(rr_in_ms, dtype='int').cumsum().tolist()


for idx, val in enumerate(cumsum_arr):
    cumsum_arr[idx] = time_ist + timedelta(milliseconds=val)

sns.scatterplot(x=cumsum_arr, y=heart_rate)
plt.show()


'''
Ques 4 : Also, access the step count column which tells number of steps taken by the subject at that instance of time. Colour the Heart Rate region as red correspondingly at that time instance whenever the step count value is above 5
'''
import matplotlib.pyplot as plt

stepcount=main_file['captured_data']['act']['step count']

for i in range(len(stepcount)):
  if stepcount[i] > 5:
    plt.plot(i,hr_in_bpm[i],color='red',marker='*')
  else:
    plt.plot(i,hr_in_bpm[i],color='blue',marker='*')    
plt.show()
