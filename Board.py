import numpy as np
from Player import Player
from Unit import Unit


class Game:

    # Each player keeps track of their own board : for movement and decision making
    #

    # Defines board, players, and end state
    def __init__(self):
        self.board = np.full((5, 4), None)
        self.end = False
        self.p1 = Player(True)
        self.p2 = Player(False)
        self.dMult = 10
        self.rMult = 2
        self.p1.createDeck()

    # returns the board in a column vector
    def getTable(self, b):
        s = []
        if(b):
            for i in range(5):
                for j in range(4):
                    s.append(self.board[i, j])
        else:
            for i in range(5):
                for j in range(4):
                    s.append(self.board[4-i, j])
        return np.reshape(s, (20, 1))

    # updates the board with the new state
    def createTable(self, s, b):
        count = 0
        if(b):
            for i in range(5):
                for j in range(4):
                    self.board[i, j] = s[count]
                    count += 1
        else:
            for i in range(5):
                for j in range(4):
                    self.board[4-i, j] = s[count]
                    count += 1

    # Sets all spaces on the board to null

    def reset(self):
        self.board = np.full((5, 4), None)
        self.end = False

    # Determines which Unit is stronger and returns the stronger Unit with reduced strength
    def battle(self, ally, enemy):
        if(ally.getStrength() > enemy.getStrength()):
            ally.reduceStrength(enemy.getStrength())

            return (ally, enemy.getStrength())
        elif(ally.getStrength() < enemy.getStrength()):
            enemy.reduceStrength(ally.getStrength())
            return (enemy, -ally.strength())
        else:
            return None

    def movement(self, player):
        damage = 0
        reward = 0
        s = self.getTable(player.getType())
        # Looks through the spaces of the board
        for i in range(20):
            # Determines if space is occuppied
            if not (s[i] == None):
                # If the Unit will invade the enemy castle
                if(i-4 < 0):
                    damage += s[i].getSterngth()
                    s[i] = None
                    # If the Unit will move to an empty space
                elif(s[i] == None):
                    s[i-4] = s[i]
                    s[i] = None
                    # If the Unit will move to a space occuppied by the enemy
                elif not (s[i-4].getType() == player.getType()):
                    (unit, destroyed) = self.battle(s[i], s[i-4])
                    reward += destroyed
                    s[i-4] = unit
                    s[i] = None
        # Rebuilds board after movement phase
        self.createTable(s, player.getType())
        return damage*self.dMult + reward*self.rMult

    def placeUnits(self, action, player):
        if not self.end:
            s = self.getTable(player.getType())
            for i in range(4):
                if(action[i] > -1):
                    s[action[i]] = player.hand[i]
            self.createTable(s, player.getType())
            player.drawHand()

    def updateState(self, player):
        reward = self.win(player)
        if not self.end:
            reward += self.movement(player)
        return reward

    # Trains the Model
    def train(self):
        reward = 0
        cur2 = []
        action2 = []
        next2 = []
        reward2 = 0
        for i in range(5100):
            first = 0
            self.reset()
            while self.end == False:
                # for p1
                cur = self.getTable(p1.getType())
                action = self.p1.chooseAction(self.getTable(p1.getType()))
                self.placeUnits(action, p1)
                reward = self.updateState(p1)
                next = self.getTable(p1.getType())
                if(first < 1):
                    first += 1
                else:
                    self.p2.addReplaySet(
                        (cur2, np.reshape(action2, (4, 1)), next2, reward2-reward, self.end))
                    self.p2.update(10)
                if(self.end):
                    break
                # for p2
                cur2 = self.getTable(p2.getType())
                action2 = self.p2.chooseAction(self.getTable(p2.getType()))
                self.placeUnits(action2, p2)
                reward2 = self.updateState(p2)
                next2 = self.getTable(p2.getType())
                self.p1.addReplaySet(
                    (cur, np.reshape(action, (4, 1)), next, reward-reward2, self.end))
                self.p1.update(10)
            print("round", i)
            self.p1.reduceExp()
            self.p2.reduceExp()

    # returns reward of winning
    def win(self, player):
        side = -1
        if(player.getType()):
            side = 1
        if(p1.getHealth <= 0):
            self.end = True
            return -1000 * side
        elif(p2.getHealth <= 0):
            self.end = True
            return 1000 * side
