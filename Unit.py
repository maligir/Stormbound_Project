class Unit:

    # Builds Units Stats
    def __init__(self, strength, mana, types):
        self.strength = strength
        self.mana = mana
        self.type = types

    # Returns strength of Unit
    def getStrength(self):
        return self.strength

    # Returns initial movement speed of Unit
    def getMovement(self):
        return self.movement

    # Unit takes damage - reduce strength of Unit
    def reduceStrength(self, damage):
        self.strength -= damage

    # Returns cost of Unit
    def getMana(self):
        return self.mana

    # Returns the side the unit is on - ally or enemy
    def getType(self):
        return self.type
