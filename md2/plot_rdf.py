import numpy as np
import matplotlib.pyplot as plt

# Read the data, skipping the header line
distances = []
values = []

with open('rdf_methanol.dat', 'r') as f:
    for line in f:
        if line.startswith('#') or not line.strip():
            continue
        parts = line.split()
        if len(parts) == 2:
            distances.append(float(parts[0]))
            values.append(float(parts[1]))

# Convert to numpy arrays
distances = np.array(distances)
values = np.array(values)

# Plot
plt.figure(figsize=(8, 5))
plt.plot(distances, values, marker='o', linestyle='-')
plt.xlabel('Distance (Angstrom)')
plt.ylabel('g(r)')
plt.title('RDF: ZN@Zn : MOH@O1')
plt.grid(True)
plt.tight_layout()
plt.show()