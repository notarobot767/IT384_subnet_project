from .model.model import Model
from .controller.controller import Controller
from .view.view import View
from .misc import misc

def main(argv):
  _mod = Model(argv)
  ctrl = Controller(_mod)
  view = View(ctrl)

  #test subnets to see working ip_tracker
  #have not yet implemented putting requirements in address block
  for subnet in [
    "172.16.0.0/29",
    "172.16.0.0/28",
    "10.16.0.0/28",
    "10.0.0.0/8",
    "2001:dead:beef::/64"
  ]:
    ctrl.add_new_subnet(subnet)

  print(misc.welcome_banner())
  view.text_gui.run()
