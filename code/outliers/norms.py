# -*- coding: utf-8 -*-

import recalc
import params
import olrem
from hecalibrators.park_martin_calibration import ParkMartinCalibrator
from outliers import precision

class NormsOutliersEliminator:
        
    def __init__(self, datafile):
        
        ''' 
        Open data file with pose pairs (R, V) and calculate all 
        transformations (A, B)
        '''    
        self.pose_pairs, self.AB, combinations = olrem.read_pairs_and_calc_AB(datafile)
        
        '''
        Perform calibration with ALL transformations and calculate norms 
        of |AX-XB| matrix
        '''
        old_pmc = ParkMartinCalibrator(self.pose_pairs)    
        self.old_sif = old_pmc.sensor_in_flange
        old_matrices, self.old_norms = olrem.calc_norms(self.AB, self.old_sif, params.norm_func)
    
        
    def remove_outliers(self, top_limit):
            
        ''' 
        Filter out some of the transformations based on specified criterion
        '''
        filtered_indices = recalc.filter_pairs(self.old_norms, lambda x: x < top_limit)
        
        '''
        Perform calibration without filtered transformations and calculate norms 
        of |AX-XB| matrix
        '''
        new_pmc = ParkMartinCalibrator(self.pose_pairs)
        new_pmc.update_move_pairs(filtered_indices)
        self.new_sif = new_pmc.sensor_in_flange    
        new_matrices, self.new_norms = olrem.calc_norms(self.AB, self.new_sif, params.norm_func)
        
        '''Calculate object to base transform: R*X*inv(V) '''
        self.old_object_in_base = precision.get_oib_data(self.pose_pairs, self.old_sif)
        self.new_object_in_base = precision.get_oib_data(self.pose_pairs, self.new_sif)