#!/bin/bash

ls -1 *cif > list
sed s/.cif//g list >> searcherrors
rm list


#this is the loop for choosing the input name from a list of names (mofs)
b=$( awk 'END{print NR}' searcherrors )
a="1"
while [ $a -le $b ]; do
  input=$(awk -v a=$a '{if(NR==a) print $0}' searcherrors)
  echo $input
  cd $input/geom
  squeue -n $input
      
  if grep 'LBFGS: Geometry optimization completed successfully.'  $input.castep
      then
      echo $input optimized
      echo ' '
      if test -f "*-out.cell"; then
	echo there is a out file here. check
        cd ../../
        else
        echo calculation needs rerun
	sed 's/-gt 1 / -gt 1 /' $input.sh > tmp
        mv tmp $input.sh
	rm slurm*
	sbatch $input.sh
        cd ../..
        fi
  else
      echo $input error unknown
      echo ' ' 
      sed 's/-gt 1 / -gt 1 /' $input.sh > tmp
      mv tmp $input.sh
      rm slurm*
      sbatch $input.sh 
      cd ../..
  fi
a=$[$a+1]
#end of the loop for the input name
done
rm searcherrors



