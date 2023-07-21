import os
import sys
from bandgap import bandgap
if len(sys.argv) < 2:
    print("ERROR: not enough arguments.  Usage: python findbg.py  source_directory")
    exit()

elenco = open("bg", "w")

for root, dirs, files in os.walk(sys.argv[1]):
        for file in files:
		if file == "OUTCAR":
			complete = False
			for line in  open(root + "/" + file):
				if "General timing and accounting informations for this job:" in line:
					complete = True
				if complete == True:
					eigenval = root+"/EIGENVAL"
					result =  bandgap(eigenval)
					print(root)
					elenco.write(str(root)+"\n")
					print(result)
					elenco.write(str(result)+"\n")
					break
elenco.close()

