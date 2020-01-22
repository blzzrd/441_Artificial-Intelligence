# world.py
import numpy as np
import random

""" 
The purpose of this file is to be able to create
the environment that the vacuum will reside in, along
with other constraints required for the program. 
"""


class world(object):
    def __init__(self, dirt_piles, MURPHY=False):
        # 3x3 Matrix 
        self.map = np.zeros((3,3))

        # Either 1, 3, 5.
        self.dirt_piles = dirt_piles

        # MURPHY'S LAW.
        self.murphy = MURPHY


    def setup(self):
        dirt = self.dirt_piles
        while dirt > 0:
            randx = np.random.randint(3)
            randy = np.random.randint(3)

            if self.map[randx][randy] == 0:
                dirt -= 1
                self.map.__setitem__((randx,randy),1)


    def isclean(self):
        if self.dirt_piles > 0:
            return False
        return True

    def check(self, x, y):
        b = self.map[x][y]
        if self.murphy:
            a = np.random.randint(100)
            if a < 10:
                b = not b
        return b

    def clean(self, x, y):
        if self.murphy:
            z = np.random.randint(100)
            if z > 74:
                return
                
        self.map[x][y] = 0
        self.dirt_piles -= 1
        return



class vacuum(object):
    def __init__(self, randomBool, world):
        self.env = world
        self.random = randomBool
        self.curloc = [0,0] # current location
        self.moves = 0


    def act(self):
        while self.env.isclean() == False:
            if self.random == True:
                x = np.random.randint(6)
                if x == 0:
                    self.left()
                elif x == 1:
                    self.up()
                elif x == 2:
                    self.right()
                elif x == 3:
                    self.down()
                elif x == 4:
                    self.suck()
                elif x == 5:
                    self.nothing()
            else:
                x = self.env.check(self.curloc[0], self.curloc[1]) 
                if x == 1:
                    self.suck()
                    continue



                """
                [  v> |  >  |  v  ] 
                [  ^  |  ^  |  v  ]
                [  ^  |  <  |  <  ]
                """


                if self.curloc == [0,0]:
                    self.down()
                    self.right()
                    self.moves -= 1
                elif self.curloc == [1,0]:
                    self.up()
                elif self.curloc == [2,0]:
                    self.up()
                elif self.curloc == [0,1]:
                    self.right()
                elif self.curloc == [1,1]:
                    self.up()
                elif self.curloc == [2,1]:
                    self.left()
                elif self.curloc == [0,2]:
                    self.down()
                elif self.curloc == [1,2]:
                    self.down()
                elif self.curloc == [2,2]:
                    self.left()

    
                

                
                # Get the table values.
                
        return self.moves


    def setup(self):
        randx = np.random.randint(3)
        randy = np.random.randint(3)
        self.curloc = [randx, randy]


    """ Actions """

    def left(self):
        self.moves += 1
        if self.curloc[1] > 0:
            self.curloc[1] -= 1

    def up(self):
        self.moves += 1
        if self.curloc[0] > 0:
            self.curloc[0] -= 1

    def right(self):
        self.moves += 1
        if self.curloc[1] < 2:
            self.curloc[1] += 1

    def down(self):
        self.moves += 1
        if self.curloc[0] < 2:
            self.curloc[0] += 1

    def suck(self):
        self.moves += 1 
        self.env.clean(self.curloc[0], self.curloc[1])
       

    def nothing(self):
        return
         




