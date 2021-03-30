# Coding Unicode Strings
Encoding and decoding become more meaningful when you start dealing with non-ASCII Unicode text. To code arbitrary Unicode characters in your strings, some of which you might not even be able to type on your keyboard, Python string literals support both "\xNN" hex byte value escapes and "\uNNNN" and "\UNNNNNNNN" Unicode escapes in string literals. In Unicode escapes, the first form gives four hex digits to encode a 2-byte (16-bit) character code point, and the second gives eight hex digits for a 4-byte (32-bit) code point. Byte strings support only hex escapes for encoded text and other forms of byte-based data.

## Coding ASCII Text
Let's step through some examples that demonstrate text coding basics. As we've seen, ASCII text is a simple type of Unicode, stored as a sequence of byte values that represent characters:
> ```powershell
> C:\code> C:\python33\python
> >>> ord('X') 							# 'X' is binary code point value 88 in the default encoding
> 88
> >>> chr(88) 							# 88 stands for character 'X'
> 'X'
> >>> S = 'XYZ' 						# A Unicode string of ASCII text
> >>> S
> 'XYZ'
> >>> len(S) 							# Three characters long
> 3
> >>> [ord(c) for c in S] 				# Three characters with integer ordinal values
> [88, 89, 90]
> ```

Normal 7-bit ASCII text like this is represented with one character per byte under each of the Unicode encoding schemes described earlier in this chapter:
> ```python
> >>> S.encode('ascii') 				# Values 0..127 in 1 byte (7 bits) each
> b'XYZ'
> >>> S.encode('latin-1') 				# Values 0..255 in 1 byte (8 bits) each
> b'XYZ'
> >>> S.encode('utf-8') 				# Values 0..127 in 1 byte, 128..2047 in 2, others 3 or 4
> b'XYZ'
> ```

In fact, the bytes objects returned by encoding ASCII text this way are really a sequence of short integers, which just happen to print as ASCII characters when possible:
> ```python
> >>> S.encode('latin-1')
> b'XYZ'
> >>> S.encode('latin-1')[0]
> 88
> >>> list(S.encode('latin-1'))
> [88, 89, 90]
> ```

## Coding Non-ASCII Text
Formally, to code non-ASCII characters, we can use:
- Hex or Unicode escapes to embed Unicode code point ordinal values in text strings -- normal string literals in 3.X, and Unicode string literals in 2.X (and in 3.3 for compatibility).
- Hex escapes to embed the encoded representation of characters in byte strings -- normal string literals in 2.X, and bytes string literals in 3.X (and in 2.X for compatibility).

Note that text strings embed actual code point values, while byte strings embed their encoded form. The value of a character's encoded representation in a byte string is the same as its decoded Unicode code point value in a text string for only certain characters and encodings. In any event, hex escapes are limited to coding a single byte's value, but Unicode escapes can name characters with values 2 and 4 bytes wide. The chr function can also be used to create a single non-ASCII character from its code point value, and as we'll see later, source code declarations apply to such characters embedded in your script.

For instance, the hex values 0xCD and 0xE8 are codes for two special accented characters outside the 7-bit range of ASCII, but we can embed them in 3.X str objects because str supports Unicode:
> ```python
> >>> chr(0xc4) 				# 0xC4, 0xE8: characters outside ASCII's range
> 'Ä'
> >>> chr(0xe8)
> 'è'
> >>> S = '\xc4\xe8' 			# Single 8-bit value hex escapes: two digits
> >>> S
> 'Äè'
> >>> S = '\u00c4\u00e8' 		# 16-bit Unicode escapes: four digits each
> >>> S
> 'Äè'
> >>> len(S) 					# Two characters long (not number of bytes!)
> 2
> ```

Note that in Unicode text string literals like these, hex and Unicode escapes denote a Unicode code point value, not byte values. The x hex escapes require exactly two digits (for 8-bit code point values), and u and U Unicode escapes require exactly four and eight hexadecimal digits, respectively, for denoting code point values that can be as big as 16 and 32 bits will allow:
> ```python
> >>> S = '\U000000c4\U000000e8' 				# 32-bit Unicode escapes: eight digits each
> >>> S
> 'Äè'
> ```

