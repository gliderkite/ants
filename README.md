# ants
An [ant colony](http://en.wikipedia.org/wiki/Ant_colony) simulator written in Python.

## How To Play
ants is a [zero-player game](http://en.wikipedia.org/wiki/Zero-player_game), so you can simply start the simulation and enjoy it!

![ants image](http://i58.tinypic.com/b55nqd.jpg)

However it is possible to configure the simulator by editing the program configuration file (config.json). In particular you can change:

1. The colors of ants (foraging or looking for food), nest, food, pheromones and for the background.
2. The world's size (and zoom factor), the ants size, the nest size and location.
3. The time between one birth/death and the next one.
4. Pheromone evaporation speed.
5. Which type of pheromone will be drawn.
6. Initial food quantity and the number of different locations.
7. The behavior of a random ant movment.
8. The ants life expactancy.
9. The quantity of food that must be collected in order to generate a new ant.


## Requirements
In order to play the ants simulator you have to download and install [Python (2.X version)](https://www.python.org/downloads/) and the [wxPython](http://www.wxpython.org/download.php) GUI library.

## Launch the game
Once you have correctly installed wxPython you can simply move to the `src` directory and run the script by typing (on Unix-based systems):
```bash
./wxAntSim.py
```

## The Rules
An ant is an [agent](http://en.wikipedia.org/wiki/Intelligent_agent) whose sole purpose is to collect food and bring it back to the nest. In order to achive this goal ants can be divided in two groups:

1. Ants seeking for food.
2. Ants seeking for the nest.

The former will follow the "food pheromone" and leave the "colony pheromone", the latter will do the opposite, that is to follow the colony pheromone and leave the food pheromone.
The world is represented by a grid, where each cell can be occupied by an ant or by the food. The visibility of an ant is quite limited: it can see only the three cells in front of it, and according to the pheromone intensity it can choose what is the path to follow. If there is no pheromone the ant will move randomly.