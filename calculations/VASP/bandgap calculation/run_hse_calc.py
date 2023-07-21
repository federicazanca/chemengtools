import os, os.path
import sys
## All metals in periodic table
all_metals = ['Al', 'Si', 'K', 'Ca', 'Ti',  'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Sr', 'Zr', 'Mo', 'Ba', 'La', 'W', 'Hg', 'Pb', 'Sc', 'Cr', 'Ga', 'Ge', 'As', 'Rb', 'Y', 'Nb', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'Cs', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Tl', 'Bi', 'Po', 'At', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'Np', 'U', 'Pu', 'Am', 'Cm']

if len(sys.argv) < 2:
    print("ERROR: not enough arguments.  Usage: python file.py target_directory")
    exit()



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
				#also the HSE calc, so nothing to do here
				if os.path.isdir(MOF_folder+"/HSE"):
					print("HSE already done")
					continue
				#need to do HSE calculation, preparing the folder and submitting
				else:
					os.system("mkdir "+ MOF_folder+"/HSE")
					print("creating directory HSE")
					os.system("cp " + MOF_folder+ "/WAVECAR "+ MOF_folder + "/HSE")
					os.system("cp " + MOF_folder+ "/POTCAR "+ MOF_folder + "/HSE")
					os.system("cp " + MOF_folder+ "/POSCAR "+ MOF_folder + "/HSE")
					os.system("cp " + MOF_folder+"/"+dir+".sh "+ MOF_folder + "/HSE")
					os.system("cp " + MOF_folder+"/../INCAR_HSE "+ MOF_folder+ "/HSE/INCAR")
					for line in open(MOF_folder+"/INCAR"):
						if line.startswith("MAGMOM"):
							magmom = line
							break
					incarfile = open(MOF_folder+"/HSE/INCAR", "a")
                                	incarfile.write(magmom)
					os.system("cd "+MOF_folder+ "/HSE; qsub "+dir+".sh; cd ../../../")
			#pbe run  but something went wrong. fix manually
			else:
				print("error PBE")
	#this is the case where you only put the POSCAR file, and you need to run PBE, so it is gonna prepare the files and submit
	else:
		print(dir + " to do")
		filename = docs[0]
		os.rename(MOF_folder+"/"+filename, MOF_folder+"/POSCAR")
		poscarfile = open(MOF_folder+"/POSCAR")
		for (i, line) in enumerate(poscarfile):
			if i < 5:
				continue
			#POTCAR creation
			elif i == 5:
				elements = line.split()
				elements_index=[]
				elements_cmd = "cat "
				for (j,el) in enumerate(elements):
					if el in all_metals:
						elements_index.append(j)
                                        #el_dir is the directory in wwhich you have all the single potcar files, vasp gives them if you have the license. In this case I have a folder called potcars in the working directory. In sharc they are in /usr/local/packages/apps/vasp/POTCAR but you need to do qrshx first
					el_dir = cwd + "/potcars/"+el
					if os.path.exists(el_dir):
						elements_cmd+=el_dir+"/POTCAR "
					elif os.path.exists(el_dir+"_pv"):
						print("Using pv potcar for "+el)
						elements_cmd+=el_dir+"_pv/POTCAR "
					else:
						raise NameError("element potcar not found for "+el)
				elements_cmd += ">> ./"+sys.argv[1]+"/"+dir+"/POTCAR"
				print("creating POTCAR for " + dir)
				os.system(elements_cmd)
			#magetic moment for spin calculations
			elif i == 6:
				numbers = line.split()
				number_str = "MAGMOM = "
				for (pos,num) in enumerate(numbers):
					if pos in elements_index:
						number_str += num+"*1 "
					else:
						number_str += num+"*0 "	
				os.system("cp ./"+sys.argv[1]+"/INCAR_PBE ./"+sys.argv[1]+"/"+dir+"/INCAR")
				print("creating INCAR for "+dir)
				incarfile = open(MOF_folder+"/INCAR", "a")
				incarfile.write(number_str)
				incarfile.close()
			else:
				break
		poscarfile.close()
		#submission
		print("creating run file for "+dir)
		os.system("cp ./"+sys.argv[1]+"/run_sharc.sh ./"+sys.argv[1]+"/"+dir+"/"+dir+".sh")
		print("submitting PBE calculation for "+dir)
		os.system("cd "+MOF_folder+"; qsub "+dir+".sh; cd ../..")

