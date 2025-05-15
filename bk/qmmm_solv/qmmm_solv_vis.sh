dist=3
cpptraj -p ZnMim2.prmtop -c md2.rst << EOF
trajin qmmm_solv.nc
trajout qmmm_solv_vis_${dist}A.pdb
strip !(:1|:1<:${dist})
go
EOF