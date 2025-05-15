#!/usr/bin/env python3
import os
import re
import sys
import shutil
from ruamel.yaml import YAML

def extract_ep_tot(file_path):
    """Extract all EPtot values from qmmm.out file."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            # Find all lines containing EPtot
            matches = re.finditer(r'EPtot\s+=\s+([-\d.]+)', content)
            values = [float(match.group(1)) for match in matches]
            return values if values else None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return None

def main():
    # Parse command line arguments
    if len(sys.argv) <= 1:
        print("Error: No directories specified")
        print(f"Usage: python3 {os.path.basename(__file__)} [--write] <directory1> [directory2 ...]")
        sys.exit(1)
    
    # Check for --write option
    write_mode = False
    if '--write' in sys.argv:
        write_mode = True
        sys.argv.remove('--write')
    
    # Get directories from remaining arguments
    run_dirs = sys.argv[1:]
    
    # Initialize YAML parser
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=2, offset=0)
    
    for run_dir in run_dirs:
        if not os.path.isdir(run_dir):
            print(f"Warning: {run_dir} is not a directory")
            continue
            
        qmmm_out = os.path.join(run_dir, 'qmmm.out')
        notes_yaml = os.path.join(run_dir, 'notes.yaml')
        
        if not os.path.exists(qmmm_out):
            print(f"Warning: {qmmm_out} not found")
            continue
            
        # Extract EPtot values
        ep_tots = extract_ep_tot(qmmm_out)
        if ep_tots is None:
            print(f"Warning: Could not extract EPtot from {qmmm_out}")
            continue
            
        # Print EPtot values
        print(f"\n{run_dir}:")
        print(f"Found {len(ep_tots)} EPtot values:")
        for i, value in enumerate(ep_tots, 1):
            print(f"  {i:2d}: {value:15.4f}")
        
        # If write mode is enabled, update notes.yaml
        if write_mode:
            # Backup existing notes.yaml if it exists
            if os.path.exists(notes_yaml):
                backup_yaml = notes_yaml + '.bk'
                try:
                    shutil.copy2(notes_yaml, backup_yaml)
                    print(f"Backed up {notes_yaml} to {backup_yaml}")
                except Exception as e:
                    print(f"Warning: Could not backup {notes_yaml}: {e}")
                    continue
            
            # Read existing notes.yaml if it exists
            notes = {}
            if os.path.exists(notes_yaml):
                try:
                    with open(notes_yaml, 'r') as f:
                        notes = yaml.load(f) or {}
                except Exception as e:
                    print(f"Warning: Error reading {notes_yaml}: {e}")
            
            notes['EPtot'] = ep_tots
            
            # Write updated notes.yaml
            try:
                with open(notes_yaml, 'w') as f:
                    yaml.dump(notes, f)
                print(f"Updated {notes_yaml} with {len(ep_tots)} EPtot values")
            except Exception as e:
                print(f"Error writing to {notes_yaml}: {e}")
    if not write_mode:
        print("\n" + "="*80)
        print("This is a preview mode. No changes have been written to the yaml files.")
        print("To apply these changes, run the command with --write flag:")
        print("="*80)
if __name__ == '__main__':
    main() 