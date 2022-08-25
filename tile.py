from dataclasses import dataclass
import os
import numpy as np
from PIL import Image
from dataclasses import dataclass

UP = 'u'
RIGHT = 'r'
DOWN = 'd'
LEFT = 'l'

@dataclass
class Joint:
    position: str
    rotations: int
    hash_val: str
    
    def is_connectable(self, joint):
        if self.hash_val != joint.hash_val:
            return False
        
        if self.position == UP:
            if joint.position != DOWN:
                return False
        if self.position == RIGHT:
            if joint.position != LEFT:
                return False    
        if self.position == DOWN:
            if joint.position != UP:
                return False
        if self.position == LEFT:
            if joint.position != RIGHT:
                return False

        return True

class Tile():
    
    def __init__(self, name, array, dim = 8, n_rotations = 4):
        self.name = name
        self.dim = dim
        self.n_rotations = n_rotations
        self.array = array
        self.joints = self._calc_joints()
        print(len(self.joints))
        
        
    def _calc_joints(self):
        rgb2hex = lambda x: '%02x%02x%02x' %(x[0],x[1],x[2])
        joints = []
        for i in range(self.n_rotations):
            arr = np.rot90(self.array, i, axes=[1,0])
            
            if i != 0 and np.array_equal(self.array, arr):
                continue
            
            u = arr[0, :]
            hash_u = ''.join([rgb2hex(i) for i in u])
            joints.append(Joint(UP, i, hash_u))
                    
            r = arr[:, self.dim-1]
            hash_r = ''.join([rgb2hex(i) for i in r])
            joints.append(Joint(RIGHT, i, hash_r))
            
            d = arr[self.dim-1, :]
            hash_d = ''.join([rgb2hex(i) for i in d])
            joints.append(Joint(DOWN, i, hash_d))
            
            l = arr[:, 0]
            hash_l = ''.join([rgb2hex(i) for i in l])
            joints.append(Joint(LEFT, i, hash_l))
        
        return joints

class Tileset():
    
    def __init__(self, path):
        self.tiles = self._load_tiles(path)

    def _load_tiles(self, path):
        tiles = []
        raws = os.listdir(path)
        
        for t in raws:
            arr = np.asarray(Image.open(path+t))
            tiles.append(Tile(t, arr))
            
        return tiles