from ..controller.controller import Controller
from .text_gui import Text_GUI

class View(object):
  def __init__(self, controller):
    self.ctrl = controller
    self.text_gui = Text_GUI(self.ctrl)

  def speak(self):
    print("Hi, I'm the view!")