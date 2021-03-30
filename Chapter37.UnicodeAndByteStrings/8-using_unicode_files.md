# Using Unicode Files
So far, we've been reading and writing basic text and binary files. It turns out to be easy to read and write Unicode text stored in files too, because the 3.X open call accepts an encoding for text files, and arranges to run the required encoding and decoding for us automatically as data is transferred. This allows us to process a variety of Unicode text created with different encodings than the default for the platform, and store the same text in different encodings for different purposes.

## Reading and Writing Unicode in 3.X
In fact, we can effectively convert a string to different encoded forms both manually with method calls as we did earlier, and automatically on file input and output. We'll use the following Unicode string in this section to demonstrate:
> ```powershell
> C:\code> C:\python33\python
> >>> S = 'A\xc4B\xe8C' 				# Five-character decoded string, non-ASCII
> >>> S
> 'AÄBèC'
> >>> len(S)
> 5
> ```

### Manual encoding
As we've already learned, we can always encode such a string to raw bytes according to the target encoding name:
> ```python
> # Encode manually with methods
> >>> L = S.encode('latin-1') 			# 5 bytes when encoded as latin-1
> >>> L
> b'A\xc4B\xe8C'
> >>> len(L)
> 5
> >>> U = S.encode('utf-8') 			# 7 bytes when encoded as utf-8
> >>> U
> b'A\xc3\x84B\xc3\xa8C'
> >>> len(U)
> 7
> ```

### File output encoding
Now, to write our string to a text file in a particular encoding, we can simply pass the desired encoding name to open -- although we could manually encode first and write in binary mode, there's no need to:
> ```python
> # Encoding automatically when written
> >>> open('latindata', 'w', encoding='latin-1').write(S) 		# Write as latin-1
> 5
> >>> open('utf8data', 'w', encoding='utf-8').write(S) 			# Write as utf-8
> 5
> >>> open('latindata', 'rb').read() 			# Read raw bytes
> b'A\xc4B\xe8C'
> >>> open('utf8data', 'rb').read() 			# Different in files
> b'A\xc3\x84B\xc3\xa8C'
> ```

### File input decoding
Similarly, to read arbitrary Unicode data, we simply pass in the file's encoding type name to open, and it decodes from raw bytes to strings automatically; we could read raw bytes and decode manually too, but that can be tricky when reading in blocks (we might read an incomplete character), and it isn't necessary:
> ```python
> # Decoding automatically when read
> >>> open('latindata', 'r', encoding='latin-1').read() 			# Decoded on input
> 'AÄBèC'
> >>> open('utf8data', 'r', encoding='utf-8').read() 				# Per encoding type
> 'AÄBèC'
> >>> X = open('latindata', 'rb').read() 							# Manual decoding:
> >>> X.decode('latin-1')
> 'AÄBèC'
> >>> X = open('utf8data', 'rb').read()
> >>> X.decode() 													# UTF-8 is default
> 'AÄBèC'
> ```

### Decoding mismatches
Finally, keep in mind that this behavior of files in 3.X limits the kind of content you can load as text. As suggested in the prior section, Python 3.X really must be able to decode the data in text files into a str string, according to either the default or a passedin Unicode encoding name. Trying to open a truly binary data file in text mode, for example, is unlikely to work in 3.X even if you use the correct object types:
> ```python
> >>> file = open(r'C:\Python33\python.exe', 'r')
> >>> text = file.read()
> UnicodeDecodeError: 'charmap' codec can't decode byte 0x90 in position 2: ...
> >>> file = open(r'C:\Python33\python.exe', 'rb')
> >>> data = file.read()
> >>> data[:20]
> b'MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00\xff\xff\x00\x00\xb8\x00\x00\x00'
> ```

The first of these examples might not fail in Python 2.X (normal files do not decode text), even though it probably should: reading the file may return corrupted data in the string, due to automatic end-of-line translations in text mode (any embedded \r\n bytes will be translated to \n on Windows when read). To treat file content as Unicode text in 2.X, we need to use special tools instead of the general open built-in function, as we'll see in a moment. First, though, let's turn to a more explosive topic.

## Handling the BOM in 3.X
As described earlier in this chapter, some encoding schemes store a special byte order marker (BOM) sequence at the start of files, to specify data endianness (which end of a string of bits is most significant to its value) or declare the encoding type. Python both skips this marker on input and writes it on output if the encoding name implies it, but we sometimes must use a specific encoding name to force BOM processing explicitly.

For example, in the UTF-16 and UTF-32 encodings, the BOM specifies big- or littleendian format. A UTF-8 text file may also include a BOM, but this isn't guaranteed, and serves only to declare that it is UTF-8 in general. When reading and writing data using these encoding schemes, Python automatically skips or writes the BOM if it is either implied by a general encoding name, or if you provide a more specific encoding name to force the issue. For instance:
- In UTF-16, the BOM is always processed for "utf-16," and the more specific encoding name "utf-16-le" denotes little-endian format.
- In UTF-8, the more specific encoding "utf-8-sig" forces Python to both skip and write a BOM on input and output, respectively, but the general "utf-8" does not.

