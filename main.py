#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 20:37:01 2017

@author: thinkpad
"""
from grid import *
from colony import *
from application import *

grid_map = Grid()
grid_map.load_grid("map.txt")

ants_colony = Colony(grid_map)

app = App()

app.begin_draw(grid_map)

app.start_app(grid_map,ants_colony)
