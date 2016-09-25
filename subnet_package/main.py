from .model.model import Model
from .controller.controller import Controller
from .view.view import View
from .misc import misc

def main():
  try:
    _mod = Model()
    ctrl = Controller(_mod)
    view = View(ctrl)

    for subnet in [
      "172.16.0.0/29",
      "172.16.0.0/28",
      "10.16.0.0/28"
    ]:
      ctrl.add_new_subnet(subnet, True)

    print(misc.welcome_banner())
    view.text_gui.run()

  except KeyboardInterrupt:
    print(misc.cut_sling_load())
  #except:
    #print("Something went horribly wrong!")