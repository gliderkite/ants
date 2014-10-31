#! /usr/bin/env python

import sys
import os
import wx

import config
import sim
import entity
import motion



# program configuration
configuration = None




class AntSimWindow(wx.Window):
  """Canvas where to draw entities."""

  def __init__(self, parent, update_info):
    """Initializes the window."""
    wx.Window.__init__(self, parent, -1)
    # init properties
    self.SetBackgroundColour(configuration['background_color'])
    self.update = update_info
    self.steps = 0
    # Window event binding
    self.Bind(wx.EVT_PAINT, self.OnPaint)
    # init entities
    size = configuration['world_size']
    nest_loc = tuple(configuration['nest_location'])
    food_qty = configuration['initial_food_quantity']
    self.world = entity.World(size, nest_loc, food_qty)
    food_cardinality = configuration['food_places_number']
    food_qty = configuration['food_quantity']
    sim.place_food(self.world, food_cardinality, food_qty)


  def OnPaint(self, evt):
    """OnPaint event handler."""
    self.DrawEntities(wx.PaintDC(self))

  def DrawEntities(self, dc):
    """set up the device context (DC) for painting"""
    dc.SetPen(wx.Pen('Black', 1, wx.SOLID))
    zoom = configuration['zoom']
    ph_factor = configuration['pheromone_scale_decreasing_factor']
    dcpl = configuration['draw_colony_pheromone_lifespan']
    dfpl = configuration['draw_food_pheromone_lifespan']
    cpc = wx.Brush(configuration['colony_pheromone_color'], wx.SOLID)
    fpc = wx.Brush(configuration['food_pheromone_color'], wx.SOLID)
    fc = wx.Brush(configuration['food_color'], wx.SOLID)
    afc =  wx.Brush(configuration['ant_foraging_color'], wx.SOLID)
    ac =  wx.Brush(configuration['ant_color'], wx.SOLID)
    # draw pheromone
    width, height = self.world.size
    x = 0
    while x < width:
      y = 0
      while y < height:
        # draw colony pheromone lifespan
        colony_ph = entity.colony_lifespan(self.world.cells[x][y])
        if dcpl and colony_ph > 0:
          dc.SetBrush(cpc)
          dc.DrawCircle(x * zoom, y * zoom, colony_ph // ph_factor)
        # draw food pheromone lifespan
        food_ph = entity.food_lifespan(self.world.cells[x][y])
        if dfpl and food_ph > 0:
          dc.SetBrush(fpc)
          dc.DrawCircle(x * zoom, y * zoom, food_ph // ph_factor)
        y += 1
      x += 1
    # draw food
    x = 0
    while x < width:
      y = 0
      while y < height:
        if self.world.cells[x][y].food_quantity > 0:
          dc.SetBrush(fc)
          qty = self.world.cells[x][y].food_quantity
          shift = qty // 2
          dc.DrawRectangle(x * zoom - shift, y * zoom - shift, qty, qty)
        y += 1
      x += 1
    # draw nest
    x, y = self.world.nest
    dc.SetBrush(wx.Brush(configuration['nest_color'], wx.SOLID))
    dc.DrawCircle(x * zoom, y * zoom, configuration['nest_size'])
    # draw ants
    for a in self.world.ants:
      x, y = a.location
      if a.foraging():
        dc.SetBrush(afc)
      else:
        dc.SetBrush(ac)
      dc.DrawCircle(x * zoom, y * zoom, configuration['ant_size'])

  def StartSimulation(self):
    """Resume the simulation."""
    self.Birth()
    self.Run()
    self.Death()

  def Run(self):
    """Move ants to the next generation if the simulation isn't over."""
    gsp = configuration['go_straight_probability']
    fphdf = configuration['food_pheromone_decreasing_factor']
    cphdf = configuration['colony_pheromone_decreasing_factor']
    sim.step(self.world, gsp, cphdf, fphdf)
    # update the status bar
    nest_food = self.world.nest_food_quantity
    world_food = self.world.food_quantity
    self.update(self.steps, len(self.world.ants), nest_food, world_food)
    # check if the simulation is over
    if len(self.world.ants) == 0 or self.world.food_quantity == 0:
      info = 'Steps {}'.format(self.steps)
      wx.MessageBox(info, 'Simulation Over!', wx.OK | wx.ICON_ASTERISK)
      self.GetParent().Destroy()
    else:
      self.steps += 1
      self.Refresh()
      if not self.GetParent().paused:
        wx.CallLater(configuration['step_delay_ms'], self.Run)

  def Birth(self):
    """Check if a new ant can born."""
    food_per_ant = configuration['food_quantity_per_ant']
    max_ants = configuration['max_ants_number']
    sim.birth(self.world, food_per_ant, max_ants)
    if not self.GetParent().paused:
      wx.CallLater(configuration['birth_delay_ms'], self.Birth)

  def Death(self):
    """Check if an ancient ant has to die."""
    sim.death(self.world, configuration['life_expectancy_steps'])
    if not self.GetParent().paused:
      wx.CallLater(configuration['death_delay_ms'], self.Death)



class AntSimFrame(wx.Frame):

  def __init__(self, size, title='Ants', pos=wx.DefaultPosition):
    no_resize = (wx.DEFAULT_FRAME_STYLE ^ 
                (wx.RESIZE_BORDER | wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX))
    wx.Frame.__init__(self, None, -1, title, pos, size, style=no_resize)
    # init properties
    self.RUN_ID = 1
    self.paused = True
    # init widgets
    self.InitStatusBar()
    #self.InitMenuBar()
    self.InitToolBar()
    self.window = AntSimWindow(self, self.UpdateStatusBar)


  def InitStatusBar(self):
    """Create and initialized the statusbar."""
    self.statusbar = self.CreateStatusBar()
    self.statusbar.SetFieldsCount(4)

  def UpdateStatusBar(self, gen, ants, nest_food, world_food):
    self.statusbar.SetStatusText('Steps: {}'.format(gen), 0)
    self.statusbar.SetStatusText('Ants: {}'.format(ants), 1)
    self.statusbar.SetStatusText('Nest food: {}'.format(nest_food), 2)
    self.statusbar.SetStatusText('Food left: {}'.format(world_food), 3)

  def InitToolBar(self):
    """Create and initialized the statusbar."""
    self.toolbar = self.CreateToolBar()
    fn = os.path.join(os.path.dirname(__file__), '../img/play.png')
    img = wx.Image(fn, wx.BITMAP_TYPE_ANY)
    img = img.Scale(40, 40, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
    item = self.toolbar.AddSimpleTool(self.RUN_ID, img, 'Run')
    self.Bind(wx.EVT_MENU, self.Run, item)
    self.toolbar.Realize()

  def Run(self, evt):
    """Run the simulation."""
    if self.paused:
      self.paused = False
      self.window.StartSimulation()
      fn = os.path.join(os.path.dirname(__file__), '../img/pause.png')
      img = wx.Image(fn, wx.BITMAP_TYPE_ANY)
      img = img.Scale(40, 40, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
      self.toolbar.SetToolNormalBitmap(id=self.RUN_ID, bitmap=img)
    else:
      self.paused = True
      fn = os.path.join(os.path.dirname(__file__), '../img/play.png')
      img = wx.Image(fn, wx.BITMAP_TYPE_ANY)
      img = img.Scale(40, 40, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
      self.toolbar.SetToolNormalBitmap(id=self.RUN_ID, bitmap=img)



class AntSimApp(wx.App):

  def OnInit(self):
    w, h = configuration['world_size']
    zoom = configuration['zoom']
    self.frame = AntSimFrame(size=(w * zoom, h * zoom))
    self.frame.Show()
    self.SetTopWindow(self.frame)
    return True



if __name__ == '__main__':
  # check if a program configuration file is provided
  if len(sys.argv) > 1:
    configuration = config.deserialize(sys.argv[1])
  elif os.path.isfile('config.json'):
    configuration = config.deserialize('config.json')
  else:
    # use default configuration
    _, configuration = config.default()
  #filename, configuration = config.default()
  #config.serialize(filename, configuration)
  app = AntSimApp()
  app.MainLoop()
