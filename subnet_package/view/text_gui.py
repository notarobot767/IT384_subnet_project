import ipaddress
from ..controller.controller import Controller
from ..misc import Misc
from ..statics import Statics

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
    for subnet in subnets_lst:
      print_str += "[{}] - {:15}- {}\n".format(i,subnet.name, subnet.network)
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
        tracker = self.ctrl._get_tracker(self.ctrl.get_subnets_lst()[int(choice)-1])
        self._run_subnet_menu(tracker)
      else:
        self._print_invalid()

  def add_new_subnet(self):
    print("Not yet implemted!\n")
    name = input("Enter requirement name: ").strip()
    hosts_count = input("Enter number of hosts: ").strip()
    self.ctrl.add_new_subnet(hosts_count, name, True)
    print()

  def display_tracked(self):
    subnets_lst = self.ctrl.get_subnets_lst()
    total_args = 5
    star_wall = "*"*39 + "\n"
    unsupported = self.ctrl.get_unsupported_lst()

    print_str = "Here are your supported requirements:\n"
    if subnets_lst:
      for subnet in subnets_lst:
        print_str += "{}\n".format(subnet.name)
      for subnet in subnets_lst:
        (broadcast, gateway, hostrange, dns) = \
          self.ctrl.get_subnet_info(self.ctrl._get_tracker(subnet))
        print_str += self._wall
        print_str += ("{:17}{}\n"*total_args).format(
          "Name:", subnet.name,
          "Assigned Hosts:", subnet.block-2,
          "Network:", subnet.network,
          "Host Range:", hostrange,
          "Broadcast:", broadcast
        ).rstrip()
        print_str += "\n" + self._wall
      print_str += star_wall
      print_str += "The following subnets were unsupported:\n"
      if unsupported:
        print_str += "\n".join(unsupported)
      else:
        print_str += "None"
      print_str += "\n" + star_wall
    else:
      print_str += "None"
    print(print_str)


  #main menu
  ########################################################
  def run(self):
    while True:
      print(
        self._pound_word("Main Menu") + "\n"
        "[1] - Enter new requirement\n" +
        "[2] - View/Modify created subnets\n" +
        "[3] - Display tracked subnets\n" +
        "[4] - Exit"
        )
      choice = self._get_choice(); print()

      if choice == "1":
        self.add_new_subnet()
      elif choice == "2":
        self.view_modify()
      elif choice == "3":
        self.display_tracked()
      elif choice == "4":
        Misc.exit_msg()
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
        print_str += "{:40}- {}\n".format(str(ip), str(descript_map[ip])) #why have to force strings?
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
    (broadcast, gateway, host_range, dns) = self.ctrl.get_subnet_info(tracker)
    print(self._wall +
      "Network:\t{}\nBroadcast:\t{}\nGateway:\t{}\nHost range:\t{}\nDNS:\t\t{}\n".format(
      tracker.network,
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

  def _import_hosts(self, tracker):
    file_name = input("Enter location of hosts file to import: ").strip()
    try:
      hosts = Statics.read_file(file_name)
      print("importing...")
    except FileNotFoundError:
      print("file '{}' could not be found!".format(file_name))

    for host in hosts.split("\n"):
      host = host.strip()
      if self.ctrl.assign_ip(tracker, host) == None:
        print("Could not fit all hosts!")
        return -1
    print("import complete!\n")

  def _export_csv(self, tracker):
    name, netmask, gateway, dns, hosts, host_map = self.ctrl.get_csv_export(tracker)
    #print(name, netmask, gateway, dns)
    file_name = "output\\{}.csv".format(name)
    with open(file_name, "w") as output_file:
      output_file.write(
        "network name,{}\n\nnetmask,{}\ndefault gateway,{}\ndns,{}\n\n".format(
        name, str(netmask), gateway, dns))
      for host in hosts:
        output_file.write("{},{}\n".format(host_map[host], host))
    print("wrote to '{}'!\n".format(file_name))

  def _run_subnet_menu(self, tracker):
    def option_txt():
      option_lst = [
        "Import devices from file", #1
        "Add a device to this subnet", #2
        "Remove a device from this network", #3
        "Display subnet information", #4
        "Export to CSV file", #5
        "Exit" #6
      ]
      n = 1
      ans_str = ""
      for x in option_lst:
        ans_str += "[{}] - {}".format(n, x) + "\n"
        n += 1
      return ans_str

    while True:
      print(
        self._pound_word(str(tracker.network)) + "\n" +
        option_txt()
      )
      choice = self._get_choice(); print()

      if choice == "1":
        self._import_hosts(tracker)
      elif choice == "2":
        self._assign_ip(tracker)
      elif choice == "3":
        self._remove_ip(tracker)
      elif choice == "4":
        self._show_subnet(tracker)
      elif choice == "5":
        self._export_csv(tracker)
      elif choice == "6":
        break
      else:
        self._print_invalid()