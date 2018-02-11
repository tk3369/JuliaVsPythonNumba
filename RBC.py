import numpy as np
import math
import time
from numba import autojit
import timeit
import datetime

@autojit
def innerloop(bbeta, nGridCapital, gridCapitalNextPeriod, mOutput, nProductivity, vGridCapital, expectedValueFunction, mValueFunction, mValueFunctionNew, mPolicyFunction):
    for nCapital in range(nGridCapital):
        valueHighSoFar = -100000.0
        capitalChoice  = vGridCapital[0]
        for nCapitalNextPeriod in range(gridCapitalNextPeriod, nGridCapital):
            consumption = mOutput[nCapital,nProductivity] - vGridCapital[nCapitalNextPeriod]
            valueProvisional = (1-bbeta)*np.log(consumption)+bbeta*expectedValueFunction[nCapitalNextPeriod,nProductivity];
            if  valueProvisional > valueHighSoFar:
                valueHighSoFar = valueProvisional
                capitalChoice = vGridCapital[nCapitalNextPeriod]
                gridCapitalNextPeriod = nCapitalNextPeriod
            else:
                break 
        mValueFunctionNew[nCapital,nProductivity] = valueHighSoFar
        mPolicyFunction[nCapital,nProductivity]   = capitalChoice
    return mValueFunctionNew, mPolicyFunction 

def main_func2():
    aalpha = 1.0/3.0     # Elasticity of output w.r.t. capital
    bbeta  = 0.95        # Discount factor
    vProductivity = np.array([0.9792, 0.9896, 1.0000, 1.0106, 1.0212],float)
    mTransition   = np.array([[0.9727, 0.0273, 0.0000, 0.0000, 0.0000],
                     [0.0041, 0.9806, 0.0153, 0.0000, 0.0000],
                     [0.0000, 0.0082, 0.9837, 0.0082, 0.0000],
                     [0.0000, 0.0000, 0.0153, 0.9806, 0.0041],
                     [0.0000, 0.0000, 0.0000, 0.0273, 0.9727]],float)
    capitalSteadyState     = (aalpha*bbeta)**(1/(1-aalpha))
    outputSteadyState      = capitalSteadyState**aalpha
    consumptionSteadyState = outputSteadyState-capitalSteadyState
    vGridCapital           = np.arange(0.5*capitalSteadyState,1.5*capitalSteadyState,0.00001)
    nGridCapital           = len(vGridCapital)
    nGridProductivity      = len(vProductivity)
    mOutput           = np.zeros((nGridCapital,nGridProductivity),dtype=float)
    mValueFunction    = np.zeros((nGridCapital,nGridProductivity),dtype=float)
    mValueFunctionNew = np.zeros((nGridCapital,nGridProductivity),dtype=float)
    mPolicyFunction   = np.zeros((nGridCapital,nGridProductivity),dtype=float)
    expectedValueFunction = np.zeros((nGridCapital,nGridProductivity),dtype=float)
    for nProductivity in range(nGridProductivity):
        mOutput[:,nProductivity] = vProductivity[nProductivity]*(vGridCapital**aalpha)
    maxDifference = 10.0
    tolerance = 0.0000001
    iteration = 0
    log = math.log
    zeros = np.zeros
    dot = np.dot
    while(maxDifference > tolerance):
        expectedValueFunction = dot(mValueFunction,mTransition.T)
        for nProductivity in range(nGridProductivity):
            gridCapitalNextPeriod = 0
            mValueFunctionNew, mPolicyFunction = innerloop(bbeta, nGridCapital, gridCapitalNextPeriod, mOutput, nProductivity, vGridCapital, expectedValueFunction, mValueFunction, mValueFunctionNew, mPolicyFunction)
        maxDifference = (abs(mValueFunctionNew-mValueFunction)).max()
        mValueFunction    = mValueFunctionNew
        mValueFunctionNew = zeros((nGridCapital,nGridProductivity),dtype=float)
        iteration += 1
    return (maxDifference, iteration, mValueFunction, mPolicyFunction)


# warm up
main_func2()

# run
iterations = 10
print(datetime.datetime.now())
x = timeit.timeit('main_func2()', setup="from __main__ import main_func2", number=iterations)
print(datetime.datetime.now())
print(x / iterations)
