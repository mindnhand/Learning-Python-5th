# Other String Tool Changes in 3.X
Many of the other popular string-processing tools in Python's standard library have also been revamped for the new str/bytes type dichotomy. We won't cover any of these application-focused tools in much detail in this core language book, but to wrap up this chapter, here's a quick look at four of the major tools impacted: the re patternmatching module, the struct binary data module, the pickle object serialization module, and the xml package for parsing XML text. As noted ahead, other Python tools, such as its json module, differ in ways similar to those presented here.

## The re Pattern-Matching Module
Python's re pattern-matching module supports text processing that is more general than that afforded by simple string method calls such as find, split, and replace. With re, strings that designate searching and splitting targets can be described by general patterns, instead of absolute text. This module has been generalized to work on objects of any string type in 3.X -- str, bytes, and bytearray -- and returns result substrings of the same type as the subject string. In 2.X it supports both unicode and str.

Here it is at work in 3.X, extracting substrings from a line of text -- borrowed, of course, from Monty Python's The Meaning of Life. Within pattern strings, (.\*) means any character (the .), zero or more times (the \*), saved away as a matched substring (the ()). Parts of the string matched by the parts of a pattern enclosed in parentheses are available after a successful match, via the group or groups method:
> ```powershell
> C:\code> C:\python33\python
> >>> import re
> >>> S = 'Bugger all down here on earth!' 					# Line of text
> >>> B = b'Bugger all down here on earth!' 				# Usually from a file
> >>> re.match('(.*) down (.*) on (.*)', S).groups() 		# Match line to pattern
> ('Bugger all', 'here', 'earth!') 							# Matched substrings
> >>> re.match(b'(.*) down (.*) on (.*)', B).groups() 		# bytes substrings
> (b'Bugger all', b'here', b'earth!')
> ```

In Python 2.X results are similar, but the unicode type is used for non-ASCII text, and str handles both 8-bit and binary text:
> ```powershell
> C:\code> C:\python27\python
> >>> import re
> >>> S = 'Bugger all down here on earth!' 					# Simple text and binary
> >>> U = u'Bugger all down here on earth!' 				# Unicode text
> >>> re.match('(.*) down (.*) on (.*)', S).groups()
> ('Bugger all', 'here', 'earth!')
> >>> re.match('(.*) down (.*) on (.*)', U).groups()
> (u'Bugger all', u'here', u'earth!')
> ```

Since bytes and str support essentially the same operation sets, this type distinction is largely transparent. But note that, like in other APIs, you can't mix str and bytes types in its calls' arguments in 3.X (although if you don't plan to do pattern matching on binary data, you probably don't need to care):
> ```powershell
> C:\code> C:\python33\python
> >>> import re
> >>> S = 'Bugger all down here on earth!'
> >>> B = b'Bugger all down here on earth!'
> >>> re.match('(.*) down (.*) on (.*)', B).groups()
> TypeError: can't use a string pattern on a bytes-like object
> >>> re.match(b'(.*) down (.*) on (.*)', S).groups()
> TypeError: can't use a bytes pattern on a string-like object
> >>> re.match(b'(.*) down (.*) on (.*)', bytearray(B)).groups()
> (bytearray(b'Bugger all'), bytearray(b'here'), bytearray(b'earth!'))
> >>> re.match('(.*) down (.*) on (.*)', bytearray(B)).groups()
> TypeError: can't use a string pattern on a bytes-like object
> ```

