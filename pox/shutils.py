#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2015 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pox/LICENSE
#
# adapted from Mike McKerns' gsl.infect.shutils
"""
shell utilities for user environment and filesystem exploration
"""

from __future__ import absolute_import
import os
import sys
from subprocess import Popen, PIPE, STDOUT
popen4 = {'shell':True, 'stdin':PIPE, 'stdout':PIPE, 'stderr':STDOUT, \
          'close_fds':True}
from ._disk import rmtree

if sys.version_info[0] < 3:
    MODE = eval('0775')
else:
    MODE = eval('0o775')

def shelltype():
    '''shelltype(); Get the name (e.g. \'bash\') of the current command shell'''
    shell = env('SHELL',all=False) or env('SESSIONNAME',all=False)
    if shell in ('Console',): shell = 'cmd' # or not?
    return os.path.basename(shell) if shell else None

def homedir():
    '''homedir(); Get the full path of the user\'s home directory'''
    try:
        homedir = env('USERPROFILE',all=False) or os.path.expandvars('$HOME')
        if '$' in homedir: raise ValueError
        return homedir
    except:
        homedir = None
        directory = os.curdir
        while not homedir:
            homedir = where(username(),os.path.abspath(directory))
            directory = os.path.join(os.pardir,directory)
        return homedir

def rootdir():
    '''rootdir(); Get the path corresponding to the root of the current drive'''
    return os.path.splitdrive(os.getcwd())[0]+os.sep

def username():
    '''username(); Get the login name of the current user'''
    try:
        return os.getlogin()
    except:
        uname = os.path.expandvars('$USER')
        if '$' in uname: uname = env('USERNAME', all=False)
        return uname

def sep(type=''):
    '''sep([type]); Get the seperator, type is one of {sep,line,path,ext,alt}'''
    if type in ['path','pathsep']: return os.pathsep
    elif type in ['ext','extsep']: return os.extsep
    elif type in ['line','linesep']: return os.linesep
    elif type in ['alt','altsep']: return os.altsep
    elif type not in ['','sep']:
        if not type.endswith('sep'): type += 'sep'
        print("Error: 'os.%s' not found" % type)
        raise TypeError
    return os.sep
    

def minpath(path,pathsep=None):
    '''minpath(path[,pathsep]); remove duplicate paths from given set of paths

    path: path string (e.g. \'/Users/foo/bin:/bin:/sbin:/usr/bin\')
    pathsep: path separator (e.g. \':\'); if none provided, use OS default

    For example:
        >>> minpath(\'.:/Users/foo/bin:.:/Users/foo/bar/bin:/Users/foo/bin\')
        \'.:/Users/foo/bin:/Users/foo/bar/bin\'
    '''
    if not pathsep: pathsep = os.pathsep
    pathlist = path.split(pathsep) 
    shortlist = []
    for item in pathlist:
        if item not in shortlist:
            shortlist.append(item)
    return pathsep.join(shortlist)

#NOTE: broke backward compatibility January 17, 2014
#      firstval=False --> all=True
#      pathDups=True  --> minimal=False
def env(variable,all=True,minimal=False):
    '''env(variable[,all,minimal]); get dict of environment {variable:value}

    variable: name or partial name string for environment variable
    all: if False, only return the first match [NOTE: use at own risk!!!]
    minimal: if True, remove all duplicate paths from the returned path string

    For example:
        >>> env(\'*PATH\')
        {\'PYTHONPATH\': \'.\', \'PATH\': \'.:/usr/bin:/bin:/usr/sbin:/sbin\'}
    '''
    #better than os.path.expandvars ?
    import fnmatch
    vals = {}
    for key,value in os.environ.items():
        if fnmatch.fnmatch(key,variable):
            vals[key] = value
    if minimal:
        for key,value in vals.items():
            if fnmatch.fnmatch(key,'*PATH'):
                vals[key] = minpath(value)
    if not all:
        if len(vals) == 0: return
        return list(vals.values())[0]
    return vals

