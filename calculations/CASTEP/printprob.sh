#!/bin/bash

ls -1 *cif > list
sed s/.cif//g list >> searcherrors
rm list


#this is the loop for choosing the input name from a list of names (mofs)
b=$( awk 'END{print NR}' searcherrors )
a="1"
while [ $a -le $b ]; do
  input=$(awk -v a=$a '{if(NR==a) print $0}' searcherrors)
  cd $input/geom
  squeue -n $input
  if grep  'Out Of Memory' slurm*
      then
      echo $input error = out of memory
        
      cd ../../
      
  elif grep ' DUE TO TIME LIMIT' slurm*
      then
      echo $input time limit
      echo ' ' 
       cd ../..

  
 
  elif grep 'LBFGS: Geometry optimization completed successfully.'  $input.castep
      then
      echo $input optimized
      echo ' '
      cd ../..
  elif grep 'max. SCF cycles performed but system has not reached the groundstate.' $input.castep
      then
      echo $input error = SCF not converged
      echo ' '
      cd ../../
  elif grep 'Geometry optimization failed to converge after' $input.castep
      then
      echo $input error = optimisation not converged 
      echo ' ' 
      cd ../../
  else
      echo $input error unknown
      echo ' ' 
      cd ../..
  fi
a=$[$a+1]
#end of the loop for the input name
done
rm searcherrors



