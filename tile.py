from dataclasses import dataclass
import os
import numpy as np
from PIL import Image
from dataclasses import dataclass


@dataclass(eq=False)
class Joint:
    position: str
    rotations: int
    hash_val: str
    
    def __eq__(self, other):
        pass
            

class Tile():
    
    def __init__(self, array, dim = 8, n_rotations = 4):
        self.dim = dim
        self.n_rotations = n_rotations
        self.array = array
        self.joints = self._calc_joints()
        print(self.joints)
        
        
    def _calc_joints(self):
        rgb2hex = lambda x: '%02x%02x%02x' %(x[0],x[1],x[2])
        joints = []
        for i in range(self.n_rotations):
            arr = np.rot90(self.array, i, axes=[1,0])
            
            u = arr[0, :]
            hash_u = ''.join([rgb2hex(i) for i in u])
            joints.append(Joint('u', i, hash_u))
                    
            r = arr[:, self.dim-1]
            hash_r = ''.join([rgb2hex(i) for i in r])
            joints.append(Joint('r', i, hash_r))
            
            d = np.flip(arr[self.dim-1, :], axis=0)
            hash_d = ''.join([rgb2hex(i) for i in d])
            joints.append(Joint('d', i, hash_d))
            
            l = np.flip(arr[:, 0], axis=0)
            hash_l = ''.join([rgb2hex(i) for i in l])
            joints.append(Joint('l', i, hash_l))
        
        return joints


class Tileset():
    
    def __init__(self, path):
        self.tiles = self._load_tiles(path)
        self.rules = self._set_rules()
        print(self.tiles)
        
    def get_rules(self):
        return self.rules
    
    def _load_tiles(self, path):
        tiles = []
        raws = os.listdir(path)
        
        for t in raws:
            arr = np.asarray(Image.open(path+t))
            tiles.append(Tile(arr))
            
        return tiles
    
    def _set_rules(self):
        pass