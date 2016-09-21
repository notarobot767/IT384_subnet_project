import ipaddress
from ..model.ip_tracker import IP_tracker
from ..model.model import Model

class Controller(object):
  def __init__(self, Model):
    self._mod = Model
    self._subnet_db = self._mod.subnet_db

  def speak(self):
    print("Hi, I'm the Controller!")

  #subnet_db
  ############################################################
  def get_subnets_lst(self):
    return self._subnet_db.subnets_lst  

  def add_new_subnet(self, net_str):
    self._subnet_db.add_new_subnet(net_str)

  def delete_subnet(self, net_str):
    self._subnet_db.delete_subnet(net_str)

  #ip_tracker
  ############################################################
  def get_tracker(self, subnet):
    return self._subnet_db.subnets[subnet]

  def get_hosts_dhcp_avail(self, tracker):
    return tracker.host_dhcp_avail

  def get_hosts_dhcp_unavail(self, tracker):
    return tracker.host_dhcp_unavail

  def get_hosts_dhcp_reserved(self, tracker):
    return tracker.hosts_dhcp_reserved

  def assign_ip(self, tracker, descript):
    tracker.assign_ip(descript)

