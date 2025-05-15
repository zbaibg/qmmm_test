export CUDA_VISIBLE_DEVICES=0  
export OMP_NUM_THREADS=14
sander -O -i qmmm.in -o qmmm.out -p ZnMim2.prmtop -c qmmm_hf.rst -r qmmm.rst -x qmmm.nc
