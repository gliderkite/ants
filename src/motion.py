#! /usr/bin/env python
"""Ants simulator motion module."""


import random
import entity



# delta used to move the ant and reach its neighbors (clockwise)
DELTA = (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)


def still(ant):
  """Performs no actions."""
  pass


def turn(ant, steps):
  """Turns the ant changing its direction.
  There are 8 possible directions (as the number of a cell neighbors).
  Negative steps represent a counterclockwise rotation; otherwise positive steps
  represent a clockwise rotation.
  """
  ant.direction = (ant.direction + steps) % 8


def turn_counterclockwise(ant):
  """Turns the ant counterclockwise."""
  turn(ant, -1)


def turn_clockwise(ant):
  """Turns the ant clockwise."""
  turn(ant, 1)


def turn_around(ant):
  """Turns the ant by 180 degrees."""
  turn(ant, 4)


def forward(ant):
  """Moves the ant forward and update the path with pheromone."""
  # update the pheromone only if the ant not already passed through here.
  if ant.location not in ant.path:
    # check if the ant has to back home with food
    if ant.foraging():
      ph = entity.food_strength(ant.world[ant.location])
      if not ph or ph >= len(ant.path):
        # mark with colony pheromone only if we can't worsen the path
        lifespan = entity.food_lifespan(ant.world[ant.location])
        ant.world[ant.location].food_ph[:] = [len(ant.path), lifespan + 1]
    # else if the ant has to find food
    else:
      ph = entity.colony_strength(ant.world[ant.location])
      if not ph or ph >= len(ant.path):
        # mark with colony pheromone only if we can't worsen the path
        lifespan = entity.colony_lifespan(ant.world[ant.location])
        ant.world[ant.location].colony_ph[:] = [len(ant.path), lifespan + 1]
  # update the path
  ant.path.add(ant.location)
  # move forward
  ant.location = ahead(ant)


def cross_path(ant, ph_strength):
  """Returns True if the ant is crossing a normal path with pheromone."""
  path = left(ant), ant.location, right(ant)
  return all(ph_strength(ant.world[l]) > 0 for l in path)


def random_step(ant, go_straight_probability):
  """Perform a random move trying to avoid already followed paths."""
  # perform a random choice
  p = random.random()
  # check if the ant can simply go forward
  if p < go_straight_probability and ahead(ant) not in ant.path:
    forward(ant)
  else:
    glp = go_straight_probability + (1 - go_straight_probability) / 2
    # check if the ant can first turn clockwise
    if p < glp and ahead_left(ant) not in ant.path:
      turn_clockwise(ant)
    # check if the ant can first turn counterclockwise
    elif ahead_right(ant) not in ant.path:
      turn_counterclockwise(ant)
    else:
      # perform a random move
      move = random.choice([turn_clockwise, turn_counterclockwise, still])
      move(ant)
    # always move forward after a turn
    forward(ant)


def fitness_step(ant, fitness, go_straight_probability):
  """Moves the ant according to the fitness function."""
  # ahead cells
  observable = [(ant.direction + x) % 8 for x in range(-1, 2)]
  best, d = None, None
  # search the "best" cell
  for o in observable:
    f, lifespan = fitness(ant.world[neighbor(ant, o)])
    if f > 0 and lifespan > 0 and (not best or f < best):
      # update the best cell
      best = f
      d = o
  # check if one ahead cell (at least) has pheromone
  if d is not None:
    # apply the move to approach the cell with pheromone
    turn(ant, (d - ant.direction) % 8)
    forward(ant)
  else:
    # perform a random choice
    random_step(ant, go_straight_probability)


def neighbor(ant, direction):
  """Get the ant neighbor according to its current location.
  Assume that the board is a torus: http://en.wikipedia.org/wiki/Torus."""
  x, y = ant.location
  width, height = ant.world.size
  dx, dy = DELTA[direction % 8]
  return (x + dx) % width, (y + dy) % height


def ahead(ant):
  """Gets the ant's ahead neighbor."""
  return neighbor(ant, ant.direction)


def ahead_left(ant):
  """Gets the ant's left ahead neighbor."""
  return neighbor(ant, (ant.direction - 1) % 8)


def ahead_right(ant):
  """Gets the ant's left ahead neighbor."""
  return neighbor(ant, (ant.direction + 1) % 8)


def left(ant):
  """Gets the ant's left neighbor."""
  return neighbor(ant, (ant.direction - 2) % 8)


def right(ant):
  """Gets the ant's left neighbor."""
  return neighbor(ant, (ant.direction + 2) % 8)


def back(ant):
  """Gets the ant's back neighbor."""
  return neighbor(ant, ant.direction - 4)