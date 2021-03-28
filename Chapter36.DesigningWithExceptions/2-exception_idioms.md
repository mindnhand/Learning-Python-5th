# Exception Idioms
We've seen the mechanics behind exceptions. Now let's take a look at some of the other ways they are typically used.

## Breaking Out of Multiple Nested Loops: "go to"
As mentioned at the start of this part of the book, exceptions can often be used to serve the same roles as other languages' "go to" statements to implement more arbitrary control transfers. Exceptions, however, provide a more structured option that localizes the jump to a specific block of nested code.

In this role, raise is like "go to," and except clauses and exception names take the place of program labels. You can jump only out of code wrapped in a try this way, but that's a crucial feature -- truly arbitrary "go to" statements can make code extraordinarily difficult to understand and maintain.

For example, Python's break statement exits just the single closest enclosing loop, but we can always use exceptions to break out of more than one loop level if needed:
> ```python
> >>> class Exitloop(Exception): pass
> ...
> >>> try:
> ...     while True:
> ...         while True:
> ...             for i in range(10):
> ...                 if i > 3: raise Exitloop 			# break exits just one level
> ...                 print('loop3: %s' % i)
> ...             print('loop2')
> ...         print('loop1')
> ... except Exitloop:
> ...     print('continuing') 							# Or just pass, to move on
> ...
> loop3: 0
> loop3: 1
> loop3: 2
> loop3: 3
> continuing
> >>> i
> 4
> ```

If you change the raise in this to break, you'll get an infinite loop, because you'll break only out of the most deeply nested for loop, and wind up in the second-level loop nesting. The code would then print "loop2" and start the for again.

Also notice that variable i is still what it was after the try statement exits. Variable assignments made in a try are not undone in general, though as we've seen, exception instance variables listed in except clause headers are localized to that clause, and the local variables of any functions that are exited as a result of a raise are discarded. Technically, active functions' local variables are popped off the call stack and the objects they reference may be garbage-collected as a result, but this is an automatic step.

## Exceptions Aren't Always Errors
In Python, all errors are exceptions, but not all exceptions are errors. For instance, we saw in Chapter 9 that file object read methods return an empty string at the end of a file. In contrast, the built-in input function -- which we first met in Chapter 3, deployed in an interactive loop in Chapter 10, and learned is named raw_input in 2.X -- reads a line of text from the standard input stream, sys.stdin, at each call and raises the builtin EOFError at end-of-file.

Unlike file methods, this function does not return an empty string -- an empty string from input means an empty line. Despite its name, though, the EOFError exception is just a signal in this context, not an error. Because of this behavior, unless the end-offile should terminate a script, input often appears wrapped in a try handler and nested in a loop, as in the following code:
> ```python
> while True:
>     try:
>         line = input() 				# Read line from stdin (raw_input in 2.X)
>     except EOFError:
>         break 						# Exit loop at end-of-file
>     else:
>         ...process next line here...
> ```

Several other built-in exceptions are similarly signals, not errors -- for example, calling sys.exit() and pressing Ctrl-C on your keyboard raise SystemExit and KeyboardInterrupt, respectively.

Python also has a set of built-in exceptions that represent warnings rather than errors; some of these are used to signal use of deprecated (phased out) language features. See the standard library manual's description of built-in exceptions for more information, and consult the warnings module's documentation for more on exceptions raised as warnings.

## Functions Can Signal Conditions with raise
User-defined exceptions can also signal nonerror conditions. For instance, a search routine can be coded to raise an exception when a match is found instead of returning a status flag for the caller to interpret. In the following, the try/except/else exception handler does the work of an if/else return-value tester:
> ```python
> class Found(Exception): pass
> def searcher():
>     if ...success...:
>         raise Found() 				# Raise exceptions instead of returning flags
>     else:
>         return
> 
> try:
>     searcher()
> except Found: 						# Exception if item was found
>     ...success...
> else: 								# else returned: not found
>     ...failure...
> ```

