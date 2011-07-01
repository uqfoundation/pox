#!/usr/bin/env python
#
# Michael McKerns
# mmckerns@caltech.edu

# check if easy_install is available
try:
#   import __force_distutils__ #XXX: uncomment to force use of distutills
    from setuptools import setup
    has_setuptools = True
except ImportError:
    from distutils.core import setup
    has_setuptools = False

# build the 'setup' call
setup_code = """
setup(name='pox',
      version='0.1a2.dev',
      description='utilities for filesystem exploration and automated builds',
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
"""

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
