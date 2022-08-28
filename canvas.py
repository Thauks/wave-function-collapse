from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import random
from dataclasses import dataclass

UP = 'u'
RIGHT = 'r'
DOWN = 'd'
LEFT = 'l'

@dataclass
class Cell:
    xcoord: int
    ycoord: int
    collapsed: bool
    tile: str
    n_rotations: int
    options: list
    north: list
    east: list
    south: list
    west: list
    
    def _update_options(self, joint):
        new_options = []
        if self.options:
            for option in self.options:
                if joint.is_connectable(option['joint']):
                    new_options.append(option)
            self.options = new_options

class Canvas():
    
    def __init__(self, tileset, height, width):
        self.tileset = tileset
        self.height = height
        self.width = width
        self.base_options = tileset.all_edges
        self.cells_left = height*width
        self.finished = False
        self.grid = self._gen_grid()
        
    def render(self):
        rended = np.zeros((self.width*8, self.height*8, 4), dtype=np.uint8)
        
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                
                self.tileset.tiles[cell.tile].render()
                arr = self.tileset.tiles[cell.tile].array
                arr = np.rot90(arr, cell.n_rotations, axes=[1,0])
                rended[i*8:i*8+8, j*8:j*8+8] = arr
                
        im = Image.fromarray(rended)
        plt.imshow(im)
        plt.show()
        pass
        
    def is_finished(self):
        return self.finished
    
    def collapse_cell(self, xcoord, ycoord):
        
        cell = self.grid[xcoord, ycoord]
        
        if cell.collapsed != True:
        
            choice = random.choice(cell.options)
            print(choice)
                    
            cell.tile = choice['tile']
            cell.n_rotations = choice['joint'].rotation_stage
            print(cell)
            cell.options = None
            self._propagate_collapse(cell)
            cell.collapsed = True
            self.cells_left -= 1
            if self.cells_left == 0: self.finished = True
            print(f'Cell collapsed ({xcoord}, {ycoord}) with {cell.tile} rotation stage: {cell.n_rotations}')
    
    def find_candidate(self):
        
        minimum = np.inf
        x, y = None, None
        
        for row in self.grid:
            for cell in row:
                if not cell.collapsed:
                    n_opt = len(cell.options)
                    if n_opt == 1:
                        x, y = cell.xcoord, cell.ycoord
                        break
                    
                    if n_opt < minimum:
                        minimum = n_opt
                        x, y = cell.xcoord, cell.ycoord
        
        print(f'Candidate found ({x}, {y})')
        return x, y
    
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
                
                mat[i, j] = Cell(xcoord=i, ycoord=j, collapsed=False, tile=None, n_rotations=None, options=self.base_options, north=north, east=east, south=south, west=west)
                
        return mat

    def _propagate_collapse(self, cell):
        joints = self.tileset.tiles[cell.tile].get_edges(cell.n_rotations)
        
        for joint in joints:
            if cell.north and joint.position == UP:
                self.grid[cell.north].flatten()[0]._update_options(joint)
                
            if cell.east and joint.position == RIGHT:
                self.grid[cell.east].flatten()[0]._update_options(joint)
                
            if cell.south and joint.position == DOWN:
                self.grid[cell.south].flatten()[0]._update_options(joint)
                
            if cell.west and joint.position == LEFT:
                self.grid[cell.west].flatten()[0]._update_options(joint)