#! /usr/bin/env python
"""Ants simulator behavior module."""


import motion



def take_food(ant):
  """Takes the food_quantity in the current location if any."""
  here = ant.world[ant.location]
  # check if the cell contains food
  if here.food_quantity > 0 and ant.location != ant.world.nest:
    # take the food
    here.food_quantity -= 1
    ant.food_quantity += 1
    # clear history and go back
    ant.path.clear()
    motion.turn_around(ant)
    return True


def approach_food(ant):
  """Moves the ant ahead if that cell contains food."""
  for d in ((ant.direction + x) % 8 for x in range(-1, 2)):
    idx = motion.neighbor(ant, d)
    cell = ant.world[idx]
    if cell.food_quantity > 0 and idx != ant.world.nest:
      motion.turn(ant, (d - ant.direction) % 8)
      motion.forward(ant)
      return True


def seek_food(ant, gsp):
  """Tries to approach the ant to a cell with food."""
  # check if the current cell contains food_quantity
  if not take_food(ant):
    # check if the cell in front contains food_quantity
    if not approach_food(ant):
      # moves the ant according to its neighbors food fitness
      motion.fitness_step(ant, lambda c: c.food_fitness(), gsp)


def drop_food(ant):
  """Drops the ant's food if it's in its nest."""
  if ant.location == ant.world.nest:
    # drop the food in the nest
    ant.world.nest_food_quantity += ant.food_quantity
    ant.world.food_quantity -= ant.food_quantity
    ant.food_quantity = 0
    # clear history and go back
    ant.path.clear()
    motion.turn_around(ant)
    return True


def approach_nest(ant):
  """Moves the ant ahead if that cell is its nest."""
  # check if the cell in front is the ant's nest
  for d in ((ant.direction + x) % 8 for x in range(-2, 3)):
    if motion.neighbor(ant, d) == ant.world.nest:
      motion.turn(ant, (d - ant.direction) % 8)
      motion.forward(ant)
      return True


def seek_nest(ant, gsp):
  """Tries to approach the ant to its own nest."""
  # check if the current cell is the nest
  if not drop_food(ant):
    # check if the nest is ahead
    if not approach_nest(ant):
      # moves the ant according to its neighbors nest fitness
      motion.fitness_step(ant, lambda c: c.nest_fitness(), gsp)


def act(ant, go_straight_probability):
  """Perform a new action according to the current ant status."""
  # acts according to the current ant status
  if ant.foraging():
    seek_nest(ant, go_straight_probability)
  else:
    seek_food(ant, go_straight_probability)
  # get older
  ant.age += 1
