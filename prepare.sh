cp ../amber_geostd/2/2MZ.* ./
cp ../amber_geostd/m/MOH.* ./
reduce  ZnMim2.pdb > ZnMim2_H.pdb
antechamber -i ZnMim2.pdb -fi pdb -o ZnMim2.mol2 -fo mol2 -at gaff2 -c rc
python assign_charge.py 2MZ.mol2 ZN.mol2 ZnMim2.mol2 ZnMim2_new.mol2
python calculate_charge.py ZnMim2.mol2
parmchk2 -i ZnMim2.mol2 -f mol2 -o ZnMim2.frcmod
tleap -s -f tleap.in > tleap.out
mv ZnMim2.prmtop ZnMim2_wrong.prmtop
mv ZnMim2.inpcrd ZnMim2_wrong.inpcrd
parmed -p ZnMim2_wrong.prmtop << EOF
loadRestrt ZnMim2_wrong.inpcrd
setMolecules solute_ions True
parmout ZnMim2.prmtop ZnMim2.inpcrd
EOF
rm ZnMim2_wrong.prmtop ZnMim2_wrong.inpcrd