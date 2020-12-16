import numpy as np
import matplotlib.pyplot as plt

#CONSTANTS
SIZE = 10

class robby():
    def __init__(self):
        # y, x
        self.loc = np.random.randint(SIZE), np.random.randint(SIZE)

    def getloc(self):
        return self.loc

    def updateloc(self, x, y):
        if 0 >= x > SIZE and 0 >= y > SIZE:
            self.loc = x, y


    def getstate(self, board):
        # HASHING FUNCTION
        # Options are after W[all], E[mpty], C[an]
        # String will be in format [ Current, Left, Up, Right, Down ]
                                    # 0      3      9   27     81

        # the way this will work issss..
        # CURRENT LEFT UP RIGHT DOWN. EMPTY = 0 CAN = 1 WALL = 2

        state = np.zeros(5)

        y, x = self.getloc()
        cr = board.loc(x, y)
        lt = board.loc(x-1, y)
        up = board.loc(x, y-1)
        rt = board.loc(x+1, y)
        dw = board.loc(x, y+1)

        direction = [cr, lt, up, rt, dw]

        representation = 0
        for d in range(len(direction)):
            representation += ((3**d)*direction[d])
           
        return int(representation)

    def act(self, action, board):
        """
        Actions = [PICKUP, LEFT, UP, RIGHT, DOWN]
        REWARDS
        if robby picks up can in empty square
            -1
        if robby crashes into wall
            -5
        if robby picks up can successfully
            +10
        """
        y, x = self.getloc()

        if action == 0:
            if board.loc(x, y) == 1:
                board.can(x, y)
                return 10
            return -1

        if action == 1:
            if board.loc(x-1, y) == 2:
                return -5
            self.loc = y, x-1
            return 0
            
        if action == 2:
            if board.loc(x, y-1) == 2:
                return -5
            self.loc = y-1, x
            return 0
 
        if action == 3:
            if board.loc(x+1, y) == 2:
                return -5
            self.loc = y, x+1
            return 0
 
        if action == 4:
            if board.loc(x, y+1) == 2:
                return -5
            self.loc = y+1, x
            return 0
        
        return None

class board():
    def __init__(self):
        randb = np.random.rand(SIZE, SIZE)
        self.b = np.round(randb)

    def loc(self, x, y):
        if y >= SIZE or y < 0 or x >= SIZE or x < 0:
            return 2
        return self.b[y][x]

    def can(self, x, y):
        self.b[y][x] = 0

def q_learn(q_m, eta=.2, gam=.9, e=.1, harsh=False):
    N = 5000
    M = 200
    rewards = 0
    rwrd_trn = []

    for episode in range(N):
        brd = board()
        rby = robby()

        rwd = 0
        for actions in range(M):
            state = rby.getstate(brd)

            if np.random.uniform(0, 1) < e:
                action = np.random.randint(0, 5)
            else:
                action = np.argmax(q_m[state])
         
            r = rby.act(action, brd) 
            if harsh:
                r -= .5
            rwd += r

            new_state = rby.getstate(brd)
            
            old_val = q_m[state][action]
            best_next = np.argmax(q_m[new_state])
            new_val = old_val + eta*(r + gam*q_m[new_state][best_next] - old_val)

            q_m[state][action] = new_val

        rewards += rwd

        if episode % 50 == 0:
            if e > 0:
                e -= .01

        if episode % 100 == 0:
            rwrd_trn.append(rewards)
            rewards = 0

    return rwrd_trn

def q_test(q_m):
    e = .1
    N = 5000
    M = 200

    avg_rew = []
    std_dev = []

    rewards = np.zeros((100))

    for episode in range(N):
        brd = board()
        rby = robby()

        rwd = 0
        for actions in range(M):
            state = rby.getstate(brd)
            if np.random.uniform(0, 1) < e:
                action = np.random.randint(0, 5)
            else:
                action = np.argmax(q_m[state])
            rwd += rby.act(action, brd)

        rewards[episode % 100] = rwd

        if episode % 100 == 0:
            avg_rew.append(np.mean( rewards ))
            std_dev.append(np.std( rewards ))
            rewards = np.zeros((100))
        
    return avg_rew, std_dev


