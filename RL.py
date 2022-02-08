import numpy as np
import tensorflow as tf


class RL:
    def __init__(self):
        self.replaySet = []
        self.gamma = .99
        self.alpha = .8
        # tf.keras.backend.set_floatx('float64')
        self.model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(20, activation='relu', input_shape=(10,)),
            tf.keras.layers.Dense(20, activation='relu'),
            tf.keras.layers.Dense(1)
        ])
        loss_fn = tf.keras.losses.MeanSquaredError()
        self.model.compile(optimizer='adam',
                           loss=loss_fn,
                           metrics=[tf.keras.metrics.MeanSquaredError()])

# check to see if passed by reference or value
    def randomAction(self, state, player):
        mana = player.mana
        rand = [-1, -1, -1, -1]
        # checks to see if there are any available spaces
        for i in range(4):
            available = False
            for j in range(self.getSpaces(state, player)):
                if(state[j] == None):
                    available = True
                    break
            if(available == False):
                return rand
            if(np.random.random() < .5 and player.hand[i].cost() < mana):
                rand[i] = np.random.randint(20)
                while(state[rand] != None or rand[i] >= self.getSpaces(state, player)):
                    rand[i] = np.random.randint(20)
                state[rand[i]] = player.hand[i]
                mana = mana-player.hand[i].cost()
        return rand

    def updateReplaySet(self, sets):
        size = len(self.replaySet)
        if size > 1000:
            self.replaySet.pop(0)
        self.replaySet.append(sets)

    def gradientDescent(self, s, a, y):
        self.model.fit([s, a], y, epochs=1)

    def updateParameters(self, n):
        rand = np.random.randint(0, len(self.replaySet), n)
        y = np.zeros((n, 1))
        x = []
        for i in range(n):
            (cur, action, next, reward, terminal) = self.replaySet[rand[i]]
            v = np.vstack((cur, action))
            if i == 0:
                x = v.T
            else:
                x = np.vstack((x, v.T))

            (value, act) = self.getBestAction(next)
            if(terminal == True):
                y[i] = (reward)
            else:
                y[i] = self.alpha * (reward + self.gamma * value) + \
                    (1-self.alpha) * self.model(v.T)
        self.model.fit(x=x, y=y, epochs=1, verbose=0)

    # returns available spaces to place unit
    def getSpaces(self, state, player):
        for i in range(20):
            if(state[19-i].getType() == player.getType()):
                if(19-i >= 16):
                    return 16
                else:
                    return int((19-i)/4) * 4+4

    # returns best action
    # experiment with variables and state representation to make AI better
    def getBestAction(self, s, player):
        # create array from -1 to getSpaces
        stren = np.zeros(len(s))
        for i in range(len(s)):
            if(s[i] == None):
                stren[i] = 0
            elif(player.getType() == s[i].getType()):
                stren[i] = s[i].getStrength()
            else:
                stren[i] = -s[i].getStrength()
        spaces = self.getSpaces()
        mx = np.NINF
        bestA = [-1, -1, -1, -1]
        for i in range(-1, spaces):
            for j in range(-1, spaces):
                for k in range(-1, spaces):
                    for l in range(-1, spaces):
                        # check if i,j,k,l is a valid action
                        # evaluate nn at each possible action
                        cost = 0
                        if(i >= 0):
                            if not(s[i] == None):
                                continue
                            cost += player.hand[0].getMana()
                        if(j >= 0):
                            if (not(s[j] == None) and not(i == j)):
                                continue
                            cost += player.hand[1].getMana()
                        if(k >= 0):
                            if (not(s[k] == None) and not(i == k) and not(j == k)):
                                continue
                            cost += player.hand[2].getMana()
                        if(l >= 0):
                            if (not(s[l] == None) and not(i == l) and not(j == l) and not(k == l)):
                                continue
                            cost += player.hand[3].getMana()
                        if(cost <= player.getMana()):
                            v = np.vstack((stren, player.hand[0].getStrength(), player.hand[1].getStrength(
                            ), player.hand[2].getStrength(), player.hand[3].getStrength(), i, j, k, l))
                            res = self.model(v.T)
                            m = np.asscalar(res.numpy())
                            if(m > mx):
                                mx = m
                                bestA[0] = i
                                bestA[1] = j
                                bestA[2] = k
                                bestA[3] = l
        return mx, bestA
