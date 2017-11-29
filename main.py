import fileinput
import numpy as np
import math
from scipy import stats


def main():
    arrayX = []
    arrayY = []
    n = 0
    i = 0

    for line in fileinput.input():
        n += 1

    for line in fileinput.input():
        if(i == 0):
            xk = int(line)
        elif(i <= n/2):
            arrayX.append(line)
        else:
            arrayY.append(line)
        i += 1
    for i in range(int(n/2)):
        arrayX[i] = float(arrayX[i])
        arrayY[i] = float(arrayY[i])

    r = correlation(int(n/2), arrayX, arrayY)
    b1 = getB1(int(n/2), arrayX, arrayY)
    b0 = getB0(int(n/2), b1, arrayX, arrayY)
    yk = b0 + b1 * xk
    o = stdDeviation(int(n/2), arrayX, arrayY, b0, b1)
    x = getX(int(n/2), r)
    t = getT(int(n/2), o, arrayX, arrayY)
    df = int(n/2) - 2
    p = 1 - stats.t.cdf(t,df=df)
    print("p = {}".format(p))

    rang = getRange(int(n/2), o, t, xk, arrayX)
    upi = yk + rang
    lpi = yk - rang

    print("r = {}".format(r))
    print("r2 = {}".format(r**2))
    print("b1 = {}".format(b1))
    print("b0 = {}".format(b0))
    print("yk = {}".format(yk))
    print("range = {}".format(rang))
    print("UPI = {}".format(upi))
    print("LPI = {}".format(lpi))

def getT(n, o, arrayX, arrayY):
    meanX = mean(n, arrayX)
    meanY = mean(n, arrayY)
    t = (meanX - meanY)/(o*np.sqrt(2/n))
    return t

def getX(n, rxy):
    x = ( abs(rxy) * math.sqrt(n-2) ) / math.sqrt(1 - (rxy ** 2))
    return x


def mean(n, arr):
    sumArray = 0
    for i in range(n):
        sumArray +=float(arr[i])
    return sumArray/n

def correlation(n, arrayX, arrayY):
    xi_mean = 0
    yi_mean = 0
    sum_xi_mean_yi_mean = 0
    sum_xi_mean_2 = 0
    sum_yi_mean_2 = 0
    meanX = mean(n, arrayX)
    meanY = mean(n, arrayY)
    for i in range(n):
        xi_mean =float(arrayX[i]) - meanX
        yi_mean =float(arrayY[i]) - meanY
        sum_xi_mean_yi_mean += xi_mean * yi_mean
        sum_xi_mean_2 += xi_mean ** 2
        sum_yi_mean_2 += yi_mean ** 2
    r = ( sum_xi_mean_yi_mean / math.sqrt ( sum_xi_mean_2 * sum_yi_mean_2 ) )
    return r

def getB1(n, arrayX, arrayY):
    sum_xiyi = 0
    sum_x2 = 0
    meanX = mean(n, arrayX)
    meanY = mean(n, arrayY)
    for i in range(n):
        sum_xiyi +=float(arrayX[i]) *float(arrayY[i])
        x =float(arrayX[i])
        x2 = x ** 2
        sum_x2 += x2
    b1 = (sum_xiyi - (n * meanX * meanY)) / (sum_x2 - (n * meanX ** 2))
    return b1

def getB0(n, b1, arrayX, arrayY):
    meanX = mean(n, arrayX)
    meanY = mean(n, arrayY)
    b0 = meanY - (b1 * meanX)
    return b0

def stdDeviation(n, arrayX, arrayY, b0, b1):
    sum_yi_B0_B1Xi = 0
    for i in range(n):
        sum_yi_B0_B1Xi += (float(arrayY[i]) - b0 - (b1 *float(arrayX[i]))) ** 2
    o = math.sqrt( (1/(n-2)) * sum_yi_B0_B1Xi )
    return o

def getRange(n, o, t, xk, arrayX):
    sum_xi_mean2 = 0
    meanX = mean(n, arrayX)
    t = 1.1081348148903627
    for i in range(n):
        sum_xi_mean2 = (float(arrayX[i]) - meanX) ** 2
    rang = t * o * math.sqrt( ( 1 + 1/n + ( ( ( xk - meanX ) ** 2) / sum_xi_mean2 )))
    return rang


"""
Main program
"""
main()
