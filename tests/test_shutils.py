#!/usr/bin/env python

"""
test pox's shell utilities
"""
from pox import *

def test():
    '''test(); script to test all functions'''
    print 'testing getSHELL...'
    print getSHELL()

    print 'testing getHOME...'
    print getHOME()

    print 'testing getROOT...'
    print getROOT()

    print 'testing getSEP...'
    print getSEP()
    print getSEP('ext')
#   print getSEP('foo')

    print 'testing mkdir...'
    newdir = 'xxxtest/testxxx'
    print mkdir(newdir)
    print 'cleaning up...'
    os.removedirs(newdir)

    print 'testing walk...'
    print walk('/usr/local','*',recurse=0,folders=1,files=0)
    homedir = walk(getHOME()+getSEP()+"..", getUSER(), 0, 1)[0]
    print homedir
    print walk(homedir,'.bashrc',recurse=0)

    print 'testing where...'
    bashrc = where('.bashrc',homedir)
    print bashrc

    print 'testing stripDups...'
    print stripDups(os.path.expandvars('$PATH'))

    print 'testing env...'
    print env('TEST')
    print env('HOME',1)
    print env('TOOLS*')
    print env('*PATH*',pathDups=False)

    print 'testing getUSER...'
    print getUSER()

    print 'testing which...'
    print which('python')
    print which('python',allowlink=False)
    print which('python',listall=True)

    print 'testing find...'
    print find('python','/usr/local',type='l')
    print find('*py;*txt')

    print 'testing shellsub...'
    command = '${HOME}/bin/which foo("bar")'
    print command
    print shellsub(command)

    return


if __name__=='__main__':
    test()


# End of file 
