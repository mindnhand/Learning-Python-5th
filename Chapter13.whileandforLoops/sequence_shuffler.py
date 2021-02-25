#!/usr/bin/env python3
#encoding=utf-8


#---------------------------------
# Usage:
# Description:
#---------------------------------


S = 'spam'
print('<-change S, and output S->', end=': ')
for i in range(len(S)):
    # change S, and output S
    S = S[1:] + S[:1]
    print(S, end=' ')
else:
    print()


S = 'spam'
print('<-keep S, change X, and output X->', end=': ')
for i in range(len(S)):
    # keep S, change X, and output X
    X = S[i:] + S[:i]
    print(X, end=' ')
else:
    print()
