# -*- coding: utf-8 -*-

from optimization import optandinit as oi
import params
from tcpcalibrators import calibinteract

if __name__ == '__main__':
    target = 'mean'
    datafiles = params.datafiles
    
    xinit_list = []
    xopt_list = []
    for f in datafiles:
        norms_initial, norms_optimal, opt = oi.compare(f, target)
        xinit_list.append(opt.XInitial)
        xopt_list.append(opt.XOptimal)
    
    print xinit_list
    print xopt_list
    
    flatten = lambda m3d_obj: calibinteract.extract(m3d_obj).flatten()   
    xinit_flattened = [flatten(x) for x in xinit_list]
    xopt_flattened = [flatten(x) for x in xopt_list]
