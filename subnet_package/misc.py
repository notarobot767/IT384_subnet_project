import random

class Misc(object):
  def welcome_banner(self):
    greet_lst = [
      "Welcome to the NHK!",
      "IT384: Project 1"
    ]
    return random.choice(greet_lst)

misc = Misc()