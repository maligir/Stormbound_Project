import numpy as np
from RL import RL
from Unit import Unit


class Player:

    # Builds RL and health and mana of player
    def __init__(self, types):
        self.RL = RL()
        self.exp = 1
        self.health = 10
        self.mana = 10
        self.type = types
        self.deck = []
        self.hand = []

    # Chooses action with RL Class or random action
    def chooseAction(self, state, player):
        if(np.random.rand() < exp):
            return self.RL.randomAction(state, player)
        else:
            (mx, action) = self.RL.getBestAction(state, player)
            return action

    # Creates the starting deck of random cards
    def createDeck(self):
        for i in range(1000):
            self.deck.append(Unit(np.random.randint(
                5), np.random.randint(5), self.type))

    # Adds cards to hand until there are 4
    def drawHand(self):
        while(len(self.hand) < 4):
            self.hand.append(self.deck.pop())

    # Adds to the RL class replay set
    def addReplaySet(self, sets):
        self.RL.updateReplaySet(sets)

    # Reduces exp, allowing model to make more decisions
    def reduceExp(self):
        self.exp = max([.05, .997*self.exp])

    # Updates the parameters of the model
    def update(self, n):
        self.RL.updateParameters(n)

    # Reduces the health of the castle
    def takeDamage(self, damage):
        self.health -= damage

    # Uses Unit cost to reduce player's mana pool for the turn
    def useMana(self, cost):
        self.mana -= cost

    # Returns mana left in player's mana pool
    def getMana(self):
        return self.mana

    # Returns health of player
    def getHealth(self):
        return self.health

    # Returns type of player
    def getType(self):
        return self.type
