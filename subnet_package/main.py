from .model.model import Model
from .controller.controller import Controller
from .view.view import View
from .misc import Misc

def main(argc, argv):
  _mod = Model(argv[0]) #sending address block to main
  ctrl = Controller(_mod)
  view = View(ctrl)

  if(argc == 2): #checking if requirements argument was passed
    for name, hosts in argv[1]:
      ctrl.add_new_subnet(hosts, name, True)

  Misc.welcome_banner()
  view.text_gui.run()
