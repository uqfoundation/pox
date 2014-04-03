#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2014 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pox/LICENSE
"""
the pox command launcher::
    - run any of the pox commands at the command shell prompt

For example::
    $ pox_launcher.py "which('python')"
"""
from pox import *

def help():
    #XXX: better would be to provide a list of available commands
    print("Please provide a 'pox' command enclosed in quotes.\n")
    print("For example:")
    print("  $ pox_launcher.py \"which('python')\"")
    return


if __name__=='__main__':
    import sys
    try:
        func = sys.argv[1]
    except: func = None
    if func:
        try:
            exec('print(%s)' % func)
        except:
            print("Error: incorrect syntax '%s'" % func)
            exec('print(%s.__doc__)' % func.split('(')[0])
    else: help()


# End of file 
