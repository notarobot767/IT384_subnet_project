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

  def get_unsupported_lst(self):
    return self._subnet_db.unsupported_lst

  def add_new_subnet(self, hosts, name, verbose=False):
    try:
      hosts = int(hosts)
    except:
      print("Hosts must be an integer!")
      return False
    return self._subnet_db.add_new_subnet(hosts, name)
        
  def delete_subnet(self, verbose=False):
    if verbose:
      print("method has been depreciated!\n")
    return False

  #ip_tracker
  ############################################################
  def _get_tracker(self, subnet):
    return self._subnet_db.subnets[subnet]

  def get_hosts_dhcp_unavail(self, tracker):
    return tracker.host_dhcp_unavail

  def get_hosts_dhcp_reserved(self, tracker):
    return tracker.host_dhcp_reserved

  def get_device_info(self, tracker):
    return (
      tracker.get_netmask(),
      tracker.get_defaultGateway(),
      tracker.get_dns()
    )

  def get_subnet_info(self, tracker):
    #tracker = self._get_tracker(subnet)
    return (
      tracker.get_broadcast(),
      tracker.get_defaultGateway(),
      tracker.get_hostRange(),
      tracker.get_dns()
    )

  def get_csv_export(self, tracker):
    return (
      tracker.name,
      tracker.get_netmask(),
      tracker.get_defaultGateway(),
      tracker.get_dns(),
      tracker.host_dhcp_unavail,
      tracker.descript_map
    )

  def get_descript_map(self, tracker):
    return tracker.descript_map

  def get_ip_from_name(self, tracker, host_name):
    for ip, name in self.get_descript_map(tracker).items():
      if host_name == name:
        return ip

  def is_address_avail(self, tracker):
    if tracker.host_dhcp_avail:
      return True
    else:
      return False

  def assign_ip(self, tracker, descript):
    if not self.is_address_avail:
      print("No hosts available to assign!\n")
    elif not descript:
      print("Host name cannot be empty!\n")
    elif descript in self.get_descript_map(tracker).values():
      print("Host '{}' already exists!\n".format(descript))
    else:
      return tracker.assign_ip(descript)

  def remove_ip(self, tracker, host_name, verbose=False):
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
          if tracker.remove_ip(ip):
            print("Host '{}' successfully unassigned!".format(host_name))
            return True
    print()
    return False
