# -*- Makefile -*-

PROJECT = pox
PACKAGE = scripts

PROJ_TIDY += *.log *.out
PROJ_CLEAN =

#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
#

EXPORT_BINS = \
    pox_launcher.py \

export:: export-binaries release-binaries

# End of file
