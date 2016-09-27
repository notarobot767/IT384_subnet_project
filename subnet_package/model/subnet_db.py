import ipaddress
from .ip_tracker import IP_tracker

class Subnet_DB(object):
  def __init__(self, argv):
    self.address_space = argv
    self.version = self.address_space[0].version
    self.subnets = dict() #network string -> IP_tracker
    self.subnets_lst = list() #list of network subnets using ipaddress.IPv4Network()
    #takes more memory but will only have to sort once when adding/deleting

  def _add_new_subnet(self, subnet):
    self.subnets[subnet] = IP_tracker(subnet)
    self.subnets_lst.append(subnet)
    self.subnets_lst = sorted(self.subnets_lst)

  def add_new_subnet(self, hosts, name):
    holder = list()
    (cidr, block) = (None, None)
    if self.version == 4:
      (cidr, block) = self.get_cidr_block_from_hosts(hosts)
    else:
      (cidr, block) = (64, self.get_block_size_from_cidr(64))

    def _get_split_addresses(start, stop, cidr):
      if start == stop:
        return list() #sqeeze and sort address_space
      else:
        address = ipaddress.ip_network("{}/{}".format(start, cidr))
        holder.append(address)
        return _get_split_addresses(start+self.get_block_size_from_cidr(cidr),
          stop, cidr-1)

    while True:
      if not self.address_space:
        print("There is no space for requirement '{}'".format(name))
        break
      else:
        avail_address = self.address_space.pop()
        avail_block = self.get_block_size_from_cidr(avail_address.prefixlen)

        if avail_block == block:
          self._add_new_subnet(avail_address)
          break
        elif avail_block > block:
          new_subnet = ipaddress.ip_network("{}/{}".format(avail_address[0], \
            self.get_cidr_from_block(block)))
          self._add_new_subnet(new_subnet)
          _get_split_addresses(avail_address[0]+block, \
            avail_address[0]+avail_block, cidr)
          break
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

  def get_cidr_from_block(self, block, pow_2=4, host_bits=2):
    if pow_2 == block:
      if self.version == 4:
        return 32-host_bits
      return 128-host_bits
    else:
      return self.get_cidr_from_block(block, pow_2*2, host_bits+1)

  def get_block_size_from_cidr(self, cidr):
    if self.version == 4:
      return 2**(32-cidr)
    return 2**(128-cidr)


