# Using Text and Binary Files
This section expands on the impact of Python 3.X's string model on the file processing basics introduced earlier in the book. As mentioned earlier, the mode in which you open a file is crucial -- it determines which object type you will use to represent the file's content in your script. Text mode implies str objects, and binary mode implies bytes objects:
- Text-mode files interpret file contents according to a Unicode encoding -- either the default for your platform, or one whose name you pass in. By passing in an encoding name to open, you can force conversions for various types of Unicode files. Textmode files also perform universal line-end translations: by default, all line-end forms map to the single '\n' character in your script, regardless of the platform on which you run it. As described earlier, text files also handle reading and writing the byte order mark (BOM) stored at the start-of-file in some Unicode encoding schemes.
- Binary-mode files instead return file content to you raw, as a sequence of integers representing byte values, with no encoding or decoding and no line-end translations.

The second argument to open determines whether you want text or binary processing, just as it does in 2.X Python -- adding a b to this string implies binary mode (e.g., "rb" to read binary data files). The default mode is "rt"; this is the same as "r", which means text input (just as in 2.X).

In 3.X, though, this mode argument to open also implies an object type for file content representation, regardless of the underlying platform -- text files return a str for reads and expect one for writes, but binary files return a bytes for reads and expect one (or a bytearray) for writes.

## Text File Basics
To demonstrate, let's begin with basic file I/O. As long as you're processing basic text files (e.g., ASCII) and don't care about circumventing the platform-default encoding of strings, files in 3.X look and feel much as they do in 2.X (for that matter, so do strings in general). The following, for instance, writes one line of text to a file and reads it back in 3.X, exactly as it would in 2.X (note that file is no longer a built-in name in 3.X, so it's perfectly OK to use it as a variable here):
> ```powershell
> C:\code> C:\python33\python
> # Basic text files (and strings) work the same as in 2.X
> >>> file = open('temp', 'w')
> >>> size = file.write('abc\n') 				# Returns number of characters written
> >>> file.close() 								# Manual close to flush output buffer
> >>> file = open('temp') 						# Default mode is "r" (== "rt"): text input
> >>> text = file.read()
> >>> text
> 'abc\n'
> >>> print(text)
> abc
> ```

