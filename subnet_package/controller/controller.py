import ipaddress
from ..model.ip_tracker import IP_tracker
from ..model.model import Model

class Controller(object):
  def __init__(self, Model):
    self._mod = Model
    self._subnet_db = self._mod.subnet_db

  def speak(self):
    print("Hi, I'm the Controller!")

  #shows
  def show_subnets(self):
    #ans_str = _poundWord("Subnets")
    ans_str = "Subnets"
    ans_str += "\nFound {} subnet(s):\n".format(len(self._subnet_db.subnets_lst))
    i = 1
    #print(self.subnet_lst)
    for net in self._subnet_db.subnets_lst:
      ans_str += "[{}] - {}\n".format(i, net)
      i += 1
    ans_str += "[{}] - Go back".format(i)
    print(ans_str)
    return i


  #adding new subnet
  def add_new_subnet(self, net_str):
    self._subnet_db.subnets[net_str] = IP_tracker(net_str)
    self._subnet_db.subnets_lst.append(net_str)
    self._subnet_db.subnets_lst = sorted(self._subnet_db.subnets_lst,
      key=lambda x: (ipaddress.IPv4Network(x).network_address))
