# efficient_programs_08

This repository contains code that runs julia set which is a way to explore the behavior of complex numbers under a specific mathematical operation.

## Dir Structure

* src.py - entrypoint for runing different versions of julia set
* julia - contains different implementations of julia set algorithm
    * sequential_julia.py
    * parallel_julia.py
    * vectorized_julia.py
    * memory_julia.py
* benchmark - contains shell scripts for benchmarking runtime
    * run_experiment.job
    * run_experiment_parallel.job
* output - output files from julia set and benchmarking scripts
    * image.png
    * *.dat files


## USAGE

### Simple script usage:
``` 
    python src.py --sequential -o output/image.png
    
    python src.py --parallel --nprocs 2 --patch 25 --size 800
```
Outputs:  
```image size, patch size, number of processes, runtime ```

See help to know more about the arguments:

```python src.py --help```    


### Benchmark usage:  

```sh benchmark/run_experiment.job``` 

Outputs:  
```image size, patch size, number of processes, runtime ```   

for each run with different setups