# task3

#QUES 1
1. Import json file
2. using for loop, open the json file 
3. load the json file to obtain a dictionary
https://stackoverflow.com/questions/58396329/opening-multiple-json-files-inside-a-for-loop


#QUES 2
1. Import the necessary libraries 
2. time_object = datetime.strptime(start_date_time, '%Y-%m-%dT%H:%M:%SZ')
time_object = datetime.strptime(start_date_time[:-1], '%Y-%m-%dT%H:%M:%S')
We can either use 'Z' in the string (line 12) or slice the Z from the string to avoid error (line 13)
3. Inbuilt func astimezone is used and time is obtained
https://stackoverflow.com/questions/25264811/pytz-converting-utc-and-timezone-to-local-time
https://blog.vivekshukla.xyz/how-to-convert-datetime-to-different-timezone-in-python-using-pytz/
https://pythonhosted.org/pytz/


#QUES 3
https://www.kaggle.com/code/stetelepta/exploring-heart-rate-variability-using-python
Cumulative sum 
cumsum() - returns the cumulative sum of the array elements along the given axis

Step 1: 
rr_in_ms = main_file['captured_data']['hr']['RR in ms']
print(type(rr_in_ms))
O/P: <class 'list'>

step 2:
converting the rr_in_ms {list} -> {array} to perform cumulative sum
cumsum_arr = np.array(rr_in_ms).cumsum()

step 3:
Adding tolist() to convert {array} -> {list} to plot
cumsum_arr = np.array(rr_in_ms).cumsum().tolist()

step 4:
for idx, val in enumerate(cumsum_arr):
  cumsum_arr[idx] = time_ist + timedelta(milliseconds=val) 

idx-index, val-value
1. enumerate cumsum_arr list
2. adding time_ist with millisecond
3. Using timedelta, we can millisecond or microsecond to current time
4. cumsum_arr[idx] -- it will alter the values based on the index 
if the index is 0, the time is changed in the list in 1st value
if the index is 1, the time is changed in the list in 2nd value and so on
5. Plot the time value with heart rate (import seaborn)


#QUES 4 
matplotlib library is used
if stepcount is above 5, the print graph in red
else, print in other color (blue) 
