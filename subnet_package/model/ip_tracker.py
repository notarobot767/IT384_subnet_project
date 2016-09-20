import ipaddress

class IP_tracker(object):
  def __init__(self, net_str):
    self.network = ipaddress.IPv4Network(net_str)
    self.host_avail = set([str(x) for x in self.network.hosts()])
    self.host_unavail = set()
    self.descript_map = dict()
    self._set_gateway(self.get_lastHost())

  def _set_gateway(self, ip):
    self._assignIP_man("Default Gateway", ip)
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

  def show_hosts_unavail(self, gateway=True):
    my_str = "Assigned IPs:\n"
    if not self.descript_map:
      my_str += "None"
    else:
      for ip, descript in sorted(self.descript_map.items(),
          key=lambda x: (ipaddress.ip_address(x[0]))):
        if not gateway:
          if ip != self.get_defaultGateway():
            my_str += "{}\t- {}\n".format(ip, descript)
        else:      
          my_str += "{}\t- {}\n".format(ip, descript)
    return my_str.lstrip()

  def show_hosts_avail(self):
    my_str = "Available IPs:\n"
    if not self.host_avail:
      my_str += "None"
    else:
      for ip in sorted(self.host_avail, key=lambda x: (ipaddress.ip_address(x))):
        my_str += "{}\t- {}\n".format(ip, "unassigned")
    return my_str.rstrip()

  def show_hosts(self):
    return self.show_hosts_unavail() + "\n" + self.show_hosts_avail()    

  def showSubnet(self):
    print(_wall +
      "IP: {}\nCIDR: {}\nNetwork Address: {}\nFirst usable: {}\n".format(
      self.network,
      self.get_CIDR(),
      self.get_networkAddr(),
      self.get_firstHost(),
      self.get_firstHost()
      ) +
      "Host addresses: {}\nLast usable: {}\nBroadcast Address: {}".format(
      self.get_hostRange(),
      self.get_lastHost(),
      self.get_broadcast()
      ) + "\n\n" +
      self.show_hosts() +
      _wall
      )

  def showDeviceInfo(self, ip):
    my_str = "IP\t\t\t: {}\nSubnet Mask\t\t: {}\n".format(
      ip,
      self.get_netmask()
      )
    my_str += "Default Gateway\t\t: {}\nDNS:\t\t\t: {}".format(
      self.get_defaultGateway(),
      _dns
      )
    return my_str

  def input_IP_descript(self):
    while True:
      descript = input("Enter a description for this host: ")
      descript = descript.strip()
      
      if not not descript:
        if descript not in self.descript_map.values():
          print()
          return descript
        else:
          print("Name is already in use!")
      print()

  def _assignIP_man(self, descript, ip=None):
    if ip == None:
      ip = self.host_avail.pop()
    if ip in self.host_avail:  
      self.host_avail.remove(ip)
    self.host_unavail.add(ip)
    self.descript_map[ip] = descript
    return ip

  def assignIP(self):
    if not self.host_avail:
      print("No host IP addresses in this subnet are available!")
    else:
      ip = self._assignIP_man(self.input_IP_descript())
      print("Enter the following network settins onto this host:\n" +
      self.showDeviceInfo(ip)
      )
    print()

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
