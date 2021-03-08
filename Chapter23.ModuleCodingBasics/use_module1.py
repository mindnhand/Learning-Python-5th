#!/usr/bin/env python3
#encoding=utf-8


#---------------------------------------------------
# Usage: python3 use_module1.py
# Description: module basic
#---------------------------------------------------



# 1. import statement
import module1

module1.printer('Hello World!')


# 2. from ... import ...
from module1 import printer

printer('Hello World!')


# 3. from ... import *
from module1 import *

printer('Hello World!')
