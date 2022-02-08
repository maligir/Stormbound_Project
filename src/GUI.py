from tkinter import *
from time import *
from PIL import Image, ImageTk


class GUI:
    def __init__(self):
        self.window = Tk()
        self.window.geometry('1366x768')
        self.cards = []
        self.cardCoords = []
        self.eCards = []
        self.eCardCoords = []
        self.selectedCard = None
        self.units = []
        self.eUnits = []
        self.unitCoords = []
        self.eUnitCoords = []
        self.xVar = 0
        self.yVar = 0
        self.health = 10
        self.eHealth = 10
        self.mana = 10
        self.eMana = 10

    def addImage(self, fileName, w, h):
        im = Image.open(fileName)
        im = im.resize((w, h), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(im)
        label = Label(self.window, image=img)
        label.image = img
        return label

    def moveCard(self, index, speedx, speedy, length):
        for i in range(length):
            (x, y) = self.cardCoords[index]
            label = self.cards[index]
            label.place(x=x+speedx, y=y+speedy)
            self.window.update()
            self.__updateCardCoords(index, x+speedx, y+speedy)
            sleep(.01)

    def moveECard(self, index, speedx, speedy, length):
        for i in range(length):
            (x, y) = self.eCardCoords[index]
            label = self.eCards[index]
            label.place(x=x+speedx, y=y+speedy)
            self.window.update()
            self.__updateECardCoords(index, x+speedx, y+speedy)
            sleep(.01)

    def addCard(self, fileName, x, y):
        label = self.addImage(fileName, 100, 170)
        label.place(x=x, y=y)
        self.cardCoords.append((x, y))
        self.cards.append(label)
        self.cards[self.cards.index(label)].bind(
            "<Button-1>", lambda e: self.__bindCard(e, label=self.cards[self.cards.index(label)]))

    def addECard(self, fileName, x, y):
        label = self.addImage(fileName, 100, 170)
        label.place(x=x, y=y)
        self.eCardCoords.append((x, y))
        self.eCards.append(label)

    def __addUnit(self, fileName, x, y):
        unit = self.addImage(fileName, 50, 50)
        unit.place(x=x, y=y)
        self.units.append(unit)
        self.unitCoords.append((x, y))
        self.useMana()
        if(self.mana <= 1):
            self.mana = 10
            self.crop.unbind('<Button-1>')
            self.eTurn = self.addImage("eTurn.png", 200, 50)
            self.eTurn.place(x=1000, y=100)
            self.enemyTurn()
            self.m.config(text=self.mana)
            self.updateGame()

    def useMana(self):
        self.mana -= 2
        self.m.config(text=self.mana)
        self.updateGame()

    def useEMana(self):
        self.eMana -= 2
        self.eM.config(text=self.eMana)
        self.updateGame()

    def begGame(self):
        board = self.addImage("Board.png", 1366, 740)
        board.place(x=0, y=0)
        self.crop = self.addImage("crop.png", 300, 310)
        self.crop.place(x=535, y=170)
        self.xVar = 535
        self.yVar = 170
        turn = self.addImage("turn.png", 200, 50)
        turn.bind('<Button-1>', self.__nextTurn)
        turn.place(x=1000, y=100)
        self.crop.bind('<Button-1>', self.__placeUnit)
        self.addImage("deck.png", 100, 170).place(x=1250, y=550)
        self.addImage("deck.png", 100, 170).place(x=15, y=15)
        self.addImage("mana.png", 50, 50).place(x=530, y=15)
        self.addImage("mana.png", 50, 50).place(x=770, y=670)
        self.h = Label(self.window, text=self.health, font=("Courier", 20))
        self.eH = Label(self.window, text=self.eHealth, font=("Courier", 20))
        self.h.place(x=666, y=490)
        self.eH.place(x=666, y=20)
        self.m = Label(self.window, text=self.mana, font=("Courier", 10))
        self.eM = Label(self.window, text=self.eMana, font=("Courier", 10))
        self.m.place(x=785, y=680)
        self.eM.place(x=545, y=25)
        # place both labels

    def __nextTurn(self, event):
        self.crop.unbind('<Button-1>')
        self.eTurn = self.addImage("eTurn.png", 200, 50)
        self.eTurn.place(x=1000, y=100)
        self.enemyTurn()

    def __damage(self, y, index):
        if(y <= 170):
            self.eHealth -= 1
            self.units[index].destroy()
            self.unitCoords.pop(index)
            self.eH.config(text=self.eHealth)
            self.updateGame()
            if(self.eHealth <= 0):
                self.crop.destroy()
                Label(self.window, text="You Win", font=(
                    "Courier", 100)).place(x=500, y=300)

    def __eDamage(self, y, index):
        if(y >= 480):
            self.health -= 1
            self.h.set(self.health)
            self.eUnits[index].destroy()
            self.eUnitCoords.pop(index)
            self.eH.config(text=self.health)
            self.updateGame()
            if(self.health <= 0):
                self.crop.destroy()
                Label(self.window, text="You Lose", font=(
                    "Courier", 100)).place(x=500, y=300)

    def rebind(self):
        self.crop.bind('<Button-1>', self.__placeUnit)

    def __moveUnit(self):
        for index in range(len(self.units)):
            for i in range(60):
                lab = self.units[index]
                (x, y) = self.unitCoords[index]
                lab.place(x=x, y=y-1)
                self.window.update()
                self.__updateUnitCoords(index, x, y-1)
                sleep(.01)
            self.__damage(y, index)

    def __moveEUnit(self):
        for index in range(len(self.eUnits)):
            for i in range(60):
                lab = self.eUnits[index]
                (x, y) = self.eUnitCoords[index]
                lab.place(x=x, y=y+1)
                self.window.update()
                self.__updateEUnitCoords(index, x, y+1)
                sleep(.01)
            self.__eDamage(y, index)

    def enemyTurn(self):
        self.__moveEUnit()
        # computer makes moves
        self.eTurn.destroy()
        self.rebind()
        self.__moveUnit()

    def __placeUnit(self, event):
        if(self.selectedCard == None):
            pass
        else:
            self.__addUnit("gr.png", self.__unitX(
                event.x), self.__unitY(event.y))
            self.selectedCard = None

    def __unitX(self, x):
        if(x > 225):
            return 225+self.xVar+4
        elif(x > 150):
            return 150+self.xVar+8
        elif(x > 75):
            return 75+self.xVar+12
        else:
            return 0+self.xVar+14

    def __unitY(self, y):
        if(y > 248):
            return 248+self.yVar+5
        elif(y > 186):
            return 186+self.yVar+8
        elif(y > 124):
            return 124+self.yVar+8
        elif(y > 62):
            return 62+self.yVar+10
        else:
            return 0+self.yVar+12

    def __bindCard(self, event, label=None):
        if(self.selectedCard == None):
            self.selectedCard = label
        else:
            self.selectedCard = None

    def __createUnit(self):
        self.addImage()

    def __updateCardCoords(self, index, x, y):
        self.cardCoords[index] = (x, y)

    def __updateECardCoords(self, index, x, y):
        self.eCardCoords[index] = (x, y)

    def __updateUnitCoords(self, index, x, y):
        self.unitCoords[index] = (x, y)

    def __updateEUnitCoords(self, index, x, y):
        self.eUnitCoords[index] = (x, y)

    def updateGame(self):
        self.window.update()

    def run(self):
        self.window.mainloop()
