from .model.model import Model
from .controller.controller import Controller
from .view.view import View

class Main(object):
  def __init__(self):
    self.mod = Model()
    self.ctrl = Controller(self.mod)
    self.view = View(self.ctrl)

  def speak(self):
    print("Hi, I'm the Main!")