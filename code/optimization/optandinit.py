# -*- coding: utf-8 -*-

'''
Compare the intitial result of hand-eye calibration
and the optimized one
'''

import olrem
import params
from matplotlib import pyplot as plt
import os
from os.path import join as opj
import cPickle as pickle

def compare(datafile, target):
    f = os.path.basename(datafile).split('.')[0]
    
    print 'Reading data file %s ...' % datafile
    pairs, AB, AB_pairs = olrem.read_pairs_and_calc_AB(datafile)
    
    pickle_file = opj(params.datadir, 'opt_%s_%s.pickle' % (target, f))
    
    print 'Unpicking data...'
    with open(pickle_file, 'rb') as f: 
        opt = pickle.load(f)
        
    XInititial = opt.XInitial
    XOptimal = opt.XOptimal
    
    norms_initial = olrem.calc_norms(AB, XInititial, params.norm_func)    
    norms_optimal = olrem.calc_norms(AB, XOptimal, params.norm_func)
    
    return norms_initial[1], norms_optimal[1], opt

def create_comparison_histogram(norms_initial, norms_optimal, opt, datafile):
    plt.figure()
    title_str = 'Intial and optimized norm distributions for data from %s\n(method: %s, minimization target: %s)'
    title_params = (os.path.basename(datafile), opt.opt_method, opt.minimization_target)
    plt.title(title_str % title_params)
    plt.xlabel('Values of ||AX-XB|| norms')
    plt.ylabel('Frequency')
    plt.hist(norms_initial, 100, color="gray", label='Original X')
    plt.hist(norms_optimal, 100, color="green", label='Optimized X')
    plt.legend(('Original X', 'Optimized X'))

    
    
    