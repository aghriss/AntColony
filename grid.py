#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 18:26:13 2017

@author: thinkpad

Defining the Grid class that contains all the cells
"""
import params
from cell import *


class Grid:
    def __init__(self):
        self.grid_size = params.grid_size
        
        self.grid = [[Cell(i, j) for j in range(params.grid_size[0])] for i in range(params.grid_size[1])]
        
        self.nests=[]
        self.update_time =0
        self.step = params.step
           
    # return the cell i,j in case it exists
    def __getitem__(self,pos):
        i, j = pos
        if (i*(i-self.grid_size[0])>0)  or (j*(j-self.grid_size[1])>0):
            print("coordinates out of bound, grid size :",(i,j),"out of",self.grid_size)
            raise NameError("Cell not found")
            return None 
        else:
            return self.grid[i][j]
    # Loads the grid from file
    # the file contains lines in the format :
    # x,y,cell_type
    def load_grid(self,filename):
        f = open(filename,"r")
        lines = f.readlines()
        f.close()
        for i in lines:
            i=i.replace("\n","").split(",")
            self.grid[int(i[0])][int(i[1])].type=i[2].upper()
            if i[2]=="NEST": self.nests.append([int(n) for n in i[:2]])
    # Saves the grid from to merory to a file
    # To use after drawing
    
    def save_grid(self,filename):
        f=open(filename,"w")
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                if self.grid[i][j].type != "ROAD":
                    f.write(str(i)+","+str(j)+","+self.grid[i][j].type+"\n")
        f.close()
    # Updates pheromones in each cell int eh grid
    def update(self):
        self.update_time = (self.update_time+1)%self.step
        if(self.update_time == 0):
            for r in self.grid:
                for c in r:
                    c.update()
    # draw each cell
    def draw(self,display):
        for r in self.grid:
            for c in r:
                c.draw(display,params.block_size)
    