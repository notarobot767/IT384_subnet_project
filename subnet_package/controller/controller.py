from ..model.model import Model

class Controller(object):
  def __init__(self, Model):
    self.mod = Model

  def speak(self):
    print("Hi, I'm the Controller!")