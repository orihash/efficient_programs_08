import numpy as np 
import tracemalloc

def compute_julia_set_vectorized(xmin, xmax, ymin, ymax, im_width, im_height, c):
    zabs_max = 10
    nit_max = 300

    tracemalloc.start() 

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

    current, peak = tracemalloc.get_traced_memory()  # Get memory usage
    tracemalloc.stop()  # Stop memory tracing

    print(f"Memory usage: {current / 10**6} MB")
    print(f"Peak memory usage: {peak / 10**6} MB")
    
    return julia.T  # Transpose the result for the correct orientation

