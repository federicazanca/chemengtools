import os, os.path
import sys
import linecache
from aligned import aligned

if len(sys.argv) < 2:
    print("ERROR: not enough arguments.  Usage: python file.py target_directory")
    exit()


elenco = open("results_potential.csv", "w")
elenco.write("MOF;Band gap (eV);Potential;Aligned CBM (LUMO);Aligned VBM (HOMO);Ionisation potential;CO2 reduction range;Water splitting range\n")
for dir in os.listdir(sys.argv[1]):
        cwd = os.getcwd()
        MOF_folder = cwd+"/"+sys.argv[1]+"/"+dir
        if os.path.isfile(MOF_folder):
                continue
        docs=[name for name in os.listdir(MOF_folder) if os.path.isfile(os.path.join(MOF_folder, name))]
        #Inside the main folder there should be folders with either the position input file (INCAR)(meaning that the first calculation, PBE, didn't start), or a lot of files (meaning that the PBE calculation is finished)

        #the first if means that the folder is actually empty, so you need to add the POSCAR file
        if len(docs) == 0:
                print(dir+" empty")
        #this one means that there are many files, meaning you already run the PBE calc
        elif len(docs) > 1:
                print(dir + " PBE done")
                #we don't need this b ut I leave it here anyway
                if MOF_folder.endswith("_ions"):
                        print("ionic MOF")
                else:
                        #this means the PBE calculation is finished ok
                        if os.path.isfile(MOF_folder+"/OUTCAR") and  "General timing and accounting informations for this job:" in open(MOF_folder+"/OUTCAR").read():
                                print("completed PBE")
                                #also the HSE calc, check results and run locpot if finished
                                if os.path.isdir(MOF_folder+"/HSE"):
                                        print("HSE already done, check results and run locpot if finished")
                                        if os.path.isfile(MOF_folder+"/HSE/OUTCAR") and  "General timing and accounting informations for this job:" in open(MOF_folder+"/HSE/OUTCAR").read():
                                                print("completed HSE")
                                                if os.path.isfile(MOF_folder+"/HSE/LOCPOT"):
                                                            os.system("cd "+ MOF_folder+"/HSE/; python /shared/cmdd1/User/fcp18fz/MacroDensity-master/examples/SphericalAverage.py > potential.txt")
                                                            line=linecache.getline(MOF_folder+"/HSE/potential.txt",27)
                                                            print(line)
                                                            pot = line.split()[0]
                                                            eigenval = MOF_folder+"/HSE/EIGENVAL"
                                                            results = aligned(eigenval, pot)
                                                            bg=results[0]
                                                            potential=results[1]
                                                            al_CBM=results[2]
                                                            al_VBM=results[3]
                                                            IP=results[4]
                                                            OER=-5.09
                                                            HER=-3.87
                                                            co2_red="no"
                                                            water_spl="no"
                                                            if -3.6 > float(al_CBM) > -4.05:
                                                                co2_red="yes"
                                                            if float(al_VBM)<OER and float(al_CBM) > HER:
                                                                water_spl="yes"
                                                            
                                                            elenco.write(dir + ";" +str(bg)+";"+str(potential)+";"+str(al_CBM)+";"+str(al_VBM)+";"+str(IP)+";"+co2_red+";"+water_spl+"\n")


