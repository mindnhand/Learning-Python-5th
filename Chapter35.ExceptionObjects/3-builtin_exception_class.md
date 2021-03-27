# Built-in Exception Classes
I didn't really pull the prior section's examples out of thin air. All built-in exceptions that Python itself may raise are predefined class objects. Moreover, they are organized into a shallow hierarchy with general superclass categories and specific subclass types, much like the prior section's exceptions class tree.

In Python 3.X, all the familiar exceptions you've seen (e.g., SyntaxError) are really just predefined classes, available as built-in names in the module named `builtins`; in Python 2.X, they instead live in \_\_builtin\_\_ and are also attributes of the standard library module exceptions. In addition, Python organizes the built-in exceptions into a hierarchy, to support a variety of catching modes. For example:
- **BaseException:** *topmost root, printing and constructor defaults*
  The top-level root superclass of exceptions. This class is not supposed to be directly inherited by user-defined classes (use Exception instead). It provides default printing and state retention behavior inherited by subclasses. If the str built-in is called on an instance of this class (e.g., by print), the class returns the display strings of the constructor arguments passed when the instance was created (or an empty string if there were no arguments). In addition, unless subclasses replace this class's constructor, all of the arguments passed to this class at instance construction time are stored in its args attribute as a tuple.
- **Exception:** *root of user-defined exceptions*
  The top-level root superclass of application-related exceptions. This is an immediate subclass of BaseException and is a superclass to every other built-in exception, except the system exit event classes (SystemExit, KeyboardInterrupt, and GeneratorExit). Nearly all user-defined classes should inherit from this class, not BaseException. When this convention is followed, naming Exception in a try statement's handler ensures that your program will catch everything but system exit events, which should normally be allowed to pass. In effect, Exception becomes a catchall in try statements and is more accurate than an empty except.
- **ArithmeticError:** *root of numeric errors*
  A subclass of Exception, and the superclass of all numeric errors. Its subclasses identify specific numeric errors: OverflowError, ZeroDivisionError, and FloatingPointError.
- **LookupError:** *root of indexing errors*
  A subclass of Exception, and the superclass category for indexing errors for both sequences and mappings -- IndexError and KeyError -- as well as some Unicode lookup errors.

And so on -- because the built-in exception set is prone to frequent changes, this book doesn't document it exhaustively. You can read further about this structure in reference texts such as Python Pocket Reference or the Python library manual. In fact, the exceptions class tree differs slightly between Python 3.X and 2.X in ways we'll omit here, because they are not relevant to examples.

You can also see the built-in exceptions class tree in the help text of the exceptions module in Python 2.X only (see Chapter 4 and Chapter 15 for help on help):
> ```python
> >>> import exceptions
> >>> help(exceptions)
> ...lots of text omitted...
> ```

This module is removed in 3.X, where you'll find up-to-date help in the other resources mentioned.

## Built-in Exception Categories
The built-in class tree allows you to choose how specific or general your handlers will be. For example, because the built-in exception ArithmeticError is a superclass for more specific exceptions such as OverflowError and ZeroDivisionError:
- By listing ArithmeticError in a try, you will catch any kind of numeric error raised.
- By listing ZeroDivisionError, you will intercept just that specific type of error, and no others.

Similarly, because Exception is the superclass of all application-level exceptions in Python 3.X, you can generally use it as a catchall -- the effect is much like an empty except, but it allows system exit exceptions to pass and propagate as they usually should:
> ```python
> try:
>     action()
> except Exception: 						# Exits not caught here
>     ...handle all application exceptions...
> else:
>     ...handle no-exception case...
> ```

This doesn't quite work universally in Python 2.X, however, because standalone userdefined exceptions coded as classic classes are not required to be subclasses of the Exception root class. This technique is more reliable in Python 3.X, since it requires all classes to derive from built-in exceptions. Even in Python 3.X, though, this scheme suffers most of the same potential pitfalls as the empty except, as described in the prior chapter -- it might intercept exceptions intended for elsewhere, and it might mask genuine programming errors. Since this is such a common issue, we'll revisit it as a "gotcha" in the next chapter.

