#! /usr/bin/env python
"""Ants simulator entities module."""



def food_lifespan(cell):
  """Gets the food pheromone lifespan."""
  return cell.food_ph[1]


def food_strength(cell):
  """Gets the food pheromone strength."""
  return cell.food_ph[0]


def colony_lifespan(cell):
  """Gets the colony pheromone lifespan."""
  return cell.colony_ph[1]


def colony_strength(cell):
  """Gets the colony pheromone strength."""
  return cell.colony_ph[0]



class Cell:
  """Represents a single cell."""

  def __init__(self, food_quantity=0):
    """Creates and initializes the Cell instance."""
    self.food_quantity = food_quantity
    # strength - lifespan
    self.food_ph = [0, 0]
    self.colony_ph = [0, 0]

  def food_fitness(self):
    """Cell fitness for an ant seeking for food."""
    return self.food_ph

  def nest_fitness(self):
    """Cell fitness for an ant seeking for its own nest."""
    return self.colony_ph



class World:
  """Represents the entire world where the simulation takes place.
  Assume that the board is a torus: http://en.wikipedia.org/wiki/Torus."""

  def __init__(self, size, nest_location, nest_food_quantity):
    """Creates and initializes the World instance."""
    # build the grid
    self.size = size
    self.nest = nest_location
    width, height = size
    self.cells = [[Cell() for _ in range(height)] for _ in range(width)]
    self.ants = []
    self.food_quantity = 0
    self.nest_food_quantity = nest_food_quantity
    x, y = nest_location

  def __getitem__(self, location):
    """Gets the cell in location."""
    x, y = location
    width, height = self.size
    return self.cells[x % width][y % height]

  def __setitem__(self, location, value):
    """Sets the cell in location."""
    x, y = location
    width, height = self.size
    self.cells[x % width][y % height] = value



class Ant:
  """Represents a single ant."""

  def __init__(self, world, direction):
    """Creates and initializes the Ant instance."""
    self.world = world
    self.location = tuple(world.nest)
    self.direction = direction
    self.path = set()
    self.food_quantity = 0
    self.age = 0


  def foraging(self):
    """Returns True if the ant's bringing some food, otherwise False."""
    return self.food_quantity > 0
