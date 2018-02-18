using BenchmarkTools

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

function black_scholes(callResult, putResult, stockPrice, optionStrike, optionYears, 
        Riskfree, Volatility)
    S = stockPrice
    X = optionStrike
    T = optionYears
    R = Riskfree
    V = Volatility
    for i in 1:length(S)
        sqrtT = sqrt(T[i])
        d1 = (Base.Math.JuliaLibm.log(S[i] / X[i]) + (R + 0.5 * V * V) * T[i]) / (V * sqrtT)
        d2 = d1 - V * sqrtT
        cndd1 = cnd(d1)
        cndd2 = cnd(d2)
        expRT = exp((-1. * R) * T[i])
        callResult[i] = (S[i] * cndd1 - X[i] * expRT * cndd2)
        putResult[i] = (X[i] * expRT * (1.0 - cndd2) - S[i] * (1.0 - cndd1))
    end
end


randfloat(r, low, high) = @. (1.0 - r) * low + r * high

function testbs(OPT_N, f)
    iterations = 10
    RISKFREE = 0.02
    VOLATILITY = 0.30
    callResult = zeros(OPT_N)
    putResult  = -ones(OPT_N)
    stockPrice    = randfloat(rand(OPT_N), 5.0, 30.0)
    optionStrike  = randfloat(rand(OPT_N), 1.0, 100.0)
    optionYears   = randfloat(rand(OPT_N), 0.25, 10.0)
    t1 = now()
    for i in 1:iterations
        f(callResult, putResult, stockPrice, optionStrike, optionYears, RISKFREE, VOLATILITY)
    end
    t2 = now()
    return div(t2 - t1, iterations)
end

# warm up
testbs(4000000, black_scholes) 

# test now
elapsed = testbs(4000000, black_scholes)
println("Average (single-threaded): $elapsed")

