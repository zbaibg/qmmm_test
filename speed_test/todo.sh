for DIR in \
./qmmm_hf_sto3g/hpc_10core_orca \
./qmmm_hf_sto3g/hpc_10core_quick \
./qmmm_hf_sto3g/hpc_16core_orca \
./qmmm_hf_sto3g/hpc_16core_quick \
./qmmm_hf_sto3g/hpc_20core_quick \
./qmmm_hf_sto3g/hpc_5core_quick \
./qmmm_hf_sto3g/hpc_8core_orca \
./qmmm_hf_sto3g/hpc_8core_quick \
./qmmm_hf_sto3g/hpc_8core_quick_apptainer \
./qmmm_hf_sto3g/hpc_8core_quick_noewald \
./qmmm_hf_sto3g/hpc_8core_quick_noewald_apptainer \
./qmmm_pbe_Def2TZVP/hpc_10core_orca \
./qmmm_pbe_Def2TZVP/hpc_20core_orca \
./qmmm_pbe_Def2TZVP/hpc_5core_orca \
./qmmm_pbe_Def2TZVP/hpc_8core_quick_apptainer \
./qmmm_pbe_Def2TZVP/pc_10core_orca \
./qmmm_pbe_LANL2DZ/hpc_10core
do
   newrun.py $DIR
done
