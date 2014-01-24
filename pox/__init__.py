#!/usr/bin/env python
 
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2014 Caltech
# License: 3-clause BSD

from __future__ import absolute_import

# get version numbers, license, and long description
try:
    from .info import this_version as __version__
    from .info import readme as __doc__, license as __license__
except ImportError:
    msg = """First run 'python setup.py build' to build pox."""
    raise ImportError(msg)

__author__ = 'Mike McKerns'

__doc__ = """
""" + __doc__

__license__ = """
""" + __license__

from .shutils import shelltype, homedir, rootdir, username, sep, \
                     minpath, env, whereis, which, find, walk, where, \
                     mkdir, rmtree, shellsub
from .utils import pattern, expandvars, getvars, convert, replace, wait_for, \
                   findpackage, select, selectdict, remote, which_python, \
                   parse_remote, kbytes, disk_used, index_slice, index_join, \
                   likely_import, _namespace


def license():
    """print license"""
    print(__license__)
    return

def citation():
    """print citation"""
    print(__doc__[-499:-140])
    return

# end of file