#NOTE: broke backward compatibility January 17, 2014
#      listall --> all
def whereis(prog,all=False): #Unix specific (Windows punts to which)
    '''whereis(prog[,all]); Get path to the given program

    prog: name of an executable to search for (e.g. python)
    all: if True, return list of paths where executable is found

    whereis searches standard binary install locations for the given executable
    '''
    if sys.platform[:3] == 'win': return which(prog,all=all)
    whcom = 'whereis '
    p = Popen(whcom+prog, **popen4)
    p.stdin.close()
    pathstr = p.stdout.read()
    p.stdout.close()
    if sys.version_info[0] > 2:
        pathstr = pathstr.decode()
    paths = pathstr.strip().split(":")[-1] #XXX: ':' ???  -1 ???
    pathlist = paths.strip().split()
    if not pathlist:
        if not all: pathlist = ''
        return pathlist
    if not all: return pathlist[0]
    return pathlist

#NOTE: broke backward compatibility January 17, 2014
#      allowlink=True   --> allow_links=True
#      allowerror=False --> ignore_errors=True
#      listall=False    --> all=False
def which(prog,allow_links=True,ignore_errors=True,all=False): #Unix specific
    '''which(prog[,allow_links,ignore_errors,all]); Get path of given program

    prog: name of an executable to search for (e.g. python)
    allow_links: if False, convert all links to the real paths
    ignore_errors: if True, ignore errors (e.g. not finding \'prog'\)
    all: if True, return list of paths where executable is found

    which searches the user\'s paths for the given executable
    '''
    if sys.platform[:3] == 'win':
        # try to deal with windows laziness about extensions
        if not prog.endswith('.exe'): prog += '' if prog.count('.') else '.exe'
        dirs = env('PATH',all=False) or os.path.abspath(os.curdir) # ?
        paths = []
        _type = None if allow_links else 'file'
        for _dir in dirs.split(os.pathsep):
            if all and paths: break
            paths += find(prog, root=_dir, recurse=False, type=_type)
        if not all: return paths[0] if len(paths) else ''
        return paths
    # non-windows
    whcom = 'which '
    if all: whcom += '-a '
    p = Popen(whcom+prog, **popen4)
    p.stdin.close()
    pathstr = p.stdout.read()
    p.stdout.close()
    errind = 'no '+prog+' in'
    if sys.version_info[0] > 2:
        pathstr = pathstr.decode()
    if (errind in pathstr) and (ignore_errors):
        return None
    pathstr = minpath(pathstr.strip(),os.linesep)
    paths = pathstr.split(os.linesep)
    for i in range(len(paths)):
        if not allow_links and os.path.islink(paths[i]):
            paths[i] = os.path.realpath(paths[i])
    if not all: return paths[0] if len(paths) else ''
    return paths
    
