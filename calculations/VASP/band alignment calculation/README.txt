How to use VASP and my scripts

Access sharc

Create a folder, we call it "main_folder"

Inside main_folder create different folder for all the different MOFs so you will have for example
/main_folder/FAFJAZ_1Cl
/main_folder/FAFJAZ_2Cl
etc

Inside FAFJAZ_1Cl put FAFJAZ_1Cl.vasp --> you create this file converting the cif file using VESTA or better using vaspkit
etc in every folder of which you have the MOF

put run_hse_calc.py, findbg.py bandgap.py band_alignment.py and aligned.py outside main_folder 
put the other files inside main_folder

run
"python run_hse_calc.py main_folder" --> to be honest python just needs the location of the folder, so even if main folder was somewhere else you could write the path and it would work
The first thing that is going to be run will be the PBE calculation. Then after it finishes you will have to rerun and another folder called HSE will be created with the HSE calculation

Specification  "el_dir" in the script is the directory in wwhich you have all the single potcar files, vasp gives them if you have the license. In this case I have a folder called potcars in the working directory. In sharc they are in /usr/local/packages/apps/vasp/POTCAR but you need to do qrshx first

Now if you want to get the band alignment from this you just need to run band_alignment.py and it will create a csv file with the results. You need to have installed the band aligned software from Butler et al.


NOTE:
If you want to use band alignment I advise you use the scripts here. You can find the results in the folder ESA/screening to see how it looks like  

