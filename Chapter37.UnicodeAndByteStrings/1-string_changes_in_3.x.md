# String Changes in 3.x
Specifically, we'll explore the basics of Python's support for Unicode text -- rich character strings used in internationalized applications -- as well as binary data -- strings that represent absolute byte values. As we'll see, the advanced string representation story has diverged in recent versions of Python:
- Python 3.X provides an alternative string type for binary data, and supports Unicode text (including ASCII) in its normal string type.
- Python 2.X provides an alternative string type for non-ASCII Unicode text, and supports both simple text and binary data in its normal string type.

In addition, because Python's string model has a direct impact on how you process non-ASCII files, we'll explore the fundamentals of that related topic here as well. Finally, we'll take a brief look at some advanced string and binary tools, such as pattern matching, object pickling, binary data packing, and XML parsing, and the ways in which they are impacted by 3.X's string changes.

One of the most noticeable changes in the Python 3.X line is the mutation of string object types. In a nutshell, 2.X's str and unicode types have morphed into 3.X's `bytes` and `str` types, and a new mutable `bytearray` type has been added. The bytearray type is technically available in Python 2.6 and 2.7 too (though not earlier), but it's a back-port from 3.X and does not as clearly distinguish between text and binary content in 2.X.

Especially if you process data that is either Unicode or binary in nature, these changes can have substantial impacts on your code. As a general rule of thumb, how much you need to care about this topic depends in large part upon which of the following categories you fall into:
- If you deal with non-ASCII Unicode text -- for instance, in the context of internationalized domains like the Web, or the results of some XML and JSON parsers and databases -- you will find support for text encodings to be different in 3.X, but also probably more direct, accessible, and seamless than in 2.X.
- If you deal with binary data -- for example, in the form of image or audio files or packed data processed with the struct module -- you will need to understand 3.X's new bytes object and 3.X's different and sharper distinction between text and binary data and files.
- If you fall into neither of the prior two categories, you can generally use strings in 3.X much as you would in 2.X, with the general str string type, text files, and all the familiar string operations we studied earlier. Your strings will be encoded and decoded by 3.X using your platform's default encoding (e.g., ASCII, or UTF-8 on Windows in the U.S. -- `sys.getdefaultencoding` gives your default if you care to check), but you probably won't notice.

In other words, if your text is always ASCII, you can get by with normal string objects and text files and can avoid most of the following story for now. As we'll see in a moment, ASCII is a simple kind of Unicode and a subset of other encodings, so string operations and files generally "just work" if your programs process only ASCII text.

Even if you fall into the last of the three categories just mentioned, though, a basic understanding of Unicode and 3.X's string model can help both to demystify some of the underlying behavior now, and to make mastering Unicode or binary data issues easier if they impact you later.

To put that more strongly: like it or not, Unicode will be part of most software development in the interconnected future we've sown, and will probably impact you eventually. Though applications are beyond our scope here, if you work with the Internet, files, directories, network interfaces, databases, pipes, JSON, XML, and even GUIs, Unicode may no longer be an optional topic for you in Python 3.X.

Python 3.X's support for Unicode and binary data is also available in 2.X, albeit in different forms. Although our main focus in this chapter is on string types in 3.X, we'll also explore how 2.X's equivalent support differs along the way for readers using 2.X. Regardless of which version you use, the tools we'll explore here can become important in many types of programs.
