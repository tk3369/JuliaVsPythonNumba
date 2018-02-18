# Benchmarking Julia vs Numba in Linux & MacOS

## Summary

The speed of execution seems to depend on system architecture.  The following test results show a possible deficiency with Anaconda's distribution on Linux.

OS | CPU | Julia | Python
---|----|----|----
MacOS | Intel(R) Core(TM) i5-4258U CPU @ 2.40GHz | 1.63 | 1.35
Linux | Intel(R) Xeon(R) CPU E5-2676 v3 @ 2.40GHz | 1.48 | 2.51
Linux | Intel(R) Xeon(R) CPU E5-2699 v4 @ 2.20GHz | 1.19 | 2.26

Discussion Reference:
https://discourse.julialang.org/t/a-comparison-of-programming-languages-in-economics/8966/20

## MacOS - Intel(R) Core(TM) i5-4258U CPU @ 2.40GHz

```
$ python RBC.py
2018-02-18 14:03:25.510170
2018-02-18 14:03:39.052123
1.3541088503901846
$ python RBC.py
2018-02-18 14:03:42.437165
2018-02-18 14:03:56.053914
1.3616010329918935

$ julia RBC.jl
2018-02-18T14:05:24.914
2018-02-18T14:05:41.25
1.6336
$ julia RBC.jl
2018-02-18T14:06:11.317
2018-02-18T14:06:27.798
1.6481

julia> versioninfo()
Julia Version 0.6.2
Commit d386e40c17 (2017-12-13 18:08 UTC)
Platform Info:
  OS: macOS (x86_64-apple-darwin14.5.0)
  CPU: Intel(R) Core(TM) i5-4258U CPU @ 2.40GHz
  WORD_SIZE: 64
  BLAS: libopenblas (USE64BITINT DYNAMIC_ARCH NO_AFFINITY Haswell)
  LAPACK: libopenblas64_
  LIBM: libopenlibm
  LLVM: libLLVM-3.9.1 (ORCJIT, haswell)

$ python
Python 3.6.3 |Anaconda, Inc.| (default, Oct  6 2017, 12:04:38) 
[GCC 4.2.1 Compatible Clang 4.0.1 (tags/RELEASE_401/final)] on darwin
```

## Linux - Intel(R) Xeon(R) CPU E5-2676 v3 @ 2.40GHz

```
$ python RBC.py
2018-02-18 21:59:17.122873
2018-02-18 21:59:42.218257
2.509495749697089
$ python RBC.py
2018-02-18 21:59:53.343028
2018-02-18 22:00:18.490104
2.5146646585315464

$ julia RBC.jl
2018-02-18T22:00:24.259
2018-02-18T22:00:39.091
1.4832
$ julia RBC.jl
2018-02-18T22:00:52.373
2018-02-18T22:01:07.212
1.4839

julia> versioninfo()
Julia Version 0.6.2
Commit d386e40c17 (2017-12-13 18:08 UTC)
Platform Info:
  OS: Linux (x86_64-pc-linux-gnu)
  CPU: Intel(R) Xeon(R) CPU E5-2676 v3 @ 2.40GHz
  WORD_SIZE: 64
  BLAS: libopenblas (USE64BITINT DYNAMIC_ARCH NO_AFFINITY Haswell)
  LAPACK: libopenblas64_
  LIBM: libopenlibm
  LVM: libLLVM-3.9.1 (ORCJIT, haswell)
  
$ python
Python 3.6.3 |Anaconda, Inc.| (default, Oct 13 2017, 12:02:49) 
[GCC 7.2.0] on linux
```

## Linux - Intel(R) Xeon(R) CPU E5-2699 v4 @ 2.20GHz

```
$ julia RBC.jl
2018-02-18T14:24:05.486
2018-02-18T14:24:17.395
1.1909
$ julia RBC.jl
2018-02-18T14:24:24.079
2018-02-18T14:24:36.011
1.1932

$ python RBC.py
2018-02-18 14:25:27.390147
2018-02-18 14:25:49.983965
2.2593497129157187
$ python RBC.py
2018-02-18 14:25:57.602881
2018-02-18 14:26:21.048854
2.344556374568492

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
