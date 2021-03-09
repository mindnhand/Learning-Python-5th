#!/usr/bin/env python3
#encoding=utf-8


#-----------------------------------------------------------
# Usage: python3 reloadall.py
# Description: reloadall2.py: transitively reload nested modules (alternative coding)
#              Call reload_all with one or more imported module module objects.
#-----------------------------------------------------------


'''
The module reloadall2.py listed next defines a reload_all function that automatically
reloads a module, every module that the module imports, and so on, all the way to the
bottom of each import chain. It uses a dictionary to keep track of already reloaded
modules, recursion to walk the import chains, and the standard library's types module,
which simply predefines type results for built-in types. The visited dictionary technique
works to avoid cycles here when imports are recursive or redundant, because module
objects are immutable and so can be dictionary keys; as we learned in Chapter 5
and Chapter 8, a set would offer similar functionality if we use visited.add(module) to
insert:
'''


import types
from importlib import reload
from reloadall import status, tryreload, tester




def transitive_reload(module, visited):
    for obj in module:
        if type(obj) == types.ModuleType and obj not in visited:
            status(obj)
            tryreload(obj)                                          # Reload this, recur to attrs
            visited.add(obj)
            transitive_reload(obj.__dict__.values(), visited)

def reload_all(*args):
    transitive_reload(args, set())




if __name__ == '__main__':
    tester(reload_all, 'reloadall2')                 # Test: reload myself
