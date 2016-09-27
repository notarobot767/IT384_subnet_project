import ipaddress
from .ip_tracker import IP_tracker

class Subnet_DB(object):
  def __init__(self, argv):
    (self.requirements, self.address_space) = argv
    self.subnets = dict() #network string -> IP_tracker
    self.subnets_lst = list() #list of network subnets using ipaddress.IPv4Network()
    #takes more memory but will only have to sort once when adding/deleting

  def _add_new_subnet(self, subnet):
    self.subnets[subnet] = IP_tracker(subnet)
    self.subnets_lst.append(subnet)
    self.subnets_lst = sorted(self.subnets_lst)

  def _get_split_addresses(self, start, stop, block):
    if start == stop:
      list()
    return [ipaddress("{}/{}".format(start, block))] + \
      self._get_split_addresses(start+block, stop, block*2)

  def _get_split_addresses(start, stop, cidr):
    if start == stop:
      return list()
    else:
      print(ipaddress.ip_network("{}/{}".format(start, cidr)))
      return [ipaddress.ip_network("{}/{}".format(start, cidr))] + \
        _get_split_addresses(start+get_block_size_from_cidr(cidr), stop, cidr-1)

  def add_new_subnet(self, block, name):
    holder = list()
    while True:
      if not self.address_space:
        print("There is no space for requirement '{}'".format(name))
        break
      else:
        avail_address = self.address_space.pop()
        avail_block = self.get_block_size_from_cidr(avail_address.prefixlen)

        if available_block == block:
          self._add_new_subnet(avail_address)
        elif available_block > block:
          new_subnet = ipaddress.ip_network("{}/{}".format(avail_address[0], \
            self.get_cidr_from_block(block)))
          self._add_new_subnet(new_subnet)
          self._get_split_addresses(new_subnet[0],available_address[0]+available_block)
        else:
          holder.append(avail_address)

    while holder:
      self.address_space.append(holder.pop())
  
  def delete_subnet(self, net_str):
    del self.subnets[net_str]
    self.subnets_lst.remove(net_str)

  def get_block_size_from_hosts(self, hosts, pow_2=4):
    if pow_2-2 > hosts+1:
      return pow_2
    else:
      self.get_block_size_from_hosts(hosts, pow_2*2)

  def get_cidr_block_from_hosts(self, hosts, pow_2=4, base=2):
    if pow_2-2 > hosts+1:
      return (32-base, pow_2)
    else:
      return self.get_cidr_block_from_hosts(hosts, pow_2*2, base+1)

  def get_cidr_from_block(self, block, pow_2=4, cidr=30):
    if pow_2 == block:
      return cidr
    else:
      return self.et_cidr_from_block(block, pow_2*2, cidr-1)


