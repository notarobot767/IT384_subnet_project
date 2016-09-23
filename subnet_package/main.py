from .model.model import Model
from .controller.controller import Controller
from .view.view import View
from .misc import misc

def main():
  try:
    _mod = Model()
    ctrl = Controller(_mod)
    view = View(ctrl)

    print(misc.welcome_banner() + "\n")
    #view.text_gui._run_subnet_menu()
    ctrl.add_new_subnet("172.16.0.0/29")
    ctrl.add_new_subnet("172.16.0.0/28")
    ctrl.add_new_subnet("127.16.0.0/28")
    ctrl.add_new_subnet("10.16.0.0/28")
    '''
    print(ctrl.get_subnets_lst())
    ctrl.assign_ip(ctrl.get_tracker(ctrl.get_subnets_lst()[0]), "test_ip")
    print(ctrl.get_hosts_dhcp_unavail(ctrl.get_tracker(ctrl.get_subnets_lst()[0])))
    '''


    view.text_gui.run()
  except KeyboardInterrupt:
    print(misc.cut_sling_load())
  except:
    print("Something went horribly wrong!")