#!/bin/bash
#SBATCH -p pzm
#SBATCH -A pzm


ls -1 *cif > list
sed s/.cif//g list >> searcherrors
rm list

 
#this is the loop for choosing the input name from a list of names (mofs)
b=$( awk 'END{print NR}' searcherrors )
a="1"
while [ $a -le $b ]; do
  input=$(awk -v a=$a '{if(NR==a) print $0}' searcherrors)
  cd $input/geom
  if grep  'Out Of Memory' slurm*
    then ls -1 slurm* > list
         sed s/'slurm-'//g list >> num1
         sed s/.out//g num1 >> num2
          c=$( awk 'END{print NR}' num2 )
          d="1"
          ID=$(awk -v d=$d '{if(NR==d) print $0}' num2)
          scancel $ID
          rm list
          rm num1  
          rm num2 
          echo $input
          cd ../..
  else cd ../../
  fi
  a=$[$a+1]
#end of the loop for the input name
done
rm searcherrors 
