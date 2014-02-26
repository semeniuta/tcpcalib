# -*- coding: utf-8 -*-

'''
Remove outliers and see how it affects the result
'''

import math
import params
from outliers import precision
from outliers.norms import NormsOutliersEliminator
from matplotlib import pyplot as plt

if __name__ == '__main__':
    
    datafile = params.datafiles[2]

    noe = NormsOutliersEliminator(datafile)    
    
    # top_limits = [0.001*i for i in range(500, math.trunc(1000*max(noe.old_norms)))]    
    top_limits = [0.01*i for i in range(50, math.trunc(100*max(noe.old_norms)))]
    
    v1, v2 = precision.precision_test(noe, top_limits)

    s1 = v1['d1'] + v1['d2'] + v1['d3']
    s2 = v2['d1'] + v2['d2'] + v2['d3']

    for d in ['d1', 'd2', 'd3']:
        plt.figure()
        plt.plot(top_limits, v1[d], label='old var(%s)' % d)
        plt.plot(top_limits, v2[d], label='new var(%s)' % d)
        
    plt.figure()
    plt.plot(top_limits, s1, label='s1')
    plt.plot(top_limits, s2, label='s2')
              
    
    
    
    
    