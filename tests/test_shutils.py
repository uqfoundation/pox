#!/usr/bin/env python

"""
test pox's shell utilities
"""
import os

def test():
    '''test(); script to test all functions'''
    from pox import *
    print 'testing shelltype...'
    print shelltype()

    print 'testing homedir...'
    print homedir()

    print 'testing rootdir...'
    print rootdir()

    print 'testing sep...'
    print sep()
    print sep('ext')
#   print sep('foo')

    print 'testing mkdir...'
    newdir = 'xxxtest/testxxx'
    print mkdir(newdir)
    print 'cleaning up...'
    os.removedirs(newdir)

    print 'testing walk...'
    print walk('/usr/local','*',recurse=0,folders=1,files=0)
    homedir = walk(homedir()+sep()+"..", username(), 0, 1)[0]
    print homedir
    print walk(homedir,'.bashrc',recurse=0)

    print 'testing where...'
    bashrc = where('.bashrc',homedir)
    print bashrc

    print 'testing minpath...'
    print minpath(os.path.expandvars('$PATH'))

    print 'testing env...'
    print env('TEST')
    print env('HOME',all=False)
    print env('TOOLS*')
    print env('*PATH*',minimal=True)

    print 'testing username...'
    print username()

    print 'testing which...'
    print which('python')
    print which('python',allow_links=False)
    print which('python',all=True)

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
