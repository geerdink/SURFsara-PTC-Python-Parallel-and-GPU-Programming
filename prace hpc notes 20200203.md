# PRACE HPC Parallel and GPU Programming in Python
# 3-2-2020
===============================

login: ptc008

SURF: sara, net, market

PRACE = partnership for advanced computing in europe
www.prace-ri.eu
non-profit organization, Brussels
training centers in spain, finland, czech, ...

# Introduction to shared memory programming ##

Damian Podareanu
damian@surfsara.nl

Memory hierarchy of computers: pyramid, see wikipedia

parallel systems vs distributed systems:
in parallel systems memory is shared, in distributed systems memory is dedicated for a program.
parallel: mainly scientific. distributed: for scaling.

Dennard scaling: moore's law is over -> after 2005 the only option is to increase the number of cores.

concurrency: pool of _different_ tasks that happen at the same time.
parallelism: execution of the _same_ task on multiple processors.

pipeline: one of the most useful mechanisms to get hardware efficiency.
pre-processing, post-processing

Flynn's taxonomy of computing:
- SISD: traditional, single instruction on one data memory
- SIMD: one instruction operates on many data memories
- MIMD: much more complex, instruction steams, data streams
- MISD: not common, multiple processing units operate on one (shared) data memory

Definition:
one core = one processor

parallelism: one task, many CPUs
sequential: one task, one thread, one step per time
concurrent: multiple tasks can be eecuted at one time. each task is specialized.

GO language: famous for parallel programming. GOphers by Rob Pike
example: burning books :)

time slicing

*interleaving*: the illusion of simulataneous processing through rapid swapping of task contexts, using 1 CPU --> e.g. many users on one website.
*multiprocessing*: using multiple CPUs to execute multiple tasks simulataneously.
*multitasking*: a single user executes multiple tasks on the same time. used to be rare, but now common in laptops and phones.
*multithreading*: time slicing between threads, to allow a single process running concurrently
Threads: the OS maps software threads to hardware threads (harts)

pipelines: not covered in this course.

Amdahl's law: there is a limit to how much we can gain from parallel processing.
rule of thumb: 80% efficiency is good.

Python is not thread safe -> a thread can look into data of another thread.
= Global Interpreter Lock
in a way, Python shares resources already. threading does not help much, since the default behavior is already similar.

*Daemon* threads: non-blocking thread, for example heart beat or folder monitor. 
Pass daemon=True when constructing a thread, or call set_daemon(True) on existing thread.
To wait for a daemon thread to complete, use join().

from Python 3.2: concurrent futures.
another option: async IO

# Numba and Cython

Python is not fast, it's mediocre for tasks like string processing. Fastest are C and Perl.
To speed it up, Cython and Numba were developed.
Cython is a compiler. It is Python with C data types.
Numba is a numpy-aware compiler. It 'just in time' compiles Python code into machine code.

## Numba
Decorators in Python are actually before-function-calls.
Important in parallel programming because they offer a form of 

A decorator @numba.jit is used to define functions. -> this alone does not speed up much.
To optimize further, the types of the function have to be declared, e.g: @numba.jit(float64(float64, int32)) -> this gives a significant speed-up