if __name__ == '__main__':
    y = np.arange(0,50)

    spectrum = [0, .1, .25, .5, .75, .9, 1]


    q_mat = np.zeros((243, 5)) 
    print("GROUND TRUTH FOR ROBBY.")
    plt.xlabel("Episode # (100)")
    plt.ylabel("Rewards")
    q_res = q_learn(q_mat, eta=.2, gam=.9, e=.1, harsh=False)
    plt.plot(y, q_res)
    plt.savefig("ground_train.png", format='png')
    plt.clf()

    print("TESTING GROUND ROBBY.")
    test_avg, test_sd = q_test(q_mat)
    plt.xlabel("Episode #")
    plt.ylabel("Testing Set Average & St. Dev")
    plt.errorbar(y, test_avg, test_sd)
    plt.savefig("ground_test.png", format='png')
    plt.clf()

    q_mat = np.zeros((243, 5)) 
    print("BIG BOARD FOR ROBBY.")
    SIZE = 1000
    plt.xlabel("Episode # (100)")
    plt.ylabel("Rewards")
    q_res = q_learn(q_mat, eta=.2, gam=.9, e=.1, harsh=False)
    plt.plot(y, q_res)
    plt.savefig("big_train.png", format='png')
    plt.clf()

    print("TESTING BIG ROBBY.")
    test_avg, test_sd = q_test(q_mat)
    plt.xlabel("Episode #")
    plt.ylabel("Testing Set Average & St. Dev")
    plt.errorbar(y, test_avg, test_sd)
    plt.savefig("big_test.png", format='png')
    plt.clf()
    SIZE = 10



    """ TESTING ETA VALUES """
    q_mats = []
    print("ETA VALS FOR ROBBY.")
    plt.xlabel("Episode # (100)")
    plt.ylabel("Rewards")
    for eta in spectrum:
        q_mat = np.zeros((243, 5)) 
        print("ETA VAL ", eta)
        q_res = q_learn(q_mat, eta=eta, gam=.9, e=.1, harsh=False)
        plt.plot(y, q_res, label='robby-eta-'+str(eta))
        q_mats.append(q_mat)
    plt.legend()
    plt.savefig("eta_train.png", format='png')
    plt.clf()

    print("Testing ETA Robby.")
    plt.xlabel("Episode #")
    plt.ylabel("Testing Set Average & St. Dev")

    for i in range(len(spectrum)):
        test_avg, test_sd = q_test(q_mats[i])
        plt.errorbar(y, test_avg, test_sd, label='robby-eta-'+str(spectrum[i]))
    plt.savefig("eta_test.png", format='png')
    plt.clf()
   


    """ TESTING GAMMA VALUES """
    q_mats = []
    print("GAMMA VALS FOR ROBBY.")
    plt.xlabel("Episode # (100)")
    plt.ylabel("Rewards")
    for gamma in spectrum:
        q_mat = np.zeros((243, 5)) 
        print("GAMMA VAL ", gamma)
        q_res = q_learn(q_mat, eta=.25, gam=gamma, e=.1, harsh=False)
        plt.plot(y, q_res, label='robby-gamma-'+str(gamma))
        q_mats.append(q_mat)
    plt.legend()
    plt.savefig("gamma_train.png", format='png')
    plt.clf()

    print("Testing GAMMA Robby.")
    plt.xlabel("Episode #")
    plt.ylabel("Testing Set Average & St. Dev")
    for i in range(len(spectrum)):
        test_avg, test_sd = q_test(q_mats[i])
        plt.errorbar(y, test_avg, test_sd, label='robby-gamma-'+str(spectrum[i]))
    plt.savefig("gamma_test.png", format='png')
    plt.clf()



    """ TESTING EPS VALUES """
    q_mats = []
    print("EPS VALS FOR ROBBY.")
    plt.xlabel("Episode # (100)")
    plt.ylabel("Rewards")
    for eps in spectrum:
        q_mat = np.zeros((243, 5)) 
        print("EPS VAL ", eps)
        q_res = q_learn(q_mat, eta=.25, gam=.9, e=eps, harsh=False)
        plt.plot(y, q_res, label='robby-eps-'+str(eps))
        q_mats.append(q_mat)
    plt.legend()
    plt.savefig("eps_train.png", format='png')
    plt.clf()
    print("Testing EPS Robby.")
    plt.xlabel("Episode #")
    plt.ylabel("Testing Set Average & St. Dev")
    for i in range(len(spectrum)):
        test_avg, test_sd = q_test(q_mats[i])
        plt.errorbar(y, test_avg, test_sd, label='robby-eps-'+str(spectrum[i]))
    plt.savefig("eps_test.png", format='png')
    plt.clf()
 
    
    q_mat = np.zeros((243, 5)) 
    print("ROBBY IN HARSH MODE.")
    plt.xlabel("Episode # (100)")
    plt.ylabel("Rewards")
    q_res = q_learn(q_mat, eta = .25, gam=.9, e=.1, harsh=True)
    plt.plot(y, q_res)
    plt.savefig("training_harsh.png", format='png')
    plt.clf()

    print("TESTING HARSH ROBBY.")
    test_avg, test_sd = q_test(q_mat)
    plt.xlabel("Episode #")
    plt.ylabel("Testing Set Average & St. Dev")
    plt.errorbar(y, test_avg, test_sd)
    plt.savefig("testing_harsh.png", format='png')

    plt.clf()

    print("PROGRAM FINISHED.")
  
