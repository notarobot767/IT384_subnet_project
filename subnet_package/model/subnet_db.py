import ipaddress
from .ip_tracker import IP_tracker

class Subnet_DB(object):
  def __init__(self):
    self.subnets = dict()
    self.subnets_lst = list()

  def add_new_subnet(self, network_str):
    self.subnets[network_str] = IP_tracker(network_str)
    self.subnets_lst.append(network_str)
    self.subnets_lst = sorted(self.subnets_lst,
      key=lambda x: (ipaddress.IPv4Network(x).network_address))
  
  def delete_subnet(self, net_str):
    del self.subnets[net_str]
    self.subnets_lst.remove(net_str)
