#! /usr/bin/env python
"""Ants simulator module."""


import random
import entity
import behavior



def place_food(world, cardinality, quantity):
  """Place some food in random cells of the world."""
  world.food_quantity = cardinality * quantity
  width, height = world.size
  i = 0
  while i < cardinality:
    loc = random.randrange(0, width), random.randrange(0, height)
    if loc != world.nest:
      world[loc].food_quantity += quantity
    else:
      world.nest_food_quantity += quantity
      world.food_quantity -= quantity
    i += 1


def birth(world, food_qty, upper_bound=None, direction=None):
  """Add a new ant if possible."""
  # check if the number of current ants is lower of the upper bound
  if not upper_bound or len(world.ants) < upper_bound:
    # check if the nest has enough food
    if world.nest_food_quantity >= food_qty:
      verse = direction or random.randrange(0, 8)
      world.nest_food_quantity -= food_qty
      world.ants.append(entity.Ant(world, verse))


def death(world, life_expectancy):
  """Kill an ald ant."""
  # get the ants too old
  ancients = [a for a in world.ants if a.age > life_expectancy]
  if ancients:
    # random choice of the dying ant
    dying = random.choice(ancients)
    # drop the food of the dying ant
    if dying.location == world.nest:
      world.nest_food_quantity += dying.food_quantity
      world.food_quantity -= dying.food_quantity
    else:
      world[dying.location].food_quantity += dying.food_quantity
    world.ants.remove(dying)


def evaporate(world, colony_ph_factor, food_ph_factor):
  width, height = world.size
  x = 0
  while x < width:
    y = 0
    while y < height:
      if entity.colony_lifespan(world.cells[x][y]) > 0:
        world.cells[x][y].colony_ph[1] -= colony_ph_factor
      if entity.food_lifespan(world.cells[x][y]) > 0:
        world.cells[x][y].food_ph[1] -= food_ph_factor
      y += 1
    x += 1


def step(world, gsp, cphdf, fphdf):
  """Move all the ants forward to the next generation."""
  for a in world.ants:
    behavior.act(a, gsp)
  # simulate pheromone evaporation
  evaporate(world, cphdf, fphdf)
