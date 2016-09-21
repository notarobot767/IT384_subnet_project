import ipaddress

class IP_tracker(object):
  def __init__(self, net_str):
    self.network = ipaddress.IPv4Network(net_str)
    self.host_dhcp_avail = set([str(x) for x in self.network.hosts()])
    self.host_dhcp_unavail = set()
    self.host_dhcp_reserved = set()
    self.descript_map = dict()
    #self._set_gateway(self.get_lastHost())

  def _set_gateway(self, ip):
    #self._assignIP_man("Default Gateway", ip)
    self.host_unavail.remove(ip)

  def get_CIDR(self):
    return "/" + str(self.network).split("/")[1]

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
    return self.get_firstHost() + "-" + self.get_lastHost().split(".")[3]   

  def assign_ip(self, descript):
    ip = self.host_dhcp_avail.pop()
    self.host_dhcp_unavail.add(ip)
    self.descript_map[ip] = descript
    return ip

  def removeIP_manual(self, ip):
    self.host_unavail.remove(ip)
    self.host_avail.add(ip)
    del self.descript_map[ip]

  def removeIP(self):
    if not self.host_unavail:
      print("Assigned IPs:\nNone\n")
    else:
      print(self.show_hosts_unavail(False))
      choice = input("Enter the description of the IP you'd like to unassign: ").strip()
      if choice == "Default Gateway":
        print("Cannot unassign that!\n")
      elif choice not in self.descript_map.values():
        print("Host not found!\n")
      else:
        for ip, descript in self.descript_map.items():
          if descript == choice:
            self.removeIP_manual(ip)
            print("Device successfully unassigned!\n")
            break
