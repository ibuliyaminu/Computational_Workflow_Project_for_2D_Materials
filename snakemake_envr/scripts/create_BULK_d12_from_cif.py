#Import the required libraries
import ase.io
import numpy as np
import math as m
import glob
import os

def basis(num, basisset):
    """
    Returns the basis set information for a given element number and basis set type.

    Args:
        num (int): Element number.
        basisset (str): Basis set type ("DZ" for Double Zeta or "TZ" for Triple Zeta).

    Returns:
        str: Basis set information for the specified element and basis set type.
    """
    if basisset == "DZ":
        # Change This Directory to Double Zeta Basis Set Directory
        dir_bas = "/mnt/home/buliyami/bin/code/full.basis.doublezeta/"
    elif basisset == "TZ":
        # Change This Directory to Triple Zeta Basis Set Directory
        dir_bas = "/mnt/home/buliyami/bin/code/full.basis.triplezeta/"
    else:
        print("ERROR Improper Basis Set")
    f = open(dir_bas + str(num))
    bs = f.read()
    f.close()
    return bs


def unique(lst):
    """
    Returns a list with unique elements, preserving the order of the original list.

    Args:
        lst (list): Input list.

    Returns:
        list: List with unique elements.
    """
    x = []
    for a in lst:
        if a not in x:
            x.append(a)
    x.sort()
    return x


def CIF2D12(material, struc, path, opt, basisset, OUTPUT_DIR):
    """
    Converts a CIF file to a D12 file with specific parameters.

    Args:
        material (str): CIF file name.
        struc (str): Structure type ("SLAB" or "BULK").
        path (str): Directory path for CIF files.
        opt (str): Optimization type ("SP", "OPT", or "OPTGEOM").
        basisset (str): Basis set type ("DZ" for Double Zeta or "TZ" for Triple Zeta).

    Returns:
        None
    """
    mat = ase.io.read(os.path.join(path, material), format="cif")
    title = material[:-4]
    output = os.path.join(
        OUTPUT_DIR, title + "_" + struc + "_" + opt + "_" + basisset + ".d12"
    )
    with open(output, "w") as f:
        # GET LATTICE PARAMETERS
        u = mat.get_cell()
        u1 = np.asarray(u[0])
        u2 = np.asarray(u[1])
        u3 = np.asarray(u[2])
        a = np.sqrt(u1.dot(u1))
        b = np.sqrt(u2.dot(u2))
        c = np.sqrt(u3.dot(u3))
        u2u3 = u2.dot(u3)
        u3u1 = u3.dot(u1)
        u1u2 = u1.dot(u2)
        alpha = m.acos(u2u3 / (b * c)) * 180 / m.pi
        beta = m.acos(u3u1 / (c * a)) * 180 / m.pi
        gamma = m.acos(u1u2 / (a * b)) * 180 / m.pi

        # GET ATOM POSITIONS
        frac = mat.get_scaled_positions()
        cart = mat.get_positions()
        an = mat.get_atomic_numbers()
        name = mat.get_chemical_symbols()

        ATOMS = len(an)
        sg_2d = 1
        sg_bk = 1
        print(title, file=f)
        if struc == "SLAB":
            print("SLAB", file=f)
            print(str(sg_2d), file=f)

            print("%-8.6f   %-8.6f  %-6.4f" % (a, b, gamma), file=f)
            print(str(ATOMS), file=f)
        if struc == "BULK":
            print("CRYSTAL\n0 0 0", file=f)
            print(str(sg_bk), file=f)

            print(
                "%-8.6f   %-8.6f  %-8.6f  %-6.4f  %-6.4f  %-6.4f"
                % (a, b, c, alpha, beta, gamma),
                file=f,
            )
            print(str(ATOMS), file=f)

        ECPs = [37, 38, 39, 40, 41, 42]  # full.basis
        for i in range(0, ATOMS):
            if (an[i] in ECPs) or (an[i] > 43):
                # Use ELECTRON CORE POTENTIALS
                an[i] += 200
            hi = frac[i][0]
            ki = frac[i][1]
            li = frac[i][2]
            zi = cart[i][2]
            if struc == "BULK":
                print(
                    "%-3d %-8.6f  %-8.6f  %-9.6f  Biso    1.000000    %s "
                    % (an[i], hi, ki, li, name[i]),
                    file=f,
                )
            if struc == "SLAB":
                if zi > 2.0 * c:
                    zi = zi - 3.0 * c
                print(
                    "%-3d %-8.6f  %-8.6f  %-9.6f  Biso    1.000000    %s "
                    % (an[i], hi, ki, zi, name[i]),
                    file=f,
                )

        if opt == "SP":
            OPT = "END"
        elif opt == "OPT":
            OPT = "OPT\nCVOLOPT\nMAXCYCLE\n800\nENDOPT\nEND"
        elif opt == "OPTGEOM":
            OPT = "OPTGEOM\nFULLOPTG\nMAXCYCLE\n800\nENDOPT\nEND"

        print(OPT, file=f)
        # WRITE INPUT DECK
        # BASIS SETS
        # DETERMINE UNIQUE ELEMENTS
        ele = unique(an)
        # Include the Basis Sets for Each element
        for i in ele:
            if struc == "BULK":
                print(basis(i, basisset), end="", file=f)
            elif struc == "SLAB":
                print(basis(i, basisset), end="", file=f)
            else:
                print("ERROR Improper Structure type input")

        ks = [2, 3, 4, 6, 10, 12, 15, 30]
        FM = 30  # FM Mixing

        ka = kb = kc = 1
        for k in ks:
            if k * a > 40.0 and k * a < 75.0 and ka == 1:
                ka = k
            if k * b > 40.0 and k * b < 75.0 and kb == 1:
                kb = k
            if k * c > 40.0 and k * c < 75.0 and kc == 1:
                kc = k
            if sg_bk != 1:
                ka = kb = kc = 20

        if ka == 0 or kb == 0 or kc == 0:
            print("ERROR:", ka, kb, kc)
        k_max = max([ka, kb, kc])
        nShrink = k_max * 2
        if struc == "BULK":
            TAIL = (
                "99 0\nEND\nDFT\nSPIN\nHSE06-D3\nXLGRID\nEND\nTOLINTEG\n7 7 7 9 30\nTOLDEE\n7\nSHRINK\n0 %d\n %d %d %d\nSCFDIR\nBIPOSIZE\n110000000\nEXCHSIZE\n110000000\nMAXCYCLE\n800\nFMIXING\n%d\nDIIS\nPPAN\nEND"
                % (nShrink, ka, kb, kc, FM)
            )
        if struc == "SLAB":
            TAIL = (
                "99 0\nEND\nDFT\nSPIN\nHSE06-D3\nXLGRID\nEND\nTOLINTEG\n7 7 7 9 30\nTOLDEE\n7\nSHRINK\n0 %d\n %d %d 1\nSCFDIR\nBIPOSIZE\n110000000\nEXCHSIZE\n110000000\nMAXCYCLE\n800\nFMIXING\n%d\nDIIS\nPPAN\nEND"
                % (nShrink, ka, kb, FM)
            )
        print(TAIL, file=f)
    return


