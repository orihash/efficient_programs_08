import argparse
import time
import numpy as np
from sequential_julia import compute_julia_set_sequential
from vectorized_julia import compute_julia_set_vectorized
from parallel_julia import compute_julia_in_parallel

BENCHMARK_C = complex(-0.2, -0.65)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--size", help="image size in pixels (square images)", type=int, default=500)
    parser.add_argument("--xmin", help="", type=float, default=-1.5)
    parser.add_argument("--xmax", help="", type=float, default=1.5)
    parser.add_argument("--ymin", help="", type=float, default=-1.5)
    parser.add_argument("--ymax", help="", type=float, default=1.5)
    parser.add_argument("--group-size", help="", type=int, default=None)
    parser.add_argument("--group-number", help="", type=int, default=None)
    parser.add_argument("--patch", help="patch size in pixels (square images)", type=int, default=20)
    parser.add_argument("--nprocs", help="number of workers", type=int, default=1)
    parser.add_argument("--draw-axes", help="Whether to draw axes", action="store_true")
    parser.add_argument("-o", help="output file")
    parser.add_argument("--benchmark", help="Whether to execute the script with the benchmark Julia set", action="store_true")
    parser.add_argument("--sequential", help="set this flag to true to run the sequential program")
    parser.add_argument("--parallel", help="set this flag to true to run the parallel program")
    parser.add_argument("--vectorized", help="set this flag to true to run the vectorized program")
    args = parser.parse_args()

    #print(args)
    # if args.group_size is not None:
    #     GROUP_SIZE = args.group_size
    # if args.group_number is not None:
    #     GROUP_NUMBER = args.group_number

    # # assign c based on mode
    c = None
    if args.benchmark:
        c = BENCHMARK_C 
    # else:
    #     c = c_from_group(GROUP_SIZE, GROUP_NUMBER) 

    stime = time.perf_counter()
    if args.sequential:
            julia_img = compute_julia_set_sequential(args.xmin, args.xmax, args.ymin, args.ymax, args.size, args.size, c)
    elif args.parallel:
        julia_img = compute_julia_in_parallel(
            args.size,
            args.xmin, args.xmax, 
            args.ymin, args.ymax, 
            args.patch,
            args.nprocs,
            c)
    elif args.vectorized:
        julia_img = compute_julia_set_vectorized(args.xmin, args.xmax, args.ymin, args.ymax, args.size, args.size, c)
    rtime = time.perf_counter() - stime

    print(f"{args.size},{args.patch},{args.nprocs},{rtime}")

    if not args.o is None:
        import matplotlib
        matplotlib.use('agg')
        import matplotlib.pyplot as plt
        import matplotlib.cm as cm
        fig, ax = plt.subplots()
        ax.imshow(julia_img, interpolation='nearest', cmap=plt.get_cmap("hot"))

        if args.draw_axes:
            # set labels correctly
            im_width = args.size
            im_height = args.size
            xmin = args.xmin
            xmax = args.xmax
            xwidth = args.xmax - args.xmin
            ymin = args.ymin
            ymax = args.ymax
            yheight = args.ymax - args.ymin

            xtick_labels = np.linspace(xmin, xmax, 7)
            ax.set_xticks([(x-xmin) / xwidth * im_width for x in xtick_labels])
            ax.set_xticklabels(['{:.1f}'.format(xtick) for xtick in xtick_labels])
            ytick_labels = np.linspace(ymin, ymax, 7)
            ax.set_yticks([(y-ymin) / yheight * im_height for y in ytick_labels])
            ax.set_yticklabels(['{:.1f}'.format(-ytick) for ytick in ytick_labels])
            ax.set_xlabel("Imag")
            ax.set_ylabel("Real")
        else:
            # disable axes
            ax.axis("off") 

        plt.tight_layout()
        plt.savefig(args.o, bbox_inches='tight')
        #plt.show()