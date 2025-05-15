#!/bin/bash
#SBATCH --job-name=qmmm_test
#SBATCH --nodes=1                        
#SBATCH --ntasks=8            
#SBATCH --cpus-per-task=1             
#SBATCH --partition=pre             
#SBATCH --time=24:00:00                 
#SBATCH --mem-per-cpu=1G     
module load openmpi
echo running MPI with $SLURM_NTASKS cores

export TMPDIR=/scratch/$USER/apptainer_tmp/${SLURM_JOB_ID}
mkdir -p $TMPDIR

srun apptainer exec -e \
    --bind /home/$USER \
    --bind /scratch/$USER \
    --bind $TMPDIR \
    /home/zbai29/JR/soft/apptainer/amber_cpu.sif bash -c \
    "source /ambertools25/amber.sh && \
    source /pmemd24/amber.sh && \
    mpirun -np $SLURM_NTASKS sander.MPI -O -i qmmm.in -o qmmm.out -p input.prmtop -y traj.nc -c input.rst -r qmmm.rst -x qmmm.nc"

rm -rf $TMPDIR
