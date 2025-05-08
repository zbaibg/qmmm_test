export CUDA_VISIBLE_DEVICES=0  
export OMP_NUM_THREADS=14
sander -O -i qmmm_sample_solv.in -o qmmm_sample_solv.out -p ZnMim2.prmtop -c md2.rst -r qmmm_sample_solv.rst -x qmmm_sample_solv.nc
