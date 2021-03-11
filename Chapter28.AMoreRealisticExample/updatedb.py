#!/usr/bin/env python3
#encoding=utf-8


#-----------------------------------------
# Usage: python3 updatedb.py
# Description: example for shelve
#-----------------------------------------



import shelve

# Read shelve
db = shelve.open('persondb')                    # Reopen shelve with same filename

for key in sorted(db):                          # Iterate to display database objects
    print(key, '\t=>', db[key])                 # Prints with custom format



# Update shelve
sue = db['Sue Jones']                           # Index by key to fetch
sue.giveRaise(.10)                              # Update in memory using class's method

db['Sue Jones'] = sue                           # Assign to key to update in shelve
db.close()                                      # Close after making changes


