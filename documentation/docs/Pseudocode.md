## I am using the materials from the Lab external drive in this project

# Step 1: Getting CIF Material

Firstly, I am getting the base materials from the Lab drive

def retrieve_matereial(material_name, lab_external_drive path, local_storage_path):

    CIF_material = retrieve_matereial_path(material_name, lab_external_drive path, local_storage_path) #Implementation of the path for the materials
    return CIF_material

# Step 2: Convert CIF to d12 Input format

In order to run the density functional theory calculation, a d12 file is required, so I am trying to convert the cif file to d12 file.

def CIF2D12(CIF_material, structure, path, opt, bassiset, OUTPUT_DIR):

    inputfile_d12 = CIF2D12_format(material, structure, path, opt, bassiset, OUTPUT_DIR)   # set a convert_to_d12_format function
    return inputfile_d12

# Step 3: Perform Density Functional Theory (DFT) Calculations (optimization) using CRYSTAL17 software on HPCC

Here I am submitting the calculation on HPCC for DFT calculation
def submitcrystal17_calculations(inputfile_d12):

    DFT_outputs = submitcrystal17_on_HPCC(inputfile_d12)  #implementing the DFT calculation function
    return DFT_outputs

# Step 4: Separate Errored ones from Optimized ones

Checking for errors in the calculation

def updatelist_errored_and_optimized(DFT_outputs):

    # Initialize lists to store errored and optimized outputs/results
    errored_outputs = []
    optimized_outputs = []

# Define a function to check if a result is errored or uptimized

def is_errored(output):

    # Loop through DFT outputs and separate them based on a condition
    for output in DFT_outputs:
        if is_errored(output):
            errored_outputs.append(output)
        else:
            optimized_outputs.append(output)

    return errored_outputs, optimized_outputs

# Step 5: Convert Optimized Outputs to CIF (only for structural vizualization)

def write_cif(optimized_outputs): # Conversion function of optimized results to CIF format

    CIF_optimized = write_cif_format(optimized_outputs)  # Implementation of the CIF conversion
    return CIF_optimized

# Step 6: Visualization using Relevant Software (e.g., Vesta)

def visualize_optimized_structure(CIF_optimized):

    # Implementation for visualizing the optimized structure using software like Vesta
    visualize_structure(CIF_optimized)  # Implementing the visualization function

# Step 7: Save Optimized Structures (END)

def save_optimized_structures(CIF_optimized):

    # Implementation to save the optimized structures to a storage location
    save_structures(optimized_structure)  # Implementing the saving function
