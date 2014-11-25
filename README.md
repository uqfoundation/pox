pox
===
utilities for filesystem exploration and automated builds

About Pox
---------
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
Pox is in active development, so any user feedback, bug reports, comments,
or suggestions are highly appreciated.  A list of known issues is maintained
at http://trac.mystic.cacr.caltech.edu/project/pathos/query, with a public
ticket list at https://github.com/uqfoundation/pox/issues.


Major Features
--------------
Pox provides utilities for discovering the user's environment::

* return the user's name, current shell, and path to user's home directory
* strip duplicate entries from the user's $PATH
* lookup and expand environment variables from ${VAR} to 'value'

Pox also provides utilities for filesystem exploration and manipulation::

* discover the path to a file, exectuable, directory, or symbolic link 
* discover the path to an installed package
* parse operating system commands for remote shell invocation
* convert text files to platform-specific formatting


Current Release
---------------
The latest stable release of pox is available from::
    http://trac.mystic.cacr.caltech.edu/project/pathos

or::
    https://github.com/uqfoundation/pox/releases

or also::
    https://pypi.python.org/pypi/pox

Pox is distributed under a 3-clause BSD license.


Development Version
-------------------
You can get the latest development version with all the shiny new features at::
    https://github.com/uqfoundation

Feel free to fork the github mirror of our svn trunk.  If you have a new
contribution, please submit a pull request.


More Information
----------------
Probably the best way to get started is to look at the tests that are
provided within pox. See `pox.tests` for a set of scripts that demonstrate
pox's ability to interact with the operating system.  Pox utilities can
also be run directly from an operating system terminal, using the
`pox_launcher.py` script.  The source code is also generally well
documented, so further questions may be resolved by inspecting the code
itself.  Please also feel free to submit a ticket on github, or ask a
question on stackoverflow (@Mike McKerns).

Pox is an active research tool. There are a growing number of publications
and presentations that discuss real-world examples and new features of pox
in greater detail than presented in the user's guide.  If you would like to
share how you use pox in your work, please post a link or send an email
(to mmckerns at caltech dot edu).


Citation
--------
If you use pox to do research that leads to publication, we ask that you
acknowledge use of pox by citing the following in your publication::

    M.M. McKerns, L. Strand, T. Sullivan, A. Fang, M.A.G. Aivazis,
    "Building a framework for predictive science", Proceedings of
    the 10th Python in Science Conference, 2011;
    http://arxiv.org/pdf/1202.1056

    Michael McKerns and Michael Aivazis,
    "pathos: a framework for heterogeneous computing", 2010- ;
    http://trac.mystic.cacr.caltech.edu/project/pathos

Please see http://trac.mystic.cacr.caltech.edu/project/pathos or
http://arxiv.org/pdf/1202.1056 for further information.

