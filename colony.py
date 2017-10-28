#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 19:10:36 2017

@author: thinkpad

defining the Ant Colony
"""
from ant import *
import params

class Colony:
    
    def __init__(self,grid):
        
        self.ants_count = params.ants_count
        self.colony = [Ant(grid) for _ in range(self.ants_count)]
    
    def work(self):
        for a in self.colony:
            a.work()
    