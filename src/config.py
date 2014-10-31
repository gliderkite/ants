#! /usr/bin/env python
"""Program configuration module."""

import json


def serialize(filename, configuration):
  """Serialize the given configuration."""
  with open(filename, 'w') as f:
    json.dump(configuration, f, indent=2, sort_keys=True)


def deserialize(filename):
  """Deerialize the given file."""
  with open(filename, 'r') as f:
    return json.load(f)


def default():
  config = dict()
  config['world_size'] = 50, 40
  config['nest_location'] = 30, 20
  config['initial_food_quantity'] = 50
  config['max_ants_number'] = 200
  config['step_delay_ms'] = 100
  config['zoom'] = 11
  config['food_places_number'] = 30
  config['food_quantity'] = 25
  config['life_expectancy_steps'] = 1000
  config['food_quantity_per_ant'] = 5
  config['birth_delay_ms'] = 500
  config['death_delay_ms'] = 500
  config['go_straight_probability'] = 0.9
  config['food_pheromone_decreasing_factor'] = 0.01
  config['colony_pheromone_decreasing_factor'] = 0.005
  config['ant_size'] = 5
  config['nest_size'] = 10
  config['pheromone_scale_decreasing_factor'] = 10
  config['draw_colony_pheromone_lifespan'] = True
  config['draw_food_pheromone_lifespan'] = False
  config['colony_pheromone_color'] = 'Red'
  config['food_pheromone_color'] = 'Yellow'
  config['food_color'] = 'Yellow'
  config['nest_color'] = 'Black'
  config['ant_color'] = 'Green'
  config['ant_foraging_color'] = 'Purple'
  config['background_color'] = 'White'
  return 'config.json', config
