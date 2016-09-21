from .model.model import Model
from .controller.controller import Controller
from .view.view import View

def main():
  _mod = Model()
  ctrl = Controller(_mod)
  view = View(ctrl)

  view.text_gui.run()