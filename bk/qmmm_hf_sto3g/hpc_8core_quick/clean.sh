#!/bin/bash

# Find all files in current directory
files=$(find . -maxdepth 1 -type f)

# Keep only specified files and remove the rest
for file in $files; do
    case "$file" in
        ./*.sh|./orc_job.tpl|./qmmm.in|./qmmm_hf.rst|./ZnMim2.prmtop|./convert.in)
            # Keep these files
            echo "Keeping file: $file"
            ;;
        *)
            # Remove everything else
            echo "Removing file: $file"
            rm -f "$file"
            ;;
    esac
done
