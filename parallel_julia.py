from multiprocessing import Pool
import numpy as np
from memory_profiler import profile

@profile
def compute_julia_in_parallel(size, xmin, xmax, ymin, ymax, patch, nprocs, c):
    task_list = []
    for x in range(0, size, patch):
        if x + patch < size:
            for y in range(0, size, patch):
                if y + patch > size:
                    y = size - y
                task_list.append((x, y, patch, xmin, xmax, ymin, ymax, c, size))              
        else: 
            x = size - x 
            for y in range(0, size, patch):
                if y + patch > size:
                    y = size - y
                task_list.append((x, y, patch, xmin, xmax, ymin, ymax, c, size))

    pool = Pool(processes=nprocs)
    results = pool.map(compute_patch, task_list, chunksize=1)
    pool.close()
    pool.join()
    julia_img = np.zeros((size, size))
    for result in results:
        x, y, patch_img = result
        julia_img[x:x+patch, y:y+patch] = patch_img
        
    return julia_img


def compute_patch(args):
    x, y, patch, xmin, xmax, ymin, ymax, c, size = args
    patch_img = np.zeros((patch, patch))
    for i in range(patch):
        for j in range(patch):
            px = x + i
            py = y + j
            z = complex(px / size * (xmax-xmin) + xmin,
                        py / size * (ymax-ymin) + ymin)
            zabs_max = 10
            nit_max = 300
            nit = 0
            while abs(z) <= zabs_max and nit < nit_max:
                z = z**2 + c
                nit += 1
            ratio = nit / nit_max
            patch_img[i, j] = ratio
    return x, y, patch_img
