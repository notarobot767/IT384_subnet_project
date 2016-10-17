'''
The base model. Not much actually goes on in here except for creating the
subcomponets such as the subnet database.
'''

from .subnet_db import Subnet_DB

class Model(object):
  def __init__(self, address_block):
    self.subnet_db = Subnet_DB(address_block)

  def speak(self):
    print("Hi, I'm the Model!")