### Dropping the BOM in Notepad
Let's make some files with BOMs to see how this works in practice. When you save a text file in Windows Notepad, you can specify its encoding type in a drop-down list -- simple ASCII text, UTF-8, or little- or big-endian UTF-16. If a two-line text file named spam.txt is saved in Notepad as the encoding type ANSI, for instance, it's written as simple ASCII text without a BOM. When this file is read in binary mode in Python, we can see the actual bytes stored in the file. When it's read as text, Python performs endofline translation by default; we can also decode it as explicit UTF-8 text since ASCII is a subset of this scheme (and UTF-8 is Python 3.X's default encoding):
> ```powershell
> C:\code> C:\python33\python 				# File saved in Notepad
> >>> import sys
> >>> sys.getdefaultencoding()
> 'utf-8'
> >>> open('spam.txt', 'rb').read() 		# ASCII (UTF-8) text file
> b'spam\r\nSPAM\r\n'
> >>> open('spam.txt', 'r').read() 			# Text mode translates line end
> 'spam\nSPAM\n'
> >>> open('spam.txt', 'r', encoding='utf-8').read()
> 'spam\nSPAM\n'
> ```

If this file is instead saved as UTF-8 in Notepad, it is prepended with a 3-byte UTF-8 BOM sequence, and we need to give a more specific encoding name ("utf-8-sig") to force Python to skip the marker:
> ```python
> >>> open('spam.txt', 'rb').read() 		# UTF-8 with 3-byte BOM
> b'\xef\xbb\xbfspam\r\nSPAM\r\n'
> >>> open('spam.txt', 'r').read()
> 'ï»¿spam\nSPAM\n'
> >>> open('spam.txt', 'r', encoding='utf-8').read()
> '\ufeffspam\nSPAM\n'
> >>> open('spam.txt', 'r', encoding='utf-8-sig').read()
> 'spam\nSPAM\n'
> ```

If the file is stored as Unicode big endian in Notepad, we get UTF-16-format data in the file, with 2-byte (16-bit) characters prepended with a 2-byte BOM sequence -- the encoding name "utf-16" in Python skips the BOM because it is implied (since all UTF-16 files have a BOM), and “utf-16-be" handles the big-endian format but does not skip the BOM (the second of the following fails to print on older Pythons):
> ```python
> >>> open('spam.txt', 'rb').read()
> b'\xfe\xff\x00s\x00p\x00a\x00m\x00\r\x00\n\x00S\x00P\x00A\x00M\x00\r\x00\n'
> >>> open('spam.txt', 'r').read()
> '\xfeÿ\x00s\x00p\x00a\x00m\x00\n\x00\n\x00S\x00P\x00A\x00M\x00\n\x00\n'
> >>> open('spam.txt', 'r', encoding='utf-16').read()
> 'spam\nSPAM\n'
> >>> open('spam.txt', 'r', encoding='utf-16-be').read()
> '\ufeffspam\nSPAM\n'
> ```

Notepad's "Unicode," by the way, is UTF-16 little endian (which, of course, is one of very many kinds of Unicode encoding!). Dropping the BOM in Python The same patterns generally hold true for output. When writing a Unicode file in Python code, we need a more explicit encoding name to force the BOM in UTF-8 -- "utf-8" does not write (or skip) the BOM, but "utf-8-sig" does:
> ```python
> >>> open('temp.txt', 'w', encoding='utf-8').write('spam\nSPAM\n')
> 10
> >>> open('temp.txt', 'rb').read() 			# No BOM
> b'spam\r\nSPAM\r\n'
> >>> open('temp.txt', 'w', encoding='utf-8-sig').write('spam\nSPAM\n')
> 10
> >>> open('temp.txt', 'rb').read() 			# Wrote BOM
> b'\xef\xbb\xbfspam\r\nSPAM\r\n'
> >>> open('temp.txt', 'r').read()
> 'ï»¿spam\nSPAM\n'
> >>> open('temp.txt', 'r', encoding='utf-8').read() 		# Keeps BOM
> '\ufeffspam\nSPAM\n'
> >>> open('temp.txt', 'r', encoding='utf-8-sig').read() 	# Skips BOM
> 'spam\nSPAM\n'
> ```

Notice that although "utf-8" does not drop the BOM, data without a BOM can be read with both "utf-8" and "utf-8-sig" -- use the latter for input if you're not sure whether a BOM is present in a file (and don't read this paragraph out loud in an airport security line!):
> ```python
> >>> open('temp.txt', 'w').write('spam\nSPAM\n')
> 10
> >>> open('temp.txt', 'rb').read() 				# Data without BOM
> b'spam\r\nSPAM\r\n'
> >>> open('temp.txt', 'r').read() 					# Either utf-8 works
> 'spam\nSPAM\n'
> >>> open('temp.txt', 'r', encoding='utf-8').read()
> 'spam\nSPAM\n'
> >>> open('temp.txt', 'r', encoding='utf-8-sig').read()
> 'spam\nSPAM\n'
> ```

