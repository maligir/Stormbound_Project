import numpy as np
from Player import Player
from Unit import Unit


class Game:

    #Each player keeps track of their own board : for movement and decision making
    #


    # Defines board, players, and end state
    def __init__(self):
        self.board = np.full((5, 4), None)
        self.end = False
        self.p1 = Player()
        self.p2 = Player()

    # returns the board in a column vector
    def getTable(self):
        s = []
        for i in range(5):
            for j in range(4):
                s.append(self.board[i, j])
        return np.reshape(s, (20, 1))

    # updates the board with the new state
    def createTable(self, s):
        count = 0
        for i in range(5):
            for j in range(4):
                self.board[i, j] = s[count]
                count += 1

    # Sets all spaces on the board to null
    def reset(self):
        self.board = np.full((5, 4), None)
        self.end = False

    # Determines which Unit is stronger and returns the stronger Unit with reduced strength
    def battle(self, ally, enemy):
        if(ally.getStrength() > enemy.getStrength()):
            ally.reduceStrength(enemy.getStrength())
            return ally
        elif(ally.getStrength() < enemy.getStrength()):
            enemy.reduceStrength(ally.getStrength())
            return enemy
        else:
            return None

    # Movement of Enemy Pieces
    def eMovement(self):
        s = self.getTable()
        # Looks through the spaces of the board
        for i in range(20):
            # Determines if space is empty or not
            if not (s[19-i] == None):
                # Determines if the piece is the enemy's
                if(s[19-i].getType() == -1):
                    # If the Unit will move into the castle
                    if(19-i+4 > 19):
                        self.p1.takeDamage(s[19-i].getStrength())
                        s[19-i] = None
                    # If the Unit will move to an empty space
                    elif(s[19-i+4] == None):
                        s[19-i+4] = s[19-i]
                        s[19-i] = None
                    # If the Unit will move to an ally occuppied space
                    elif(s[19-i+4].getType() == 1):
                        s[19-i+4] = self.battle(s[19-i], s[19-i+4])
                        s[19-i] = None
        # Rebuilds the completed movement of the board
        self.createTable(s)
#combine the movements and rotate the board
    def aMovement(self):
        s = self.getTable()
        # Looks through the spaces of the board
        for i in range(20):
            # Determines if space is occuppied
            if not (s[i] == None):
                # Determines if the Unit is an ally
                if(s[i].getType() == 1):
                    # If the Unit will invade the enemy castle
                    if(i-4 < 0):
                        self.p2.takeDamage(s[i].getStrength())
                        s[i] = None
                    # If the Unit will move to an empty space
                    elif(s[i] == None):
                        s[i-4] = s[i]
                        s[i] = None
                    # If the Unit will move to a space occuppied by the enemy
                    elif(s[i-4].getType() == -1):
                        s[i-4] = self.battle(s[i], s[i-4])
                        s[i] = None
        # Rebuilds board after movement phase
        self.createTable(s)

    def updatePlayer1(self):
        reward1 = 0
        reward2 = 0
        count = 0
        self.aMovement()
        s = self.getTable()
        if not self.end:
            # P1 takes action until end of turn
            (turn, action, unit) = self.p1.chooseAction(s)
            while(turn and not self.end):
                s[action] = unit
                self.createTable(s)
                reward1 += self.win1()
                reward2 += self.win2()
                (turn, action, unit) = self.p1.chooseAction(s)
        self.eMovement()
        s = self.getTable()
        if not self.end:
            # P2 takes action until end of turn
            (turn, action, unit) = self.p2.chooseAction(s)
            while (turn and not self.end):
                s[action] = unit
                self.createTable(s)
                reward2 += self.win2()
                reward1 = self.win1()
                (turn, action, unit) = self.p2.chooseAction(s)
                self.createTable(s)
        return (reward1, reward2)

    # Trains the Model
    def train(self):
        reward = 0.0
        # Trains for set of games
        for i in range(2000):
            self.reset()
            # Plays the game while it has not ended and updates replay set
            while not self.end:
                #Move these to update state to account for both players
                cur = self.getTable()
                (reward1, reward2) = self.updateState()
                next = self.getTable()
                self.p1.addReplaySet(
                    (cur, np.reshape(action, (1, 1)), next, reward, self.end))
                #Does this need to be in update state too?
                self.p1.update(10)
                self.p2.update(10)
                print("round", i)
            self.p1.reduceExp()
            self.p2.reduceExp()

    # updates reward for player 1
    def win1(self):
        if(self.p2.getHealth() <= 0):
            self.end = True
            return 1000
        elif(self.p1.getHealth() <= 0):
            self.end = True
            return -1000
        else:
            return 0

    # updates reward for player 2
    def win2(self):
        if(self.p1.getHealth <= 0):
            self.end = True
            return 1
        elif(self.p2.getHealth() <= 0):
            self.end = True
            return -1
        else:
            return 0

    # Tests the Model
    def test(self):
        reward = 0
        expReward = 0
        wins = 0
        losses = 0
        ties = 0
        # Plays set of games to test Model
        for i in range(100):
            self.reset()
            while self.end == False:
                action = self.p1.chooseAction(self.getTable())
                reward = self.updateState(action)
            expReward = expReward+reward
            # Reports the success of the Model Training
            if(reward == 0):
                ties += 1
            if(reward == 1):
                wins += 1
            if(reward == -1):
                losses += 1
            print("Wins ", wins)
            print("Ties ", ties)
            print("Losses ", losses)
            print("Win Rate: ", expReward/100)
