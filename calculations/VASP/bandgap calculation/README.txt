How to use VASP and my scripts

Access sharc

Create a folder, we call it "main_folder"

Inside main_folder create different folder for all the different MOFs so you will have for example
/main_folder/FAFJAZ_1Cl
/main_folder/FAFJAZ_2Cl
etc

Inside FAFJAZ_1Cl put FAFJAZ_1Cl.vasp --> you create this file converting the cif file using VESTA or better using vaspkit(I'll show you, or I'll do it)
etc in every folder of which you have the MOF

put run_hse_calc.py, findbg.py and bandgap.py outside main_folder
put the other files inside main_folder

run
"python run_hse_calc.py main_folder"
The first thing that is going to be run will be the PBE calculation. Then after it finishes you will have to rerun and another folder called HSE will be created with the HSE calculation

Specification  "el_dir" in the script is the directory in wwhich you have all the single potcar files, vasp gives them if you have the license. In this case I have a folder called potcars in the working directory. In sharc they are in /usr/local/packages/apps/vasp/POTCAR but you need to do qrshx first

Now if you want to get the band gap from this you just need to run findbg.py and it will create a csv file with the results


NOTE:
I wrote this to run the HSE calculation for the high throughput screening, so you will find the copy of this in the HTS folder in the cluster. 
When we decided to do the band alignemnt I wrote the scrit band_alignment, which is based on the fact that I needed to rerun a third calculation in a third folder to create the LOCPOT file.
To be honest in future if we need to run band alignment just use the files from the band alignment folder