## The struct Binary Data Module
The Python struct module, used to create and extract packed binary data from strings, also works the same in 3.X as it does in 2.X, but in 3.X packed data is represented as bytes and bytearray objects only, not str objects (which makes sense, given that it's intended for processing binary data, not decoded text); and "s" data code values must be bytes as of 3.2 (the former str UTF-8 auto-encode is dropped).

Here are both Pythons in action, packing three objects into a string according to a binary type specification (they create a 4-byte integer, a 4-byte string, and a 2-byte integer):
> ```powershell
> C:\code> C:\python33\python
> >>> from struct import pack
> >>> pack('>i4sh', 7, b'spam', 8) 			# bytes in 3.X (8-bit strings)
> b'\x00\x00\x00\x07spam\x00\x08'
> C:\code> C:\python27\python
> >>> from struct import pack
> >>> pack('>i4sh', 7, 'spam', 8) 			# str in 2.X (8-bit strings)
> '\x00\x00\x00\x07spam\x00\x08'
> ```

Since bytes has an almost identical interface to that of str in 3.X and 2.X, though, most programmers probably won't need to care -- the change is irrelevant to most existing code, especially since reading from a binary file creates a bytes automatically. Although the last test in the following example fails on a type mismatch, most scripts will read binary data from a file, not create it as a string as we do here:
> ```powershell
> C:\code> C:\python33\python
> >>> import struct
> >>> B = struct.pack('>i4sh', 7, b'spam', 8)
> >>> B
> b'\x00\x00\x00\x07spam\x00\x08'
> >>> vals = struct.unpack('>i4sh', B)
> >>> vals
> (7, b'spam', 8)
> >>> vals = struct.unpack('>i4sh', B.decode())
> TypeError: 'str' does not support the buffer interface
> ```

Apart from the new syntax for bytes, creating and reading binary files works almost the same in 3.X as it does in 2.X. Still, code like this is one of the main places where programmers will notice the bytes object type:
> ```powershell
> C:\code> C:\python33\python
> # Write values to a packed binary file
> >>> F = open('data.bin', 'wb') 			# Open binary output file
> >>> import struct
> >>> data = struct.pack('>i4sh', 7, b'spam', 8) 		# Create packed binary data
> >>> data 									# bytes in 3.X, not str
> b'\x00\x00\x00\x07spam\x00\x08'
> >>> F.write(data) 						# Write to the file
> 10
> >>> F.close()
> # Read values from a packed binary file
> >>> F = open('data.bin', 'rb') 			# Open binary input file
> >>> data = F.read() 						# Read bytes
> >>> data
> b'\x00\x00\x00\x07spam\x00\x08'
> >>> values = struct.unpack('>i4sh', data) # Extract packed binary data
> >>> values 								# Back to Python objects
> (7, b'spam', 8)
> ```

Once you've extracted packed binary data into Python objects like this, you can dig even further into the binary world if you have to -- strings can be indexed and sliced to get individual bytes' values, individual bits can be extracted from integers with bitwise operators, and so on (see earlier in this book for more on the operations applied here):
> ```python
> >>> values 						# Result of struct.unpack
> (7, b'spam', 8)
> # Accessing bits of parsed integers
> >>> bin(values[0]) 				# Can get to bits in ints
> '0b111'
> >>> values[0] & 0x01 				# Test first (lowest) bit in int
> 1
> >>> values[0] | 0b1010 			# Bitwise or: turn bits on
> 15
> >>> bin(values[0] | 0b1010) 		# 15 decimal is 1111 binary
> '0b1111'
> >>> bin(values[0] ^ 0b1010) 		# Bitwise xor: off if both true
> '0b1101'
> >>> bool(values[0] & 0b100) 		# Test if bit 3 is on
> True
> >>> bool(values[0] & 0b1000) 		# Test if bit 4 is set
> False
> ```

Since parsed bytes strings are sequences of small integers, we can do similar processing with their individual bytes:
> ```python
> # Accessing bytes of parsed strings and bits within them
> >>> values[1]
> b'spam'
> >>> values[1][0] 					# bytes string: sequence of ints
> 115
> >>> values[1][1:] 				# Prints as ASCII characters
> b'pam'
> >>> bin(values[1][0]) 			# Can get to bits of bytes in strings
> '0b1110011'
> >>> bin(values[1][0] | 0b1100) 	# Turn bits on
> '0b1111111'
> >>> values[1][0] | 0b1100
> 127
> ```

Of course, most Python programmers don't deal with binary bits; Python has higherlevel object types, like lists and dictionaries that are generally a better choice for representing information in Python scripts. However, if you must use or produce lowerlevel data used by C programs, networking libraries, or other interfaces, Python has tools to assist.

## The pickle Object Serialization Module
We met the pickle module briefly in Chapter 9, Chapter 28, and Chapter 31. In Chapter 28, we also used the shelve module, which uses pickle internally. For completeness here, keep in mind that the Python 3.X version of the pickle module always creates a bytes object, regardless of the default or passed-in "protocol" (data format level). You can see this by using the module's dumps call to return an object's pickle string:
> ```powershell
> C:\code> C:\python33\python
> >>> import pickle 				# dumps() returns pickle string
> >>> pickle.dumps([1, 2, 3]) 		# Python 3.X default protocol=3=binary
> b'\x80\x03]q\x00(K\x01K\x02K\x03e.'
> >>> pickle.dumps([1, 2, 3], protocol=0) 		# ASCII protocol 0, but still bytes!
> b'(lp0\nL1L\naL2L\naL3L\na.'
> ```

This implies that files used to store pickled objects must always be opened in binary mode in Python 3.X, since text files use str strings to represent data, not bytes -- the dump call simply attempts to write the pickle string to an open output file:
> ```python
> >>> pickle.dump([1, 2, 3], open('temp', 'w')) 			# Text files fail on bytes!
> TypeError: must be str, not bytes 			# Despite protocol value
> >>> pickle.dump([1, 2, 3], open('temp', 'w'), protocol=0)
> TypeError: must be str, not bytes
> >>> pickle.dump([1, 2, 3], open('temp', 'wb')) 			# Always use binary in 3.X
> >>> open('temp', 'r').read() 					# This works, but just by luck
> '\u20ac\x03]q\x00(K\x01K\x02K\x03e.'
> ```

Notice the last result here didn't issue an error in text mode only because the stored binary data was compatible with the Windows platform's UTF-8 default decoder; this was really just luck (and in fact, this command failed when printing in older Pythons, and may fail on other platforms). Because pickle data is not generally decodable Unicode text, the same rule holds on input -- correct usage in 3.X requires always both writing and reading pickle data in binary modes, whether unpickling or not:
> ```python
> >>> pickle.dump([1, 2, 3], open('temp', 'wb'))
> >>> pickle.load(open('temp', 'rb'))
> [1, 2, 3]
> >>> open('temp', 'rb').read()
> b'\x80\x03]q\x00(K\x01K\x02K\x03e.'
> ```

In Python 2.X, we can get by with text-mode files for pickled data, as long as the protocol is level 0 (the default in 2.X) and we use text mode consistently to convert line ends:
> ```powershell
> C:\code> C:\python27\python
> >>> import pickle
> >>> pickle.dumps([1, 2, 3]) 			# Python 2.X default=0=ASCII
> '(lp0\nI1\naI2\naI3\na.'
> >>> pickle.dumps([1, 2, 3], protocol=1)
> ']q\x00(K\x01K\x02K\x03e.'
> >>> pickle.dump([1, 2, 3], open('temp', 'w')) 		# Text mode works in 2.X
> >>> pickle.load(open('temp'))
> [1, 2, 3]
> >>> open('temp').read()
> '(lp0\nI1\naI2\naI3\na.'
> ```

If you care about version neutrality, though, or don't want to care about protocols or their version-specific defaults, always use binary-mode files for pickled data -- the following works the same in Python 3.X and 2.X:
> ```python
> >>> import pickle
> >>> pickle.dump([1, 2, 3], open('temp', 'wb')) 		# Version neutral
> >>> pickle.load(open('temp', 'rb')) 			# And required in 3.X
> [1, 2, 3]
> ```

Because almost all programs let Python pickle and unpickle objects automatically and do not deal with the content of pickled data itself, the requirement to always use binary file modes is the only significant incompatibility in Python 3.X's newer pickling model. See reference books or Python's manuals for more details on object pickling.

## XML Parsing Tools
XML is a tag-based language for defining structured information, commonly used to define documents and data shipped over the Web. Although some information can be extracted from XML text with basic string methods or the re pattern module, XML's nesting of constructs and arbitrary attribute text tend to make full parsing more accurate.

Because XML is such a pervasive format, Python itself comes with an entire package of XML parsing tools that support the SAX and DOM parsing models, as well as a package known as ElementTree -- a Python-specific API for parsing and constructing XML. Beyond basic parsing, the open source domain provides support for additional XML tools, such as XPath, Xquery, XSLT, and more.

XML by definition represents text in Unicode form, to support internationalization. Although most of Python's XML parsing tools have always returned Unicode strings, in Python 3.X their results have mutated from the 2.X unicode type to the 3.X general str string type -- which makes sense, given that 3.X's str string is Unicode, whether the encoding is ASCII or other.

We can't go into many details here, but to sample the flavor of this domain, suppose we have a simple XML text file, mybooks.xml:
>
> > ```xml
> > <books>
> >     <date>1995~2013</date>
> >     <title>Learning Python</title>
> >     <title>Programming Python</title>
> >     <title>Python Pocket Reference</title>
> >     <publisher>O'Reilly Media</publisher>
> > </books>
> > ```
> 
> and we want to run a script to extract and display the content of all the nested title tags, as follows:
> 
> > Learning Python
> > Programming Python
> > Python Pocket Reference
> 

There are at least four basic ways to accomplish this (not counting more advanced tools like XPath). First, we could run basic pattern matching on the file's text, though this tends to be inaccurate if the text is unpredictable. Where applicable, the re module we met earlier does the job -- its match method looks for a match at the start of a string, search scans ahead for a match, and the findall method used here locates all places where the pattern matches in the string (the result comes back as a list of matched substrings corresponding to parenthesized pattern groups, or tuples of such for multiple groups):
> ```python
> # File patternparse.py
> import re
> text = open('mybooks.xml').read()
> found = re.findall('<title>(.*)</title>', text)
> for title in found: print(title)
> ```

Second, to be more robust, we could perform complete XML parsing with the standard library's DOM parsing support. DOM parses XML text into a tree of objects and provides an interface for navigating the tree to extract tag attributes and values; the interface is a formal specification, independent of Python:
> ```python
> # File domparse.py
> from xml.dom.minidom import parse, Node
> xmltree = parse('mybooks.xml')
> for node1 in xmltree.getElementsByTagName('title'):
>     for node2 in node1.childNodes:
>         if node2.nodeType == Node.TEXT_NODE:
>             print(node2.data)
> ```

As a third option, Python's standard library supports SAX parsing for XML. Under the SAX model, a class's methods receive callbacks as a parse progresses and use state information to keep track of where they are in the document and collect its data:
> ```python
> # File saxparse.py
> import xml.sax.handler
> class BookHandler(xml.sax.handler.ContentHandler):
>     def __init__(self):
>         self.inTitle = False
>     def startElement(self, name, attributes):
>         if name == 'title':
>             self.inTitle = True
>     def characters(self, data):
>         if self.inTitle:
>             print(data)
>     def endElement(self, name):
>         if name == 'title':
>             self.inTitle = False
> 
> import xml.sax
> parser = xml.sax.make_parser()
> handler = BookHandler()
> parser.setContentHandler(handler)
> parser.parse('mybooks.xml')
> ```

Finally, the ElementTree system available in the etree package of the standard library can often achieve the same effects as XML DOM parsers, but with remarkably less code. It's a Python-specific way to both parse and generate XML text; after a parse, its API gives access to components of the document:
> ```python
> # File etreeparse.py
> from xml.etree.ElementTree import parse
> tree = parse('mybooks.xml')
> for E in tree.findall('title'):
>     print(E.text)
> ```

When run in either 2.X or 3.X, all four of these scripts display the same printed result:
> ```powershell
> C:\code> C:\python27\python domparse.py
> Learning Python
> Programming Python
> Python Pocket Reference
> C:\code> C:\python33\python domparse.py
> Learning Python
> Programming Python
> Python Pocket Reference
> ```

Technically, though, in 2.X some of these scripts produce unicode string objects, while in 3.X all produce str strings, since that type includes Unicode text (whether ASCII or other):
> ```powershell
> C:\code> C:\python33\python
> >>> from xml.dom.minidom import parse, Node
> >>> xmltree = parse('mybooks.xml')
> >>> for node in xmltree.getElementsByTagName('title'):
>         for node2 in node.childNodes:
>             if node2.nodeType == Node.TEXT_NODE:
>                 node2.data
> 
> 'Learning Python'
> 'Programming Python'
> 'Python Pocket Reference'
> C:\code> C:\python27\python
> >>> ...same code...
> u'Learning Python'
> u'Programming Python'
> u'Python Pocket Reference'
> ```

Programs that must deal with XML parsing results in nontrivial ways will need to account for the different object type in 3.X. Again, though, because all strings have nearly identical interfaces in both 2.X and 3.X, most scripts won't be affected by the change; tools available on unicode in 2.X are generally available on str in 3.X. The major feat, if there is one, is likely in getting the encoding names right when transferring the parsedout data to and from files, network connections, GUIs, and so on.

Regrettably, going into further XML parsing details is beyond this book's scope. If you are interested in text or XML parsing, it is covered in more detail in the applications focused follow-up book Programming Python. For more details on re, struct, pickle, and XML, as well as the additional impacts of Unicode on other library tools such as filename expansion and directory walkers, consult the Web, the aforementioned book and others, and Python's standard library manual.

For a related topic, see also the JSON example in Chapter 9 -- a language-neutral data exchange format, whose structure is very similar to Python dictionaries and lists, and whose strings are all Unicode that differs in type between Pythons 2.X and 3.X much the same as shown for XML here.

> **Why You Will Care: Inspecting Files, and Much More**
> As I was updating this chapter, I stumbled onto a use case for some of its tools. After saving a formerly ASCII HTML file in Notepad as "UTF8," I found that it had grown a mystery non-ASCII character along the way due to an apparent keyboard operator error, and would no longer work as ASCII in text tools. To find the bad character, I simply started Python, decoded the file's content from its UTF-8 format via a text mode file, and scanned character by character looking for the first byte that was not a valid ASCII character too:
> > ```python
> > >>> f = open('py33-windows-launcher.html', encoding='utf8')
> > >>> t = f.read()
> > >>> for (i, c) in enumerate(t):
> > try:
> >     x = c.encode(encoding='ascii')
> > except:
> >     print(i, sys.exc_info()[0])
> > 
> > 9886 <class 'UnicodeEncodeError'>
> > ```
> 
> With the bad character's index in hand, it's easy to slice the Unicode string for more details:
> 
> > ```python
> > >>> len(t)
> > 31021
> > >>> t[9880:9890]
> > 'ugh. \u206cThi'
> > >>> t[9870:9890]
> > 'trace through. \u206cThi'
> > ```
> 
> After fixing, I could also open in binary mode to verify and explore actual undecoded file content further:
> 
> > ```python
> > >>> f = open('py33-windows-launcher.html', 'rb')
> > >>> b = f.read()
> > >>> b[0]
> > 60
> > >>> b[:10]
> > b'<HTML>\r\n<T'
> > ```
> 
> Not rocket science, perhaps, and there are other approaches, but Python makes for a convenient tactical tool in such cases, and its file objects give you a tangible window on your data when needed, both in scripts and interactive mode.
> 
> For more realistically scaled examples of Unicode at work, I suggest my other book Programming Python, 4th Edition (or later). That book develops much larger programs than we can here, and has numerous up close and personal encounters with Unicode along the way, in the context of files, directory walkers, network sockets, GUIs, email content and headers, web page content, databases, and more. Though clearly an important topic in today's global software world, Unicode is more mandatory than you might expect, especially in a language like Python 3.X, which elevates it to its core string and file types, thus bringing all its users into the Unicode fold -- ready or not!

