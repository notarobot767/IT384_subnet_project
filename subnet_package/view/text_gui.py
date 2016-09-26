import ipaddress
from ..controller.controller import Controller
from ..misc import misc

class Text_GUI(object):
  def __init__(self, controller):
    self.ctrl = controller
    self._wall_length = 72
    self._wall = "=" * self._wall_length + "\n"

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
          self.ctrl.get_subnets_lst()[int(choice)-1]))
      else:
        self._print_invalid()

  def add_new_subnet(self):
    net_str = input("Enter your subnet followed by CIDR: ")
    self.ctrl.add_new_subnet(net_str, True)

  def delete_subnet(self):
    self.ctrl.delete_subnet(True)

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
        print(misc.exit_string())
        break
      else:
        self._print_invalid()

  #subnet menu
  ########################################################
  def __show_hosts_pool(self, tracker, pool, msg):
    print_str = msg + "\n"
    if not pool:
      print_str += "None\n"
    else:
      descript_map = self.ctrl.get_descript_map(tracker)
      for ip in pool:
        print_str += "{:40}- {}\n".format(str(ip), str(descript_map[ip]))
    return print_str

  def _show_hosts_assigned(self, tracker):
    return self.__show_hosts_pool(tracker,
      self.ctrl.get_hosts_dhcp_unavail(tracker),
      "Assigned DHCP host IPs")

  def _show_hosts_reserved(self, tracker):
    return self.__show_hosts_pool(tracker,
      self.ctrl.get_hosts_dhcp_reserved(tracker),
      "Reserved DHCP host IPs")

  def _show_hosts(self, tracker):
    return self._show_hosts_assigned(tracker) + "\n" + \
      self._show_hosts_reserved(tracker)

  def _show_subnet(self, tracker):
    (network, broadcast, gateway, host_range, dns) = self.ctrl.get_subnet_info(tracker)
    print(self._wall +
      "Network:\t{}\nBroadcast:\t{}\nGateway:\t{}\nHost range:\t{}\nDNS:\t\t{}\n".format(
      network,
      broadcast,
      gateway,
      host_range,
      dns
      ) +"\n\n" +
      self._show_hosts(tracker) +
      self._wall
      )

  def _show_device_info(self, tracker, ip):
    (mask, gateway, dns) = self.ctrl.get_device_info(tracker)
    print(
      self._wall +
      "IP:\t\t{}\nSubnet Mask:\t{}\n".format(
        ip,
        mask
      ) +
      "Gateway:\t{}\nDNS:\t\t{}\n".format(
        gateway,
        dns
      ) +
      self._wall
    )

  def _assign_ip(self, tracker):
    descript = input("Enter a description for this host: ").strip()
    ip = self.ctrl.assign_ip(tracker, descript)
    if ip != None:
      self._show_device_info(tracker, ip)

  def _remove_ip(self, tracker):
    if self.ctrl.get_hosts_dhcp_unavail(tracker):
      print(self._show_hosts_assigned(tracker))
      host_name = input("Enter host name of device to be unassigned: ").strip()
      self.ctrl.remove_ip(tracker, host_name, True)
    else:
      print("No hosts to remove!")
    print()

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
        self._assign_ip(tracker)
      elif choice == "2":
        self._remove_ip(tracker)
      elif choice == "3":
        self._show_subnet(tracker)
      elif choice == "4":
        break
      else:
        self._print_invalid()