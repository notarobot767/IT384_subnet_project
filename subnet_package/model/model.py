from .subnet_db import Subnet_DB

class Model(object):
  def __init__(self, argv):
    self.subnet_db = Subnet_DB(argv)

  def speak(self):
    print("Hi, I'm the Model!")
