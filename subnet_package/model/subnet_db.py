import ipaddress
from .ip_tracker import IP_tracker

class Subnet_DB(object):
  def __init__(self):
    self.subnets = dict() #network string -> IP_tracker
    self.subnets_lst = list() #list of network subnets using ipaddress.IPv4Network()
    #takes more memory but will only have to sort once when adding/deleting

  def add_new_subnet(self, network_str):
    self.subnets[network_str] = IP_tracker(network_str)
    self.subnets_lst.append(network_str)
    self.subnets_lst = sorted(self.subnets_lst)
  
  def delete_subnet(self, net_str):
    del self.subnets[net_str]
    self.subnets_lst.remove(net_str)
