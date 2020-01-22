# homework.py
import world
import pdb



""" The purpose of this homework.py is to 
execute all the code to give the results that
the homework is asking for.
Specifically, the homework is looking for comparative 
performance measures of 12 cases.

12 CASES ======
----------------------------------------------- |
----------------------------------------------- |
Initial Dirt Piles >    1       3       5       |
----------------------------------------------- |
Agent Type                                      |
----------------------------------------------- |
(i)                                             |
Simple Reflex                                   |
                                                |
----------------------------------------------- |
(ii)                                            |
Randomized Agent                                |
                                                |
----------------------------------------------- |
(iii)                                           |
Simple Reflex                                   |
w/ Murphy                                       |
----------------------------------------------- |
(iv)                                            |
Randomized Agent                                |
w/ Murphy                                       |
----------------------------------------------- |

"""




if __name__ == '__main__':

    for i in [1, 3, 5]:
        x = 0
        murphy = False
        random = False
        for _ in range(100): # 100 Tests
            env = world.world(i, murphy)
            env.setup()

            v = world.vacuum(random, env)
            v.setup()
            x += v.act()
        x /= 100
        print("Dirt Spots: ", i, "M:",  murphy, "R:", random, "Avg. Steps:", x)

    for i in [1, 3, 5]:
        x = 0
        murphy = False
        random = True
        for _ in range(100): # 100 Tests
            env = world.world(i, murphy)
            env.setup()

            v = world.vacuum(random, env)
            v.setup()
            x += v.act()
        x /= 100
        print("Dirt Spots: ", i, "M:",  murphy, "R:", random, "Avg. Steps:", x)

    for i in [1, 3, 5]:
        x = 0
        murphy = True
        random = False
        for _ in range(100): # 100 Tests
            env = world.world(i, murphy)
            env.setup()

            v = world.vacuum(random, env)
            v.setup()
            x += v.act()
        x /= 100
        print("Dirt Spots: ", i, "M:",  murphy, "R:", random, "Avg. Steps:", x)

    for i in [1, 3, 5]:
        x = 0
        murphy = True
        random = True
        for _ in range(100): # 100 Tests
            env = world.world(i, murphy)
            env.setup()

            v = world.vacuum(random, env)
            v.setup()
            x += v.act()
        x /= 100
        print("Dirt Spots: ", i, "M:",  murphy, "R:", random, "Avg. Steps:", x)


