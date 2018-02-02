# Force Sense of Security?

Perhaps a common misconception for any newbie is to assume that Python Numba will 
make _everything_ super-fast with a simple `@jit` decorator.  This page demonstrate how
it may not work and instead just make things worse.

The case study here is a simple string concatenation function.  Consider the following code, one 
jitted and another not. 

```python
@jit
def foo(x, y):
    return x + y
    
def bar(x, y):
    return x + y
```

Let's define a simple function that runs these functions repeatedly:

```python
def bmk(f, n, *args):
    for i in range(0,n):
        f(*args)
```

Running `foo` function the first time gives a nice warning about type inference.  
This would be the first warning sign that Numba wouldn't be able to help.

```
In [23]: foo("a", "b")
<ipython-input-22-75680c5bffbd>:1: NumbaWarning: Function "foo" failed type inference: Invalid usage of + with parameters (str, str)
Known signatures:
 * (int64, int64) -> int64
 * (int64, uint64) -> int64
 * (uint64, int64) -> int64
 * (uint64, uint64) -> uint64
 * (float32, float32) -> float32
 * (float64, float64) -> float64
 * (complex64, complex64) -> complex64
 * (complex128, complex128) -> complex128
 * (uint64,) -> uint64
 * (uint16,) -> uint64
 * (uint8,) -> uint64
 * (uint32,) -> uint64
 * (int8,) -> int64
 * (int32,) -> int64
 * (int64,) -> int64
 * (int16,) -> int64
 * (float32,) -> float32
 * (float64,) -> float64
 * (complex64,) -> complex64
 * (complex128,) -> complex128
 * parameterized
File "<ipython-input-22-75680c5bffbd>", line 3
[1] During: typing of intrinsic-call at <ipython-input-22-75680c5bffbd> (3)
  @jit
<ipython-input-22-75680c5bffbd>:1: NumbaWarning: Function "foo" was compiled in object mode without forceobj=True.
  @jit
```

Benchmarking both functions, we get a a nice surprise of 16x slowdown with the jit version!

```python
In [28]: %timeit bmk(foo, 1000000, "a", "b")
7.87 s ± 81.1 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

In [29]: %timeit bmk(bar, 1000000, "a", "b")
197 ms ± 6.54 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
```

Want to try this in Julia?  Here's we go.  

```julia
julia> foo(x, y) = x * y
foo (generic function with 1 method)

julia> foo("a", "b")
"ab"

julia> @benchmark for i in 1:1000000 foo("a", "b") end
BenchmarkTools.Trial: 
  memory estimate:  30.52 MiB
  allocs estimate:  1000000
  --------------
  minimum time:     33.785 ms (6.51% GC)
  median time:      36.242 ms (6.60% GC)
  mean time:        36.092 ms (8.97% GC)
  maximum time:     43.915 ms (12.27% GC)
  --------------
  samples:          139
  evals/sample:     1
```
