#!/usr/bin/env python3
import numpy as np
import sys

def read_xyz(filename):
    """Reads an .xyz file and returns a list of coordinates as numpy arrays"""
    with open(filename, 'r') as f:
        lines = f.readlines()[2:]  # skip first two lines
        coords = [np.array(list(map(float, line.split()[1:4]))) for line in lines]
    return coords

def calc_dihedral(p0, p1, p2, p3):
    """Calculate dihedral angle in degrees from 4 points"""
    b0 = -1.0 * (p1 - p0)
    b1 = p2 - p1
    b2 = p3 - p2

    b1 /= np.linalg.norm(b1)
    v = b0 - np.dot(b0, b1) * b1
    w = b2 - np.dot(b2, b1) * b1

    x = np.dot(v, w)
    y = np.dot(np.cross(b1, v), w)

    return np.degrees(np.arctan2(y, x))

if __name__ == "__main__":
  if len(sys.argv) < 4:
    print("Error: Insufficient arguments provided.")
    print("Arguments provided:", sys.argv)
    print("Number of arguments:", len(sys.argv))
    print("Usage: python dihedral.py [-q] file.xyz i1 i2 i3 i4")
    print("       python dihedral.py [-q] file.xyz 'i1 i2 i3 i4'")
    print("       (atom indices start from 1)")
    print("       -q: quiet mode, only print angle")
    sys.exit(1)

  quiet = False
  if sys.argv[1] == '-q':
    quiet = True
    xyz_file = sys.argv[2]
    # Check if indices are provided as separate args or single space-separated string
    if len(sys.argv) == 4:
      # Single string with space-separated indices
      idx = [int(i)-1 for i in sys.argv[3].split()]
    else:
      # Separate arguments
      if len(sys.argv) < 7:
        print("Error: Insufficient arguments provided.")
        print("Usage: python dihedral.py [-q] file.xyz i1 i2 i3 i4")
        sys.exit(1)
      idx = [int(i)-1 for i in sys.argv[3:7]]
  else:
    xyz_file = sys.argv[1]
    # Check if indices are provided as separate args or single space-separated string
    if len(sys.argv) == 3:
      # Single string with space-separated indices
      idx = [int(i)-1 for i in sys.argv[2].split()]
    else:
      # Separate arguments
      if len(sys.argv) < 6:
        print("Error: Insufficient arguments provided.")
        print("Usage: python dihedral.py [-q] file.xyz i1 i2 i3 i4")
        sys.exit(1)
      idx = [int(i)-1 for i in sys.argv[2:6]]

  # Validate that we have exactly 4 indices
  if len(idx) != 4:
    print("Error: Exactly 4 atom indices are required.")
    sys.exit(1)

  coords = read_xyz(xyz_file)
  # Check if file exists
  try:
    with open(xyz_file, 'r') as f:
      pass
  except FileNotFoundError:
    print(f"Error: File '{xyz_file}' not found.")
    sys.exit(1)

  # Process coordinates and calculate dihedral
  try:
    angle = calc_dihedral(coords[idx[0]], coords[idx[1]],
          coords[idx[2]], coords[idx[3]])
    if quiet:
      print(f"{angle:.3f}")
    else:
      print(f"Atom 1: {coords[idx[0]][0]:.3f} {coords[idx[0]][1]:.3f} {coords[idx[0]][2]:.3f}")
      print(f"Atom 2: {coords[idx[1]][0]:.3f} {coords[idx[1]][1]:.3f} {coords[idx[1]][2]:.3f}")
      print(f"Atom 3: {coords[idx[2]][0]:.3f} {coords[idx[2]][1]:.3f} {coords[idx[2]][2]:.3f}")
      print(f"Atom 4: {coords[idx[3]][0]:.3f} {coords[idx[3]][1]:.3f} {coords[idx[3]][2]:.3f}")
      print(f"Dihedral angle: {angle:.3f} degrees")
  except IndexError:
    print("Error: Atom index out of range.")