More generally, such a coding structure may also be useful for any function that cannot return a sentinel value to designate success or failure. In a widely applicable function, for instance, if all objects are potentially valid return values, it's impossible for any return value to signal a failure condition. Exceptions provide a way to signal results without a return value:
> ```python
> class Failure(Exception): pass
> def searcher():
>     if ...success...:
>         return ...founditem...
>     else:
>         raise Failure()
> 
> try:
>     item = searcher()
> except Failure:
>     ...not found...
> else:
>     ...use item here...
> ```

Because Python is dynamically typed and polymorphic to the core, exceptions, rather than sentinel return values, are the generally preferred way to signal such conditions.

## Closing Files and Server Connections
We encountered examples in this category in Chapter 34. As a summary, though, exception processing tools are also commonly used to ensure that system resources are finalized, regardless of whether an error occurs during processing or not.

For example, some servers require connections to be closed in order to terminate a session. Similarly, output files may require close calls to flush their buffers to disk for waiting consumers, and input files may consume file descriptors if not closed; although file objects are automatically closed when garbage-collected if still open, in some Pythons it may be difficult to be sure when that will occur.

As we saw in Chapter 34, the most general and explicit way to guarantee termination actions for a specific block of code is the try/finally statement:
> ```python
> myfile = open(r'C:\code\textdata', 'w')
> try:
>     ...process myfile...
> finally:
>     myfile.close()
> ```

As we also saw, some objects make this potentially easier in Python 2.6, 3.0, and later by providing context managers that terminate or close the objects for us automatically when run by the with/as statement:
> ```python
> with open(r'C:\code\textdata', 'w') as myfile:
>     ...process myfile...
> ```

So which option is better here? As usual, it depends on your programs. Compared to the traditional try/finally, context managers are more implicit, which runs contrary to Python's general design philosophy. Context managers are also arguably less general -- they are available only for select objects, and writing user-defined context managers to handle general termination requirements is more complex than coding a try/finally.

On the other hand, using existing context managers requires less code than using try/finally, as shown by the preceding examples. Moreover, the context manager protocol supports entry actions in addition to exit actions. In fact, it can save a line of code when no exceptions are expected at all (albeit at the expense of further nesting and indenting file processing logic):
> ```python
> myfile = open(filename, 'w') 				# Traditional form
> ...process myfile...
> myfile.close()
> 
> with open(filename) as myfile: 			# Context manager form
>     ...process myfile...
> ```

Still, the implicit exception processing of with makes it more directly comparable to the explicit exception handling of try/finally. Although try/finally is the more widely applicable technique, context managers may be preferable where they are already available, or where their extra complexity is warranted.

## Debugging with Outer try Statements
You can also make use of exception handlers to replace Python's default top-level exception-handling behavior. By wrapping an entire program (or a call to it) in an outer try in your top-level code, you can catch any exception that may occur while your program runs, thereby subverting the default program termination.

In the following, the empty except clause catches any uncaught exception raised while the program runs. To get hold of the actual exception that occurred in this mode, fetch the `sys.exc_info` function call result from the built-in sys module; it returns a tuple whose first two items contain the current exception's class and the instance object raised (more on `sys.exc_info` in a moment):
> ```python
> try:
>     ...run program...
> except: 					# All uncaught exceptions come here
>     import sys
>     print('uncaught!', sys.exc_info()[0], sys.exc_info()[1])
> ```

This structure is commonly used during development, to keep programs active even after errors occur -- within a loop, it allows you to run additional tests without having to restart. It’s also used when testing other program code, as described in the next section.

> **On a related note:** for more about handling program shutdowns without recovery from them, see also Python's `atexit` standard library module. It's also possible to customize what the top-level exception handler does with `sys.excepthook`. These and other related tools are described in Python's library manual.

## Running In-Process Tests
Some of the coding patterns we've just looked at can be combined in a test-driver application that tests other code within the same process. The following partial code sketches the general model:
> ```
> import sys
> log = open('testlog', 'a')
> from testapi import moreTests, runNextTest, testName
> def testdriver():
>     while moreTests():
>         try:
>             runNextTest()
>         except:
>             print('FAILED', testName(), sys.exc_info()[:2], file=log)
>         else:
>             print('PASSED', testName(), file=log)
> 
> testdriver()
> ```

