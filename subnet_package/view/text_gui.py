from ..controller.controller import Controller

class Text_GUI(object):
  def __init__(self, controller):
    self.ctrl = controller
    self._wall_length = 40
    self._wall = "\n" + "=" * self._wall_length + "\n"

  def _poundWord(self, word):
    return "{0}\n#{1}#\n{0}".format("#"*(len(word)+2), word)

  def run_main(self):
    while True:
      print(
        self._poundWord("Main Menu") + "\n"
        "[1] - Create subnet\n" +
        "[2] - View/Modify created subnets\n" +
        "[3] - Delete a subnet\n" +
        "[4] - Exit"
        )
      break