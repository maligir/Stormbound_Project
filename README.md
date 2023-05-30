# Stormbound_Project

## Overview
Game-Bot is a reinforcement learning-based game bot designed for a strategy card game. The game consists of two players, each with a set of units. The players' decks are composed of these units, each with specific strength, mana cost, and type (ally or enemy). 

The bot makes use of reinforcement learning to make strategic choices during gameplay, progressively improving its decision-making capabilities over time through the collection and analysis of its experiences (replays). 

## Files
This repository consists of the following python files:

1. `Unit.py` - Defines the `Unit` class which represents individual units in the game. 
2. `RL.py` - Defines the `RL` class which implements the reinforcement learning aspect of the game bot.
3. `Player.py` - Defines the `Player` class which represents a player in the game.
4. `Game.py` - Defines the `Game` class which represents the main game loop and mechanics.
5. `GUI.py` - Defines the `GUI` class which manages the graphical user interface for the game.
6. `Cards.py` - Defines the `Cards` class, representing the individual cards (units) that players use in the game.
7. `Board.py` - Defines the `Board` class which manages the game board where players place their cards.

## Details

### Unit.py
This module implements the Unit class. Each unit has attributes such as strength, mana cost, and type. 

### RL.py
This is where the reinforcement learning model resides. It consists of a neural network model, defined and trained using TensorFlow. The RL class also has several methods which perform various tasks, such as performing a random action, updating the replay set, performing gradient descent, updating parameters, etc.

### Player.py
The Player class represents a player in the game. Each player has a deck of units and a hand of units which they can play. The player class uses the RL class to choose actions and make decisions.

### Game.py
The Game class represents the actual game mechanics and loops. It initializes two players and handles the gameplay turns, interactions, and game state updates.

### GUI.py
The GUI module houses the graphical user interface for the game. It is responsible for displaying game elements and rendering visual updates on the screen.

### Cards.py
The Cards module defines the individual cards that players can play in the game. Each card is associated with a specific unit and has its attributes.

### Board.py
The Board module is responsible for managing the game board. It tracks the placement of cards, oversees the battlefield, and helps determine the state of the game.

## Requirements
- Python 3.7+
- TensorFlow 2.4+
- Numpy

## Installation
You can install the required packages by running:
```
pip install tensorflow numpy
```
## Running
To run the game, simply run the `Game.py` file:
```
python Game.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
