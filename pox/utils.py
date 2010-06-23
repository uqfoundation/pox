#!/usr/bin/env python
#
## higher-level shell utilities
# adapted from Mike McKerns' gsl.infect.utils
# by mmckerns@caltech.edu

"""
higher-level shell utilities for user environment and filesystem exploration
"""

import os
import shutils

def makefilter(list=[],seperator=';'):
    '''makefilter([list,seperator]) --> filter pattern generated from a list
    returned filter is a string, with items seperated by seperator'''
    filter = ''
    for item in list:
        filter += '%s%s' % (str(item),str(seperator))
    return filter.rstrip(str(seperator))

_varprog = None
def expandvars(path,ref=None,secondref={}):
    """expandvars(string[,ref,secondaryref]) --> string with replaced vars
    vars will reference to ref first, and optionally secondref afterward.
    Expand shell variables of form $var and ${var}.  Unknown variables
    are left unchanged."""
    if not ref: ref = os.environ
    refdict = {}
    refdict.update(secondref)
    for key,value in ref.items():
        refdict[key] = value
    global _varprog
    if '$' not in path:
        return path
    if not _varprog:
        import re
        _varprog = re.compile(r'\$(\w+|\{[^}]*\})')
    i = 0
    while True:
        m = _varprog.search(path, i)
        if not m:
            break
        i, j = m.span(0)
        name = m.group(1)
        if name[:1] == '{' and name[-1:] == '}':
            name = name[1:-1]
        if name in refdict:
            tail = path[j:]
            path = path[:i] + refdict[name]
            i = len(path)
            path = path + tail
        else:
            i = j
    return path

def getVars(value,vdict={}):
    '''getVars(value[,vdict]) --> newdict
    if value has environment variables, retrieve them from vdict;
    or if vdict=None, get them from os.environ'''
    #what about using os.path.expandvars ?
    ndict = {}
    dirs = value.split(os.sep)
    for dir in dirs:
        if '$' in dir:
            key = dir.split('$')[1].lstrip('{').rstrip('}')
            if vdict.has_key(key): #get the value from vdict
                val = vdict[key]
            else:  #get the current value or raise a KeyError
                val = os.environ[key] #get the current environment value
            ndict[key] = val
    return ndict

def convert(files,platform=None,pathsep=None):
    '''convert(files[,platform,pathsep])
    Convert text files to given platform type (os.linesep is not good enough)'''
    if not platform: platform = os.name
    if not pathsep: pathsep = os.pathsep
    MAC = '\r'
    WIN = '\r\n'
    LIN = '\n'
    linesep = [WIN,MAC,LIN]
    #os.name ==> ['posix','nt','os2','mac','ce','riscos']
    if platform in ['linux2','linux','unix','lin','posix','riscos']: #???
        newlinesep = LIN
    elif platform in ['windows','mswindows','win','dos','nt','os2','ce']: #???
        newlinesep = WIN
    elif platform in ['mac','macosx']: #???
        newlinesep = MAC
    else:
        print "Error: Platform '%s' not recognized" % platform
        return 0
    allconverted = 1
    import string
    for file in string.split(files, pathsep):
        try:
            infile = open(file, 'r')
            filestring = infile.read()
            infile.close()
            for i in linesep:
                filestring = string.replace(filestring, i, newlinesep)
            outfile = open(file, 'w')
            outfile.write(filestring)
            outfile.close()
            print "Converted '%s' to '%s' format" % (file,platform)
        except:
            print "File conversion failed for '%s'" % (file)
            allconverted = 0
    return allconverted

def replaceText(infile,sub={},outfile=None):
    '''replaceText(infile,[sub,outfile]) --> replace text {old:new} in a file
    this function uses regular expressions, if a pattern is given as old text
    Note: this may fail if order of substitution is important'''
    if outfile == None: outfile = infile
    input = open(infile, 'r')
    filestring = input.read()
    input.close()
    import re
    for old,new in sub.items():
        filestring = re.compile(old).sub(new,filestring)
    output = open(outfile, 'w')
    output.write(filestring)
    output.close()
    return

