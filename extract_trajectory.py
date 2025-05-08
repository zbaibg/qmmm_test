#!/usr/bin/env python3

import re
import numpy as np
from typing import List, Tuple, Dict

def extract_trajectory(filename: str) -> Tuple[List[float], List[np.ndarray], List[str]]:
    """
    Extract trajectory data from a quick output file.
    
    Args:
        filename (str): Path to the quick output file
        
    Returns:
        Tuple containing:
        - List of timesteps
        - List of numpy arrays containing coordinates for each timestep
        - List of element symbols
    """
    timesteps = []
    coordinates = []
    elements = []
    current_coords = []
    current_elements = []
    
    # Regular expressions for matching
    input_geom_pattern = re.compile(r'--\s+INPUT\s+GEOMETRY\s+--\s*:')
    gradient_pattern = re.compile(r'@ Begin Gradient Calculation')
    coord_pattern = re.compile(r'\s*(\d+)([XYZ])\s+([-+]?\d*\.\d+)\s+([-+]?\d*\.\d+)')
    coord_header_pattern = re.compile(r'COORDINATE\s+XYZ\s+GRADIENT')
    point_charge_pattern = re.compile(r'POINT CHARGE GRADIENT')
    element_pattern = re.compile(r'\s*([A-Za-z]+)\s+([-+]?\d*\.\d+)\s+([-+]?\d*\.\d+)\s+([-+]?\d*\.\d+)')
    
    print("Starting to read file...")
    line_count = 0
    frame_count = 0
    in_gradient_section = False
    in_coord_section = False
    in_input_geom = False
    current_atom = None
    current_x = None
    current_y = None
    current_z = None
    
    # Dictionary to store atom number to element mapping
    atom_to_element: Dict[int, str] = {}
    
    try:
        with open(filename, 'r') as f:
            for line in f:
                line_count += 1
                if line_count % 100000 == 0:
                    print(f"Processed {line_count} lines...")
                
                # Check for input geometry section
                if input_geom_pattern.search(line):
                    print(f"Found input geometry section at line {line_count}")
                    in_input_geom = True
                    atom_num = 1
                    continue
                
                # Collect element symbols from input geometry
                if in_input_geom:
                    element_match = element_pattern.search(line)
                    if element_match:
                        element = element_match.group(1)
                        atom_to_element[atom_num] = element
                        atom_num += 1
                    elif line.strip() and not line.startswith('--'):  # Empty line or section end
                        in_input_geom = False
                        print(f"Found {len(atom_to_element)} atoms in input geometry")
                    continue
                
                # Check for gradient section start
                if gradient_pattern.search(line):
                    print(f"Found gradient section at line {line_count}")
                    in_gradient_section = True
                    in_coord_section = False
                    frame_count += 1
                    if frame_count % 100 == 0:
                        print(f"Found frame {frame_count}")
                    
                    # If we have coordinates from previous frame, save them
                    if current_coords:
                        coordinates.append(np.array(current_coords))
                        elements.append(current_elements)
                        timesteps.append(frame_count)
                        current_coords = []
                        current_elements = []
                    continue
                
                # Check for coordinate section header
                if in_gradient_section and coord_header_pattern.search(line):
                    print(f"Found coordinate section at line {line_count}")
                    in_coord_section = True
                    continue
                
                # Check for end of coordinate section
                if in_coord_section and point_charge_pattern.search(line):
                    print(f"End of coordinate section at line {line_count}")
                    in_coord_section = False
                    in_gradient_section = False
                    continue
                
                # If we're in coordinate section, look for coordinates
                if in_coord_section:
                    coord_match = coord_pattern.search(line)
                    if coord_match:
                        atom_num = int(coord_match.group(1))
                        coord_type = coord_match.group(2)
                        value = float(coord_match.group(3))
                        
                        if coord_type == 'X':
                            if current_atom is not None and current_x is not None and current_y is not None and current_z is not None:
                                current_coords.append([current_x, current_y, current_z])
                                current_elements.append(atom_to_element.get(current_atom, f"X{current_atom}"))
                            current_atom = atom_num
                            current_x = value
                        elif coord_type == 'Y':
                            current_y = value
                        elif coord_type == 'Z':
                            current_z = value
                            if current_atom is not None and current_x is not None and current_y is not None:
                                current_coords.append([current_x, current_y, current_z])
                                current_elements.append(atom_to_element.get(current_atom, f"X{current_atom}"))
                                current_atom = None
                                current_x = None
                                current_y = None
                                current_z = None
    
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return [], [], []
    
    # Add the last set of coordinates
    if current_coords:
        coordinates.append(np.array(current_coords))
        elements.append(current_elements)
        timesteps.append(frame_count)
    
    print(f"\nSummary:")
    print(f"Total lines processed: {line_count}")
    print(f"Total frames found: {len(timesteps)}")
    if timesteps:
        print(f"First frame: {timesteps[0]}")
        print(f"Last frame: {timesteps[-1]}")
    if coordinates:
        print(f"Number of atoms in first frame: {len(coordinates[0])}")
        print(f"Number of atoms in last frame: {len(coordinates[-1])}")
    
    return timesteps, coordinates, elements

def save_xyz_trajectory(timesteps: List[float], coordinates: List[np.ndarray], elements: List[List[str]], output_file: str):
    """
    Save the extracted trajectory to an XYZ file.
    
    Args:
        timesteps (List[float]): List of timesteps
        coordinates (List[np.ndarray]): List of coordinate arrays
        elements (List[List[str]]): List of element symbols for each timestep
        output_file (str): Path to save the trajectory data
    """
    print(f"\nSaving trajectory to {output_file}...")
    frame_count = 0
    
    with open(output_file, 'w') as f:
        for i, (ts, coords, elems) in enumerate(zip(timesteps, coordinates, elements)):
            frame_count += 1
            if frame_count % 100 == 0:
                print(f"Saved {frame_count} frames...")
            
            # Write number of atoms
            f.write(f"{len(coords)}\n")
            # Write comment line with frame number
            f.write(f"Frame {ts}\n")
            # Write coordinates
            for elem, coord in zip(elems, coords):
                f.write(f"{elem} {coord[0]:12.6f} {coord[1]:12.6f} {coord[2]:12.6f}\n")
    
    print(f"Successfully saved {frame_count} frames to {output_file}")

def main():
    input_file = 'quick_qmmm_solv.out'
    output_file = 'quick_qmmm_solv.xyz'
    
    print(f"Extracting trajectory from {input_file}...")
    timesteps, coordinates, elements = extract_trajectory(input_file)
    
    if not timesteps:
        print("Error: No frames found in the input file!")
        return
    
    print(f"\nFound {len(timesteps)} frames")
    save_xyz_trajectory(timesteps, coordinates, elements, output_file)
    print("Done!")

if __name__ == "__main__":
    main() 