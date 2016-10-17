import argparse, sys, ipaddress
from .main import main
from .statics import Statics

def get_network(net_str):
  return ipaddress.ip_network(net_str)

def ask_keep_going():
  while True:
    choice = input("Would you like to continue anyway? [y | n] ")
    if choice == "y":
      break
    elif choice == "n":
      sys.exit()

def get_requirements(file_name):
  require_dic = dict()

  def sorted_dic(dic):
    return list(sorted(dic.items(), key=lambda x: (-x[1], x[0])))

  def parse_require(line):
    line = line.split(",")
    isBad = True
    if len(line) == 2:
      (name, size) = map(str.strip, line)
      if name in require_dic:
        print("Duplicate name '{}' found in the requirements file!".format(name))
      elif not size.isdigit():
        print("Invaild size of '{}' found in '{}' requirement!".format(size, name))
      else:
        require_dic[name] = int(size)
        isBad = False
    else:
      print("line '{}' did not split right".format(line))
    return isBad

  for line in Statics.read_file(file_name).split("\n"):
    if parse_require(line):
      ask_keep_going()

  return sorted_dic(require_dic)

def _get_parser():
  parser = argparse.ArgumentParser(
    description="Automated Subnet Calculator"
  )
  parser.add_argument("-r", type=str,
    default=None, metavar='requirements',
    help="path to requirements text document"
  )
  parser.add_argument("N", type=str,
    help="Allocated network block of IP space ex) 172.16.0.0/16"
  )
  return parser.parse_args()

def parse_args():
  args = _get_parser()

  try:
    address_space = get_network(args.N)
    if args.r != None:
      requirements = get_requirements(args.r)
    else:
      requirements = None
    
  except ValueError:
    print("'{}' does not appear to be an IPv4 or IPv6 network".format(args.N))
    return -1
  except FileNotFoundError:
    print("File '{}' could not be opened!".format(args.r))
    return -1

  main(address_space, requirements)

  #print("Requrements to add:\n{}\n".format(argv)) #remove later
