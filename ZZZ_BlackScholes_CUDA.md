### Julia CUDAnative Test

Server: p2.xlarge instance on AWS

TODO: 
- CUDA result seems too good to be true (see below)

```
julia> @benchmark testbs_cuda(1, 4000000, black_scholes_cuda, 1, 1024)
BenchmarkTools.Trial: 
  memory estimate:  274.66 MiB
  allocs estimate:  95
  --------------
  minimum time:     258.635 ms (65.42% GC)
  median time:      259.549 ms (65.41% GC)
  mean time:        262.931 ms (66.12% GC)
  maximum time:     326.611 ms (76.31% GC)
  --------------
  samples:          20
  evals/sample:     1

julia> @benchmark testbs(1, 4000000, black_scholes)
BenchmarkTools.Trial: 
  memory estimate:  274.66 MiB
  allocs estimate:  18
  --------------
  minimum time:     627.344 ms (27.52% GC)
  median time:      628.119 ms (27.64% GC)
  mean time:        638.424 ms (28.80% GC)
  maximum time:     708.265 ms (35.78% GC)
  --------------
  samples:          8
  evals/sample:     1

```

### Related Source Code

```julia
using CUDAnative, CUDAdrv

randfloat(r, low, high) = @. (1.0 - r) * low + r * high

function cnd(d::Float64) 
    A1 = 0.31938153
    A2 = -0.356563782
    A3 = 1.781477937
    A4 = -1.821255978
    A5 = 1.330274429
    RSQRT2PI = 0.39894228040143267793994605993438
    K = 1.0 / (1.0 + 0.2316419 * abs(d))
    ret_val = (RSQRT2PI * exp(-0.5 * d * d) *
              (K * (A1 + K * (A2 + K * (A3 + K * (A4 + K * A5))))))
    d > 0 ? 1.0 - ret_val : ret_val
end

function black_scholes(callResult, putResult, S, X, T, R, V)
    for i in 1:length(S)
        sqrtT = sqrt(T[i])
        d1 = (log(S[i] / X[i]) + (R + 0.5 * V * V) * T[i]) / (V * sqrtT)
        d2 = d1 - V * sqrtT
        cndd1 = cnd(d1)
        cndd2 = cnd(d2)
        expRT = exp((-1. * R) * T[i])
        callResult[i] = (S[i] * cndd1 - X[i] * expRT * cndd2)
        putResult[i] = (X[i] * expRT * (1.0 - cndd2) - S[i] * (1.0 - cndd1))
    end
end

function testbs(iterations, OPT_N, f)
    RISKFREE = 0.02
    VOLATILITY = 0.30
    callResult = zeros(OPT_N)
    putResult  = -ones(OPT_N)
    stockPrice    = randfloat(rand(OPT_N), 5.0, 30.0)
    optionStrike  = randfloat(rand(OPT_N), 1.0, 100.0)
    optionYears   = randfloat(rand(OPT_N), 0.25, 10.0)
    for i in 1:iterations
        f(callResult, putResult, stockPrice, optionStrike, optionYears, RISKFREE, VOLATILITY)
    end
end

function cnd_cuda(d::Float64) 
    A1 = 0.31938153
    A2 = -0.356563782
    A3 = 1.781477937
    A4 = -1.821255978
    A5 = 1.330274429
    RSQRT2PI = 0.39894228040143267793994605993438
    K = 1.0 / (1.0 + 0.2316419 * CUDAnative.abs(d))
    ret_val = (RSQRT2PI * CUDAnative.exp(-0.5 * d * d) *
              (K * (A1 + K * (A2 + K * (A3 + K * (A4 + K * A5))))))
    d > 0 ? 1.0 - ret_val : ret_val
end
function black_scholes_cuda(callResult, putResult, S, X, T, R, V)
    i = (blockIdx().x-1) * blockDim().x + threadIdx().x
    i > length(S) && return
    sqrtT = CUDAnative.sqrt(T[i])
    d1 = (CUDAnative.log(S[i] / X[i]) + (R + 0.5 * V * V) * T[i]) / (V * sqrtT)
    d2 = d1 - V * sqrtT
    cndd1 = cnd(d1)
    cndd2 = cnd(d2)
    expRT = CUDAnative.exp((-1. * R) * T[i])
    callResult[i] = (S[i] * cndd1 - X[i] * expRT * cndd2)
    putResult[i] = (X[i] * expRT * (1.0 - cndd2) - S[i] * (1.0 - cndd1))
    return
end

function testbs_cuda(iterations, OPT_N, f, m, n)
    RISKFREE = 0.02
    VOLATILITY = 0.30
    callResult = CuArray(zeros(OPT_N))
    putResult  = CuArray(-ones(OPT_N))
    stockPrice    = CuArray(randfloat(rand(OPT_N), 5.0, 30.0))
    optionStrike  = CuArray(randfloat(rand(OPT_N), 1.0, 100.0))
    optionYears   = CuArray(randfloat(rand(OPT_N), 0.25, 10.0))
    for i in 1:iterations
        @cuda (m,n) f(callResult, putResult, stockPrice, optionStrike, optionYears, RISKFREE, VOLATILITY)
    end
end

iterations = 10
asize = 4000000

println("Normal version")
tic()
testbs(iterations, asize, black_scholes)
toc()

println("CUDA version")
tic()
testbs_cuda(iterations, asize, black_scholes_cuda, 1, 12)
toc()
```

CUDA scale weirdness - marginal difference.

```julia
julia> @time testbs_cuda(10, 10000000, black_scholes_cuda, 1, 12)
Iteration #1
Iteration #2
Iteration #3
Iteration #4
Iteration #5
Iteration #6
Iteration #7
Iteration #8
Iteration #9
Iteration #10
  0.551615 seconds (501 allocations: 686.660 MiB, 46.46% gc time)

julia> @time testbs_cuda(20, 10000000, black_scholes_cuda, 1, 12)
Iteration #1
Iteration #2
Iteration #3
Iteration #4
Iteration #5
Iteration #6
Iteration #7
Iteration #8
Iteration #9
Iteration #10
Iteration #11
Iteration #12
Iteration #13
Iteration #14
Iteration #15
Iteration #16
Iteration #17
Iteration #18
Iteration #19
Iteration #20
  0.599880 seconds (950 allocations: 686.673 MiB, 42.27% gc time)

100 iterations:
  0.605452 seconds (4.40 k allocations: 686.772 MiB, 42.32% gc time)

500 iterations:
  0.614027 seconds (21.62 k allocations: 687.266 MiB, 43.48% gc time)

5,000 iterations:
0.753455 seconds (219.99 k allocations: 692.902 MiB, 34.30% gc time)


```
