import numpy as np 
from memory_profiler import profile

def compute_julia_set_vectorized(xmin, xmax, ymin, ymax, im_width, im_height, c):
    zabs_max = 10
    nit_max = 300

    x = np.linspace(xmin, xmax, im_width)
    y = np.linspace(ymin, ymax, im_height)

    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y  # Create a complex grid

    julia = np.zeros_like(Z, dtype=float)

    for nit in range(nit_max):
        mask = np.abs(Z) <= zabs_max
        Z[mask] = Z[mask]**2 + c
        julia += mask.astype(float)

    julia /= nit_max
    return julia.T  # Transpose the result for the correct orientation

