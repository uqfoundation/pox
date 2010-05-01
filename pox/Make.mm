# -*- Makefile -*-
 
PROJECT = pox
PACKAGE = pox

BUILD_DIRS = 
RECURSE_DIRS = $(BUILD_DIRS)

PROJ_TIDY += *.txt
PROJ_CLEAN = 

#--------------------------------------------------------------------------
#

all: export
	BLD_ACTION="all" $(MM) recurse

release: tidy
	cvs release .

update: clean
	cvs update .

#--------------------------------------------------------------------------
#
# export

EXPORT_PYTHON_MODULES = \
    __init__.py      \
    utils.py         \
    shutils.py       \

export:: export-python-modules

# End of file
