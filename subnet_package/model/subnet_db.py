class Subnet_DB(object):
  def __init__(self):
    self.subnets = dict()
    self.subnets_lst = list()

  def isValidNetwork(self, network):
    network = network.strip()
    if ":" in network:
      print("Only IPv4 networks only!\n")
      return (False, False)
    else:
      try:
        network = ipaddress.IPv4Network(network)
        cidr = int(str(network).split("/")[1])
        if cidr > 30 or cidr < 24:
          print("CIDR mask must be between 24 and 30 inclusive!\n")
          return (False, False)
        else:
          return (True, network)
      except ValueError:
        print("Not a vaild network!\n<usage> [IPv4 network address]/[CIDR]\n")
        return (False, False)

  def _addNewSubnet_manual(self, network_str):
    self.subnets[network_str] = IP_tracker(network_str)
    self.subnets_lst.append(network_str)
    self.subnets_lst = sorted(self.subnets_lst,
      key=lambda x: (ipaddress.IPv4Network(x).network_address))

  def addNewSubnet(self):
    net = input("Enter your subnet followed by CIDR: ")
    (isValid, net) = self.isValidNetwork(net)
    if(isValid):
      net_str = str(net)
      if net_str in self.subnets:
        print("Network already exists!\n")
      else:
        self._addNewSubnet_manual(net_str)
        print("Successfully added network " + net_str + "\n")

  def viewSubnets(self):
    ans_str = _poundWord("Subnets")
    ans_str += "\nFound {} subnet(s):\n".format(len(self.subnets_lst))
    i = 1
    #print(self.subnet_lst)
    for net in self.subnets_lst:
      ans_str += "[{}] - {}\n".format(i, net)
      i += 1
    ans_str += "[{}] - Go back".format(i)
    print(ans_str)
    return i
  
  def _deleteSubnet_manual(self, network_str):
    del self.subnets[network_str]
    self.subnets_lst.remove(network_str)

  def deleteSubnet(self):
    if(self.subnets):
      network = input("Enter the subnet to delete followed by CIDR: ")
      (isValid, network) = self.isValidNetwork(network)
      if(isValid):
        network = str(network)
        if(network in self.subnets):
          self._deleteSubnet_manual(str(network))
          print(network + " has been successfully deleted!\n")
        else:
          print(network + " could not be found in subnet database!\n")
    else:
      print("Subnet database is empty!\n")


  def viewModify(self):
    while True:
      i = self.viewSubnets()
      choice = input("Which subnet would you like to modify? ")
      choice = choice.strip()
      if choice in [str(x) for x in range(1, i)]:
        print()
        gui_subnet(self.subnets[self.subnets_lst[int(choice) - 1]])
      elif choice == str(i):
        print()
        break
      else:
        print()
        print("Not a valid option!\n")
