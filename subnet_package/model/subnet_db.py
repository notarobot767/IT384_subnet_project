import ipaddress
from .subnet import Subnet
from .ip_tracker import IP_tracker
from ..statics import Statics

class Subnet_DB(object):
  def __init__(self, address_block):
    self.address_space = [address_block]
    self.version = self.address_space[0].version
    self.subnets = dict() #network string -> IP_tracker
    self.subnets_lst = list() #list of network subnets using ipaddress.IPv4Network()
    #takes more memory but will only have to sort once when adding/deleting
    self.unsupported_lst = list()

  def add_new_subnet(self, hosts, name):
    holder = list()

    if self.version == 4:
      (cidr, block) = self.get_cidr_block_from_hosts(hosts)
    else:
      (cidr, block) = (64, Statics.get_block_size_from_cidr(64, self.version))

    def add(name, network):
      subnet = Subnet(name, network)
      self.subnets[subnet] = IP_tracker(subnet)
      self.subnets_lst.append(subnet)
      self.subnets_lst = sorted(self.subnets_lst,
        key=lambda x: (x.network, x.name))

    def get_split_addr(start, stop, cidr):
      if start == stop:
        return list() #sqeeze and sort address_space
      else:
        holder.append(ipaddress.ip_network("{}/{}".format(start, cidr)))
        return get_split_addr(start+Statics.get_block_size_from_cidr(cidr, self.version),
          stop, cidr-1)

    while True:
      if not self.address_space:
        self.unsupported_lst.append("{}, {}".format(name, hosts))
        print("There is no space for requirement '{}'!".format(name))
        break
      else:
        avail_address = self.address_space.pop()
        avail_block = Statics.get_block_size_from_cidr(avail_address.prefixlen, self.version)

        if avail_block == block:
          add(name, avail_address)
          break
        elif avail_block > block:
          new_subnet = ipaddress.ip_network("{}/{}".format(avail_address[0],
            self.get_cidr_from_block(block)))
          add(name, new_subnet)
          get_split_addr(avail_address[0]+block,
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
