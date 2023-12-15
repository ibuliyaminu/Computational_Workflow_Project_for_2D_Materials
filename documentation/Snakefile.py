rule all:
    input:
        "result1/WTe2_BULK_OPTGEOM_TZ.d12",
        "result2/completelist.csv",
        "result2/errorlist.csv",
        "data3/WTe2_BULK_OPTGEOM_TZ.cif"

# Rule 1: Converting CIF file to d12 file as needed for the Density Function Theory Calculation using CRYSTAL17 software 
rule create_BULK_d12_from_cif:
    input:
        data_in1="data1/WTe2.cif"
    output:
        data_out1="result1/WTe2_BULK_OPTGEOM_TZ.d12"
    shell:
        "python scripts/create_BULK_d12_from_cif.py {input.data_in1} > {output.data_out1}" "&&"
        "cp {output.data_out1} data2/" "&&"
        "cp scripts/submitcrystal17.sh data2/" "&&"
        "cp scripts/submitcrystal17.py data2/"

# This second step requre me to submit job to HPCC for about 5 days. As discussed in the class, I have 
#submitted this job outside the snakemake and copy the output files back to the snakemake.


#Rule 2: Submit inputfile.d12 to CRYSTAL17 software via HPCC
#rule run_crystal17:
#    input:
#        data_in1="data2/submitcrystal17.sh",
#        data_in2="data2/WTe2_BULK_OPTGEOM_TZ.d12"
#    output:
#        data_out1=multiext ("data2/WTe2_BULK_OPTGEOM_TZ", ".out", ".f9", ".sh", ".o")
#    shell:
#        "python data2/submitcrystal17.py {input.data_in1} {input.data_in2} {output.data_out1}"

# Rule 3: Confirm errors in the output files from the hpcc
rule check_errored_output:
    input:
        "data2/WTe2_BULK_OPTGEOM_TZ.out"
    output:
        "result2/completelist.csv",
        "result2/errorlist.csv"
    shell:
        "python scripts/updatelists.py {input} > {output}"

# Rule 4: Convert the completed output file (.out) to cif file for visualization
rule convert_output_to_cif:
    input:
        "data2/WTe2_BULK_OPTGEOM_TZ.out"
    output:
        "data3/WTe2_BULK_OPTGEOM_TZ.cif"
    shell:
        "python data3/CRYSTAL2cif.py {input} {output}"

# Rule 5: Visualize CIF using external software (Vesta)
# This requres an external software, as discussed in the class, I will also check this outside the snakemake
#and upload it to the git hub.