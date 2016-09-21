from .model.model import Model
from .controller.controller import Controller
from .view.view import View
from .misc import misc

def main():
  _mod = Model()
  ctrl = Controller(_mod)
  view = View(ctrl)

  print(misc.welcome_banner() + "\n")
  #view.text_gui._run_subnet_menu()
  ctrl.add_new_subnet("172.16.0.0/29")
  print(ctrl.show_subnets())