The testdriver function here cycles through a series of test calls (the module testapi is left abstract in this example). Because an uncaught exception in a test case would normally kill this test driver, you need to wrap test case calls in a try if you want to continue the testing process after a test fails. The empty except catches any uncaught exception generated by a test case as usual, and it uses `sys.exc_info` to log the exception to a file. The else clause is run when no exception occurs -- the test success case.

Such boilerplate code is typical of systems that test functions, modules, and classes by running them in the same process as the test driver. In practice, however, testing can be much more sophisticated than this. For instance, to test external programs, you could instead check status codes or outputs generated by program-launching tools such as `os.system` and `os.popen`, used earlier in this book and covered in the standard library manual. Such tools do not generally raise exceptions for errors in the external programs -- in fact, the test cases may run in parallel with the test driver.

At the end of this chapter, we'll also briefly meet more complete testing frameworks provided by Python, such as `doctest` and `PyUnit`, which provide tools for comparing expected outputs with actual results.

## More on `sys.exc_info`
The `sys.exc_info` result used in the last two sections allows an exception handler to gain access to the most recently raised exception generically. This is especially useful when using the empty except clause to catch everything blindly, to determine what was raised:
> ```python
> try:
>     ...
> except:
>     # sys.exc_info()[0:2] are the exception class and instance
> ```

If no exception is being handled, this call returns a tuple containing three None values. Otherwise, the values returned are (type, value, traceback), where:
- type is the exception class of the exception being handled.
- value is the exception class instance that was raised.
- traceback is a traceback object that represents the call stack at the point where the exception originally occurred, and used by the traceback module to generate error messages.

As we saw in the prior chapter, `sys.exc_info` can also sometimes be useful to determine the specific exception type when catching exception category superclasses. As we've also learned, though, because in this case you can also get the exception type by fetching the \_\_class\_\_ attribute of the instance obtained with the as clause, `sys.exc_info` is often redundant apart from the empty except:
> ```python
> try:
>     ...
> except General as instance:
>     # instance.__class__ is the exception class
> ```

As we've seen, using Exception for the General exception name here would catch all nonexit exceptions, similar to an empty except but less extreme, and still giving access to the exception instance and its class. Even so, using the instance object's interfaces and polymorphism is often a better approach than testing exception types -- exception methods can be defined per class and run generically:
> ```python
> try:
>     ...
> except General as instance:
>     # instance.method() does the right thing for this instance
> ```

As usual, being too specific in Python can limit your code's flexibility. A polymorphic approach like the last example here generally supports future evolution better than explicitly type-specific tests or actions.

## Displaying Errors and Tracebacks
Finally, the exception traceback object available in the prior section's `sys.exc_info` result is also used by the standard library's traceback module to generate the standard error message and stack display manually. This file has a handful of interfaces that support wide customization, which we don't have space to cover usefully here, but the basics are simple. Consider the following aptly named file, badly.py:
> ```python
> import traceback
> def inverse(x):
>     return 1 / x
> 
> try:
>     inverse(0)
> except Exception:
>     traceback.print_exc(file=open('badly.exc', 'w'))
> print('Bye')
> ```

This code uses the `print_exc` convenience function in the `traceback` module, which uses `sys.exc_info` data by default; when run, the script prints the error message to a file -- handy in testing programs that need to catch errors but still record them in full:
> ```powershell
> c:\code> python badly.py
> Bye
> c:\code> type badly.exc
> Traceback (most recent call last):
> File "badly.py", line 7, in <module>
> inverse(0)
> File "badly.py", line 4, in inverse
> return 1 / x
> ZeroDivisionError: division by zero
> ```

For much more on traceback objects, the traceback module that uses them, and related topics, consult other reference resources and manuals.

> **Version skew note:** In Python 2.X, the older tools sys.exc_type and sys.exc_value still work to fetch the most recent exception type and value, but they can manage only a single, global exception for the entire process. These two names have been removed in Python 3.X. The newer and preferred `sys.exc_info()` call available in both 2.X and 3.X instead keeps track of each thread's exception information, and so is threadspecific. Of course, this distinction matters only when using multiple threads in Python programs (a subject beyond this book's scope), but 3.X forces the issue. See other resources for more details.

