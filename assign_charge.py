import sys

def read_charges(mol2_file):
    charges = {}
    with open(mol2_file) as f:
        lines = f.readlines()
    in_atom = False
    for line in lines:
        if line.startswith("@<TRIPOS>ATOM"):
            in_atom = True
            continue
        if line.startswith("@<TRIPOS>"):
            in_atom = False
        if in_atom:
            parts = line.split()
            if len(parts) >= 9:
                atom_name = parts[1]
                res_num = parts[6]
                res_name = parts[7]
                charge = float(parts[8])
                charges[(atom_name, res_num, res_name)] = charge
    return charges

def read_charges(mol2_file):
    charges = {}
    with open(mol2_file) as f:
        lines = f.readlines()
    in_atom = False
    for line in lines:
        if line.startswith("@<TRIPOS>ATOM"):
            in_atom = True
            continue
        if line.startswith("@<TRIPOS>"):
            in_atom = False
        if in_atom:
            parts = line.split()
            if len(parts) >= 9:
                atom_name = parts[1]
                charge = float(parts[8])
                charges[atom_name] = charge
    return charges

def replace_charges(target_file, charge_maps, output_file):
    with open(target_file) as f:
        lines = f.readlines()
    new_lines = []
    in_atom = False
    for line in lines:
        if line.startswith("@<TRIPOS>ATOM"):
            in_atom = True
            new_lines.append(line)
            continue
        if line.startswith("@<TRIPOS>"):
            in_atom = False
            new_lines.append(line)
            continue
        if in_atom:
            parts = line.split()
            if len(parts) >= 9:
                atom_name = parts[1]
                res_name = parts[7]
                replaced = False
                # Zn原子用ZN.mol2的电荷
                if res_name.upper() == "ZN" and atom_name.upper() in ["ZN", "ZN"]:
                    for charges in charge_maps:
                        for k, v in charges.items():
                            if k.upper() in ["ZN", "ZN"]:
                                parts[8] = f"{v:.6f}"
                                replaced = True
                                break
                        if replaced:
                            break
                # 其他原子用2MZ.mol2的电荷
                else:
                    for charges in charge_maps:
                        if atom_name in charges:
                            parts[8] = f"{charges[atom_name]:.6f}"
                            break
                line = "{:>7} {:<4} {:>10} {:>10} {:>10} {:<6} {:>2} {:<6} {:>10}\n".format(*parts[:9])
            new_lines.append(line)
        else:
            new_lines.append(line)
    with open(output_file, "w") as f:
        f.writelines(new_lines)
if __name__ == "__main__":
    # 用法: python assign_charge.py 2MZ.mol2 ZN.mol2 ZnMim2.mol2 ZnMim2_new.mol2
    charges_2mz = read_charges(sys.argv[1])
    charges_zn = read_charges(sys.argv[2])
    replace_charges(sys.argv[3], [charges_2mz, charges_zn], sys.argv[4])