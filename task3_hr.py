import json
from turtle import color
from numpy import cumsum
from datetime import datetime, timedelta
import pytz
from pytz import timezone
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy
import scipy.signal as signal

all_files = ['Elga.json','mayukha.json','Prathibha.json','Sharika.json','Vishakh.json']
for file in all_files:
    with open(file) as json_file:
      main_file = json.load(json_file)

      print(main_file['captured_data'].keys())
      print(main_file['captured_data']['hr'].keys())
      print(main_file['captured_data']['slp'].keys())
      print(main_file['captured_data']['act'].keys())
      print(main_file['captured_data']['bat'].keys())
      print(main_file['captured_data']['err'].keys())

      start_date_time = main_file['Start_date_time']
      str(start_date_time).replace('+00:00', 'Z')
      time_object = datetime.strptime(start_date_time, '%Y-%m-%dT%H:%M:%SZ')
      time = pytz.timezone("UTC")
      loc_time = time.localize(time_object, is_dst=None) #https://stackoverflow.com/questions/25264811/pytz-converting-utc-and-timezone-to-local-time
      time_utc = loc_time.astimezone(pytz.utc)
      time_ist = loc_time.astimezone(pytz.timezone('Asia/Kolkata'))
      print(time_utc,time_ist)

      hr_in_bpm=main_file['captured_data']['hr']['HR in BPM']
      rr_in_ms = main_file['captured_data']['hr']['RR in ms']
      heart_rate = np.array(main_file['captured_data']['hr']['HR in BPM'])
      cum_arr = np.array(rr_in_ms).cumsum().tolist()
      print(len(cum_arr))
      print(type(cum_arr))
      # print(cum_arr)
      x_axis_data = []
      for val in cum_arr:
          x_axis_data.append(time_ist + timedelta(milliseconds=val))
      sns.scatterplot(x=x_axis_data, y=heart_rate)
      plt.xlabel('Time')
      plt.xlabel('Heart rate')
      plt.show()
      stepcount=main_file['captured_data']['act']['step count']
      cum_arr=np.array(cum_arr)/1000
      hr_in_bpm=np.array(hr_in_bpm)
      new=stepcount[0:int(cum_arr[-1]/10)]
      print(len(new)) 
      for i in range(len(new)):
        if stepcount[i] > 5:
          plt.plot(cum_arr[(cum_arr >= i*10) & (cum_arr <= (i+1)*10)],hr_in_bpm[(cum_arr >= i*10) & (cum_arr <= (i+1)*10)],color='red')
        else:
          plt.plot(cum_arr[(cum_arr >= i*10) & (cum_arr <= (i+1)*10)],hr_in_bpm[(cum_arr >= i*10) & (cum_arr <= (i+1)*10)],color='blue')
      plt.show()
      fil_x=[]
      fil_y=[]
      cum_arr=np.array(cum_arr)/1000
      hr_in_bpm=np.array(hr_in_bpm)
      new=stepcount[0:int(cum_arr[-1]/10)]
      filter_order = 4    
      cutoff_frequency = 0.05
      B, A = signal.butter(filter_order, cutoff_frequency, output='ba')
      filtered_hr = scipy.signal.filtfilt(B, A,hr_in_bpm)
      for a in range(len(new)):
        q = cum_arr[(cum_arr >= a*10) & (cum_arr <= (a+1)*10)].tolist()
        w = filtered_hr[(cum_arr >= a*10) & (cum_arr <= (a+1)*10)].tolist()
        if new[a] > 5:
          plt.plot(q,w,color='red')
        else:
          plt.plot(q,w,color='black')
        fil_x += q 
        fil_y += w
      plt.show()


