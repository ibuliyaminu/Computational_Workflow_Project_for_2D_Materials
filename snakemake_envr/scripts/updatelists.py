#!/usr/bin/env python3
"""
This script creates two separate CSV lists for all errored runs and successfully completed runs.

Please run this before check_errored.py and check_completed.py.
"""
import os
import sys
import math
import re
import pandas as pd

# Initialize DataFrames to store various error lists
error_list = pd.DataFrame(columns=["data_files"])
potentialerror_list = pd.DataFrame(columns=["data_files"])
numscf_list = pd.DataFrame(columns=["data_files"])
complete_list = pd.DataFrame(columns=["data_files"])
memory_list = pd.DataFrame(columns=["data_files"])
quotaerror_list = pd.DataFrame(columns=["data_files"])
timeerror_list = pd.DataFrame(columns=["data_files"])
smalldisterror_list = pd.DataFrame(columns=["data_files"])
ongoing_list = pd.DataFrame(columns=["data_files"])
shrinkerror = pd.DataFrame(columns=["data_files"])
linearbs = pd.DataFrame(columns=["data_files"])

# Get a list of files in the working directory
data_files = "/mnt/home/buliyami/Computational_Workflow_Project_for_2D_Materials/snakemake_envr/data2/"

# Loop through each file in the directory
for file_name in data_files:
    # Check if the file has a ".out" extension
    if ".out" in file_name:
        # Open the file and extract submit_name
        files = open(file_name)
        submit_name = file_name.split(".out")[0]
        temp = pd.DataFrame([submit_name], columns=["data_files"])
        i = []

        # Loop through lines in the file
        for i, line in enumerate(files):
            errorss = False
            duplicate = False

            # Check for various completion or error conditions
            if "OPT END" in line or line.startswith(" EEEEEEEEEE TERMINATION"):
                complete_list = pd.concat([complete_list, temp], ignore_index=True)
                duplicate = True
                break
            elif "TOO MANY CYCLES" in line:
                numscf_list = pd.concat([numscf_list, temp], ignore_index=True)
                duplicate = True
                break
            elif "out-of-memory handler" in line:
                memory_list = pd.concat([memory_list, temp], ignore_index=True)
                duplicate = True
                break
            elif "DUE TO TIME LIMIT" in line:
                timeerror_list = pd.concat([timeerror_list, temp], ignore_index=True)
                duplicate = True
                break
            elif "**** NEIGHB ****" in line:
                smalldisterror_list = pd.concat(
                    [smalldisterror_list, temp], ignore_index=True
                )
                duplicate = True
                break
            elif "ANISOTROPIC SHRINKING FACTOR" in line:
                shrinkerror = pd.concat([shrinkerror, temp], ignore_index=True)
                duplicate = True
                break
            elif "BASIS SET LINEARLY DEPENDENT" in line:
                linearbs = pd.concat([linearbs, temp], ignore_index=True)
                duplicate = True
                break
            elif "error" in line and duplicate is False:
                if "error during write" in line:
                    quotaerror_list = pd.concat(
                        [quotaerror_list, temp], ignore_index=True
                    )
                    duplicate = True
                    break
                elif "srun: error: Munge decode failed: Expired credential" in line:
                    potentialerror_list = pd.concat(
                        [potentialerror_list, temp], ignore_index=True
                    )
                    duplicate = True
                    break
                else:
                    errorss = True

        # If the file is not a duplicate, categorize it based on errors or ongoing
        if duplicate is False:
            if errorss is True:
                error_list = pd.concat([error_list, temp], ignore_index=True)
            else:
                ongoing_list = pd.concat([ongoing_list, temp], ignore_index=True)

# Print various error lists and completion message
print("Unknown Errored:\n")
print(error_list)
print("\nK Shrink Error:\n")
print(shrinkerror)
print("\nBasis Sets are Linearly Dep\n")
print(linearbs)
print("\nNot enough SCF cycles:\n")
print(numscf_list)
print("\nMemory Error:\n")
print(memory_list)
print("\nQuota Error:\n")
print(quotaerror_list)
print("\nOut of Time Error:\n")
print(timeerror_list)
print("\nGeometry Error, Distance Too Small:\n")
print(smalldisterror_list)
print("\nPotentially Errored:\n")
print(potentialerror_list)
print("\nCompleted:\n")
print(complete_list)
print("\nCurrently Running:\n")
print(ongoing_list)

# Save error lists to CSV files
complete_list.to_csv("/mnt/home/buliyami/Computational_Workflow_Project_for_2D_Materials/snakemake_envr/result2/completelist.csv", index=False)
error_list.to_csv("/mnt/home/buliyami/Computational_Workflow_Project_for_2D_Materials/snakemake_envr/result2/errorlist.csv", index=False)
#numscf_list.to_csv("numscflist.csv", index=False)
#memory_list.to_csv("memorylist.csv", index=False)
#potentialerror_list.to_csv("perrorlist.csv", index=False)
#quotaerror_list.to_csv("quotaerrorlist.csv", index=False)
#timeerror_list.to_csv("timeerrorlist.csv", index=False)
#smalldisterror_list.to_csv("smalldisterrorlist.csv", index=False)
#ongoing_list.to_csv("currentlyrunning.csv", index=False)
#shrinkerror.to_csv("shrinkerrorlist.csv", index=False)
#linearbs.to_csv("linearbslist.csv", index=False)
