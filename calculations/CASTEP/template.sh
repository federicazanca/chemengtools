
echo starting file
ls -1 *.cell > list
sed s/.cell//g list >> name
rm list

b=$( awk 'END{print NR}' name )
a="1"
input=$(awk -v a=$a '{if(NR==a) print $0}' name)
echo $input
rm name
cp $input.cell $input-original.cell
rm $input.castep
echo  start calculation
date 
#this will change to 1 when the optimisation is over
 finished=0

#start of the loop, for all the time finished > 0 the loop continues
   while [ $finished -eq 0 ];  do
#run the calculation
   
   module use /usr/local/modulefiles/staging/eb/all
   module load CASTEP/18.1-intel-2017b

   srun --export=ALL  castep.mpi $input
   echo  calculation done
   date 
#remove useless stuff
   rm *.bands *.bib

#define the variable that will tell you if the optimisation is fine, you get it from the ouput file .castep, you just care about the number of iterations (that is the 4th number of the line where it is written 'finished iteration' in the file, and that's why you define a=4 and print a). If that's >0, you want to re run the optimization so you want to change the output .cell file into an $input cell file, so you have to delete some parameters (you do this with the sed command)
  num_iterations=$( awk '/BFGS: finished iteration/{a=$4}END{print a}' $input.castep )
     echo step 5: iterations
     echo $num_iterations
     if [ $num_iterations -gt 0 ]; then

       if grep -Fxq "%BLOCK cell_constraints" $input-out.cell
       then
         line1=$( awk -v IGNORECASE=1 '/%BLOCK cell_constraints/{print NR}' $input-out.cell )
         sed "$line1,$(( $line1+3 ))d" $input-out.cell > tmp
         mv tmp $input-out.cell
       fi

       if grep -Fxq "FIX_ALL_IONS : true" $input-out.cell
       then
         line2=$( awk -v IGNORECASE=1 '/FIX_ALL_IONS : true/{print NR}' $input-out.cell )
         sed "${line2}d" $input-out.cell > tmp
         mv tmp $input-out.cell
       fi
       if grep -Fxq "FIX_VOL : true" $input-out.cell
       then
         line2=$( awk -v IGNORECASE=1 '/FIX_VOL : true/{print NR}' $input-out.cell )
         sed "${line2}d" $input-out.cell > tmp
         mv tmp $input-out.cell
       fi
 
       if grep -Fxq "FIX_COM : true" $input-out.cell
       then
         line3=$( awk -v IGNORECASE=1 '/FIX_COM : true/{print NR}' $input-out.cell )
         sed "${line3}d" $input-out.cell > tmp
         mv tmp $input-out.cell
         mv $input-out.cell $input.cell
       fi
 #this is connected to the first if, it says that in the case num iterations is not greater than 0, the optimisation ends, so you can change the value of finished and the loop will stop
     else
     finished=1
     fi
#close the while loop
   done
echo finished
  if grep  'LBFGS: Geometry optimization completed successfully.' *.castep
   then  
        rm *.check
        cd ../dos
        echo submit dos
        sbatch $input-dos.sh

  else
     if  grep  'Out Of Memory' slurm*
     then
     echo out of memory error 
     else 
     echo calculation not properly done
     fi  
  fi
