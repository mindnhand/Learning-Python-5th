#!/usr/bin/env python3
#encoding=utf-8


#-------------------------------------------------
# Usage: python3 lister.py
# Description: mix-in class
#              File lister.py
#              Collect all three listers in one module for convenience
#-------------------------------------------------

from listinstance import ListInstance
from listinherited import ListInherited
from listtree import ListTree
Lister = ListTree                   # Choose a default lister
