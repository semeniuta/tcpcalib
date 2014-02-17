# -*- coding: utf-8 -*-

from helpers import m3dinteract as m3di
import numpy as np
import pandas as pd
import scipy

def calc_object_in_base(R, V, X):
    return R*X*V.inverse()

def get_oib_data(pose_pairs, X):
    oib_list = [m3di.flatten_transform(calc_object_in_base(R, V, X)) for R, V in pose_pairs]
    return np.array(oib_list)
    
def get_oib_data_pandas(oib_data):
    colnames = ['r11', 'r12', 'r13', 'r21', 'r22', 'r23', 'r31', 'r32', 'r33', 'd1', 'd2', 'd3']
    return pd.DataFrame(oib_data, columns=colnames)
    
def print_var(oib1, oib2):
    for j in range(9, 12):
        old = scipy.var(oib1[:, j])
        new = scipy.var(oib2[:, j])
        print old, new, old - new

def print_mean(oib1, oib2):
    for j in range(9, 12):
        old = scipy.mean(oib1[:, j])
        new = scipy.mean(oib2[:, j])
        print old, new, old - new