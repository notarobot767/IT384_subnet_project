from ..controller.controller import Controller

class Text_GUI(object):
  def __init__(self, controller):
    self.ctrl = controller
    self._wall_length = 40
    self._wall = "\n" + "=" * self._wall_length + "\n"

  def _pound_word(self, word):
    return "{0}\n#{1}#\n{0}".format("#"*(len(word)+2), word)

  def _get_choice(self):
    return input("Enter your choice: ").strip()

  def _print_invalid(self):
    print("Not a valid choice!\n")

  def _get_subnets_lst(self):
    subnets_lst = self.ctrl.get_subnets_lst()
    print_str = self._pound_word("Subnets")
    print_str += "\nFound {} subnet(s):\n".format(len(subnets_lst))
    i = 1
    for net_str in subnets_lst:
      print_str += "[{}] - {}\n".format(i, net_str)
      i += 1
    print_str += "[{}] - Go back".format(i)
    return (i, print_str)

  def view_modify(self):
    (i, print_str) = self._get_subnets_lst()
    while True:
      print(print_str)
      choice = input("Which subnet would you like to modify? ").strip()
      print()
      if choice == str(i):
        break
      elif choice.isdigit() and int(choice) > 0 and int(choice) < i:

        self._run_subnet_menu(self.ctrl.get_tracker(
          self.ctrl.get_subnets_lst()[0]))
      else:
        self._print_invalid()

  def add_new_subnet(self):
    net_str = input("Enter your subnet followed by CIDR: ")
    self.ctrl.add_new_subnet(net_str)

  def delete_subnet(self):
    self.ctrl.delete_subnet()

  #main menu
  ########################################################
  def run(self):
    while True:
      print(
        self._pound_word("Main Menu") + "\n"
        "[1] - Create subnet\n" +
        "[2] - View/Modify created subnets\n" +
        "[3] - Delete a subnet\n" +
        "[4] - Exit"
        )
      choice = self._get_choice(); print()

      if choice == "1":
        self.add_new_subnet()
      elif choice == "2":
        self.view_modify()
      elif choice == "3":
        self.delete_subnet()
      elif choice == "4":
        break
      else:
        self._print_invalid()

  #subnet menu
  ########################################################
  def show_hosts_assigned(self):
    print_str = "Assigned DHCP host IPs:\n"
    hosts_dhcp_unavail = self.ctrl.get_hosts_dhcp_unavail()
    if not hosts_dhcp_unavail:
      my_str += "None"
    else:
      descript_map = self.ctrl.get_descript_map()
      for ip in sorted(hosts_dhcp_unavail,
          key=lambda x: (ipaddress.ip_address(x))):
        descript = 
        print_str += "{}\t- {}\n".format(ip, descript)
    return my_str.lstrip()

  def _show_hosts(self, tracker):
    return self.show_hosts_assigned(tracker) + "\n" +
      self.show_host_dhcp_avail(tracker)

  def _show_subnet(self, tracker):
    subnet_info = self.ctrl.get_subnet_info(tracker)
    print(_wall +
      "IP: {}\nCIDR: {}\nNetwork Address: {}\nFirst usable: {}\n".format(
      tracker[0],
      tracker[1],
      tracker[2],
      tracker[3],
      tracker[4]
      ) +
      "Host addresses: {}\nLast usable: {}\nBroadcast Address: {}".format(
      tracker[5],
      tracker[6],
      tracker[7]
      ) + "\n\n" +
      self._show_hosts() +
      _wall
      )

  def assign_ip(self, tracker):
    descript = input("Enter a description for this host: ").strip()
    ip = self.ctrl.assign_ip(tracker, descript)
    if ip != None:
      device_info = self.ctrl.get_device_info(tracker)
      print_str = "Enter the following network settins onto this host:\n"
      print_str = "IP\t\t\t: {}\nSubnet Mask\t\t: {}\n".format(
        ip,
        device_info[0]
        )
      print_str += "Default Gateway\t\t: {}\nDNS:\t\t\t: {}\n".format(
        device_info[1],
        device_info[2]
        )
    print(print_str)

  def _run_subnet_menu(self, tracker):
    while True:
      print(
        self._pound_word(str(tracker.network)) + "\n" +
        "[1] - Add a device to this subnet\n" +
        "[2] - Remove a device from this network\n" +
        "[3] - Display subnet information\n" +
        "[4] - Exit"
      )
      choice = self._get_choice(); print()

      if choice == "1":
        self.assign_ip(tracker)
      elif choice == "2":
        pass
      elif choice == "3":
        self._show_subnet()
      elif choice == "4":
        break
      else:
        self._print_invalid()