class Static(object):
  def read_file(self, file_name):
    with open(file_name, "r") as input_file:
      data = input_file.read()
    return data

Statics = Static()