As shown later, Python 2.X works similarly in this regard, but Unicode escapes are allowed only in its Unicode literal form. They work in normal string literals in 3.X here simply because its normal strings are always Unicode.

## Encoding and Decoding Non-ASCII text
Now, if we try to encode the prior section's non-ASCII text string into raw bytes using as ASCII, we'll get an error, because its characters are outside ASCII's 7-bit code point value range:
> ```python
> >>> S = '\u00c4\u00e8' 				# Non-ASCII text string, two characters long
> >>> S
> 'Äè'
> >>> len(S)
> 2
> >>> S.encode('ascii')
> UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-1:
> ordinal not in range(128)
> ```

Encoding this as Latin-1 works, though, because each character falls into that encoding's 8-bit range, and we get 1 byte per character allocated in the encoded byte string.

Encoding as UTF-8 also works: this encoding supports a wide range of Unicode code points, but allocates 2 bytes per non-ASCII character instead. If these encoded strings are written to a file, the raw bytes shown here for encoding results are what is actually stored on the file for the encoding types given:
> ```python
> >>> S.encode('latin-1') 				# 1 byte per character when encoded
> b'\xc4\xe8'
> >>> S.encode('utf-8') 				# 2 bytes per character when encoded
> b'\xc3\x84\xc3\xa8'
> >>> len(S.encode('latin-1')) 			# 2 bytes in latin-1, 4 in utf-8
> 2
> >>> len(S.encode('utf-8'))
> 4
> ```

Note that you can also go the other way, reading raw bytes from a file and decodin them back to a Unicode string. However, as we'll see later, the encoding mode you give to the open call causes this decoding to be done for you automatically on input (and avoids issues that may arise from reading partial character sequences when reading by blocks of bytes):
> ```python
> >>> B = b'\xc4\xe8' 					# Text encoded per Latin-1
> >>> B
> b'\xc4\xe8'
> >>> len(B) 							# 2 raw bytes, two encoded characters
> 2
> >>> B.decode('latin-1') 				# Decode to text per Latin-1
> 'Äè'
> >>> B = b'\xc3\x84\xc3\xa8' 			# Text encoded per UTF-8
> >>> len(B) 							# 4 raw bytes, two encoded characters
> 4
> >>> B.decode('utf-8') 				# Decode to text per UTF-8
> 'Äè'
> >>> len(B.decode('utf-8')) 			# Two Unicode characters in memory
> 2
> ```

## Other Encoding Schemes
Some encodings use even larger byte sequences to represent characters. When needed, you can specify both 16- and 32-bit Unicode code point values for characters in your strings -- as shown earlier, we can use "\u..." with four hex digits for the former, and "\U..." with eight hex digits for the latter, and can mix these in literals with simpler ASCII characters freely:
> ```python
> >>> S = 'A\u00c4B\U000000e8C'
> >>> S 								# A, B, C, and 2 non-ASCII characters
> 'AÄBèC'
> >>> len(S) 							# Five characters long
> 5
> >>> S.encode('latin-1')
> b'A\xc4B\xe8C'
> >>> len(S.encode('latin-1')) 			# 5 bytes when encoded per latin-1
> 5
> >>> S.encode('utf-8')
> b'A\xc3\x84B\xc3\xa8C'
> >>> len(S.encode('utf-8')) 			# 7 bytes when encoded per utf-8
> 7
> ```

Technically speaking, you can also build Unicode strings piecemeal using chr instead of Unicode or hex escapes, but this might become tedious for large strings:
> ```python
> >>> S = 'A' + chr(0xC4) + 'B' + chr(0xE8) + 'C'
> >>> S
> 'AÄBèC'
> ```

Some other encodings may use very different byte formats, though. The cp500 EBCDIC encoding, for example, doesn't even encode ASCII the same way as the encodings we've been using so far; since Python encodes and decodes for us, we only generally need to care about this when providing encoding names for data sources:
> ```python
> >>> S
> 'AÄBèC'
> >>> S.encode('cp500') 				# Two other Western European encodings
> b'\xc1c\xc2T\xc3'
> >>> S.encode('cp850') 				# 5 bytes each, different encoded values
> b'A\x8eB\x8aC'
> >>> S = 'spam' 						# ASCII text is the same in most
> >>> S.encode('latin-1')
> b'spam'
> >>> S.encode('utf-8')
> b'spam'
> >>> S.encode('cp500') 				# But not in cp500: IBM EBCDIC!
> b'\xa2\x97\x81\x94'
> >>> S.encode('cp850')
> b'spam'
> ```

