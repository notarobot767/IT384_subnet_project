'''
The butter of the model. Each network from subnet_db points to its own ip_tracker.
The tracker allows adding and removing hosts as well as requests about information
of the subnet.
'''

import ipaddress, itertools

class IP_tracker(object):
  def __init__(self, subnet):
    self.name = subnet.name
    self.network = subnet.network
    self.host_dhcp_avail = self.network.hosts()
    self.host_dhcp_unavail = list()
    self.host_dhcp_reserved = list()
    self.descript_map = dict()
    self._set_gateway(self.get_defaultGateway())

  def _set_gateway(self, ip):
    last_host = self.get_lastHost()
    self.host_dhcp_reserved.append(last_host)
    self.host_dhcp_reserved = sorted(self.host_dhcp_reserved)
    self.descript_map[last_host] = "Default Gateway"

  def get_dns(self):
    if self.get_version() == 4:
      return "8.8.8.8  8.8.4.4"
    return "2001:4860:4860::8888  2001:4860:4860::8844"

  def get_version(self):
    return self.network.version

  def get_netmask(self):
    return str(self.network.netmask)

  def get_broadcast(self):
    return str(self.network.broadcast_address)

  def get_firstHost(self):
    return str(self.network[1])

  def get_lastHost(self):
    return str(self.network[-2])

  def get_defaultGateway(self):
    return self.get_lastHost()

  def get_hostRange(self):
    return "{} - {}".format(self.get_firstHost(), self.get_lastHost()) 

  def assign_ip(self, descript):
    ip = None
    while ip == None or ip in self.host_dhcp_reserved:
      ip = next(self.host_dhcp_avail)
      #instead of removing reserved IPs from the start from the iterator,
      #just remove as you get to them
    
    self.host_dhcp_unavail.append(ip)
    self.host_dhcp_unavail = sorted(self.host_dhcp_unavail)
    self.descript_map[ip] = descript
    return ip

  def remove_ip(self, ip):
    self.host_dhcp_unavail.remove(ip)
    self.host_dhcp_avail = itertools.chain([ip], self.host_dhcp_avail)
      #http://stackoverflow.com/questions/571850/adding-elements-to-python-generators
    del self.descript_map[ip]
    return True
