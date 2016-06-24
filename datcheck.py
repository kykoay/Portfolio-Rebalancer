#Code to query each entry one by one, get the price from Yahoo Finance API and then update FTPORTFOLIO with current price and does the delta calculation
import sqlite3
import pandas_datareader.data as web
import datetime
import numpy as np
import decimal
#Since we have weekday data only, what this does is to give us the last closest week day volume
# Stuff to update: Get non-trading days due to holidays
start_date = datetime.datetime.today().strftime('%Y-%m-%d')
start_date=np.busday_offset(start_date,0,roll='backward')

print "Welcome to your Portfolio Rebalancing Calculator. Today's date is %s" %start_date
#print start_date
#print start_date - 1 
cash=raw_input("Input total amount of USD that you will be investing this period if any : >>>")
try: 	
	int(cash)
	print "Ok you used an integer good job!"
except ValueError:
	try:
		float(cash)
		print "Floating values? What are you doing mate? Buying penny stocks?"
	except ValueError:
		print "Cash input must be numeric"

#Get USD/CAD rate for the day
try:
	er=web.DataReader("CAD=X",'yahoo',start_date)["Close"][0]
except:
	print "Can't find the USD/CAD exchange rate of :" + start_date
	er=web.DataReader("CAD=X",'yahoo',start_date-1)["Close"][0]
	print "Retrieved USD/CAD exchange rate using " + start_date-1 + " date instead."

convert=1/er
print "The USD/CAD conversion rate we will use is: %s"  %str(convert)


conn = sqlite3.connect('portalloc.sqlite')
cur = conn.cursor()

cur.execute('''
		INSERT INTO FTPORTFOLIO (tickers,quantity,currency_id,cashind,current_price_lc,current_price_usd) VALUES ('CASHUSD',?,2,1,1,1)
	''',(cash,))

sqlstatement = 'SELECT ID,TICKERS,QUANTITY FROM FTPORTFOLIO WHERE CASHIND = 0 ' 

tickers=list()

for row in cur.execute(sqlstatement):
	print row[0],row[1],row[2]
	tickers.append(row[1])

#Get closing price from Yahoo Finance and update and insert into the table

for item in tickers:
	print item
	try:
		close_price = web.DataReader(item,"yahoo",start_date)
		cp = "%.2f" %close_price["Adj Close"][0]
		cp = float(cp) 
	#Need to add update statement to add stock price in the table
		cur.execute('''UPDATE FTPORTFOLIO SET current_price_lc= ? WHERE tickers = ? ''', (cp,item))
		print 'Ticker :' + item + ' ' +  'Updated' +' With Close Price' + ' ' +  str(cp) +" of date :" + str(start_date)
	except:
		#continue
		print "Can't find the data of: " + item + "for the date: " + str(start_date)
		close_price = web.DataReader(item,"yahoo",start_date-1)
		cp = "%.2f" %close_price["Adj Close"][0]
		cp = float(cp) 
	#Need to add update statement to add stock price in the table
		cur.execute('''UPDATE FTPORTFOLIO SET current_price_lc= ? WHERE tickers = ? ''', (cp,item))
		print 'Ticker :' + item + ' ' +  'Updated' +' With Close Price' + ' ' +  str(cp) + 'with data of' + str(start_date-1)


conn.commit() #Add this to have data committed LOL

#Need to have an update part to get the USD price,before calculating portfolio value since we normalise to USD
for item in tickers:
	cur.execute(
		'''
		UPDATE FTPORTFOLIO
		SET current_price_usd = CASE currency_id WHEN 1 THEN current_price_lc WHEN 2 THEN current_price_lc*? END 
		WHERE tickers = ?
		''',(convert,item))
conn.commit()


for item in tickers:
	cur.execute(''' 
		UPDATE FTPORTFOLIO
		SET tickerportvalue = quantity*current_price_usd 
		WHERE tickers = ? ''',(item,))

conn.commit()

cur.execute('''
		UPDATE FTPORTFOLIO
		set tickerportvalue = quantity*current_price_usd 
		WHERE tickers = 'CASHUSD'
	''')

sqlstatement = 'SELECT SUM(tickerportvalue) FROM FTPORTFOLIO' 

total=0

cur.execute(sqlstatement)
total=cur.fetchone()[0]

tickers.append("CASHUSD")
for item in tickers:
	cur.execute('''
		UPDATE FTPORTFOLIO
		SET current_percentage = tickerportvalue/? 
		WHERE tickers = ?
		''',(total,item))
conn.commit()

cur.close()

print "Everything executed perfectly"