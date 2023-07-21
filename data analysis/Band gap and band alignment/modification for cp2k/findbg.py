import os
import sys
from bandgap import bandgap
if len(sys.argv) < 2:
    print("ERROR: not enough arguments.  Usage: python findbg.py  source_directory")
    exit()
#this will create a file with the band gap of the desired materials
elenco = open("bg", "w")

for root, dirs, files in os.walk(sys.argv[1]):
        for file in files:
                #modify OUTCAR with the name of the cp2k output file
		if file == "OUTCAR":
			complete = False
			for line in  open(root + "/" + file):
                                #modify this line with any line that could mean that the calculation is finished in the output file
				if "General timing and accounting informations for this job:" in line:
					complete = True
				if complete == True:
                                        #modify EIGENVAL with the name of the output file that has the eigenvalues
					eigenval = root+"/EIGENVAL"
					result =  bandgap(eigenval)
					print(root)
					#this is going to use the name of the folder in which you are as identifier for the structure you are calculating
					elenco.write(str(root)+"\n")
					print(result)
					elenco.write(str(result)+"\n")
					break
elenco.close()

