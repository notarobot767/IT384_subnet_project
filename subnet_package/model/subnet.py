from ..statics import Statics

class Subnet(object):
  def __init__(self, name, network):
    self.name = name
    self.network = network
    self.block = \
      Statics.get_block_size_from_cidr(network.prefixlen, network.version)
