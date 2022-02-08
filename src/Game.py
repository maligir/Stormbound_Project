from GUI import GUI
from Cards import Cards
from Player import Player


class Game:
    def __init__(self):
        self.deck1 = []
        self.hand1 = []
        self.player1 = Player(10, 10)
        self.board1 = []
        self.deck2 = []
        self.hand2 = []
        self.player2 = Player(10, 10)
        self.board2 = []
        self.gui = GUI()

    def createGUI(self):
        self.gui.begGame()

    def createDeck(self):
        for i in range(20):
            self.deck1.append(Cards(2))
            self.deck2.append(Cards(2))

    def startGame(self):
        for i in range(4):
            self.hand1.append(self.deck1.pop(i))
            self.hand2.append(self.deck2.pop(i))
            self.gui.addCard("sad.png", 1250, 550)
            self.gui.moveCard(i, -4-i*4, 0, 25)
            self.gui.addECard("deck.png", 15, 15)
            self.gui.moveECard(i, 4+i*4, 0, 25)

    def runGame(self):
        self.gui.run()
