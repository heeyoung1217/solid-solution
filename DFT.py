from ase.io import read

atoms = read('yourfile.cif')

from gpaw import GPAW, PW
calc = GPAW(mode=PW(300), xc='PBE', txt='yourfile.txt')  # Setup calculator
atoms.set_calculator(calc)
energy = atoms.get_potential_energy()  # Single-point energy calculation