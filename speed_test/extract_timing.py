#!/usr/bin/env python3
import argparse
import os
import re
import sys
import pandas as pd
# Add the path to import utils from exptree
sys.path.append(os.path.expanduser("~/JR/soft/exptree"))
from utils import modify_yamls_by_func, read_notes_yaml
def parse_mdinfo(filename):
    """Parse mdinfo file to extract NSTEP and Elapsed time"""
    nstep_str = None
    elapsed_s_str = None
    with open(filename, 'r') as f:
        lines = f.readlines()
        
        # Extract NSTEP from the first line
        if lines:
            nstep_match = re.search(r'NSTEP\s*=\s*(\d+)', lines[1])
            if nstep_match:
                nstep_str = nstep_match.group(1).strip()
            else:
                raise ValueError(f"NSTEP is not found in {filename}")
        
        # Find the Elapsed time after "Average timings for all steps:"
        for i, line in enumerate(lines):
            if "Average timings for all steps:" in line:
                # The elapsed time should be in the next line
                if i+1 < len(lines):
                    elapsed_s_match = re.search(r'Elapsed\(s\)\s*=\s*(\d+\.\d+)', lines[i+1])
                    if elapsed_s_match:
                        elapsed_s_str = elapsed_s_match.group(1).strip()
                    else:
                        raise ValueError(f"Elapsed time is not found in {filename}")

                break

    return nstep_str, elapsed_s_str

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Extract timing information from mdinfo files')
    parser.add_argument('--write', action='store_true', help='Write changes to files (default: preview only)')
    args = parser.parse_args()

    def modify_df(df: pd.DataFrame):
        for index,row in df.iterrows():
            mdinfo_path = os.path.join(row['id'], "mdinfo")
            yaml_path = os.path.join(row['id'], "notes.yaml")
            nstep_str, elapsed_s_str = parse_mdinfo(mdinfo_path)
            yaml_data = read_notes_yaml(yaml_path)
            df.loc[index, 'nstep'] = nstep_str
            df.loc[index, 'elapsed_s'] = elapsed_s_str
            df.loc[index, 'sec_per_step'] = str(float(elapsed_s_str)/int(nstep_str))
            assert 'timestep_fs' in yaml_data.keys(), f"timestep_fs is not found in {yaml_path}"
            timestep_fs=float(yaml_data['timestep_fs'])
            df.loc[index, 'days_per_100ps'] = str(float(elapsed_s_str)/int(nstep_str)/timestep_fs/60/60/24*1e5)
        return df
    modify_yamls_by_func(modify_df,check_template=False,write=args.write)

if __name__ == "__main__":
    main() 