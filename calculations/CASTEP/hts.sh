#!/bin/bash
#SBATCH -p pzm
#SBATCH -A pzm

module use /usr/local/modulefiles/staging/eb/all
module load CASTEP/18.1-intel-2017b


ls -1 *cif > list
sed s/.cif//g list >> mofs
rm list

 
#this is the loop for choosing the input name from a list of names (mofs)
b=$( awk 'END{print NR}' mofs )
a="1"
while [ $a -le $b ]; do
  input=$(awk -v a=$a '{if(NR==a) print $0}' mofs)
  echo $input
  if [ -d "./$input/" ]
  then
  echo "Directory $input already exists."
  a=$[$a+1]
  else
 
  #convert cell file and create all the folders; the template files must be in the folder
  /home/fcp18fz/cif2cell-1.2.10/cif2cell $input.cif -p castep
  mv *.cell $input.cell
  cp template.param $input.param
  cp template-dos.param $input-dos.param
  cp template-dos.odi $input-dos.odi


  echo kpoints_mp_spacing : 0.03 > kpoint
  cat kpoint >> $input.cell
  rm kpoint
  
  mkdir $input
  cd $input
  mkdir geom
  mkdir dos
  cd ..
  mv $input.param $input/geom
  mv $input.cell $input/geom
  mv $input-dos.param $input/dos
  mv $input-dos.odi $input/dos

  cd $input
  cd geom
  srun --export=ALL  castep.mpi -d $input
  kpoints1=$( awk '/Number of kpoints used = /{a=$6}END{print a}' $input.castep )
    if (( $(echo "$kpoints1 > 40") )); then
        kpoints=10
    else 
        kpoints=$kpoints1
    fi
  memory=$( awk '/Approx. total storage required per process/{b=$8}END{print b}' $input.castep )
  memory2=$(echo $memory*10 |bc -l)
    if (( $(echo "$memory2 < 10000" |bc -l) )); then

       mem='15000'

    elif (( $(echo "$memory2 < 15000" |bc -l) )); then

       mem='20000'
    elif (( $(echo "$memory2 < 30000" |bc -l) )); then      
       mem='40000'
    elif (( $(echo "$memory2 < 60000" |bc -l) )); then
       mem='70000'
    elif (( $(echo "$memory2 < 95000" |bc -l) )); then
       mem='90000'
    elif (( $(echo "$memory2 < 120000" |bc -l) )); then
       mem='150000'
    elif (( $(echo "$memory2 < 160000" |bc -l) )); then
       mem='170000'

    else
       mem='192000' 

    fi
  echo $memory
  echo $mem  
  echo $kpoints1 k points
  echo $kpoints  cores
  cat > $input.sh <<EOF
#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=$kpoints
#SBATCH --mem=$mem
#SBATCH --job-name=$input
#SBATCH --time=72:00:00
EOF

  cp ../../template.sh .
  cat template.sh >> $input.sh
  #crea lo script per dos e copialo nella cartella
  cat > $input-dos.sh <<EOF
#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=$kpoints
#SBATCH --mem=$mem
#SBATCH --job-name=$input
#SBATCH --time=90:00:00

EOF
  cp ../../template-dos.sh .
  cat template-dos.sh >> $input-dos.sh
  mv $input-dos.sh ../dos/
  
#qua devi mettergli di mandare il calcolo
  sbatch $input.sh
  cd ../..         	   
  a=$[$a+1]
  fi
#end of the loop for the input name
done 
