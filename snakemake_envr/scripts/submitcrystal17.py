#!/usr/bin/env python3
"""Script to submit Crystal17 jobs for d12 files in the current working directory."""

import os
import sys
import math
import re
import linecache
import shutil
import itertools

def main():
    """Main function to execute Crystal17 jobs for D12 files."""
    # Set the data_folder to the working directory
    data_folder = "/mnt/home/buliyami/Computational_Workflow_Project_for_2D_Materials/snakemake_envr/data2/" # Change This Directory to d12 Directory

    data_files = os.listdir(data_folder)

    # Loop through each file in the data_folder
    for file_name in data_files:
        # Check if the file is a D12 file
        if ".d12" in file_name:
            # Extract the submit_name from the file name
            submit_name = file_name.split(".d12")[0]

            # Run a system command to submit a Crystal17 job with the specified submit_name and 100 steps
            os.system(data_folder + "/mnt/home/buliyami/Computational_Workflow_Project_for_2D_Materials/snakemake_envr/data2/submitcrystal17.sh " + submit_name + " 100")

if __name__ == "__main__":
    main()
