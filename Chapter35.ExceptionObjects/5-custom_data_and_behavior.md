# Custom Data and Behavior
Besides supporting flexible hierarchies, exception classes also provide storage for extra state information as instance attributes. As we saw earlier, built-in exception superclasses provide a default constructor that automatically saves constructor arguments in an instance tuple attribute named args. Although the default constructor is adequate for many cases, for more custom needs we can provide a constructor of our own. In addition, classes may define methods for use in handlers that provide precoded exception processing logic.

## Providing Exception Details
When an exception is raised, it may cross arbitrary file boundaries -- the raise statement that triggers an exception and the try statement that catches it may be in completely different module files. It is not generally feasible to store extra details in global variables because the try statement might not know which file the globals reside in. Passing extra state information along in the exception itself allows the try statement to access it more reliably.

With classes, this is nearly automatic. As we've seen, when an exception is raised, Python passes the class instance object along with the exception. Code in try statements can access the raised instance by listing an extra variable after the as keyword in an except handler. This provides a natural hook for supplying data and behavior to the handler.

For example, a program that parses data files might signal a formatting error by raising an exception instance that is filled out with extra details about the error:
> ```python
> >>> class FormatError(Exception):
>         def __init__(self, line, file):
>             self.line = line
>             self.file = file
> >>> def parser():
>         raise FormatError(42, file='spam.txt') # When error found
> >>> try:
> ...     parser()
> ... except FormatError as X:
> ...     print('Error at: %s %s' % (X.file, X.line))
> ...
> Error at: spam.txt 42
> ```

In the except clause here, the variable X is assigned a reference to the instance that was generated when the exception was raised. This gives access to the attributes attached to the instance by the custom constructor. Although we could rely on the default state retention of built-in superclasses, it's less relevant to our application (and doesn't support the keyword arguments used in the prior example):
> ```python
> >>> class FormatError(Exception): pass 			# Inherited constructor
> >>> def parser():
>         raise FormatError(42, 'spam.txt') 		# No keywords allowed!
> >>> try:
> ...     parser()
> ... except FormatError as X:
> ...     print('Error at:', X.args[0], X.args[1]) 	# Not specific to this app
> ...
> Error at: 42 spam.txt
> ```

## Providing Exception Methods
Besides enabling application-specific state information, custom constructors also better support extra behavior for exception objects. That is, the exception class can also define methods to be called in the handler. The following code in excparse.py, for example, adds a method that uses exception state information to log errors to a file automatically:
> 
> > ```python
> > from __future__ import print_function 			# 2.X compatibility
> > class FormatError(Exception):
> >     logfile = 'formaterror.txt'
> >     def __init__(self, line, file):
> >         self.line = line
> >         self.file = file
> >     def logerror(self):
> >         log = open(self.logfile, 'a')
> >         print('Error at:', self.file, self.line, file=log)
> > 
> > def parser():
> >     raise FormatError(40, 'spam.txt')
> > 
> > if __name__ == '__main__':
> >     try:
> >         parser()
> >     except FormatError as exc:
> >         exc.logerror()
> > ```
> When run, this script writes its error message to a file in response to method calls in the exception handler:
> > ```powershell
> > c:\code> del formaterror.txt
> > c:\code> py −3 excparse.py
> > c:\code> py −2 excparse.py
> > c:\code> type formaterror.txt
> > Error at: spam.txt 40
> > Error at: spam.txt 40
> > ```
> 
In such a class, methods (like logerror) may also be inherited from superclasses, and instance attributes (like line and file) provide a place to save state information that provides extra context for use in later method calls. Moreover, exception classes are free to customize and extend inherited behavior:
> ```python
> class CustomFormatError(FormatError):
>     def logerror(self):
>         ...something unique here...
> raise CustomFormatError(...)
> ```

In other words, because they are defined with classes, all the benefits of OOP that we studied in Part VI are available for use with exceptions in Python.

Two final notes here: 
- First, the raised instance object assigned to exc in this code is also available generically as the second item in the result tuple of the sys.exc_info() call -- a tool that returns information about the most recently raised exception. This interface must be used if you do not list an exception name in an except clause but still need access to the exception that occurred, or to any of its attached state information or methods. 
- Second, although our class's logerror method appends a custom message to a logfile, it could also generate Python's standard error message with stack trace using tools in the traceback standard library module, which uses traceback objects.

To learn more about sys.exc_info and tracebacks, though, we need to move ahead to the next chapter.
