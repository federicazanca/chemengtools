#!/bin/bash
#$ -cwd
#$ -l h_rt=30:00:00
#$ -l rmem=2G
#$ -pe mpi 8
#$ -m bea
#$ -M federicazanca8@gmail.com

module load apps/vasp/5.4.4.pl2/intel-17.0.0-openmpi-2.0.1

mpirun vasp_std