def find(patterns,root=None,recurse=True,type=None,verbose=False):
    '''find(patterns[,root,recurse,type]); Get path to a file or directory

    patterns: name or partial name string of items to search for
    root: path string of top-level directory to search
    recurse: if True, recurse down from root directory
    type: item filter; one of {None, file, dir, link, socket, block, char}
    verbose: if True, be a little verbose about the search

    On some OS, recursion can be specified by recursion depth (an integer).
    patterns can be specified with basic pattern matching. Additionally,
    multiple patterns can be specified by splitting patterns with a \';'\

    For example:
        >>> find(\'pox*\', root=\'..\')
        [\'/Users/foo/pox/pox\', \'/Users/foo/pox/scripts/pox_launcher.py\']

        >>> find(\'*shutils*;*init*\')
        [\'/Users/foo/pox/pox/shutils.py\', \'/Users/foo/pox/pox/__init__.py\']
    '''
    if not root: root = os.curdir
    if type is None: pass
    elif type in ['f','file']: type = 'f'
    elif type in ['d','dir']: type = 'd'
    elif type in ['l','link']: type = 'l'
    elif type in ['s','socket']: type = 's'
    elif type in ['b','block']: type = 'b'
    elif type in ['c','char']: type = 'c'
    else:
        if verbose: print("type '%s' not understood, will be ignored" % type)
        type = None
    try:
        if sys.platform[:3] == 'win': raise NotImplementedError
        pathlist = []
        search_list = patterns.split(';')
        for item in search_list:
            command = 'find %s -name %r' % (root, item)
            if type:
                command += ' -type '+type
            if not recurse:
                command += ' -maxdepth 1'
            elif recurse is not True:
                command += ' -maxdepth %d' % (int(recurse) + 1)
            if verbose: print(command)
            p = Popen(command, **popen4)
            p.stdin.close()
            pathstr = p.stdout.readlines()
            p.stdout.close()
            errind = ['find:','Usage:']
            if errind[1] in pathstr: #XXX: raise error?
                if verbose: print("Error: incorrect usage '%s'" % command)
                return
            for path in pathstr:
                if sys.version_info[0] > 2:
                    path = path.decode()
                if errind[0] not in path:
                    path = path.strip()
                    pathlist.append(os.path.abspath(path))
    except:
        folders = False;files = False;links = False
        if type in ['f']: files = True
        elif type in ['l']: links = True
        elif type in ['d']: folders = True
        else: folders = True;files = True;links = True
        pathlist = walk(root,patterns,recurse,folders,files,links)
    return pathlist

# TODO: enable recursion depth
def walk(root,patterns='*',recurse=True,folders=False,files=True,links=True):
    '''walk(root[,patterns,recurse,folders,files,links]); walk directory tree

    Walk the directory tree and return list matching the requested pattern

    root: path string of top-level directory to search
    patterns: name or partial name string of items to search for
    recurse: if True, recurse down from root directory
    folders: if True, include folders in results of the walk
    files: if True, include files in results of the walk
    links: if True, include links in results of the walk

    patterns can be specified with basic pattern matching. Additionally,
    multiple patterns can be specified by splitting patterns with a \';'\

    For example:
        >>> walk(\'..\', patterns=\'pox*\')
        [\'/Users/foo/pox/pox\', \'/Users/foo/pox/scripts/pox_launcher.py\']

        >>> walk(\'.\', patterns=\'*shutils*;*init*\')
        [\'/Users/foo/pox/pox/shutils.py\', \'/Users/foo/pox/pox/__init__.py\']
    '''
    import fnmatch
    #create a list by splitting patterns at ';'
    pattern_list = patterns.split(';')
    try:
        _walk = os.walk
    except AttributeError:
        _walk = None
   #print("walking... ")
    if _walk:
        results = []
        for dirname,dirs,items in os.walk(root): #followlinks=False
            if folders or links:
                for name in dirs:
                    fullname = os.path.normpath(os.path.join(dirname,name))
                    if(folders and os.path.isdir(fullname) and \
                               not os.path.islink(fullname)) or \
                      (links and os.path.islink(fullname)):
                        for pattern in pattern_list:
                            if fnmatch.fnmatch(name,pattern):
                                results.append(fullname)
                                break
            if files or links:
                for name in items:
                    fullname = os.path.normpath(os.path.join(dirname,name))
                    if(files and os.path.isfile(fullname) and \
                             not os.path.islink(fullname)) or \
                      (links and os.path.islink(fullname)):
                        for pattern in pattern_list:
                            if fnmatch.fnmatch(name,pattern):
                                results.append(fullname)
                                break
            #block recursion if disallowed
            if not recurse:
                dirs[:] = []
        return results
    #collect arguments into a bunch
    class Bunch:
        def __init__(self, **kwds):
            self.__dict__.update(kwds)
    arg = Bunch(recurse=recurse,pattern_list=pattern_list,
                folders=folders, files=files, links=links, results=[])
    def visit(arg,dirname,items):
        #append to arg.results all relevant items
        for name in items:
            fullname = os.path.normpath(os.path.join(dirname,name))
            if(arg.files and os.path.isfile(fullname) and \
                         not os.path.islink(fullname)) or \
              (arg.folders and os.path.isdir(fullname) and \
                           not os.path.islink(fullname)) or \
              (arg.links and os.path.islink(fullname)):
                for pattern in arg.pattern_list:
                    if fnmatch.fnmatch(name,pattern):
                        arg.results.append(fullname)
                        break
        #block recursion if disallowed
        if not arg.recurse:
            items[:] = []
    os.path.walk(root,visit,arg) # removed in python 3.x
    return arg.results

