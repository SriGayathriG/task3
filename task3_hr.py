import json
from datetime import datetime, timedelta
import pytz
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy
import scipy.signal as signal

all_files = ['Elga.json','mayukha.json','Prathibha.json','Sharika.json','Vishakh.json']
for file in all_files:
    with open(file) as json_file:
      main_file = json.load(json_file)
      '''
      All the json files are opened and loaded into main_file variable
      '''

      print(main_file['captured_data'].keys())
      print(main_file['captured_data']['hr'].keys())
      print(main_file['captured_data']['slp'].keys())
      print(main_file['captured_data']['act'].keys())
      print(main_file['captured_data']['bat'].keys())
      print(main_file['captured_data']['err'].keys())
      '''
      The keys of each json file is identified
      '''

      start_date_time = main_file['Start_date_time']
      str(start_date_time).replace('+00:00', 'Z')
      time_object = datetime.strptime(start_date_time, '%Y-%m-%dT%H:%M:%SZ')
      time = pytz.timezone("UTC")
      loc_time = time.localize(time_object, is_dst=None) 
      time_utc = loc_time.astimezone(pytz.utc)
      time_ist = loc_time.astimezone(pytz.timezone('Asia/Kolkata'))
      print(time_utc,time_ist)
      '''
      From the start_date_time in the file, time information is obtained.strptime() is used to create formatted strings.
      astimezone() function returns a datetime instance according to the specified zone time 
      Further, UTC is converted into IST 
      '''

      hr_in_bpm=main_file['captured_data']['hr']['HR in BPM']
      rr_in_ms = main_file['captured_data']['hr']['RR in ms']
      heart_rate = np.array(main_file['captured_data']['hr']['HR in BPM'])
      cum_arr = np.array(rr_in_ms).cumsum().tolist()
      print(len(cum_arr))
      print(type(cum_arr))
      '''
      cumsum() is used to compute the cumulative sum of array of elements 
      '''

      time_data = []
      for val in cum_arr:
          time_data.append(time_ist + timedelta(milliseconds=val))
      sns.scatterplot(x=time_data, y=heart_rate)
      plt.xlabel('Time')
      plt.xlabel('Heart rate')
      plt.show()
      '''
      Scatter plot is used to plot the time in x-axis and heart rate in y-axis
      '''

      stepcount=main_file['captured_data']['act']['step count']
      cum_arr=np.array(cum_arr)/1000
      hr_in_bpm=np.array(hr_in_bpm)
      new_step=stepcount[0:int(cum_arr[-1]/10)]
      print(len(new_step)) 
      for i in range(1,len(new_step)):
        if stepcount[i] > 5:
          plt.plot(cum_arr[(cum_arr >= i*10) & (cum_arr <= (i+1)*11)],hr_in_bpm[(cum_arr >= i*10) & (cum_arr <= (i+1)*11)],color='red')
        else:
          plt.plot(cum_arr[(cum_arr >= i*10) & (cum_arr <= (i+1)*11)],hr_in_bpm[(cum_arr >= i*10) & (cum_arr <= (i+1)*11)],color='blue')
      plt.show()
      '''
      A required range is ierted using for loop. The range (11) in hr_in_bpm provides an overlap between each window, thereby eliminating gaps
      '''

      fil_x=[]
      fil_y=[]
      filter_order = 4    
      cutoff_frequency = 0.05
      B, A = signal.butter(filter_order, cutoff_frequency, output='ba')
      filtered_hr = scipy.signal.filtfilt(B, A,hr_in_bpm)
      '''
      The signal is filtered using butter filter and scipy filtfilt function. 
      '''
      for a in range(1,len(new_step)):
        '''
        range(1,len()), (1)is used. The 0 value in the 1st index is removed in order to avoid a drop in the beginning of the graph
        '''
        q = cum_arr[(cum_arr >= a*10) & (cum_arr <= (a+1)*11)].tolist()
        w = filtered_hr[(cum_arr >= a*10) & (cum_arr <= (a+1)*11)].tolist()
        if new_step[a] > 5:
          plt.plot(q,w,color='red')
        else:
          plt.plot(q,w,color='blue')
        fil_x += q 
        fil_y += w
      plt.show()
      '''
      The filtered heart rate is then plotted. If the step count is above 5, i is indicated in red, otherwise in blue.
      '''

      stepcount=main_file['captured_data']['act']['step count']
      print(type(stepcount))
      print(len(stepcount))
    
      ticks = main_file['captured_data']['act']['ticks']
      print(type(ticks))

      ticks_int = [eval(i) for i in ticks]
      print(len(ticks_int))
      print(type(ticks_int))
      '''
      The ticks is converted into integer from strings using eval() function.
      '''

      tick_arr = np.array(ticks_int)
      fs = 512 #sampling rate
      ticks_sampling=tick_arr/fs
      ticks_cum = ticks_sampling.cumsum().tolist()
      print(type(ticks_cum))
      '''
      The cumulative sum of the values is obtained and stored as a list
      '''
      
      cum_list = []
      for va in ticks_cum:
        cum_list.append(time_ist + timedelta(seconds=va))
      sns.scatterplot(x=cum_list,y=stepcount)
      plt.ylabel('Step count')
      plt.xlabel('time')
      plt.show()

