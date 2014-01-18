#!/usr/bin/env python

"""
test pox's higher-level shell utilities
"""
import os

def test():
    '''test(); script to test all functions'''
    from pox import pattern, getvars, expandvars, convert, replace, \
                    index_join, findpackage, remote, parse_remote, \
                    select, selectdict, env, homedir, username

    print('testing pattern...')
    print(pattern(['PYTHON*','DEVELOPER']))
    print(pattern([]))

    print('testing getvars...')
    bogusdict = {'PYTHIA_STUFF':'${DV_DIR}/pythia-${PYTHIA_VERSION}/stuff',
                 'MIKE_VERSION':'1.0','MIKE_DIR':'${HOME}/junk',
                 'DUMMY_VERSION':'6.9','DUMMY_STUFF':'/a/b',
                 'DV_DIR':'${HOME}/dev', 'PYTHIA_VERSION':'0.0.1'}
    home = homedir()
    print(getvars(home))
    print(getvars('${DV_DIR}/pythia-${PYTHIA_VERSION}/stuff',bogusdict))
    print(getvars('${MIKE_DIR}/stuff',bogusdict))
    print(getvars('${HOME}/stuff'))

    print('testing expandvars...')
    print(expandvars(home))
    print(expandvars('${DV_DIR}/pythia-${PYTHIA_VERSION}/stuff'))
    print(expandvars('${MIKE_DIR}/${DV_DIR}/stuff',bogusdict))
    print(expandvars('${DV_DIR}/${PYTHIA_VERSION}',secondref=bogusdict))
    print(expandvars('${DV_DIR}/${PYTHIA_VERSION}',bogusdict,os.environ))
    print(expandvars('${HOME}/stuff'))

    print('testing convert...')
    source = 'test.txt'
    f = open(source,'w')
    f.write('this is a test file.'+os.linesep)
    f.close()
    convert(source,'mac')
    convert(source)

    print('testing replace...')
    replace(source,{' is ':' was '})
    replace(source,{'\sfile.\s':'.'})
    f = open(source,'r')
    print(f.read())
    f.close()
    os.remove(source)

    print('testing index_join...')
    fl = ['begin\n','hello\n','world\n','string\n']
    print(index_join(fl,'hello\n','world\n'))

    print('testing findpackage...')
    print(findpackage('python*','/usr/lib',all=True))
    print(findpackage('lib/python*',env('HOME',all=False),all=False))

    print('testing remote...')
    myhost = 'login.cacr.caltech.edu'
    print(remote('~/dev'))
    print(remote('~/dev',loopback=True))
    print(remote('~/dev',host=myhost,user=username()))

    print('testing parse_remote...')
    destination = 'danse@%s:~/dev' % myhost
    print(parse_remote(destination,login_flag=True))
    destination = 'danse@%s:' % myhost
    print(parse_remote(destination))
    destination = '%s:' % myhost
    print(parse_remote(destination,login_flag=True))
    destination = 'test.txt'
    print(parse_remote(destination,loopback=True))

    print('testing select...')
    test = ['zero','one','two','three','4','five','six','seven','8','9/81']
    print(select(test))
    print(select(test,minimum=True))
    print(select(test,reverse=True,all=False))
    print(select(test,counter=os.sep,all=False))
    test = [[1,2,3],[4,5,6],[1,3,5]]
    print(select(test))
    print(select(test,counter=3))
    print(select(test,counter=3,minimum=True))

    print('testing selectdict...')
    print(selectdict(bogusdict,minimum=True))
    print(selectdict(bogusdict,counter=os.sep))
    print(selectdict(bogusdict,counter=os.sep,all=False))
    return

if __name__=='__main__':
    test()


# End of file 
