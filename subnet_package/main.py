from .model.model import Model
from .controller.controller import Controller
from .view.view import View
from .misc import Misc

def main(argv):
  (requirements, address_space) = argv
  _mod = Model(address_space)
  ctrl = Controller(_mod)
  view = View(ctrl)

  for name, hosts in requirements:
    ctrl.add_new_subnet(hosts, name, True)

  Misc.welcome_banner()
  view.text_gui.run()
