#!/usr/bin/env python3
#encoding=utf-8


#--------------------------------------------------
# Usage: python3 makedb.py
# Description: example for shelve
#--------------------------------------------------



# make instances
from person import Person, Manager                      # Load our classes


bob = Person('Bob Smith')                               # Re-create objects to be stored
sue = Person('Sue Jones', job='dev', pay=100000)
tom = Manager('Tom Jones', 50000)


# store instances in shelve
import shelve

db = shelve.open('persondb')                            # Filename where objects are stored

for obj in (bob, sue, tom):                             # Use object's name attr as key
    db[obj.name] = obj                                  # Store object on shelve by key

db.close()                                              # Close after making changes


# read instances from shelve
db_r = shelve.open('persondb')                          # Reopen the shelve
print('the length of db_r is %s' % len(db_r))

print('keys in db_r is %s' % list(db_r.keys()))

bob_r = db_r['Bob Smith']
print(bob_r)
print(bob_r.lastName())

print('Iterate db_r')
for key in db_r:
    print(key, '=>', db_r[key])

print('Iterate db_r with sorted')
for key in (db_r):
    print(key, '=>', db_r[key])
