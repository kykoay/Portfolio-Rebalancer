import pandas_datareader.data as web
import datetime
import numpy as np

start_date = datetime.datetime.today().strftime('%Y-%m-%d')
start_date1=datetime.datetime.strptime("2016-06-06",'%Y-%m-%d')
print start_date
print np.busday_offset(start_date,0,roll='backward') #If weekend, find the last closest Friday
print np.busday_offset(start_date1,0,roll='backward') #If weekday keeps being weekday


a = web.DataReader("F","yahoo","2016-06-03")

print type(a)
print a
print "      "
print a["Adj Close"][0]
