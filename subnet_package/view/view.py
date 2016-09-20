from ..controller.controller import Controller

class View(object):
  def __init__(self, controller):
    self.ctrl = controller

  def speak(self):
    print("Hi, I'm the view!")