echo starting dos
ls -1 *.sh > list
sed s/-dos.sh//g list >> name
rm list

b=$( awk 'END{print NR}' name )
a="1"
input=$(awk -v a=$a '{if(NR==a) print $0}' name)
rm name
echo $input

#############
echo creating files
cp ../geom/$input.cell $input-dos.cell
cp ../geom/$input-out.cell $input-dos.cell

echo spectral_kpoints_mp_spacing  : 0.02 > kpoint
cat kpoint >> $input-dos.cell
rm kpoint

module use /usr/local/modulefiles/staging/eb/all
module load CASTEP/18.1-intel-2017b
echo starting dos calculation
date +"%r"
srun --export=ALL  castep.mpi $input-dos
echo finished calculation
date +"%r"
echo optados
/shared/cmdd1/User/fcp18fz/optados/src/optados.gfortran.x86_64 $input-dos
bandgap=$( awk '/Thermal Bandgap :/{a=$5}END{print a}' $input-dos.odo )
 echo band gap = $bandgap
dosatfermi=$( awk '/DOS at Fermi Energy/{a=$11}END{print a}' $input-dos.odo)
number=$(echo 0.01 )
echo change dir, write result
cd ../../
  if (( $(echo "$bandgap > $number" |bc -l) )); then

          echo non metallic
          echo $input = non metallic >> result
          echo bandgap : $bandgap eV >> result
          echo dos at Fermi energy: $dosatfermi eln/cell >> result   
   else
          echo metallic
          echo $input = metallic >> result
          echo band gap $input = $bandgap
          echo bandgap : $bandgap eV >> result
          echo dos at Fermi energy: $dosatfermi eln/cell >> result
   fi



