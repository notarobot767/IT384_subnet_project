'''
funcions used accross multiple files
'''

class Static(object):
  def read_file(self, file_name):
    with open(file_name, "r") as input_file:
      data = input_file.read()
    return data

  def get_block_size_from_cidr(self, cidr, version):
    if version == 4:
      return 2**(32-cidr)
    return 2**(128-cidr)

Statics = Static()