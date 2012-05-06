#!/usr/bin/env python
#
# Michael McKerns
# mmckerns@caltech.edu

from __future__ import with_statement
import os

# set version numbers
stable_version = '0.1a1'
target_version = '0.2a'
is_release = False

# check if easy_install is available
try:
#   import __force_distutils__ #XXX: uncomment to force use of distutills
    from setuptools import setup
    has_setuptools = True
except ImportError:
    from distutils.core import setup
    has_setuptools = False

# generate version number
if os.path.exists('pox/info.py'):
    # is a source distribution, so use existing version
    from pox.info import this_version
elif stable_version == target_version:
    # we are building a stable release
    this_version = target_version
else:
    # we are building a distribution
    this_version = target_version + '.dev'
    if is_release:
      from datetime import date
      today = "".join(date.isoformat(date.today()).split('-'))
      this_version += "-" + today

# get the license info
with open('LICENSE') as file:
    license_text = file.read()

# generate the readme text
long_description = \
"""--------------------------------------------------------------
pox: utilities for filesystem exploration and automated builds
--------------------------------------------------------------

Pox provides a collection of utilities for navigating and manipulating
filesystems. This module is designed to facilitate some of the low level
operating system interactions that are useful when exploring a filesystem
on a remote host, where queries such as "what is the root of the filesystem?",
"what is the user's name?", and "what login shell is preferred?" become
essential in allowing a remote user to function as if they were logged in
locally. While pox is in the same vein of both the `os` and `shutil`
builtin modules, the majority of its functionality is unique and compliments
these two modules.

Pox provides python equivalents of several unix shell commands such as
"which" and "find". These commands allow automated discovery of what has
been installed on an operating system, and where the essential tools are
located. This capability is useful not only for exploring remote hosts,
but also locally as a helper utility for automated build and installation.

Several high-level operations on files and filesystems are also provided.
Examples of which are: finding the location of an installed python package,
determining if and where the source code resides on the filesystem, and
determining what version the installed package is.

Pox also provides utilities to enable the abstraction of commands sent
to a remote filesystem.  In conjunction with a registry of environment
variables and installed utilites, pox enables the user to interact with
a remote filesystem as if they were logged in locally. 

Pox is part of pathos, a python framework for heterogeneous computing.
Pox is in the early development stages, and any user feedback is
highly appreciated. Contact Mike McKerns [mmckerns at caltech dot edu]
with comments, suggestions, and any bugs you may find. A list of known
issues is maintained at http://dev.danse.us/trac/pathos/query.


Major Features
==============

Pox provides utilities for discovering the user's environment::

    - return the user's name, current shell, and path to user's home directory
    - strip duplicate entries from the user's $PATH
    - lookup and expand environment variables from ${VAR} to 'value'

Pox also provides utilities for filesystem exploration and manipulation::

    - discover the path to a file, exectuable, directory, or symbolic link 
    - discover the path to an installed package
    - parse operating system commands for remote shell invocation
    - convert text files to platform-specific formatting


Current Release
===============

The latest stable release version is pox-%(relver)s. You can download it here.
The latest stable version of pox is always available at:

    http://dev.danse.us/trac/pathos


Development Release
===================

If you like living on the edge, and don't mind the promise
of a little instability, you can get the latest development
release with all the shiny new features at:

    http://dev.danse.us/packages.


Installation
============

Pox is packaged to install from source, so you must
download the tarball, unzip, and run the installer::

    [download]
    $ tar -xvzf pox-%(thisver)s.tgz
    $ cd pox-%(thisver)s
    $ python setup py build
    $ python setup py install

You will be warned of any missing dependencies and/or settings
after you run the "build" step above. 

Alternately, pox can be installed with easy_install::

    [download]
    $ easy_install -f . pox


Requirements
============

Pox requires::

    - python, version >= 2.5, version < 3.0

Optional requirements::

    - setuptools, version >= 0.6


Usage Notes
===========

Probably the best way to get started is to look at the tests
that are provided within pox. See `pox.tests` for a set of scripts
that demonstrate pox's ability to interact with the operating system.
Pox utilities can also be run directly from an operating system terminal,
using the `pox_launcher.py` script.

Important utilities and functions are found here::

    - pox.pox.shutils             [low-level shell utilities]
    - pox.pox.utils               [high-level shell utilities]


License
=======

Pox is distributed under a modified BSD license.

    >>> import pox
    >>> print pox.license()


Citation
========

If you use pox to do research that leads to publication,
we ask that you acknowledge use of pox by citing the
following in your publication::

    M.M. McKerns, L. Strand, T. Sullivan, A. Fang, M.A.G. Aivazis,
    "Building a framework for predictive science", Proceedings of
    the 10th Python in Science Conference, 2011;
    http://arxiv.org/pdf/1202.1056

    Michael McKerns and Michael Aivazis,
    "pathos: a framework for heterogeneous computing", 2010- ;
    http://dev.danse.us/trac/pathos


More Information
================

Please see http://dev.danse.us/trac/pathos or http://arxiv.org/pdf/1202.1056 for further information.

""" % {'relver' : stable_version, 'thisver' : this_version}

# write readme file
with open('README', 'w') as file:
    file.write(long_description)

# generate 'info' file contents
def write_info_py(filename='pox/info.py'):
    contents = """# THIS FILE GENERATED FROM SETUP.PY
this_version = '%(this_version)s'
stable_version = '%(stable_version)s'
readme = '''%(long_description)s'''
license = '''%(license_text)s'''
"""
    with open(filename, 'w') as file:
        file.write(contents % {'this_version' : this_version,
                               'stable_version' : stable_version,
                               'long_description' : long_description,
                               'license_text' : license_text })
    return

# write info file
write_info_py()

# build the 'setup' call
setup_code = """
setup(name='pox',
      version='%s',
      description='utilities for filesystem exploration and automated builds',
      long_description = '''%s''',
      author = 'Mike McKerns',
      maintainer = 'Mike McKerns',
      maintainer_email = 'mmckerns@caltech.edu',
      license = 'BSD',
      platforms = ['any'],
      url = 'http://www.cacr.caltech.edu/~mmckerns',
      classifiers = ('Intended Audience :: Developers',
                     'Programming Language :: Python',
                     'Topic :: Physics Programming'),

      packages = ['pox'],
      package_dir = {'pox':'pox'},
""" % (target_version, long_description)

'''
# add dependencies
dummy_version = '>=0.1'
if has_setuptools:
    setup_code += """
        install_requires = ['dummy%s'],
""" % (dummy_version)
'''

# close 'setup' call
setup_code += """    
      zip_safe=True,
      scripts=['scripts/pox_launcher.py'])
"""

# exec the 'setup' code
exec setup_code

# if dependencies are missing, print a warning
try:
    pass
except ImportError:
    print "\n***********************************************************"
    print "WARNING: One of the following dependencies is unresolved:"
#   print "    dummy %s" % dummy_version
    print "***********************************************************\n"


if __name__=='__main__':
    pass

# end of file
