# Coding Basic Strings
Let's step through a few examples that demonstrate how the 3.X string types are used. One note up front: the code in this section was run with and applies to 3.X only. Still, basic string operations are generally portable across Python versions. Simple ASCII strings represented with the str type work the same in 2.X and 3.X (and exactly as we saw in Chapter 7 of this book).

Moreover, although there is no bytes type in Python 2.X (it has just the general str), it can usually run code that thinks there is -- in 2.6 and 2.7, the call bytes(X) is present as a synonym for str(X), and the new literal form b'...' is taken to be the same as the normal string literal '...'. You may still run into version skew in some isolated cases, though; the 2.6/2.7 bytes call, for instance, does not require or allow the second argument (encoding name) that is required by 3.X's bytes.

## Python 3.X String Literals
Python 3.X string objects originate when you call a built-in function such as str or bytes, read a file created by calling open (described in the next section), or code literal syntax in your script. For the latter, a new literal form, b'xxx' (and equivalently, B'xxx') is used to create bytes objects in 3.X, and you may create bytearray objects by calling the bytearray function, with a variety of possible arguments.

More formally, in 3.X all the current string literal forms -- 'xxx', "xxx", and triplequoted blocks -- generate a str; adding a b or B just before any of them creates a bytes instead. This new b'...' bytes literal is similar in form to the r'...' raw string used to suppress backslash escapes. Consider the following, run in 3.X:
> ```powershell
> C:\code> C:\python33\python
> >>> B = b'spam' 				# 3.X bytes literal make a bytes object (8-bit bytes)
> >>> S = 'eggs' 				# 3.X str literal makes a Unicode text string
> >>> type(B), type(S)
> (<class 'bytes'>, <class 'str'>)
> >>> B 						# bytes: sequence of int, prints as character string
> b'spam'
> >>> S
> 'eggs'
> ```

The 3.X bytes object is actually a sequence of short integers, though it prints its content as characters whenever possible:
> ```python
> >>> B[0], S[0] 				# Indexing returns an int for bytes, str for str
> (115, 'e')
> >>> B[1:], S[1:] 				# Slicing makes another bytes or str object
> (b'pam', 'ggs')
> >>> list(B), list(S)
> ([115, 112, 97, 109], ['e', 'g', 'g', 's']) 			# bytes is really 8-bit small ints
> ```

The bytes object is also immutable, just like str (though bytearray, described later, is not); you cannot assign a str, bytes, or integer to an offset of a bytes object.
> ```python
> >>> B[0] = 'x' # Both are immutable
> TypeError: 'bytes' object does not support item assignment
> >>> S[0] = 'x'
> TypeError: 'str' object does not support item assignment
> ```

Finally, note that the bytes literal's b or B prefix also works for any string literal form, including triple-quoted blocks, though you get back a string of raw bytes that may or may not map to characters:
> ```python
> >>> # bytes prefix works on single, double, triple quotes, raw
> >>> B = B"""
> ... xxxx
> ... yyyy
> ... """
> >>> B
> b'\nxxxx\nyyyy\n'
> ```

### Python 2.X Unicode literals in Python 3.3
Python 2.X's u'xxx' and U'xxx' Unicode string literal forms were removed in Python 3.0 because they were deemed redundant -- normal strings are Unicode in 3.X. To aid both forward and backward compatibility, though, they are available again as of 3.3, where they are treated as normal str strings:
> ```powershell
> C:\code> C:\python33\python
> >>> U = u'spam' 				# 2.X Unicode literal accepted in 3.3+
> >>> type(U) 					# It is just str, but is backward compatible
> <class 'str'>
> >>> U
> 'spam'
> >>> U[0]
> 's'
> >>> list(U)
> ['s', 'p', 'a', 'm']
> ```

