# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 17:51:50 2017

@author: Ayoub


Defining the Ant class
"""
###############################################################################
import random
import bisect
import numpy as np
import params


directs_vect = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
Directions = {i:directs_vect[i] for i in range(8)}
Labels = dict(map(reversed, Directions.items()))


class Ant:
    """
Ant Class
"""
    def __init__(self, grid):
        """
        """
        #.colony = colony
        self.grid = grid
        self.x, self.y = random.choice(self.grid.nests)

        self.alpha = params.alpha
        self.beta = params.beta

        self.phero_min = params.phero_min
        self.phero_max = params.phero_max

        self.has_food = False
        self.distance = 500

        self.weights = np.zeros(8)
        self.direction = random.randint(0, 7)

    def reset(self):
        """
        reset
        """
        self.has_food = False
        self.distance = 500

        self.weights = np.zeros(8)
        self.direction = random.randint(0, 7)

        self.x, self.y = random.choice(self.grid.nests)
###############################################################################

    def when_has_food(self):
        """
        when_has_food
        """
        return self.phero_max

    def when_no_food(self):
        """
        when_no_food
        """
        #return self.phero_max
        return (self.phero_max-self.phero_min)/300

    def scatter_phero(self):
        """
        scatter
        """


        if self.has_food:
            self.grid[self.x, self.y].phero = self.when_has_food()
        else:
            self.grid[self.x, self.y].phero += self.when_no_food()

###############################################################################

    def weights_vector(self):
        """
        wieghts vectors
        """
        for i in range(8):
            self.weights[i] = 0
            if i != (self.direction+4)%8:
                dest = np.array(Directions[i])+[self.x, self.y]

                try:
                    if self.grid[dest].type != "WALL":
                        if self.direction%2:
                            self.weights[i] = \
                            self.grid[dest].phero**self.alpha\
                            *np.sqrt(2)**self.beta
                        else:
                            self.weights[i] = self.grid[dest].phero**self.alpha

                except:
                    self.weights[i] = 0
                    print("Error accessing cell", dest, "in the grid")
        self.weights /= 1+np.abs(np.arange(8)-self.direction)

###############################################################################

    def choose_direction(self):
        """
        choose direction
        """
        self.weights_vector()
        total = sum(self.weights)
        if total != 0:

            self.direction = bisect.bisect(np.cumsum(self.weights)/total, random.random())
            return True
        return False
###############################################################################

    def rotate(self):
        """
        rotation
        """
        self.direction = (self.direction+1)%8
###############################################################################

    def work(self): # the brain
        """
        working 
        """
        self.scatter_phero()

        if self.choose_direction():
            self.grid[self.x, self.y].count -= 1
            destination = Directions[self.direction]
            self.x += destination[0]
            self.y += destination[1]
            self.grid[self.x, self.y].count += 1
            self.distance -=1
        else:
            self.direction = (self.direction+4)%8

        if self.grid[self.x, self.y].type == "FOOD":
            self.has_food = True
            self.distance = 500

        if self.grid[self.x, self.y].type == "NEST" or self.distance<0:
            self.grid[self.x, self.y].count -= 1
            self.reset()