import numpy as np 
from memory_profiler import profile

@profile
def compute_julia_set_vectorized(xmin, xmax, ymin, ymax, im_width, im_height, c):
    zabs_max = 10
    nit_max = 300

    xwidth = xmax - xmin
    yheight = ymax - ymin

    julia = np.empty((im_width, im_height), dtype=np.float32)
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
            julia[ix, iy] = ratio

    return julia