from subnet_package.argparse import get_parser
from subnet_package.misc import misc

if __name__ == '__main__':
  try:
    get_parser()
  except KeyboardInterrupt:
    print(misc.cut_sling_load())
