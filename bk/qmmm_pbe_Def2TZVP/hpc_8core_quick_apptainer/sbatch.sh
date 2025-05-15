#!/bin/bash
#SBATCH --job-name=qmmm_test
#SBATCH --nodes=1                        
#SBATCH --ntasks=8            
#SBATCH --cpus-per-task=1             
#SBATCH --partition=pre             
#SBATCH --time=24:00:00                 
#SBATCH --mem-per-cpu=2G     
module load openmpi
echo running MPI with $SLURM_NTASKS cores

export TMPDIR=/scratch/$USER/apptainer_tmp/${SLURM_JOB_ID}
mkdir -p $TMPDIR
#Currently this only support running in one node.
#For more nodes, the apptainer needs to be rebuilt as https://github.com/CHTC/recipes/tree/main/workflows-hpc/multi-node-container
/usr/bin/apptainer exec -e \
--bind /home/$USER \
--bind /scratch/$USER \
--bind $TMPDIR \
--bind $PWD \
-W $PWD \
/home/zbai29/JR/soft/apptainer/amber_cpu_single_node.sif bash -c \
"source /ambertools25/amber.sh && \
source /pmemd24/amber.sh && \
mpirun -np $SLURM_NTASKS sander.MPI -O -i qmmm.in -o qmmm.out -p ZnMim2.prmtop -c qmmm_hf.rst -r qmmm.rst -x qmmm.nc"

rm -rf $TMPDIR