Whether or not you will leverage the categories in the built-in class tree, it serves as a good example; by using similar techniques for class exceptions in your own code, you can provide exception sets that are flexible and easily modified.

> **Version Skew:** Python 3.3 reworks the built-in IO and OS exception hierarchies. It adds new specific exception classes corresponding to common file and system error numbers, and groups these and others related to operating system calls under the OSError category superclass. Former exception names are retained for backward compatibility.
> 
> Prior to this, programs inspect the data attached to the exception instance to see what specific error occurred, and possibly reraise others to be propagated (the errno module has names preset to the error codes for convenience, and the error number is available in both the generic tuple as V.args[0] and attribute V.errno):
> > ```powershell
> > c:\temp> py -3.2
> > >>> try:
> > ...     f = open('nonesuch.txt')
> > ... except IOError as V:
> > ...     if V.errno == 2: 				# Or errno.N, V.args[0]
> > ...     print('No such file')
> > ... else:
> > ...     raise 							# Propagate others
> > ...
> > No such file
> > ```
> 
> This code still works in 3.3, but with the new classes, programs in 3.3 and later can be more specific about the exceptions they mean to process, and ignore others:
> > ```powershell
> > c:\temp> py −3.3
> > >>> try:
> > ...     f = open('nonesuch.txt')
> > ... except FileNotFoundError:
> > ...     print('No such file')
> > ...
> > No such file
> > ```
> 
> For full details on this extension and its classes, see the other resources listed earlier.
>

## Default Printing and State
Built-in exceptions also provide default print displays and state retention, which is often as much logic as user-defined classes require. Unless you redefine the constructors your classes inherit from them, any constructor arguments you pass to these classes are automatically saved in the instance's args tuple attribute, and are automatically displayed when the instance is printed. An empty tuple and display string are used if no constructor arguments are passed, and a single argument displays as itself (not as a tuple).

This explains why arguments passed to built-in exception classes show up in error messages -- any constructor arguments are attached to the instance and displayed when the instance is printed:
> ```python
> >>> raise IndexError 					# Same as IndexError(): no arguments
> Traceback (most recent call last):
> File "<stdin>", line 1, in <module>
> IndexError
> >>> raise IndexError('spam') 			# Constructor argument attached, printed
> Traceback (most recent call last):
> File "<stdin>", line 1, in <module>
> IndexError: spam
> >>> I = IndexError('spam') 			# Available in object attribute
> >>> I.args
> ('spam',)
> >>> print(I) 							# Displays args when printed manually
> spam
> ```

The same holds true for user-defined exceptions in Python 3.X (and for new-style classes in 2.X), because they inherit the constructor and display methods present in their builtin superclasses:
> ```python
> >>> class E(Exception): pass
> ...
> >>> raise E
> Traceback (most recent call last):
> File "<stdin>", line 1, in <module>
> __main__.E
> >>> raise E('spam')
> Traceback (most recent call last):
> File "<stdin>", line 1, in <module>
> __main__.E: spam
> >>> I = E('spam')
> >>> I.args
> ('spam',)
> >>> print(I)
> spam
> ```

When intercepted in a try statement, the exception instance object gives access to both the original constructor arguments and the display method:
> ```python
> >>> try:
> ...     raise E('spam')
> ... except E as X:
> ...     print(X) 					# Displays and saves constructor arguments
> ...     print(X.args)
> ...     print(repr(X))
> ...
> spam
> ('spam',)
> E('spam',)
> >>> try: 							# Multiple arguments save/display a tuple
> ...     raise E('spam', 'eggs', 'ham')
> ... except E as X:
> ...     print('%s %s' % (X, X.args))
> ...
> ('spam', 'eggs', 'ham') ('spam', 'eggs', 'ham')
> ```

Note that exception instance objects are not strings themselves, but use the \_\_str\_\_ operator overloading protocol we studied in Chapter 30 to provide display strings when printed; to concatenate with real strings, perform manual conversions: str(X) + 'astr', '%s' % X, and the like.

Although this automatic state and display support is useful by itself, for more specific display and state retention needs you can always redefine inherited methods such as \_\_str\_\_ and \_\_init\_\_ in Exception subclasses -- as the next section shows.
