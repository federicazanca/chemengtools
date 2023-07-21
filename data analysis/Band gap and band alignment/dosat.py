import os
import sys
if len(sys.argv) < 3:
    print("ERROR: not enough arguments.  Usage: python dosat.py target_filename source_directory")
    exit()


elenco = open(sys.argv[1], "w")
for root, dirs, files in os.walk(sys.argv[2]):
	for file in files:
		if file.endswith(".odo"):
			for line in open(root + "/" + file):
				if " Spin Component : 1   DOS at Fermi Energy " in line:
					value =float(line[48:-23])
					print(file[:-8])
					print(value)
					elenco.write(file[:-8] + ";"+ str(value))
				if "Thermal Bandgap : " in line:
					bandgap=float(line[35:-30])
					print(bandgap)
					if (bandgap < 0.01):
						met="conductor"
					elif (bandgap <= 3):
						met="semiconductor"
					else:
						met="insulator"
					print(met)
					elenco.write(";" + str(bandgap) + ";")
					if value < 0.3 and bandgap > 0.01:
						print("bss")	
						agrfile = file.split(".")[0] + ".adaptive.agr"
						print(agrfile)
						file2 = open(root + "/" + agrfile, 'r') #questo file da aprire
						hbg = bandgap / 2.0

						atData = False	
						trovatoSx = False
						for line in file2:
							if atData:
								dati = map(float, line.strip().split())
								if trovatoSx:
									if dati[0] > hbg:
										ptDxFuori = dati
										ptDxDentro = precedente
										break
								else:
									if dati[0] > -hbg:
										ptSxDentro = dati
										ptSxFuori = precedente
										trovatoSx = True
								precedente = dati
		
							else:
								if '@type xy' in line:
									atData = True

						# valore medio sinistra
						y1 = ptSxDentro[1]
						y0 = ptSxFuori[1]
						x1 = ptSxDentro[0]
						x0 = ptSxFuori[0]
						VBM_dos = (y1 - y0)/(x1 - x0) * (-hbg - x0) + y0
	
						# valore medio destro
						y1 = ptDxFuori[1]
						y0 = ptDxDentro[1]
						x1 = ptDxFuori[0]
						x0 = ptDxDentro[0]
						CBM_dos = (y1 - y0)/(x1 - x0) * (hbg - x0) + y0
	
						print(VBM_dos)
						print(CBM_dos)
						elenco.write(";" + str(VBM_dos)+";"+ str(CBM_dos)+ ";" + met + ";" +root)
					else:
						elenco.write(";" + str(value)+";"+ str(value)+ ";" + met + ";" +root) 	
					break
			elenco.write(file + "\n")
elenco.close()
				
