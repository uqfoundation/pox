#!/usr/bin/env python
#
## higher-level shell utilities
# adapted from Mike McKerns' gsl.infect.utils
# by mmckerns@caltech.edu

"""
higher-level shell utilities for user environment and filesystem exploration
"""

from __future__ import absolute_import
import os
from . import shutils
from ._disk import kbytes, disk_used

#NOTE: broke backward compatibility January 17, 2014
#      seperator --> separator
def pattern(list=[],separator=';'):
    '''pattern([list,separator]); Generate a filter pattern from list of strings

    The returned filter is a string, with items seperated by separator'''
    filter = ''
    for item in list:
        filter += '%s%s' % (str(item),str(separator))
    return filter.rstrip(str(separator))

_varprog = None
def expandvars(string,ref=None,secondref={}):
    """expandvars(string[,ref,secondaryref]); expand shell variables in string

    Expand shell variables of form $var and ${var}.  Unknown variables
    are left unchanged. If a reference dictionary (ref) is provided,
    restrict the lookup to ref. A second reference dictionary (secondref)
    can also be provided for failover searches. If ref is not provided,
    lookup variables defined in the user\'s environment variables.

    For example:
        >>> expandvars(\'found:: $PYTHONPATH\')
        \'found:: .:/Users/foo/lib/python3.4/site-packages\'

        >>> expandvars(\'found:: $PYTHONPATH\', ref={})
        \'found:: $PYTHONPATH\'
    """
    if ref is None: ref = os.environ
    refdict = {}
    refdict.update(secondref)
    refdict.update(ref)
    global _varprog
    if '$' not in string:
        return string
    if not _varprog:
        import re
        _varprog = re.compile(r'\$(\w+|\{[^}]*\})')
    i = 0
    while True:
        m = _varprog.search(string, i)
        if not m:
            break
        i, j = m.span(0)
        name = m.group(1)
        if name[:1] == '{' and name[-1:] == '}':
            name = name[1:-1]
        if name in refdict:
            tail = string[j:]
            string = string[:i] + refdict[name]
            i = len(string)
            string = string + tail
        else:
            i = j
    return string

#NOTE: broke backward compatibility January 17, 2014
#      vdict --> ref
def getvars(path,ref=None):
    '''getvars(path[,ref]); Get a dictionary of all variables defined in path

    Extract shell variables of form $var and ${var}.  Unknown variables
    will raise an exception. If a reference dictionary (ref) is provided,
    first try the lookup in ref.  Failover from ref will lookup variables
    defined in the user\'s environment variables.

    For example:
        >>> getvars(\'$HOME/stuff\')
        {\'HOME\': \'/Users/foo\'}
    '''
    #what about using os.path.expandvars ?
    if ref is None: ref = {}
    ndict = {}
    dirs = path.split(os.sep)
    for dir in dirs:
        if '$' in dir:
            key = dir.split('$')[1].lstrip('{').rstrip('}')
            #get value from ref, or failing...
            try:
                ndict[key] = ref[key]
            #get value from os.environ, or failing... raise a KeyError
            except KeyError:
                ndict[key] = os.environ[key]
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
        print("Error: Platform '%s' not recognized" % platform)
        return 2 # Error 2: platform not recognized
    allconverted = 0 # Success
    for file in files.split(pathsep):
        try:
            infile = open(file, 'r')
            filestring = infile.read()
            infile.close()
            for i in linesep:
                filestring = filestring.replace(i, newlinesep)
            outfile = open(file, 'w')
            outfile.write(filestring)
            outfile.close()
            print("Converted '%s' to '%s' format" % (file,platform))
        except:
            print("File conversion failed for '%s'" % (file))
            allconverted = 1 # Error 1: file conversion failed
    return allconverted

def replace(file,sub={},outfile=None):
    '''replace(file,[sub,outfile]); Replace text {old:new} in the given file

    file: path to original file
    sub: dictionary of strings to replace, with entries of {old:new}
    outfile: if an outfile is given, don't overwrite the original file

    replace uses regular expressions, thus a pattern may be given as old text.
    Note this function can fail if order of substitution is important.'''
    #XXX: use OrderedDict instead... would enable ordered substitutions
    if outfile == None: outfile = file
    input = open(file, 'r')
    filestring = input.read()
    input.close()
    import re
    for old,new in sub.items():
        filestring = re.compile(old).sub(new,filestring)
    output = open(outfile, 'w')
    output.write(filestring)
    output.close()
    return

def index_slice(sequence,start,stop,step=1,sequential=False,inclusive=False):
    '''index_slice(sequence,start,stop[,step,sequential,inclusive]);
    Get the slice for a sequence, where the slice indicies are determined
    by the positions of \'start\' and \'stop\' within the sequence.

    If start is not found in the sequence, slice from the beginning. If stop
    is not found in the sequence, slice to the end. If inclusive=False,
    slicing will be performed with standard conventions (i.e. include start,
    but not stop); if inclusive=True, stop will be included. If sequential,
    then stop will not be searched for before start.'''
    if start in sequence:
        begin = sequence.index(start)
    else: begin = None
    if sequential: here = None
    else: here = begin
    if stop in sequence[here:]:
        end = sequence[here:].index(stop)
        if here: end += here
    else: end = None
    if inclusive and end != None: end += 1
    return slice(begin,end,step)

def index_join(sequence,start,stop,step=1,sequential=True,inclusive=True):
    '''index_join(sequence,start,stop[,step,sequential,inclusive]);
    Slices a list of strings, then joins the remaining strings.

    If start is not found in the sequence, slice from the beginning. If stop
    is not found in the sequence, slice to the end. If inclusive=False,
    slicing will be performed with standard conventions (i.e. include start,
    but not stop); if inclusive=True, stop will be included. If sequential,
    then stop will not be searched for before start.'''
    islice = index_slice(sequence,start,stop,step,sequential,inclusive)
    return ''.join(sequence[islice])

#NOTE: broke backward compatibility January 17, 2014
#      firstval=False --> all=False
def findpackage(package,root=None,all=False):
    '''findpackage(package[,root,all]); Get path(s) for a source distribution

    root: path string of top-level directory to search
    all: if True, return list of paths where package is found

    findpackage will do standard pattern matching for names of packages,
    attempting to match the head directory of the distribution
    '''
    if not root: root = os.curdir
    print('searching %s...' % root)
    if package[0] != os.sep: package = os.sep+package
    packdir,basedir = os.path.split(package)
    targetdir = shutils.find(basedir,root,recurse=1,type='d')
    #print("targetdir: "+targetdir)
    #remove invalid candidate directories (and 'BLD_ROOT' & 'EXPORT_ROOT')
    bldroot = shutils.env('BLD_ROOT',all=False)
    exproot = shutils.env('EXPORT_ROOT',all=False)
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
    if targetdir: print('%s found' % package)
    else: print('%s not found' % package)
    if all:
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


# backward compatability
makefilter = pattern
getVars = getvars
replaceText = replace
getLines = index_join


if __name__=='__main__':
    pass


# End of file 
