import argparse
import sys
import ipaddress
from .main import main

def get_requirements(file_name):
  require_dic = dict()

  def sort_my_dic(dic):
    return list(sorted(dic.items(), key=lambda x: (-x[1], x[0])))

  def is_keep_going():
    while True:
      choice = input("Would you like to continue anyway? [y | n] ")
      if choice == "y":
        break
      elif choice == "n":
        sys.exit()

  def parse_requirements(line):
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
      print("line '{}' did not split right".fomat(line))
    return isBad

  with open(file_name, "r") as input_file:
    for line in input_file:
      if(parse_requirements(line)):
        is_keep_going()

  return sort_my_dic(require_dic)

def get_network(net_str):
  return list(ipaddress.ip_network(net_str))

def get_parser():
  parser = argparse.ArgumentParser(
    description="Automated Subnet Calculator"
  )
  parser.add_argument("N", type=str,
    help="Allocated network block of IP space ex) 172.16.0.0/16"
  )
  parser.add_argument("R", type=str,
    help="Path to requirements text document"
  )
  args = parser.parse_args()

  argv = None
  try:
    argv = (get_requirements(args.R), get_network(args.N))
  except FileNotFoundError:
    print("File '{}' could not be opened!".format(args.R))
    argv = None
  except ValueError:
    print("'{}' does not appear to be an IPv4 or IPv6 network".format(args.N))

  if argv != None:
    print("Requrements to add:\n{}\n".format(argv))
    main(argv)

  