# -*- coding: utf-8 -*-

'''
Remove outliers and see how it affects the result
'''

import recalc as recalc
import params
import olrem
from helpers import stats
from matplotlib import pyplot as plt
from hecalibrators.park_martin_calibration import ParkMartinCalibrator
from hecalibrators import calibinteract as ci

def calc_avg_min_max_norms(norms):
    s = stats.calc_statistics(norms)
    return s['mean'], s['min'], s['max']

if __name__ == '__main__':
    
    datafile = params.datafiles[2]
    pairs, AB, AB_pairs = olrem.read_pairs_and_calc_AB(datafile)
    old_X = ci.get_calibration_result(pairs, ParkMartinCalibrator)
    old_matrices, old_norms = olrem.calc_norms(AB, old_X, params.norm_func)
        
    ''' Try Park-Martin calibration with new pairs '''
    top_limit = 0.5
    filtered_indices = recalc.filter_pairs(old_norms, lambda x: x < top_limit)
    
    pmc = ParkMartinCalibrator(pairs)
    pmc.update_move_pairs(filtered_indices)
    new_X = pmc.sensor_in_flange
    
    new_matrices, new_norms = olrem.calc_norms(AB, new_X, params.norm_func)
    
    print '\tavg\tmin\tmax'
    print 'Old:\t%.2f\t%.2f\t%.2f' % calc_avg_min_max_norms(old_norms)   
    print 'New:\t%.2f\t%.2f\t%.2f' % calc_avg_min_max_norms(new_norms)
    
    print '\nMatrix X (old):'
    print old_X
    
    print '\nMatrix X (new):'
    print new_X
    
    plt.figure()
    plt.hist(old_norms, 100, color='blue')
    plt.hist(new_norms, 100, color='green')