These literals are gone in 3.0 through 3.2, where you must use 'xxx' instead. You should generally use 3.X 'xxx' text literals in new 3.X-only code, because the 2.X form is superfluous. However, in 3.3 and later, using the 2.X literal form can ease the task of porting 2.X code, and boost 2.X code compatibility (for a case in point, see Chapter 25's currency example, described in an upcoming note). Regardless of how text strings are coded in 3.X, though, they are all Unicode, even if they contain only ASCII characters (more on writing non-ASCII Unicode text in the section "Coding Non-ASCII Text" on page 1179).

## Python 2.X String Literals
All three of the 3.X string forms of the prior section can be coded in 2.X, but their meaning differs. As mentioned earlier, in Python 2.6 and 2.7 the b'xxx' bytes literal is present for forward compatibility with 3.X, but is the same as 'xxx' and makes a str (the b is ignored), and bytes is just a synonym for str; as you've seen, in 3.X both of these address the distinct bytes type:
> ```powershell
> C:\code> C:\python27\python
> >>> B = b'spam' # 3.X bytes literal is just str in 2.6/2.7
> >>> S = 'eggs' # str is a bytes/character sequence
> >>> type(B), type(S)
> (<type 'str'>, <type 'str'>)
> >>> B, S
> ('spam', 'eggs')
> >>> B[0], S[0]
> ('s', 'e')
> >>> list(B), list(S)
> (['s', 'p', 'a', 'm'], ['e', 'g', 'g', 's'])
> In 2.X the special Unicode literal and type accommodates richer forms of text:
> >>> U = u'spam' # 2.X Unicode literal makes a distinct type
> >>> type(U) # Works in 3.3 too, but is just a str there
> <type 'unicode'>
> >>> U
> u'spam'
> >>> U[0]
> u's'
> >>> list(U)
> [u's', u'p', u'a', u'm']
> ```

As we saw, for compatibility this form works in 3.3 and later too, but it simply makes a normal str there (the u is ignored).

## String Type Conversions
Although Python 2.X allowed str and unicode type objects to be mixed in expressions (when the str contained only 7-bit ASCII text), 3.X draws a much sharper distinction -- str and bytes type objects never mix automatically in expressions and never are converted to one another automatically when passed to functions. A function that expects an argument to be a str object won't generally accept a bytes, and vice versa.

Because of this, Python 3.X basically requires that you commit to one type or the other, or perform manual, explicit conversions when needed:
- `str.encode()` and `bytes(S, encoding)` translate a string to its raw bytes form and create an encoded bytes from a decoded str in the process.
- `bytes.decode()` and `str(B, encoding)` translate raw bytes into its string form and create a decoded str from an encoded bytes in the process.

These encode and decode methods (as well as file objects, described in the next section) use either a default encoding for your platform or an explicitly passed-in encoding name. For example, in Python 3.X:
> ```python
> >>> S = 'eggs'
> >>> S.encode() 						# str->bytes: encode text into raw bytes
> b'eggs'
> >>> bytes(S, encoding='ascii') 		# str->bytes, alternative
> b'eggs'
> >>> B = b'spam'
> >>> B.decode() 						# bytes->str: decode raw bytes into text
> 'spam'
> >>> str(B, encoding='ascii') 			# bytes->str, alternative
> 'spam'
> ```

Two cautions here. First of all, your platform's default encoding is available in the sys module, but the encoding argument to bytes is not optional, even though it is in str.encode (and bytes.decode).

Second, although calls to str do not require the encoding argument like bytes does, leaving it off in str calls does not mean that it defaults -- instead, a str call without an encoding returns the bytes object's print string, not its str converted form (this is usually not what you'll want!). Assuming B and S are still as in the prior listing:
> ```python
> >>> import sys
> >>> sys.platform 					# Underlying platform
> 'win32'
> >>> sys.getdefaultencoding() 		# Default encoding for str here
> 'utf-8'
> >>> bytes(S)
> TypeError: string argument without an encoding
> >>> str(B) 						# str without encoding
> "b'spam'" 						# A print string, not conversion!
> >>> len(str(B))
> 7
> >>> len(str(B, encoding='ascii')) # Use encoding to convert to str
> 4
> ```

When in doubt, pass in an encoding name argument in 3.X, even if it may have a default. Conversions are similar in Python 2.X, though 2.X's support for mixing string types in expressions makes conversions optional for ASCII text, and the tool names differ for the different string type model -- conversions in 2.X occur between encoded str and decoded unicode, rather than 3.X’s encoded bytes and decoded str:
> ```python
> >>> S = 'spam' 					# 2.X type string conversion tools
> >>> U = u'eggs'
> >>> S, U
> ('spam', u'eggs')
> >>> unicode(S), str(U) 			# 2.X converts str->uni, uni->str
> (u'spam', 'eggs')
> >>> S.decode(), U.encode() 		# versus 3.X byte->str, str->bytes
> (u'spam', 'eggs')
> ```