## Cython
Create a .pyx file
Create setup.py (Python's makefile) with function in it: cythonize("myfile.pyx")
python setup.py build_ext -inplace --> genaretes .so file

Cython enforces static typing.

use _cdef_ statement to declare C variables, struct, enum, ...
e.g. cdef int i

to time things in Python: timeit.timeit(...)

## OpenMP
Used to parellize loops
in C: #pragma omp parallel for --> one line to parellize a loop
To get in full control of your parallelism, don't use Python but use C.

# Exercises

use pip install package_name --user

cProfile: decorate a function with some intermediate code, then call the actual function.
def do_profile(func):
    def wrapper(*args, *kwargs)

Runsnake: https://github.com/mcfletch/runsnakerun 

from inspect import getsourcelines

d = threading.Thread(name='daemon', target=daemon, daemon=True)
d = threading.Thread(name='non-daemon', target=non_daemon)

preferred pythonic way of threading: concurrent futures. give a lot of control.

limitations of numba: in many cases, numpy and/or scipy are even faster. they are highly optimized libraries.
so if it's available, use the standard functions.
if no standard libraries are available, for example mandelbrot, and calculations are expensive, numba is much faster than standard Python.

# Introduction in MPI using MPI4PY (for distributed memory processing)

Lykle Voort
lykle.voort@surfsara.nl

Cartesius: supercomputer with 47000 cores. 1800 computers.

Python: not best for HPC, but illustrates code in a nice way.
Focus on concepts rather than details (core dumps, pointers, ...)

MPI = messsage passing interface
is a standard, not a library. a way to communicate between processes.
common implementations: OpenMPI, MPICH, ...

MPI in practice:
work distributions for monte carlo simulations
e.g. weather models
now also: machine learning.

MPI is for problems that can be split.
interfaces communicate states or partial results.

All communication is done through communicators. Like a radio channel where a group can communicate.
A communicator always has a _size_. Each processes within the group (communicator) has an unique _rank_.
There is always a global communicator: MPI.COMM_WORLD

All ranks (= processes) in a communicator must call collective calls. (the same function call)
Calls are *blocking*. It will wait until all calls have completed within a communicator.
e.g. broadcast: send data (array) to other ranks
    data = comm.bcast(data)
e.g. scatter: distribute data (array) over other ranks 
    data = comm.scatter(data)
    ! the number of ranks has to match the number of elements, else there will be an error
e.g. gather: combine data of ranks into one array
    mydata = comm.rank
    data = comm.gather(mydata)
e.g. allgather: combine data of ranks into one array, then copy it to all ranks
e.g. reduction (sum/max/product/...): combine data of ranks into one value
    example: calculate pi by counting points in a quarter circle.

for bcase and scatter there is an implicit argument: the number of the root node, default = 0

## Point-to-point communication
send data to other rank, e.g. with higher ID. sending requires an explicit destination. receiving _may_ specify a source. both can use _tags_ for verifying content consistency. 
    comm.send(obj, int dest, int tag=0)
    obj = comm.recv(buf=None, int source=ANY_SOURCE, int tag=ANY_TAG, Status status=None)
send() and recv() are _blocking_ (in theory).
    send waits for confirmation
    recv waits for a message to come in
    therefore, in theory Bob and Alice in mpi-task7b should never be able to send each other messages.

## Non-blocking communication
non-blocking is asynchronous

principle:
0. instead of send(), use isend()
0. use status.wait() to receive

## ...
send vs Send: 
in Python, normally a function argument cannot be modified. the MPI standard _can_ do this, so there has to a Python solution for that. That solution is the Send method with capital S. Downside is that it can only accept predefined MPI argument types.
Benefits of Send vs send: faster, good for numpy arrays.

# 4-2-2020
===============================

PyCuda basics

running on Lisa; https://jupyter2.lisa.surfsara.nl/

Python 3.6.6 

from pycuda import gpuarray

The CUDA _kernel_ is the elementary function of parallelization. It features an extended C syntax and is the unit of computation that runs in parallel on the thousands of cores that compose a GPU. The kernel can be of one of the following tyes.
- global - denotes general CUDA kernel. These functions are called from the host
- device - represents a device (GPU) function. - These functions can be called either from device or global
- host - represents a host (CPU) function.

## Parallelizatino
Each time a kernel is called it is necessary to give it a thread distribution (or threads) which are organized in blocks (blocks) and these in turn in a grid (these can have different dimensions: 1D, 2D, 3D). These threads are copies of the kernel and each is a process to be carried out on the GPU cores, i.e. if we launch a grid with 5 blocks (gridDim = (5,1,1)) with 10 threads per block (blockDim = (10,1,1)), then we will have launched 50 tasks in parallel. Although the kernels to be executed by the threads are copies of the one that we originally wrote, the differentiation is given by the assignment of a counter to each process. The usual way to determine this ** global process index ** is exemplified below:

## PyCUDA
This Python library lets you access Nvidia‘s CUDA parallel computation API from Python. It allows us in principle to do everything we can do with CUDA C, but in a simpler way. One of the virtues of PyCUDA is that is allows us to use the class GPUArray, which in turn allows us to easily manage memory, assign of values, perform data transfer between CPU and GPU, etc. This class of pyCUDA maintains the same structure as the numpy library, giving developers the same feel as they were using numpy.

After initializing the context of pyCUDA we can make use of the class GPUArray. The simplest way to generate an array in the global memory of the GPU is through gpuarray.togpu (), where the value that is passed to the function is a numpy array. Although all GPU global memory arrays are linear arrays, the GPUArray class handles the possibility of preserving array dimensions.