Finally, for the encoding name "utf-16," the BOM is handled automatically: on output, data is written in the platform's native endianness, and the BOM is always written; on input, data is decoded per the BOM, and the BOM is always stripped because it's standard in this scheme:
> ```python
> >>> sys.byteorder
> 'little'
> >>> open('temp.txt', 'w', encoding='utf-16').write('spam\nSPAM\n')
> 10
> >>> open('temp.txt', 'rb').read()
> b'\xff\xfes\x00p\x00a\x00m\x00\r\x00\n\x00S\x00P\x00A\x00M\x00\r\x00\n\x00'
> >>> open('temp.txt', 'r', encoding='utf-16').read()
> 'spam\nSPAM\n'
> ```

More specific UTF-16 encoding names can specify different endianness, though you may have to manually write and skip the BOM yourself in some scenarios if it is required or present -- study the following examples for more BOM-making instructions:
>
> > ```python
> > >>> open('temp.txt', 'w', encoding='utf-16-be').write('\ufeffspam\nSPAM\n')
> > 11
> > >>> open('spam.txt', 'rb').read()
> > b'\xfe\xff\x00s\x00p\x00a\x00m\x00\r\x00\n\x00S\x00P\x00A\x00M\x00\r\x00\n'
> > >>> open('temp.txt', 'r', encoding='utf-16').read()
> > 'spam\nSPAM\n'
> > >>> open('temp.txt', 'r', encoding='utf-16-be').read()
> > '\ufeffspam\nSPAM\n'
> 
> The more specific UTF-16 encoding names work fine with BOM-less files, though "utf-16" requires one on input in order to determine byte order:
> 
> ```python
> > >>> open('temp.txt', 'w', encoding='utf-16-le').write('SPAM')
> > 4
> > >>> open('temp.txt', 'rb').read() 				# OK if BOM not present or expected
> > b'S\x00P\x00A\x00M\x00'
> > >>> open('temp.txt', 'r', encoding='utf-16-le').read()
> > 'SPAM'
> > >>> open('temp.txt', 'r', encoding='utf-16').read()
> > UnicodeError: UTF-16 stream does not start with BOM
> > ```
> 
Experiment with these encodings yourself or see Python's library manuals for more details on the BOM.

## Unicode Filenames and Streams
In closing, this section has focused on the encoding and decoding of Unicode text file content, but Python also supports the notion of non-ASCII file names. In fact, they are independent settings in sys, which can vary per Python version and platform (2.X returns ASCII for the first of the following on Windows):
> ```python
> >>> import sys
> >>> sys.getdefaultencoding(), sys.getfilesystemencoding() 		# File content, names
> ('utf-8', 'mbcs')
> ```

### Filenames: Text versus bytes
Filename encoding is often a nonissue. In short, for filenames given as Unicode text strings, the open call encodes automatically to and from the underlying platform's filename conventions. Passing arbitrarily pre-encoded filenames as byte strings to file tools (including open and directory walkers and listers) overrides automatic encodings, and forces filename results to be returned in encoded byte string form too -- useful if filenames are undecodable per the underlying platform's conventions (I'm using Windows, but some of the following may fail on other platforms):
> ```python
> >>> f = open('xxx\u00A5', 'w') 					# Non-ASCII filename
> >>> f.write('\xA5999\n') 						# Writes five characters
> >>> f.close()
> >>> print(open('xxx\u00A5').read()) 			# Text: auto-encoded
> ¥999
> >>> print(open(b'xxx\xA5').read()) 				# Bytes: pre-encoded
> ¥999
> >>> import glob 								# Filename expansion tool
> >>> glob.glob('*\u00A5*') 						# Get decoded text for decoded text
> ['xxx¥']
> >>> glob.glob(b'*\xA5*') 						# Get encoded bytes for encoded bytes
> [b'xxx\xa5']
> ```

### Stream content: PYTHONIOENCODING
In addition, the environment variable PYTHONIOENCODING can be used to set the encoding used for text in the standard streams -- input, output, and error. This setting overrides Python's default encoding for printed text, which on Windows currently uses a Windows format on 3.X and ASCII on 2.X. Setting this to a general Unicode format like UTF-8 may sometimes be required to print non-ASCII text, and to display such text in shell windows (possibly in conjunction with code page changes on some Windows machines). A script that prints non-ASCII filenames, for example, may fail unless this setting is made.

For more background on this subject, see also "Currency Symbols: Unicode in Action" in Chapter 25. There, we work through an example that demonstrates the essentials of portable Unicode coding, as well as the roles and requirements of PYTHONIOENCODING settings, which we won't rehash here.

For more on these topics in general, see Python manuals or books such as Programming Python, 4th Edition (or later, if later may be). The latter of these digs deeper into streams and files from an applications-level perspective.