The same holds true for the UTF-16 and UTF-32 encodings, which use fixed 2- and 4-byte-per-character schemes with same-sized headers -- non-ASCII encodes differently, and ASCII is not 1 byte per character:
> ```python
> >>> S = 'A\u00c4B\U000000e8C'
> >>> S.encode('utf-16')
> b'\xff\xfeA\x00\xc4\x00B\x00\xe8\x00C\x00'
> >>> S = 'spam'
> >>> S.encode('utf-16')
> b'\xff\xfes\x00p\x00a\x00m\x00'
> >>> S.encode('utf-32')
> b'\xff\xfe\x00\x00s\x00\x00\x00p\x00\x00\x00a\x00\x00\x00m\x00\x00\x00'
> ```

## Byte String Literals: Encoded Text
Two cautions here too. First, Python 3.X allows special characters to be coded with both hex and Unicode escapes in str strings, but only with hex escapes in bytes strings -- Unicode escape sequences are silently taken verbatim in bytes literals, not as escapes.

In fact, bytes must be decoded to str strings to print their non-ASCII characters properly:
> ```python
> >>> S = 'A\xC4B\xE8C' 				# 3.X: str recognizes hex and Unicode escapes
> >>> S
> 'AÄBèC'
> >>> S = 'A\u00C4B\U000000E8C'
> >>> S
> 'AÄBèC'
> >>> B = b'A\xC4B\xE8C' 				# bytes recognizes hex but not Unicode
> >>> B
> b'A\xc4B\xe8C'
> >>> B = b'A\u00C4B\U000000E8C' 		# Escape sequences taken literally!
> >>> B
> b'A\\u00C4B\\U000000E8C'
> >>> B = b'A\xC4B\xE8C' 				# Use hex escapes for bytes
> >>> B 								# Prints non-ASCII as hex
> b'A\xc4B\xe8C'
> >>> print(B)
> b'A\xc4B\xe8C'
> >>> B.decode('latin-1') 				# Decode as latin-1 to interpret as text
> 'AÄBèC'
> ```

Second, bytes literals require characters either to be ASCII characters or, if their values are greater than 127, to be escaped; str stings, on the other hand, allow literals containing any character in the source character set -- which, as discussed later, defaults to UTF-8 unless an encoding declaration is given in the source file:
> ```python
> >>> S = 'AÄBèC' 				# Chars from UTF-8 if no encoding declaration
> >>> S
> 'AÄBèC'
> >>> B = b'AÄBèC'
> SyntaxError: bytes can only contain ASCII literal characters.
> >>> B = b'A\xC4B\xE8C' 		# Chars must be ASCII, or escapes
> >>> B
> b'A\xc4B\xe8C'
> >>> B.decode('latin-1')
> 'AÄBèC'
> >>> S.encode() 				# Source code encoded per UTF-8 by default
> b'A\xc3\x84B\xc3\xa8C' 		# Uses system default to encode, unless passed
> >>> S.encode('utf-8')
> b'A\xc3\x84B\xc3\xa8C'
> >>> B.decode() 				# Raw bytes do not correspond to utf-8
> UnicodeDecodeError: 'utf8' codec can't decode bytes in position 1-2: ...
> ```

Both these constraints make sense if you remember that byte strings hold bytes-based data, not decoded Unicode code point ordinals; while they may contain the encoded form of text, decoded code point values don't quite apply to byte strings unless the characters are first encoded.

## Converting Encodings
So far, we've been encoding and decoding strings to inspect their structure. It's also possible to convert a string to a different encoding than its original, but we must provide an explicit encoding name to encode to and decode from. This is true whether the original text string originated in a file or a literal.

