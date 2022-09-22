import getopt, sys

argumentList = sys.argv[1:]

# Options
options = "hip:"

# Long options
long_options = ["help", "init", "process="]

try:
	arguments, values = getopt.getopt(argumentList, options, long_options)
	
	# checking each argument
	for currentArgument, currentValue in arguments:

		if currentArgument in ("-h", "--help"):
			print("Displaying Help")
			
		elif currentArgument in ("-i", "--init"):
			print("Displaying file_name:", sys.argv[0], currentValue)
			
			
		elif currentArgument in ("-p", "--process"):
			print(("Enabling special output mode (% s)") % (currentValue))
			
except getopt.error as err:
	# output error, and return with an error code
	print(err)
