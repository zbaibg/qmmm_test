import sys

def calculate_total_charge(mol2_file):
    total_charge = 0.0
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
                charge = float(parts[8])
                total_charge += charge
    return total_charge

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python calculate_charge.py <mol2_file>")
        sys.exit(1)
    total_charge = calculate_total_charge(sys.argv[1])
    print(f"Total charge of {sys.argv[1]}: {total_charge:.6f}")