The term conversion may be a misnomer here -- it really just means encoding a text string to raw bytes per a different encoding scheme than the one it was decoded from. As stressed earlier, decoded text in memory has no encoding type, and is simply a string of Unicode code points (a.k.a. characters); there is no concept of changing its encoding in this form. Still, this scheme allows scripts to read data in one encoding and store it in another, to support multiple clients of the same data:
> ```python
> >>> B = b'A\xc3\x84B\xc3\xa8C' 				# Text encoded in UTF-8 format originally
> >>> S = B.decode('utf-8') 					# Decode to Unicode text per UTF-8
> >>> S
> 'AÄBèC'
> >>> T = S.encode('cp500') 					# Convert to encoded bytes per EBCDIC
> >>> T
> b'\xc1c\xc2T\xc3'
> >>> U = T.decode('cp500') 					# Convert back to Unicode per EBCDIC
> >>> U
> 'AÄBèC'
> >>> U.encode() 								# Per default utf-8 encoding again
> b'A\xc3\x84B\xc3\xa8C'
> ```

Keep in mind that the special Unicode and hex character escapes are only necessary when you code non-ASCII Unicode strings manually. In practice, you'll often load such text from files instead. As we'll see later in this chapter, 3.X's file object (created with the open built-in function) automatically decodes text strings as they are read and encodes them when they are written; because of this, your script can often deal with strings generically, without having to code special characters directly.

Later in this chapter we'll also see that it's possible to convert between encodings when transferring strings to and from files, using a technique very similar to that in the last example; although you'll still need to provide explicit encoding names when opening a file, the file interface does most of the conversion work for you automatically.

## Source File Character Set Encoding Declarations
Finally, Unicode escape codes are fine for the occasional Unicode character in string literals, but they can become tedious if you need to embed non-ASCII text in your strings frequently. To interpret the content of strings you code and hence embed within the text of your script files, Python uses the UTF-8 encoding by default, but it allows you to change this to support arbitrary character sets by including a comment that names your desired encoding. The comment must be of this form and must appear as either the first or second line in your script in either Python 2.X or 3.X:
`# -*- coding: latin-1 -*-`

When a comment of this form is present, Python will recognize strings represented natively in the given encoding. This means you can edit your script file in a text editor that accepts and displays accented and other non-ASCII characters correctly, and Python will decode them correctly in your string literals. For example, notice how the comment at the top of the following file, text.py, allows Latin-1 characters to be embedded in strings, which are themselves embedded in the script file's text:
> ```python
> # -*- coding: latin-1 -*-
> # Any of the following string literal forms work in latin-1.
> # Changing the encoding above to either ascii or utf-8 fails,
> # because the 0xc4 and 0xe8 in myStr1 are not valid in either.
> myStr1 = 'aÄBèC'
> myStr2 = 'A\u00c4B\U000000e8C'
> myStr3 = 'A' + chr(0xC4) + 'B' + chr(0xE8) + 'C'
> import sys
> print('Default encoding:', sys.getdefaultencoding())
> for aStr in myStr1, myStr2, myStr3:
>     print('{0}, strlen={1}, '.format(aStr, len(aStr)), end='')
>     bytes1 = aStr.encode() 					# Per default utf-8: 2 bytes for non-ASCII
>     bytes2 = aStr.encode('latin-1') 			# One byte per char
>     #bytes3 = aStr.encode('ascii') 			# ASCII fails: outside 0..127 range
>     print('byteslen1={0}, byteslen2={1}'.format(len(bytes1), len(bytes2)))
> ```

When run, this script produces the following output, giving, for each of three coding techniques, the string, its length, and the lengths of its UTF-8 and Latin-1 encoded byte string forms.
> ```powershell
> C:\code> C:\python33\python text.py
> Default encoding: utf-8
> aÄBèC, strlen=5, byteslen1=7, byteslen2=5
> AÄBèC, strlen=5, byteslen1=7, byteslen2=5
> AÄBèC, strlen=5, byteslen1=7, byteslen2=5
> ```

Since many programmers are likely to fall back on the standard UTF-8 encoding, I'll defer to Python's standard manual set for more details on this option and other advanced Unicode support topics, such as properties and character name escapes in strings I'm omitting here. For this chapter, let's take a quick look at the new byte string object types in Python 3.X, before moving on to its file and tool changes.

