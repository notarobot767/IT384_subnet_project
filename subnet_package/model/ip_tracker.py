import ipaddress

class IP_tracker(object):
  def __init__(self, net_str):
    self.network = ipaddress.ip_network(net_str)
    self.host_dhcp_avail = set([str(x) for x in self.network.hosts()])
    self.host_dhcp_unavail = set()
    self.host_dhcp_reserved = set()
    self.descript_map = dict()
    self._set_gateway(self.get_lastHost())
    self._dns = self.get_dns()

  def __cmp__(self, other):
    if self.network < other.network:
      return -1
    elif self.network > other.network:
      return 1
    else:
      return 0

  def _set_gateway(self, ip):
    self.assign_ip("Default Gateway", ip)

  def get_dns(self):
    if self.get_version() == 4:
      return "8.8.8.8\t8.8.4.4"
    return "2001:4860:4860::8888"

  def get_version(self):
    return self.network.version

  def get_CIDR(self):
    return self.network.prefixlen

  def get_networkAddr(self):
    return str(self.network.network_address)

  def get_netmask(self):
    return str(self.network.netmask)

  def get_broadcast(self):
    return str(self.network.broadcast_address)

  def get_firstHost(self):
    net_lst = self.get_networkAddr().split(".")
    net_lst[3] = str(int(net_lst[3]) + 1)
    return ".".join(net_lst)

  def get_lastHost(self):
    net_lst = self.get_broadcast().split(".")
    net_lst[3] = str(int(net_lst[3]) - 1)
    return ".".join(net_lst)

  def get_defaultGateway(self):
    return self.get_lastHost()

  def get_hostRange(self):
    return self.get_firstHost() + "-" + self.get_lastHost()  

  def assign_ip(self, descript, ip=None):
    if ip == None:
      ip = self.host_dhcp_avail.pop()
      self.host_dhcp_unavail.add(ip)
    else:
      self.host_dhcp_reserved.add(ip)
    self.descript_map[ip] = descript
    if ip in self.host_dhcp_avail:
      self.host_dhcp_avail.remove(ip)
    return ip

  def remove_ip(self, ip):
    self.host_dhcp_unavail.remove(ip)
    self.host_dhcp_avail.add(ip)
    del self.descript_map[ip]
