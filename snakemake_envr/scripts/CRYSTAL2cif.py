#!/usr/bin/env python
"""
This script converts the final geometry of CRYSTAL09 output into a CIF file.

Usage: CRYSTAL2cif.py [CRYSTAL09 output] [cif file name]
"""

import os
import sys
import math
import re


def parse_cryout(cryout):
    """
    Parses the CRYSTAL09 output file to extract lattice parameters and atomic positions.

    Args:
        cryout (file): CRYSTAL09 output file.

    Returns:
        tuple: Lattice parameters (a, b, c, alpha, beta, gamma) and atomic positions.
    """
    for line in cryout:
        if re.match(r"^ PRIMITIVE CELL", line):
            next(cryout)  # Skip the line after matching pattern
            # Extract lattice parameters
            [a, b, c, alpha, beta, gamma] = [float(i) for i in next(cryout).split()]
            next(cryout)  # Skip a line
            natoms = int(next(cryout).split()[-1])  # Number of atoms
            next(cryout)  # Skip a line
            next(cryout)  # Skip a line

            # Initialize lists to store atomic information
            atomindex = [0] * natoms
            atomname = ["N/A"] * natoms
            atomx = [1.0] * natoms
            atomy = [1.0] * natoms
            atomz = [1.0] * natoms

            # Loop through atomic positions
            for i in range(natoms):
                atom = next(cryout).split()
                atomindex[i] = int(atom[0])
                atomname_i = str(atom[3])

                # Handle atom names with two characters (uppercase + lowercase)
                if len(atomname_i) == 1:
                    atomname[i] = atomname_i
                elif len(atomname_i) == 2:
                    ABCs = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                    abcs = "abcdefghijklmnopqrstuvwxyz"
                    lowercase = {ABCs[i]: abcs[i] for i in range(len(ABCs))}
                    atomname[i] = atomname_i[0] + lowercase[atomname_i[1]]

                atomx[i] = float(atom[4])
                atomy[i] = float(atom[5])
                atomz[i] = float(atom[6])

    cryout.close()
    return a, b, c, alpha, beta, gamma, natoms, atomindex, atomname, atomx, atomy, atomz


def write_cif(
    cif, a, b, c, alpha, beta, gamma, natoms, atomname, atomindex, atomx, atomy, atomz
):
    """
    Writes CIF file with lattice parameters and atomic positions.

    Args:
        cif (file): CIF file to write.
        a, b, c, alpha, beta, gamma (float): Lattice parameters.
        natoms (int): Number of atoms.
        atomname, atomindex, atomx, atomy, atomz (list): Atomic information.

    Returns:
        None
    """
    print("data_%s" % (str(sys.argv[1])), file=cif)
    print("", file=cif)
    print("_cell_length_a                         %.6f" % (a), file=cif)
    print("_cell_length_b                         %.6f" % (b), file=cif)
    print("_cell_length_c                         %.6f" % (c), file=cif)
    print("_cell_angle_alpha                      %.6f" % (alpha), file=cif)
    print("_cell_angle_beta                       %.6f" % (beta), file=cif)
    print("_cell_angle_gamma                      %.6f" % (gamma), file=cif)
    print("_symmetry_space_group_name_H-M         'P 1'", file=cif)
    print("_symmetry_Int_Tables_number            1", file=cif)
    print("", file=cif)
    print("loop_", file=cif)
    print("_symmetry_equiv_pos_as_xyz", file=cif)
    print("   'x, y, z'", file=cif)
    print("", file=cif)
    print("loop_", file=cif)
    print("   _atom_site_label", file=cif)
    print("   _atom_site_type_symbol", file=cif)
    print("   _atom_site_fract_x", file=cif)
    print("   _atom_site_fract_y", file=cif)
    print("   _atom_site_fract_z", file=cif)

    # Loop through atomic positions and write to CIF file
    for i in range(natoms):
        print(
            "%2s%03d  %2s  %9.6f  %9.6f  %9.6f"
            % (atomname[i], atomindex[i], atomname[i], atomx[i], atomy[i], atomz[i]),
            file=cif,
        )

    cif.close()


# Check if command line arguments are provided
if len(sys.argv) != 3:
    print("Usage: CRYSTAL2cif.py [CRYSTAL17 output] [cif file name]")
    sys.exit(1)

# Open CRYSTAL17 output file and CIF file
cryout = open(sys.argv[1])
cif = open(sys.argv[2], "w")

# Parse CRYSTAL09 output and write to CIF file
(
    a,
    b,
    c,
    alpha,
    beta,
    gamma,
    natoms,
    atomindex,
    atomname,
    atomx,
    atomy,
    atomz,
) = parse_cryout(cryout)
write_cif(
    cif, a, b, c, alpha, beta, gamma, natoms, atomname, atomindex, atomx, atomy, atomz
)

# Print completion message
print("Conversion completed successfully.")
