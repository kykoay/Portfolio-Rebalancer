cash=raw_input("Input total amount of USD that you will be investing this period if any ")
try:
	int(cash)
	print "Ok you used an integer good job!"
except ValueError:
	try:
		float(cash)
		print "Floating values? What are you doing mate? Buying penny stocks?"
	except ValueError:
		print "Cash input must be numeric"