import numpy as np
def freq():
    with open('f.txt', 'r') as f:  
    	v = map(float,f.readlines()) 
        v = np.array(v)
    N0 = 6.022E23
    T = 298.15
    h = 6.626E-34
    R = 8.314
    kB = 1.38E-23
    c = 2.99792458E10
    eV2J = 96485
    Thv = h*c*v/kB
    dH = R * Thv / (np.exp(Thv/T)-1)
    s = R * (Thv/T/ (np.exp(Thv/T)-1) - np.log(1-np.exp(-Thv/T)))
    dZPE = 0.5 * h * c * v * N0
#    print s
    ZPE = np.sum(dZPE) / eV2J
    Uv = np.sum(dH) / eV2J
    TSv = np.sum(s) * T / eV2J
    print ZPE, Uv, TSv, ZPE+Uv-TSv
    return

freq()
