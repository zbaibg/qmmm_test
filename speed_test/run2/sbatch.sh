#!/bin/bash
#SBATCH --job-name=phenothrin_MD
#SBATCH --nodes=1                        
#SBATCH --ntasks=16                 
#SBATCH --cpus-per-task=1             
#SBATCH --partition=pre             
#SBATCH --time=24:00:00                 
#SBATCH --mem-per-cpu=1G     
module load openmpi

source /home/zbai29/condainit.sh
conda activate amber
source $CONDA_PREFIX/amber.sh

#load the customized mpirun because this cluster does not have a supported mpirun.
export PATH="/scratch/zbai29/soft/orca_6_0_1_linux_x86-64_shared_openmpi416/:$PATH"
which mpirun
#load the openmpi library path to the LD_LIBRARY_PATH
export LD_LIBRARY_PATH="$(dirname $(dirname $(which mpiexec)))/lib:$LD_LIBRARY_PATH"

sh qmmm.sh