# Set the directory for CIF and d12 files
DIR = "/mnt/home/buliyami/Computational_Workflow_Project_for_2D_Materials/snakemake_envr/data/"  # Change This Directory to CIF Directory
OUTPUT_DIR = "/mnt/home/buliyami/Computational_Workflow_Project_for_2D_Materials/snakemake_envr/result1/" # Change This Directory to d12 Directory

pathlist = glob.glob(DIR + "*.cif")
nDIR = len(DIR)
ntype = len(".cif")

# Get user input for calculation options (I have defined values for )
options1 = 2
options2 = 4
options3 = 6

material = ""
for path in pathlist:
    option1 = options1
    option2 = options2
    option3 = options3
    path_in_str = str(path)
    material = path_in_str[nDIR:]
    if material == "":
        break
    if option1 == 0:
        option1 = "SP"
    elif option1 == 1:
        option1 = "OPT"
    elif option1 == 2:
        option1 = "OPTGEOM"
    else:
        print("Invalid Input for Option 1. Try again.")
        break
    if option2 == 3:
        option2 = "SLAB"
    elif option2 == 4:
        option2 = "BULK"
    else:
        print("Invalid Input for Option 2. Try again.")
        break
    if option3 == 5:
        option3 = "DZ"
    elif option3 == 6:
        option3 = "TZ"
    else:
        print("Invalid Input for Option 3. Try again.")
        break
    CIF2D12(material, option2, DIR, option1, option3, OUTPUT_DIR)
