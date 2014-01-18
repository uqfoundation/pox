#!/usr/bin/env python

"""
test pox's higher-level shell utilities
"""
import os

def test():
    '''test(); script to test all functions'''
    from pox import *
    print 'testing pattern...'
    print pattern(['PYTHON*','DEVELOPER'])
    print pattern([])

    print 'testing getvars...'
    bogusdict = {'PYTHIA_STUFF':'${DV_DIR}/pythia-${PYTHIA_VERSION}/stuff',
                 'MIKE_VERSION':'1.0','MIKE_DIR':'${HOME}/junk',
                 'DUMMY_VERSION':'6.9','DUMMY_STUFF':'/a/b',
                 'DV_DIR':'${HOME}/dev', 'PYTHIA_VERSION':'0.0.1'}
    home = homedir()
    print getvars(home)
    print getvars('${DV_DIR}/pythia-${PYTHIA_VERSION}/stuff',bogusdict)
    print getvars('${MIKE_DIR}/stuff',bogusdict)
    print getvars('${HOME}/stuff')

    print 'testing expandvars...'
    print expandvars(home)
    print expandvars('${DV_DIR}/pythia-${PYTHIA_VERSION}/stuff')
    print expandvars('${MIKE_DIR}/${DV_DIR}/stuff',bogusdict)
    print expandvars('${DV_DIR}/${PYTHIA_VERSION}',secondref=bogusdict)
    print expandvars('${DV_DIR}/${PYTHIA_VERSION}',bogusdict,os.environ)
    print expandvars('${HOME}/stuff')

    print 'testing convert...'
    source = 'test.txt'
    f = open(source,'w')
    f.write('this is a test file.'+os.linesep)
    f.close()
    convert(source,'mac')
    convert(source)

    print 'testing replace...'
    replace(source,{' is ':' was '})
    replace(source,{'\sfile.\s':'.'})
    f = open(source,'r')
    print f.read()
    f.close()
    os.remove(source)

    print 'testing index_join...'
    fl = ['begin\n','hello\n','world\n','string\n']
    print index_join(fl,'hello\n','world\n')

    print 'testing findpackage...'
    print findpackage('python*','/usr/lib',all=True)
    print findpackage('lib/python*',env('HOME',all=False),all=False)

    print 'testing makeTarget...'
    myhost = 'login.cacr.caltech.edu'
    print makeTarget('~/dev')
    print makeTarget('~/dev',forceSSH=True)
    print makeTarget('~/dev',host=myhost,user=username())

    print 'testing parseTarget...'
    destination = 'danse@%s:~/dev' % myhost
    print parseTarget(destination,useOption=True)
    destination = 'danse@%s:' % myhost
    print parseTarget(destination)
    destination = '%s:' % myhost
    print parseTarget(destination,useOption=True)
    destination = 'test.txt'
    print parseTarget(destination,forceSSH=True)

    print 'testing prunelist...'
    testlist = ['zero','one','two','three','4','five','six','seven','8','9/81']
    print prunelist(testlist)
    print prunelist(testlist,minimum=False)
    print prunelist(testlist,minimum=False,reverse=True,all=False)
    print prunelist(testlist,counter=os.sep,minimum=False,all=False)

    print 'testing prunedict...'
    print prunedict(bogusdict)
    print prunedict(bogusdict,minimum=False,counter=os.sep)
    print prunedict(bogusdict,minimum=False,counter=os.sep,all=False)
    return

if __name__=='__main__':
    test()


# End of file 
