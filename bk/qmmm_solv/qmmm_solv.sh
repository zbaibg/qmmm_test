export CUDA_VISIBLE_DEVICES=0  
export OMP_NUM_THREADS=14
sander -O -i qmmm_solv.in -o qmmm_solv.out -p ZnMim2.prmtop -c qmmm.rst -r qmmm_solv.rst -x qmmm_solv.nc