def where(name,path,pathsep=None):
    '''where(name,path[,pathsep]); Get the full path for the given name string
    on the given search path.

    name: string name of file, folder, etc to find
    path: path string (e.g. \'/Users/foo/bin:/bin:/sbin:/usr/bin\')
    pathsep: path separator (e.g. \':\'); if none provided, use OS default
    '''
    if not pathsep: pathsep = os.pathsep
    for _path in path.split(pathsep):
        candidate = os.path.join(_path,name)
        if os.path.exists(candidate):
            return os.path.abspath(candidate)
    return None

def mkdir(path,root=None,mode=None):
    '''mkdir(path[,root,mode]); make a new directory in the root directory

    path: string name of new directory
    root: path string of directory in which to build the new directory
    mode: octal representing read/write permissions [default is 0o775]

    mkdir will create any necessary parents (like unix \'mkdir -p\').  Default
    mode is read/write/execute for \'user\', \'group\'; read/execute otherwise)
    '''
    if mode is None: mode = MODE
    if not root: root = os.curdir
    newdir = os.path.join(root,path)
    absdir = os.path.abspath(newdir)
    import errno
    try:
        os.makedirs(absdir,mode)
        return absdir
    except OSError:
        err = sys.exc_info()[0]
        if (err.errno != errno.EEXIST) or (not os.path.isdir(absdir)):
            raise

def shellsub(command):
    '''shellsub(command); Parse command formatted for remote shell invocation

    Secure shell (ssh) can be used to send and execute commands to remote
    machines (using ssh <hostname> <command>).  Additional escape characters
    are needed to enable the command to be correctly formed and executed
    remotely.  shellsub attemps to parse the given command string correctly
    so that it can be executed remotely with ssh.'''
    import re
    command = re.compile('\'').sub('\\\'',command) 
    command = re.compile('\"').sub('\\\"',command)
    command = re.compile('\$').sub('\\\$',command)
    command = re.compile('\(').sub('\\\(',command)
    command = re.compile('\)').sub('\\\)',command)
    #command = re.compile('\{').sub('\\\{',command)
    #command = re.compile('\}').sub('\\\}',command)
    #command = re.compile('\[').sub('\\\[',command)
    #command = re.compile('\]').sub('\\\]',command)
    #command = re.compile('\~').sub('\\\~',command)
    #command = re.compile('\!').sub('\\\!',command)
    #command = re.compile('\&').sub('\\\&',command)
    #command = re.compile('\|').sub('\\\|',command)
    #command = re.compile('\*').sub('\\\*',command)
    #command = re.compile('\%').sub('\\\%',command)
    #command = re.compile('\#').sub('\\\#',command)
    #command = re.compile('\@').sub('\\\@',command)
    #command = re.compile('\:').sub('\\\:',command)
    #command = re.compile('\;').sub('\\\;',command)
    #command = re.compile('\,').sub('\\\,',command)
    #command = re.compile('\.').sub('\\\.',command)
    #command = re.compile('\?').sub('\\\?',command)
    #command = re.compile('\>').sub('\\\>',command)
    #command = re.compile('\<').sub('\\\<',command)
    #command = re.compile('\/').sub('\\\/',command)
    #command = re.compile('\\\\').sub('\\\\\\\\',command) 
    return command

# backward compatibility
getSHELL = shelltype
getHOME = homedir
getROOT = rootdir
getUSER = username
getSEP = sep
stripDups = minpath


if __name__=='__main__':
    pass


# End of file 
