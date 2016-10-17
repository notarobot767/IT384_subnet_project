'''
As the name suggests, the main function. Initializes the model, controller, and view.
Main then launches the view which in this case is a text gui.
'''

from .model.model import Model
from .controller.controller import Controller
from .view.view import View
from .misc import Misc

def main(address_space, requirements=None):
  _mod = Model(address_space) #sending address block to model
  ctrl = Controller(_mod)
  view = View(ctrl)

  if(requirements != None): #checking if requirements argument was passed
    for name, hosts in requirements:
      ctrl.add_new_subnet(hosts, name, True)

  print()
  Misc.welcome_banner()
  view.text_gui.run()
