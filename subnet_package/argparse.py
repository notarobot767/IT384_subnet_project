'''
parses the command line input and send the address_space and requirements(if any)
to main
'''

import argparse, sys, ipaddress
from .main import main
from .statics import Statics

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
    help="path to requirements text document; line ex) [Str],[Int]"
  )
  parser.add_argument("N", type=ipaddress.ip_network,
    help="Allocated network block of IP space ex) 172.16.0.0/16; " +
    "CIDR for IPv4 <= 30 for IPv6 <=64"
  )
  return parser.parse_args()

def parse_args():
  args = _get_parser()

  try:
    if args.N.version == 4:
      if args.N.prefixlen > 30:
        print("IPv4 needs at least a /30 CIDR!")
        return -1
    else:
      if args.N.prefixlen > 64:
        print("IPv6 needs at least a /64 CIDR!")
        return -1

    if args.r != None:
      requirements = get_requirements(args.r)
    else:
      requirements = args.r
    
  except ValueError:
    print("'{}' does not appear to be an IPv4 or IPv6 network".format(args.N))
    return -1
  except FileNotFoundError:
    print("File '{}' could not be opened!".format(args.r))
    return -1
  except ValueError:
    print("{} has host bits set!".format(args.N))
    return -1

  main(args.N, requirements)
    #I wanted separate except clauses within main and subcomponets
