from turtle import title
from PIL import Image
import numpy as np
from dataclasses import dataclass

@dataclass
class Cell:
    collapsed: bool
    tile: str
    options: list
    north: list
    east: list
    south: list
    west: list


class Canvas():
    
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.grid = self._gen_grid()
    
    
    def _gen_grid(self):
        mat = np.zeros((self.height, self.width), dtype=Cell)
        
        for i in range(self.width):
            for j in range(self.height):
                pi, pj, mi, mj = i+1, j+1, i-1, j-1
                north=[i, mj]
                east=[pi, j]
                south=[i, pj]
                west=[mi, j]
                
                if (i == self.width-1): east = None
                if (j == self.height-1): south = None
                if (i == 0): west = None
                if (j == 0): north = None
                
                mat[i, j] = Cell(collapsed=False, tile=None, options=[], north=north, east=east, south=south, west=west)
                
        return mat
