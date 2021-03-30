# Using 3.X/2.6+ bytearray Objects
So far we've focused on str and bytes, because they subsume Python 2's unicode and str. Python 3.X grew a third string type, though -- bytearray, a mutable sequence of integers in the range 0 through 255, which is a mutable variant of bytes. As such, it supports the same string methods and sequence operations as bytes, as well as many of the mutable in-place-change operations supported by lists.

Bytearrays support in-place changes to both truly binary data as well as simple forms of text such as ASCII, which can be represented with 1 byte per character (richer Unicode text generally requires Unicode strings, which are still immutable). The bytear ray type is also available in Python 2.6 and 2.7 as a back-port from 3.X, but it does not enforce the strict text/binary distinction there that it does in 3.X.

## bytearrays in Action
Let's take a quick tour. We can create bytearray objects by calling the bytearray builtin. In Python 2.X, any string may be used to initialize:
> 
> > ```python
> > # Creation in 2.6/2.7: a mutable sequence of small (0..255) ints
> > >>> S = 'spam'
> > >>> C = bytearray(S) 				# A back-port from 3.X in 2.6+
> > >>> C 								# b'..' == '..' in 2.6+ (str)
> > bytearray(b'spam')
> > ```
> 
>  In Python 3.X, an encoding name or byte string is required, because text and binary strings do not mix (though byte strings may reflect encoded Unicode text):
> 
> > ```python
> > # Creation in 3.X: text/binary do not mix
> > >>> S = 'spam'
> > >>> C = bytearray(S)
> > TypeError: string argument without an encoding
> > >>> C = bytearray(S, 'latin1') 		# A content-specific type in 3.X
> > >>> C
> > bytearray(b'spam')
> > >>> B = b'spam' 					# b'..' != '..' in 3.X (bytes/str)
> > >>> C = bytearray(B)
> > >>> C
> > bytearray(b'spam')
> > ```
> 

Once created, bytearray objects are sequences of small integers like bytes and are mutable like lists, though they require an integer for index assignments, not a string (all of the following is a continuation of this session and is run under Python 3.X unless otherwise noted -- see comments for 2.X usage notes):
> ```python
> # Mutable, but must assign ints, not strings
> >>> C[0]
> 115
> >>> C[0] = 'x' 						# This and the next work in 2.6/2.7
> TypeError: an integer is required
> >>> C[0] = b'x'
> TypeError: an integer is required
> >>> C[0] = ord('x') 					# Use ord() to get a character's ordinal
> >>> C
> bytearray(b'xpam')
> >>> C[1] = b'Y'[0] 					# Or index a byte string
> >>> C
> bytearray(b'xYam')
> ```

Processing bytearray objects borrows from both strings and lists, since they are mutable byte strings. While the bytearray's methods overlap with both str and bytes, it also has many of the list's mutable methods. Besides named methods, the __iadd__ and __setitem__ methods in bytearray implement += in-place concatenation and index assignment, respectively:
> ```python
> # in bytes but not bytearray
> >>> set(dir(b'abc')) - set(dir(bytearray(b'abc')))
> {'__getnewargs__'}
> # in bytearray but not bytes
> >>> set(dir(bytearray(b'abc'))) - set(dir(b'abc'))
> {'__iadd__', 'reverse', '__setitem__', 'extend', 'copy', '__alloc__',
> '__delitem__', '__imul__', 'remove', 'clear', 'insert', 'append', 'pop'}
> ```

You can change a bytearray in place with both index assignment, as you've just seen, and list-like methods like those shown here (to change text in place prior to 2.6, you would need to convert to and then from a list, with list(str) and ''.join(list) -- see Chapter 4 and Chapter 6 for examples):
> ```python
> # Mutable method calls
> >>> C
> bytearray(b'xYam')
> >>> C.append(b'LMN') 						# 2.X requires string of size 1
> TypeError: an integer is required
> >>> C.append(ord('L'))
> >>> C
> bytearray(b'xYamL')
> >>> C.extend(b'MNO')
> >>> C
> bytearray(b'xYamLMNO')
> ```

All the usual sequence operations and string methods work on bytearrays, as you would expect (notice that like bytes objects, their expressions and methods expect bytes arguments, not str arguments):
> ```python
> # Sequence operations and string methods
> >>> C
> bytearray(b'xYamLMNO')
> >>> C + b'!#'
> bytearray(b'xYamLMNO!#')
> >>> C[0]
> 120
> >>> C[1:]
> bytearray(b'YamLMNO')
> >>> len(C)
> 8
> >>> C.replace('xY', 'sp') 					# This works in 2.X
> TypeError: Type str doesn't support the buffer API
> >>> C.replace(b'xY', b'sp')
> bytearray(b'spamLMNO')
> >>> C
> bytearray(b'xYamLMNO')
> >>> C * 4
> bytearray(b'xYamLMNOxYamLMNOxYamLMNOxYamLMNO')
> ```

## Python 3.X String Types Summary
Finally, by way of summary, the following examples demonstrate how bytes and byte array objects are sequences of ints, and str objects are sequences of characters:
> ```python
> # Binary versus text
> >>> B 						# B is same as S in 2.6/2.7
> b'spam'
> >>> list(B)
> [115, 112, 97, 109]
> >>> C
> bytearray(b'xYamLMNO')
> >>> list(C)
> [120, 89, 97, 109, 76, 77, 78, 79]
> >>> S
> 'spam'
> >>> list(S)
> ['s', 'p', 'a', 'm']
> ```

Although all three Python 3.X string types can contain character values and support many of the same operations, again, you should always:
- Use str for textual data.
- Use bytes for binary data.
- Use bytearray for binary data you wish to change in place.
Related tools such as files, the next section's topic, often make the choice for you.


