import getopt, sys, pickle, os
from glob import glob

from dedoubloneur import avance

def save_object(obj, filename):
    with open(f"res/{filename}", 'wb') as outp:
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)
        
os.makedirs("res/", exist_ok=True)

i = len((glob("res/instance*.pkl")))
print(i)
fichier = ""

argumentList = sys.argv[1:]

# Options
options = "hf:i:u:"

# Long options
long_options = ["help", "file=", "init=", "use="]

try:
    arguments, values = getopt.getopt(argumentList, options, long_options)
    
    for currentArgument, currentValue in arguments:
        
        if currentArgument in ("-h", "--help"):
            print("help")
        
        elif currentArgument in ("-f", "--file"):
            fichier = currentValue
            print(f"initialazing {fichier}")
            
            with open(currentValue, 'rb') as fp:
                list_to_process = pickle.load(fp)
            
        elif currentArgument in ("-i", "--init"):
            if not fichier:
                raise("No file given (use the -f argument to pass a file path/name")
            
            instance = avance.Avance(list_to_process,  nb_pivots = 40)
            instance.process(taillegroupe = 50, sensibilite  = .0004)
            save_object(instance, f"instance{i}.pkl")
        
        elif currentArgument in ("-u", "--use"):
            if not fichier:
                raise("No file given (use the -f argument to pass a file path/name")
            if currentValue == 

except getopt.error as err:
	# output error, and return with an error code
	print(err)
