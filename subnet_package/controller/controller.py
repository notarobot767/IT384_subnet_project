import ipaddress
#from ..model.ip_tracker import IP_tracker
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

  def isValidNetwork(self, net_str):
    net_str = net_str.strip()
    if ":" in net_str:
      print("Only IPv4 networks only!\n")
      return (False, False)
    else:
      try:
        network = ipaddress.IPv4Network(net_str)
        cidr = int(net_str.split("/")[1])
        if cidr > 30 or cidr < 24:
          print("CIDR mask must be between 24 and 30 inclusive!\n")
          return (False, False)
        else:
          return (True, network)
      except ValueError:
        print("Not a vaild network!\n<usage> [IPv4 network address]/[CIDR]\n")
        return (False, False)

  def add_new_subnet(self, net_str):
    (isValid, net) = self.isValidNetwork(net_str)
    if isValid:
      net_str = str(net)
      if net_str in self._subnet_db.subnets:
        print("Network '{}' already exists!\n".format(net_str))
      else:
        self._subnet_db.add_new_subnet(net_str)
        print("Network '{}' successfully added!\n".format(net_str))
    
  def delete_subnet(self):
    print("method has been depreciated!\n")
    #self._subnet_db.delete_subnet(net_str)

  #ip_tracker
  ############################################################
  def get_tracker(self, subnet):
    return self._subnet_db.subnets[subnet]

  def get_hosts_dhcp_avail(self, tracker):
    return tracker.host_dhcp_avail

  def get_hosts_dhcp_unavail(self, tracker):
    return tracker.host_dhcp_unavail

  def get_hosts_dhcp_reserved(self, tracker):
    return tracker.host_dhcp_reserved

  def get_device_info(self, tracker):
    return (
      tracker.get_netmask(),
      tracker.get_defaultGateway(),
      tracker._dns
    )

  def get_subnet_info(self, tracker):
    return (
      tracker.network,
      tracker.get_broadcast(),
      tracker.get_broadcast(), #gateway
      tracker.get_hostRange(),
      tracker._dns
    )

  def get_descript_map(self, tracker):
    return tracker.descript_map

  def get_ip_from_name(self, tracker, host_name):
    for ip, name in self.get_descript_map(tracker).items():
      if host_name == name:
        return ip

  def assign_ip(self, tracker, descript):
    if not self.get_hosts_dhcp_avail:
      print("No hosts available to assign")
    elif not descript:
      print("Host name cannot be empty!")
    elif not self.get_hosts_dhcp_avail(tracker):
      print("No host IP addresses in this subnet are available!")
    else:
      return tracker.assign_ip(descript)

  def remove_ip(self, tracker, host_name):
    if not host_name:
      print("Empty host name is invalid!")
    else:
      ip = self.get_ip_from_name(tracker, host_name)
      if ip == None:
        print("Host '{}' could not be found!".format(host_name))
      else:
        if ip in tracker.host_dhcp_reserved:
          print("Host '{}'' is a reserved address!".format(host_name))
        else:
          tracker.remove_ip(ip)
          print("Host '{}' successfully unassigned!".format(host_name))
    print()
