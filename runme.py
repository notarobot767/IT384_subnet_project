# Purpose (What) --------------------------------------------------------------
"""
Create a subnet planner calculator for a given block of IP address space for
a given list of requirements that can also manage the hosts of each subnet
"""

# Assumptions:
"""
This is not a database. Subnets and hosts created from the last run will not
be persistent.
"""

# Concept (How) ---------------------------------------------------------------
"""
This will be an expansion based off of hw2. Using the ipaddress module, I can
easily add support for IPv6 in the ip_tracker class.

My implementation is largely based off of the model, view, controller methodology.

The model will contain the data and basic data manipulation. This is where I
will define my classes for the subnet database and ip tracker. These methods
should never be accessed directly.

The controller essentailly is the API which has methods that are "safe" to be
executed. This is where I will perform my input sanitation and prevent illegal
moves instead of crashing.

The view is how the user will interact with the program. Currently this is
implemented as a text based GUI. Methods in the view will call methods in the
controller to access and modify data.

The point of the model, view, controller is to logically split up my program. This
both splits up the program into many separate files where each class or method
focuses on a particular function.
"""

# Imports ---------------------------------------------------------------------
from subnet_package.argparse import get_parser
from subnet_package.misc import misc

# Class Definitions -----------------------------------------------------------

# Function Definitions --------------------------------------------------------

# Testing ---------------------------------------------------------------------

# Execution ------------------------------------
"""
Well, here it is.
"""
if __name__ == '__main__':
  try:
    get_parser()
  except KeyboardInterrupt:
    print(misc.cut_sling_load())
