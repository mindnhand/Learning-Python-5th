# String Basics
Before we look at any code, let's begin with a general overview of Python's string model. To understand why 3.X changed the way it did on this front, we have to start with a brief look at how characters are actually represented in computers -- both when encoded in files and when stored in memory.

## Character Encoding Schemes
Most programmers think of strings as series of characters used to represent textual data. While that's accurate, the way characters are stored can vary, depending on what sort of character set must be recorded. When text is stored on files, for example, its character set determines its format.

Character sets are standards that assign integer codes to individual characters so they can be represented in computer memory. The ASCII standard, for example, was created in the U.S., and it defines many U.S. programmers' notion of text strings. ASCII defines character codes from 0 through 127 and allows each character to be stored in one 8-bit byte, only 7 bits of which are actually used.

For example, the ASCII standard maps the character 'a' to the integer value 97 (0x61 in hex), which can be stored in a single byte in memory and files. If you wish to see how this works, Python's ord built-in function gives the binary identifying value for a character, and chr returns the character for a given integer code value:
> ```python
> >>> ord('a') 				# 'a' is a byte with binary value 97 in ASCII (and others)
> 97
> >>> hex(97)
> '0x61'
> >>> chr(97) 				# Binary value 97 stands for character 'a'
> 'a'
> ```

Sometimes one byte per character isn't enough, though. Various symbols and accented characters, for instance, do not fit into the range of possible characters defined by ASCII. To accommodate special characters, some standards use all the possible values in an 8-bit byte, 0 through 255, to represent characters, and assign the values 128 through 255 (outside ASCII’s range) to special characters.

One such standard, known as the Latin-1 character set, is widely used in Western Europe. In Latin-1, character codes above 127 are assigned to accented and otherwise special characters. The character assigned to byte value 196, for example, is a specially marked non-ASCII character:
> ```python
> >>> 0xC4
> 196
> >>> chr(196) 				# Python 3.X result form shown
> 'Ä'
> ```

This standard allows for a wide array of extra special characters, but still supports ASCII as a 7-bit subset of its 8-bit representation. Still, some alphabets define so many characters that it is impossible to represent each of them as one byte. Unicode allows more flexibility. Unicode text is sometimes referred to as "wide-character" strings, because characters may be represented with multiple bytes if needed. Unicode is typically used in internationalized programs, to represent European, Asian, and other non-English character sets that have more characters than 8-bit bytes can represent.

To store such rich text in computer memory, we say that characters are translated to and from raw bytes using an encoding -- the rules for translating a string of Unicode characters to a sequence of bytes, and extracting a string from a sequence of bytes. More procedurally, this translation back and forth between bytes and strings is defined by two terms:
- Encoding is the process of translating a string of characters into its raw bytes form, according to a desired encoding name.
- Decoding is the process of translating a raw string of bytes into its character string form, according to its encoding name.

That is, we encode from string to raw bytes, and decode from raw bytes to string. To scripts, decoded strings are just characters in memory, but may be encoded into a variety of byte string representations when stored on files, transferred over networks, embedded in documents and databases, and so on.

For some encodings, the translation process is trivial -- ASCII and Latin-1, for instance, map each character to a fixed-size single byte, so no translation work is required. For other encodings, the mapping can be more complex and yield multiple bytes per character, even for simple 8-bit forms of text.

The widely used UTF-8 encoding, for example, allows a wide range of characters to be represented by employing a variable-sized number of bytes scheme. Character codes less than 128 are represented as a single byte; codes between 128 and 0x7ff (2047) are turned into 2 bytes, where each byte has a value between 128 and 255; and codes above 0x7ff are turned into 3- or 4-byte sequences having values between 128 and 255. This keeps simple ASCII strings compact, sidesteps byte ordering issues, and avoids null (zero value) bytes that can cause problems for C libraries and networking.

Because their encodings' character maps assign characters to the same codes for compatibility, ASCII is a subset of both Latin-1 and UTF-8. That is, a valid ASCII character string is also a valid Latin-1- and UTF-8-encoded string. For example, every ASCII file is a valid UTF-8 file, because the ASCII character set is a 7-bit subset of UTF-8.

