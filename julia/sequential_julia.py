import numpy as np
import tracemalloc

def compute_julia_set_sequential(xmin, xmax, ymin, ymax, im_width, im_height, c):

    zabs_max = 10
    nit_max = 300

    xwidth  = xmax - xmin
    yheight = ymax - ymin
    
    tracemalloc.start() 

    julia = np.zeros((im_width, im_height))
    for ix in range(im_width):
        for iy in range(im_height):
            nit = 0
            # Map pixel position to a point in the complex plane
            z = complex(ix / im_width * xwidth + xmin,
                        iy / im_height * yheight + ymin)
            # Do the iterations
            while abs(z) <= zabs_max and nit < nit_max:
                z = z**2 + c
                nit += 1
            ratio = nit / nit_max
            julia[ix,iy] = ratio

    current, peak = tracemalloc.get_traced_memory()  # Get memory usage
    tracemalloc.stop()  # Stop memory tracing

    print(f"Memory usage: {current / 10**6} MB")
    print(f"Peak memory usage: {peak / 10**6} MB")
    
    return julia