# Using 3.X bytes Objects
We studied a wide variety of operations available for Python 3.X's general str string type in Chapter 7; the basic string type works identically in 2.X and 3.X, so we won't rehash this topic. Instead, let's dig a bit deeper into the operation sets provided by the new bytes type in 3.X.

As mentioned previously, the 3.X bytes object is a sequence of small integers, each of which is in the range 0 through 255, that happens to print as ASCII characters when displayed. It supports sequence operations and most of the same methods available on str objects (and present in 2.X's str type). However, bytes does not support the format method or the % formatting expression, and you cannot mix and match bytes and str type objects without explicit conversions -- you generally will use all str type objects and text files for text data, and all bytes type objects and binary files for binary data.

## Method Calls
If you really want to see what attributes str has that bytes doesn't, you can always check their dir built-in function results. The output can also tell you something about the expression operators they support (e.g., \_\_mod\_\_ and \_\_rmod\_\_ implement the % operator):
> ```powershell
> C:\code> C:\python33\python
> # Attributes in str but not bytes
> >>> set(dir('abc')) - set(dir(b'abc'))
> {'isdecimal', '__mod__', '__rmod__', 'format_map', 'isprintable',
> 'casefold', 'format', 'isnumeric', 'isidentifier', 'encode'}
> # Attributes in bytes but not str
> >>> set(dir(b'abc')) - set(dir('abc'))
> {'decode', 'fromhex'}
> ```

As you can see, str and bytes have almost identical functionality. Their unique attributes are generally methods that don't apply to the other; for instance, decode translates a raw bytes into its str representation, and encode translates a string into its raw bytes representation. Most of the methods are the same, though bytes methods require bytes arguments (again, 3.X string types don't mix). Also recall that bytes objects are immutable, just like str objects in both 2.X and 3.X (error messages here have been shortened for brevity):
> ```python
> >>> B = b'spam' 						# b'...' bytes literal
> >>> B.find(b'pa')
> 1
> >>> B.replace(b'pa', b'XY') 			# bytes methods expect bytes arguments
> b'sXYm'
> >>> B.split(b'pa') 					# bytes methods return bytes results
> [b's', b'm']
> >>> B
> b'spam'
> >>> B[0] = 'x'
> TypeError: 'bytes' object does not support item assignment
> ```

One notable difference is that string formatting works only on str objects in 3.X, not on bytes objects (see Chapter 7 for more on string formatting expressions and methods):
> ```python
> >>> '%s' % 99
> '99'
> >>> b'%s' % 99
> TypeError: unsupported operand type(s) for %: 'bytes' and 'int'
> >>> '{0}'.format(99)
> '99'
> >>> b'{0}'.format(99)
> AttributeError: 'bytes' object has no attribute 'format'
> ```

## Sequence Operations
Besides method calls, all the usual generic sequence operations you know (and possibly love) from Python 2.X strings and lists work as expected on both str and bytes in 3.X; this includes indexing, slicing, concatenation, and so on. Notice in the following that indexing a bytes object returns an integer giving the byte's binary value; bytes really is a sequence of 8-bit integers, but for convenience prints as a string of ASCII-coded characters where possible when displayed as a whole. To check a given byte's value, use the chr built-in to convert it back to its character, as in the following:
> ```python
> >>> B = b'spam' 					# A sequence of small ints
> >>> B 							# Prints as ASCII characters (and/or hex escapes)
> b'spam'
> >>> B[0] 							# Indexing yields an int
> 115
> >>> B[-1]
> 109
> >>> chr(B[0]) 					# Show character for int
> 's'
> >>> list(B) 						# Show all the byte's int values
> [115, 112, 97, 109]
> >>> B[1:], B[:-1]
> (b'pam', b'spa')
> >>> len(B)
> 4
> >>> B + b'lmn'
> b'spamlmn'
> >>> B * 4
> b'spamspamspamspam'

## Other Ways to Make bytes Objects
So far, we've been mostly making bytes objects with the b'...' literal syntax. We can also create them by calling the bytes constructor with a str and an encoding name, calling the bytes constructor with an iterable of integers representing byte values, or encoding a str object per the default (or passed-in) encoding. As we've seen, encoding takes a text str and returns the raw encoded byte values of the string per the encoding specified; conversely, decoding takes a raw bytes sequence and translates it to its str text string representation -- a series of Unicode characters. Both operations create new string objects:
> ```python
> >>> B = b'abc' 						# Literal
> >>> B
> b'abc'
> >>> B = bytes('abc', 'ascii') 		# Constructor with encoding name
> >>> B
> b'abc'
> >>> ord('a')
> 97
> >>> B = bytes([97, 98, 99]) 			# Integer iterable
> >>> B
> b'abc'
> >>> B = 'spam'.encode() 				# str.encode() (or bytes())
> >>> B
> b'spam'
> >>>
> >>> S = B.decode() 					# bytes.decode() (or str())
> >>> S
> 'spam'
> ```

From a functional perspective, the last two of these operations are really tools for converting between str and bytes, a topic introduced earlier and expanded upon in the next section.

## Mixing String Types
In the replace call of the section "Method Calls" on page 1189, we had to pass in two bytes objects -- str types won't work there. Although Python 2.X automatically converts str to and from unicode when possible (i.e., when the str is 7-bit ASCII text), Python 3.X requires specific string types in some contexts and expects manual conversions if needed:
> ```python
> # Must pass expected types to function and method calls
> >>> B = b'spam'
> >>> B.replace('pa', 'XY')
> TypeError: expected an object with the buffer interface
> >>> B.replace(b'pa', b'XY')
> b'sXYm'
> >>> B = B'spam'
> >>> B.replace(bytes('pa'), bytes('xy'))
> TypeError: string argument without an encoding
> >>> B.replace(bytes('pa', 'ascii'), bytes('xy', 'utf-8'))
> b'sxym'
> # Must convert manually in 3.X mixed-type expressions
> >>> b'ab' + 'cd'
> TypeError: can't concat bytes to str
> >>> b'ab'.decode() + 'cd' 				# bytes to str
> 'abcd'
> >>> b'ab' + 'cd'.encode() 				# str to bytes
> b'abcd'
> >>> b'ab' + bytes('cd', 'ascii') 			# str to bytes
> b'abcd'
> ```

Although you can create bytes objects yourself to represent packed binary data, they can also be made automatically by reading files opened in binary mode, as we'll see in more detail later in this chapter. First, though, let's introduce bytes's very close, and mutable, cousin.