Conversely, the UTF-8 encoding is binary compatible with ASCII, but only for character codes less than 128. Latin-1 and UTF-8 simply allow for additional characters: Latin-1 for characters mapped to values 128 through 255 within a byte, and UTF-8 for characters that may be represented with multiple bytes.

Other encodings allow for richer character sets in different ways. UTF-16 and UTF-32, for example, format text with a fixed-size 2 and 4 bytes per each character scheme, respectively, even for characters that could otherwise fit in a single byte. Some encodings may also insert prefixes that identify byte ordering.

To see this for yourself, run a string's encode method, which gives its encoded bytestring format under a named scheme -- a two-character ASCII string is 2 bytes in ASCII, Latin-1, and UTF-8, but it's much wider in UTF-16 and UTF-32, and includes header bytes:
> ```python
> >>> S = 'ni'
> >>> S.encode('ascii'), S.encode('latin1'), S.encode('utf8')
> (b'ni', b'ni', b'ni')
> >>> S.encode('utf16'), len(S.encode('utf16'))
> (b'\xff\xfen\x00i\x00', 6)
> >>> S.encode('utf32'), len(S.encode('utf32'))
> (b'\xff\xfe\x00\x00n\x00\x00\x00i\x00\x00\x00', 12)
> ```

These results differ slightly in Python 2.X (you won't get the leading b for byte strings). But all of these encoding schemes -- ASCII, Latin-1, UTF-8, and many others -- are considered to be Unicode.

To Python programmers, encodings are specified as strings containing the encoding's name. Python comes with roughly 100 different encodings; see the Python library reference for a complete list. Importing the module encodings and running help(encodings) shows you many encoding names as well; some are implemented in Python, and some in C. Some encodings have multiple names, too; for example, latin-1, iso_8859_1, and 8859 are all synonyms for the same encoding, Latin-1. We'll revisit encodings later in this chapter, when we study techniques for writing Unicode strings in a script.

For more on the underlying Unicode story, see the Python standard manual set. It includes a "Unicode HOWTO" in its "Python HOWTOs" section, which provides additional background that we will skip here in the interest of space.

## How Python Stores Strings in Memory
The prior section's encodings really only apply when text is stored or transferred externally, in files and other mediums. In memory, Python always stores decoded text strings in an encoding-neutral format, which may or may not use multiple bytes for each character. All text processing occurs in this uniform internal format. Text is translated to and from an encoding-specific format only when it is transferred to or from external text files, byte strings, or APIs with specific encoding requirements. Once in memory, though, strings have no encoding. They are just the string object presented in this book.

Though irrelevant to your code, it may help some readers to make this more tangible. The way Python actually stores text in memory is prone to change over time, and in fact mutated substantially as of 3.3:
- **Python 3.2 and earlier**
  Through Python 3.2, strings are stored internally in fixed-length UTF-16 (roughly, UCS-2) format with 2 bytes per character, unless Python is configured to use 4 bytes per character (UCS-4).
- **Python 3.3 and later**
  Python 3.3 and later instead use a variable-length scheme with 1, 2, or 4 bytes per character, depending on a string's content. The size is chosen based upon the character with the largest Unicode ordinal value in the represented string. This scheme allows a space-efficient representation in common cases, but also allows for full UCS-4 on all platforms.

Python 3.3's new scheme is an optimization, especially compared to former wide Unicode builds. Per Python documentation: memory footprint is divided by 2 to 4 depending on the text; encoding an ASCII string to UTF-8 doesn't need to encode characters anymore, because its ASCII and UTF-8 representations are the same; repeating a single ASCII letter and getting a substring of an ASCII strings is 4 times faster; UTF-8 is 2 to 4 times faster; and UTF-16 encoding is up to 10 times faster. On some benchmarks, Python 3.3's overall memory usage is 2 to 3 times smaller than 3.2, and similar to the less Unicode-centric 2.7.

Regardless of the storage scheme used, as noted in Chapter 6 Unicode clearly requires us to think of strings in terms of characters, instead of bytes. This may be a bigger hurdle for programmers accustomed to the simpler ASCII-only world where each character mapped to a single byte, but that idea no longer applies, in terms of both the results of text string tools and physical character size:
- **Text tools**
  Today, both string content and length really correspond to Unicode code points -- identifying ordinal numbers for characters. For instance, the built-in `ord` function now returns a character's Unicode code point ordinal, which is not necessarily an ASCII code, and which may or may not fit in a single 8-bit byte's value. Similarly, `len` returns the number of characters, not bytes; the string is probably larger in memory, and its characters may not fit in bytes anyhow.
- **Text size**
As we saw by example in Chapter 4, under Unicode a single character does not necessarily map directly to a single byte, either when encoded in a file or when stored in memory. Even characters in simple 7-bit ASCII text may not map to bytes -- UTF-16 uses multiple bytes per character in files, and Python may allocate 1, 2, or 4 bytes per character in memory. Thinking in terms of characters allows us to abstract away the details of external and internal storage.

The key point here, though, is that encoding pertains mostly to files and transfers. Once loaded into a Python string, text in memory has no notion of an "encoding," and is simply a sequence of Unicode characters (a.k.a. code points) stored generically. In your script, that string is accessed as a Python string object -- the next section's topic.


## Python's String Types
At a more concrete level, the Python language provides string data types to represent character text in your scripts. The string types you will use in your scripts depend upon the version of Python you're using. Python 2.X has a general string type for representing binary data and simple 8-bit text like ASCII, along with a specific type for representing richer Unicode text:
- str for representing 8-bit text and binary data
- unicode for representing decoded Unicode text

Python 2.X's two string types are different (unicode allows for the extra size of some Unicode characters and has extra support for encoding and decoding), but their operation sets largely overlap. The str string type in 2.X is used for text that can be represented with 8-bit bytes (including ASCII and Latin-1), as well as binary data that represents absolute byte values.

By contrast, Python 3.X comes with three string object types -- one for textual data and two for binary data:
- str for representing decoded Unicode text (including ASCII)
- bytes for representing binary data (including encoded text)
- bytearray, a mutable flavor of the bytes type
As mentioned earlier, bytearray is also available in Python 2.6 and 2.7, but it's simply a back-port from 3.X with less content-specific behavior and is generally considered a 3.X type.

### Why the different string types?
All three string types in 3.X support similar operation sets, but they have different roles. The main goal behind this change in 3.X was to merge the normal and Unicode string types of 2.X into a single string type that supports both simple and Unicode text: developers wanted to remove the 2.X string dichotomy and make Unicode processing more natural. Given that ASCII and other 8-bit text is really a simple kind of Unicode, this convergence seems logically sound.

To achieve this, 3.X stores text in a redefined str type -- an immutable sequence of characters (not necessarily bytes), which may contain either simple text such as ASCII whose character values fit in single bytes, or richer character set text such as UTF-8 whose character values may require multiple bytes. Strings processed by your script with this type are stored generically in memory, and are encoded to and decoded from byte strings per either the platform Unicode default or an explicit encoding name. This allows scripts to translate text to different encoding schemes, both in memory and when transferring to and from files.

While 3.X's new str type does achieve the desired string/unicode merging, many programs still need to process raw binary data that is not encoded per any text format. Image and audio files, as well as packed data used to interface with devices or C programs you might process with Python's struct module, fall into this category. Because Unicode strings are decoded from bytes, they cannot be used to represent bytes.

To support processing of such truly binary data, a new string type, bytes, also was introduced -- an immutable sequence of 8-bit integers representing absolute byte values, which prints as ASCII characters when possible. Though a distinct object type, bytes supports almost all the same operations that the str type does; this includes string methods, sequence operations, and even re module pattern matching, but not string formatting. In 2.X, the general str type fills this binary data role, because its strings are just sequences of bytes; the separate unicode type handles richer text strings.

In more detail, a 3.X bytes object really is a sequence of small integers, each of which is in the range 0 through 255; indexing a bytes returns an int, slicing one returns another bytes, and running the list built-in on one returns a list of integers, not characters. When processed with operations that assume characters, though, the contents of bytes objects are assumed to be ASCII-encoded bytes (e.g., the isalpha method assumes each byte is an ASCII character code). Further, bytes objects are printed as character strings instead of integers for convenience.

While they were at it, Python developers also added a bytearray type in 3.X. bytear ray is a variant of bytes that is mutable and so supports in-place changes. It supports the usual string operations that str and bytes do, as well as many of the same in-place change operations as lists (e.g., the append and extend methods, and assignment to indexes). This can be useful both for truly binary data and simple types of text. Assuming your text strings can be treated as raw 8-bit bytes (e.g., ASCII or Latin-1 text), bytearray finally adds direct in-place mutability for text data -- something not possible without conversion to a mutable type in Python 2.X, and not supported by Python 3.X's str or bytes.

Although Python 2.X and 3.X offer much the same functionality, they package it differently. In fact, the mapping from 2.X to 3.X string types is not completely direct -- 2.X's str equates to both str and bytes in 3.X, and 3.X's str equates to both str and unicode in 2.X. Moreover, the mutability of 3.X's bytearray is unique.

In practice, though, this asymmetry is not as daunting as it might sound. It boils down to the following: in 2.X, you will use str for simple text and binary data and unicode for advanced forms of text whose character sets don't map to 8-bit bytes; in 3.X, you'll use str for any kind of text (ASCII, Latin-1, and all other kinds of Unicode) and bytes or bytearray for binary data. In practice, the choice is often made for you by the tools you use -- especially in the case of file processing tools, the topic of the next section.

## Text and Binary Files
File I/O (input and output) was also revamped in 3.X to reflect the str/bytes distinction and automatically support encoding Unicode text on transfers. Python now makes a sharp platform-independent distinction between text files and binary files; in 3.X:
- **Text files**
  When a file is opened in text mode, reading its data automatically decodes its content and returns it as a str; writing takes a str and automatically encodes it before transferring it to the file. Both reads and writes translate per a platform default or a provided encoding name. Text-mode files also support universal end-of-line translation and additional encoding specification arguments. Depending on the encoding name, text files may also automatically process the byte order mark sequence at the start of a file (more on this momentarily).
- **Binary files**
  When a file is opened in binary mode by adding a b (lowercase only) to the modestring argument in the built-in open call, reading its data does not decode it in any way but simply returns its content raw and unchanged, as a bytes object; writing similarly takes a bytes object and transfers it to the file unchanged. Binary-mode files also accept a bytearray object for the content to be written to the file. 

Because the language sharply differentiates between str and bytes, you must decide whether your data is text or binary in nature and use either str or bytes objects to represent its content in your script, as appropriate. Ultimately, the mode in which you open a file will dictate which type of object your script will use to represent its content:
- If you are processing image files, data transferred over networks, packed binary data whose content you must extract, or some device data streams, chances are good that you will want to deal with it using bytes and binary-mode files. You might also opt for bytearray if you wish to update the data without making copies of it in memory.
- If instead you are processing something that is textual in nature, such as program output, HTML, email content, or CSV or XML files, you'll probably want to use str and text-mode files.

Notice that the mode string argument to built-in function open (its second argument) becomes fairly crucial in Python 3.X -- its content not only specifies a file processing mode, but also implies a Python object type. By adding a b to the mode string, you specify binary mode and will receive, or must provide, a bytes object to represent the file's content when reading or writing. Without the b, your file is processed in text mode, and you'll use str objects to represent its content in your script. For example, the modes rb, wb, and rb+ imply bytes; r, w+, and rt (the default) imply str.

Text-mode files also handle the byte order marker (BOM) sequence that may appear at the start of files under some encoding schemes. In the UTF-16 and UTF-32 encodings, for example, the BOM specifies big- or little-endian format (essentially, which end of a bit-string is most significant) -- see the leading bytes in the results of the UTF-16 and UTF-32 encoding calls we ran earlier for examples. A UTF-8 text file might also include a BOM to declare that it is UTF-8 in general. When reading and writing data using these encoding schemes, Python skips or writes the BOM according to rules we'll study later in this chapter.

In Python 2.X, the same behavior is supported, but normal files created by open are used to access bytes-based data, and Unicode files opened with the codecs.open call are used to process Unicode text data. The latter of these also encode and decode on transfer, as we'll see later in this chapter. First, let's explore Python's Unicode string model live.
