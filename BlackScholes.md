# BlackScholes Test

## Summary

Configuration | Time Elapsed
----|----
Julia | 390 msec
Julia (Libm) | 356 msec
Python (Numba) | 517 msec
Python (Numpy) | 772 msec

## Linux - Intel(R) Xeon(R) CPU E5-2699 v4 @ 2.20GHz

```
julia> include("blackscholes.jl")
Average (single-threaded): 390 milliseconds

julia> include("blackscholes.jl")
Average (single-threaded): 391 milliseconds

julia> include("blackscholes_libm.jl")
Average (single-threaded): 363 milliseconds

julia> include("blackscholes_libm.jl")
Average (single-threaded): 356 milliseconds

$ python blackscholes_numba.py
Numpy Time: 772.598004 msec
Numba Time: 517.418265 msec
L1 norm: 0.000000E+00
Max absolute error: 0.000000E+00
```

Versions:
```
julia> versioninfo()
Julia Version 0.6.2
Commit d386e40c17 (2017-12-13 18:08 UTC)
Platform Info:
  OS: Linux (x86_64-pc-linux-gnu)
  CPU: Intel(R) Xeon(R) CPU E5-2699 v4 @ 2.20GHz
  WORD_SIZE: 64
  BLAS: libopenblas (USE64BITINT DYNAMIC_ARCH NO_AFFINITY Haswell)
  LAPACK: libopenblas64_
  LIBM: libopenlibm
  LLVM: libLLVM-3.9.1 (ORCJIT, broadwell)

$ python
Python 3.6.3 |Anaconda, Inc.| (default, Oct 13 2017, 12:02:49)
[GCC 7.2.0] on linux

```