## Text and Binary Modes in 2.X and 3.X
In Python 2.X, there is no major distinction between text and binary files -- both accept and return content as str strings. The only major difference is that text files automatically map \n end-of-line characters to and from \r\n on Windows, while binary files do not (I'm stringing operations together into one-liners here just for brevity):
> ```powershell
> C:\code> C:\python27\python
> >>> open('temp', 'w').write('abd\n') # Write in text mode: adds \r
> >>> open('temp', 'r').read() # Read in text mode: drops \r
> 'abd\n'
> >>> open('temp', 'rb').read() # Read in binary mode: verbatim
> 'abd\r\n'
> >>> open('temp', 'wb').write('abc\n') # Write in binary mode
> >>> open('temp', 'r').read() # \n not expanded to \r\n
> 'abc\n'
> >>> open('temp', 'rb').read()
> 'abc\n'
> ```

In Python 3.X, things are a bit more complex because of the distinction between str for text data and bytes for binary data. To demonstrate, let's write a text file and read it back in both modes in 3.X. Notice that we are required to provide a str for writing, but reading gives us a str or a bytes, depending on the open mode:
> ```powershell
> C:\code> C:\python33\python
> # Write and read a text file
> >>> open('temp', 'w').write('abc\n') 				# Text mode output, provide a str
> 4
> >>> open('temp', 'r').read() 						# Text mode input, returns a str
> 'abc\n'
> >>> open('temp', 'rb').read() 					# Binary mode input, returns a bytes
> b'abc\r\n'
> ```

Notice how on Windows text-mode files translate the \n end-of-line character to \r\n on output; on input, text mode translates the \r\n back to \n, but binary-mode files do not. This is the same in 2.X, and it's normally what we want -- text files should for portability map end-of-line markers to and from \n (which is what is actually present in files in Linux, where no mapping occurs), and such translations should never occur for binary data (where end-of-line bytes are irrelevant). Although you can control this behavior with extra open arguments in 3.X if desired, the default usually works well.

Now let's do the same again, but with a binary file. We provide a bytes to write in this case, and we still get back a str or a bytes, depending on the input mode:
> ```python
> # Write and read a binary file
> >>> open('temp', 'wb').write(b'abc\n') 			# Binary mode output, provide a bytes
> 4
> >>> open('temp', 'r').read() 						# Text mode input, returns a str
> 'abc\n'
> >>> open('temp', 'rb').read() 					# Binary mode input, returns a bytes
> b'abc\n'
> ```

Note that the \n end-of-line character is not expanded to \r\n in binary-mode output -- again, a desired result for binary data. Type requirements and file behavior are the same even if the data we're writing to the binary file is truly binary in nature. In the following, for example, the "\x00" is a binary zero byte and not a printable character:
> ```python
> # Write and read truly binary data
> >>> open('temp', 'wb').write(b'a\x00c') 			# Provide a bytes
> 3
> >>> open('temp', 'r').read() 						# Receive a str
> 'a\x00c'
> >>> open('temp', 'rb').read() 					# Receive a bytes
> b'a\x00c'
> ```

Binary-mode files always return contents as a bytes object, but accept either a bytes or bytearray object for writing; this naturally follows, given that bytearray is basically just a mutable variant of bytes. In fact, most APIs in Python 3.X that accept a bytes also allow a bytearray:
> ```python
> # bytearrays work too
> >>> BA = bytearray(b'\x01\x02\x03')
> >>> open('temp', 'wb').write(BA)
> 3
> >>> open('temp', 'r').read()
> '\x01\x02\x03'
> >>> open('temp', 'rb').read()
> b'\x01\x02\x03'
> ```

## Type and Content Mismatches in 3.X
Notice that you cannot get away with violating Python's str/bytes type distinction when it comes to files. As the following examples illustrate, we get errors (shortened here) if we try to write a bytes to a text file or a str to a binary file (the exact text of the error messages here is prone to change):
> ```python
> # Types are not flexible for file content
> >>> open('temp', 'w').write('abc\n') 					# Text mode makes and requires str
> 4
> >>> open('temp', 'w').write(b'abc\n')
> TypeError: must be str, not bytes
> >>> open('temp', 'wb').write(b'abc\n') 				# Binary mode makes and requires bytes
> 4
> >>> open('temp', 'wb').write('abc\n')
> TypeError: 'str' does not support the buffer interface
> ```

This makes sense: text has no meaning in binary terms, before it is encoded. Although it is often possible to convert between the types by encoding str and decoding bytes, as described earlier in this chapter, you will usually want to stick to either str for text data or bytes for binary data. Because the str and bytes operation sets largely intersect, the choice won't be much of a dilemma for most programs (see the string tools coverage in the final section of this chapter for some prime examples of this).

In addition to type constraints, file content can matter in 3.X. Text-mode output files require a str instead of a bytes for content, so there is no way in 3.X to write truly binary data to a text-mode file. Depending on the encoding rules, bytes outside the default character set can sometimes be embedded in a normal string, and they can always be written in binary mode (some of the following raise errors when displaying their string results in Pythons prior to 3.3, but the file operations work successfully):
> ```python
> # Can't read truly binary data in text mode
> >>> chr(0xFF) 				# FF is a valid char, FE is not
> 'ÿ'
> >>> chr(0xFE) 				# An error in some Pythons
> '\xfe'
> >>> open('temp', 'w').write(b'\xFF\xFE\xFD') 			# Can't use arbitrary bytes!
> TypeError: must be str, not bytes
> >>> open('temp', 'w').write('\xFF\xFE\xFD') 			# Can write if embeddable in str
> 3
> >>> open('temp', 'wb').write(b'\xFF\xFE\xFD') 		# Can also write in binary mode
> 3
> >>> open('temp', 'rb').read() 						# Can always read as binary bytes
> b'\xff\xfe\xfd'
> >>> open('temp', 'r').read() 							# Can't read text unless decodable!
> 'ÿ\xfe\xfd' 					# An error in some Pythons
> ```

In general, however, because text-mode input files in 3.X must be able to decode content per a Unicode encoding, there is no way to read truly binary data in text mode, as the next section explains.

