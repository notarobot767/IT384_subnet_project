from ..controller.controller import Controller

class Text_GUI(object):
  def __init__(self, controller):
    self.ctrl = controller
    self._wall_length = 40
    self._wall = "\n" + "=" * self._wall_length + "\n"

  def _poundWord(self, word):
    return "{0}\n#{1}#\n{0}".format("#"*(len(word)+2), word)

  def _get_choice(self):
    return input("Enter your choice: ").strip()

  def _print_invalid(self):
    print("Not a valid choice!\n")

  #main menu
  ########################################################
  def run(self):
    while True:
      print(
        self._poundWord("Main Menu") + "\n"
        "[1] - Create subnet\n" +
        "[2] - View/Modify created subnets\n" +
        "[3] - Delete a subnet\n" +
        "[4] - Exit"
        )
      
      choice = self._get_choice()

      if choice == "1":
        pass
      elif choice == "2":
        pass
      elif choice == "3":
        pass
      elif choice == "4":
        break
      else:
        self._print_invalid()

  #subnet menu
  ########################################################
  