def getLines(fl,begin,end):
    '''getLines(list,begin,end) --> get lines inclusive from begin to end'''
    add = 0
    for line in fl:
        if line in [begin]:
            chunk = line
            if end is begin:
                return chunk
            add = 1
        elif line in [end]:
            chunk += line
            add = 0
        elif add == 1:
            chunk += line
    return chunk

def findpackage(package,root=None,firstval=0):
    '''findpackage(package[,root,firstval]) --> path(s) to package'''
    if not root: root = os.curdir
    print 'searching %s...' % root
    if package[0] != os.sep: package = os.sep+package
    packdir,basedir = os.path.split(package)
    targetdir = shutils.find(basedir,root,recurse=1,type='d')
    #print "targetdir" ,targetdir
    #remove invalid candidate directories (and 'BLD_ROOT' & 'EXPORT_ROOT')
    bldroot = shutils.env('BLD_ROOT',firstval=1)
    exproot = shutils.env('EXPORT_ROOT',firstval=1)
    remlist = []
    import fnmatch
    for dir in targetdir:
        if (not fnmatch.fnmatch(dir,'*'+package)) or \
           (not fnmatch.fnmatch(os.path.basename(dir),basedir)) or \
           ((bldroot) and (bldroot in dir)) or \
           ((exproot) and (exproot in dir)):
            remlist.append(dir) #build list of bad matches
    for dir in remlist:
        targetdir.remove(dir)
    if targetdir: print '%s found' % package
    else: print '%s not found' % package
    if not firstval:
        return targetdir
    return prunelist(targetdir,counter=os.sep,all=False)

def prunelist(targetlist,counter='',minimum=True,reverse=False,all=True):
    '''prunelist(list[,counter,minimum,reverse,all]) --> pruned list'''
    m = []
    for item in targetlist:
        m.append(item.count(counter))
    if reverse:
        m.reverse()
        targetlist.reverse()
    if not m:
        if all == True:
            return []
        else:
            return ''
    if minimum:
        x = min(m)
    else: x = max(m)
    if not all:
        return targetlist[m.index(x)]
    shortlist = []
    tmp = []
    for item in targetlist: tmp.append(item)
    occurances = m.count(x)
    for i in range(occurances):
        shortlist.append(tmp.pop(m.index(x)))
        m.pop(m.index(x))
    return shortlist

def prunedict(target,counter='',minimum=True,all=True):
    '''prunedict(dict[,counter,miminum,all]) --> pruned dict'''
    keylist = []
    vallist = []
    for key,value in target.items():
        keylist.append(key)
        vallist.append(value)
    shortlist = prunelist(vallist,counter,minimum,all=all)
    shortdict = {}
    if not all:
        x = vallist.index(shortlist)
        shortdict[keylist[x]] = vallist[x]
        return shortdict
    for i in range(len(vallist)):
        if vallist[i] in shortlist:
            shortdict[keylist[i]] = vallist[i]
    return shortdict

def makeTarget(target,host=None,user=None,forceSSH=False):
    '''makeTarget(path[,host,user,forceSSH]) --> [[user@]host:]path'''
    if forceSSH and not host: host = 'localhost'
    if host:
        target = '%s:%s' % (host,target)
        if user:
            target = '%s@%s' % (user,target)
    return target

def parseTarget(target,forceSSH=False,useOption=False):
    """parseTarget(target[,forceSSH,useOption]) --> (login, host, path)
    if useOption, then login will prepend '-l' if login is included"""
    dpath = target.split(':')[-1]
    rhost = target.split(':')[0]
    if rhost == dpath:
        if forceSSH: return '','localhost',dpath
        return '','',dpath
    dhost = rhost.split('@')[-1]
    duser = rhost.split('@')[0]
    if duser == dhost: return '',dhost,dpath
    if useOption: duser = '-l '+duser
    return duser,dhost,dpath


if __name__=='__main__':
    pass


# End of file 
