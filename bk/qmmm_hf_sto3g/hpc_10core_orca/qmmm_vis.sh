dist=3
cpptraj -p ZnMim2.prmtop -c md2.rst << EOF
trajin qmmm.nc
trajout qmmm_vis_${dist}A.pdb
strip !(:1|:1<:${dist})
go
EOF