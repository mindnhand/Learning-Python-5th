# with/as Context Managers
Python 2.6 and 3.0 introduced a new exception-related statement -- the with, and its optional as clause. This statement is designed to work with context manager objects, which support a new method-based protocol, similar in spirit to the way that iteration tools work with methods of the iteration protocol. This feature is also available as an option in 2.5, but must be enabled there with an import of this form:
> ```python
> from __future__ import with_statement
> ```

In short, the with/as statement is designed to be an alternative to a common try/finally usage idiom; like that statement, with is in large part intended for specifying termination-time or "cleanup" activities that must run regardless of whether an exception occurs during a processing step.

Unlike try/finally, the with statement is based upon an object protocol for specifying actions to be run around a block of code. This makes with less general, qualifies it as redundant in termination roles, and requires coding classes for objects that do not support its protocol. On the other hand, with also handles entry actions, can reduce code size, and allows code contexts to be managed with full OOP.

Python enhances some built-in tools with context managers, such as files that automatically close themselves and thread locks that automatically lock and unlock, but programmers can code context managers of their own with classes, too. Let's take a brief look at the statement and its implicit protocol.

## Basic Usage
The basic format of the with statement looks like this, with an optional part in square brackets here:
> ```python
> with expression [as variable]:
>     with-block
> ```

The expression here is assumed to return an object that supports the context management protocol (more on this protocol in a moment). This object may also return a value that will be assigned to the name variable if the optional as clause is present.

Note that the variable is not necessarily assigned the result of the expression; the result of the expression is the object that supports the context protocol, and the variable may be assigned something else intended to be used inside the statement. The object returned by the expression may then run startup code before the with-block is started, as well as termination code after the block is done, regardless of whether the block raised an exception or not.

Some built-in Python objects have been augmented to support the context management protocol, and so can be used with the with statement. For example, file objects (covered in Chapter 9) have a context manager that automatically closes the file after the with block regardless of whether an exception is raised, and regardless of if or when the version of Python running the code may close automatically:
> ```python
> with open(r'C:\misc\data') as myfile:
>     for line in myfile:
>         print(line)
>         ...more code here...
> ```

Here, the call to open returns a simple file object that is assigned to the name myfile. We can use myfile with the usual file tools -- in this case, the file iterator reads line by line in the for loop.

However, this object also supports the context management protocol used by the with statement. After this with statement has run, the context management machinery guarantees that the file object referenced by myfile is automatically closed, even if the for loop raised an exception while processing the file.

Although file objects may be automatically closed on garbage collection, it's not always straightforward to know when that will occur, especially when using alternative Python implementations. The with statement in this role is an alternative that allows us to be sure that the close will occur after execution of a specific block of code.

As we saw earlier, we can achieve a similar effect with the more general and explicit try/finally statement, but it requires three more lines of administrative code in this case (four instead of just one):
> ```python
> myfile = open(r'C:\misc\data')
> try:
>     for line in myfile:
>         print(line)
>         ...more code here...
> finally:
>     myfile.close()
> ```

We won't cover Python's multithreading modules in this book (for more on that topic, see follow-up application-level texts such as Programming Python) but the lock and condition synchronization objects they define may also be used with the with statement, because they support the context management protocol -- in this case adding both entry and exit actions around a block:
> ```python
> lock = threading.Lock() 				# After: import threading
> with lock:
>     # critical section of code
>     ...access shared resources...
> ```

Here, the context management machinery guarantees that the lock is automatically acquired before the block is executed and released once the block is complete, regardless of exception outcomes.

As introduced in Chapter 5, the decimal module also uses context managers to simplify saving and restoring the current decimal context, which specifies the precision and rounding characteristics for calculations:
> ```python
> with decimal.localcontext() as ctx: 			# After: import decimal
>     ctx.prec = 2
>     x = decimal.Decimal('1.00') / decimal.Decimal('3.00')
> ```

After this statement runs, the current thread's context manager state is automatically restored to what it was before the statement began. To do the same with a try/finally, we would need to save the context before and restore it manually after the nested block.

## The Context Management Protocol
Although some built-in types come with context managers, we can also write new ones of our own. To implement context managers, classes use special methods that fall into the operator overloading category to tap into the with statement. The interface expected of objects used in with statements is somewhat complex, and most programmers only need to know how to use existing context managers. For tool builders who might want to write new application-specific context managers, though, let's take a quick look at what's involved.

Here's how the with statement actually works:
1. The expression is evaluated, resulting in an object known as a context manager that must have \_\_enter\_\_ and \_\_exit\_\_ methods.
2. The context manager's \_\_enter\_\_ method is called. The value it returns is assigned to the variable in the as clause if present, or simply discarded otherwise.
3. The code in the nested with block is executed.
4. If the with block raises an exception, the \_\_exit\_\_(type, value, traceback) method is called with the exception details. These are the same three values returned by `sys.exc_info`, described in the Python manuals and later in this part of the book.
  If this method returns a false value, the exception is reraised; otherwise, the exception is terminated. The exception should normally be reraised so that it is propagated outside the with statement.
5. If the with block does not raise an exception, the \_\_exit\_\_ method is still called, but its type, value, and traceback arguments are all passed in as None.

Let's look at a quick demo of the protocol in action. The following, file withas.py, defines a context manager object that traces the entry and exit of the with block in any with statement it is used for:
> ```python
> class TraceBlock:
>     def message(self, arg):
>         print('running ' + arg)
>     def __enter__(self):
>         print('starting with block')
>         return self
>     def __exit__(self, exc_type, exc_value, exc_tb):
>         if exc_type is None:
>             print('exited normally\n')
>         else:
>             print('raise an exception! ' + str(exc_type))
>             return False 						# Propagate
> 
> if __name__ == '__main__':
>     with TraceBlock() as action:
>         action.message('test 1')
>         print('reached')
> 
>     with TraceBlock() as action:
>         action.message('test 2')
>         raise TypeError
>         print('not reached')
> ```

Notice that this class's \_\_exit\_\_ method returns False to propagate the exception; deleting the return statement would have the same effect, as the default None return value of functions is False by definition. Also notice that the \_\_enter\_\_ method returns self as the object to assign to the as variable; in other use cases, this might return a completely different object instead.

When run, the context manager traces the entry and exit of the with statement block with its \_\_enter\_\_ and \_\_exit\_\_ methods. Here's the script in action being run under either Python 3.X or 2.X (as usual, mileage varies slightly in some 2.X displays, and this runs on 2.6, 2.7, and 2.5 if enabled):
> ```powershell
> c:\code> py −3 withas.py
> starting with block
> running test 1
> reached
> exited normally
> starting with block
> running test 2
> raise an exception! <class 'TypeError'>
> Traceback (most recent call last):
> File "withas.py", line 22, in <module>
> raise TypeError
> TypeError
> ```

Context managers can also utilize OOP state information and inheritance, but are somewhat advanced devices for tool builders, so we'll skip additional details here (see Python's standard manuals for the full story -- for example, there's a new `contextlib` standard module that provides additional tools for coding context managers). For simpler purposes, the `try/finally` statement provides sufficient support for terminationtime activities without coding classes.

## Multiple Context Managers in 3.1, 2.7, and Later
Python 3.1 introduced a with extension that eventually appeared in Python 2.7 as well. In these and later Pythons, the with statement may also specify multiple (sometimes referred to as "nested") context managers with new comma syntax. In the following, for example, both files' exit actions are automatically run when the statement block exits, regardless of exception outcomes:
> ```python
> with open('data') as fin, open('res', 'w') as fout:
>     for line in fin:
>         if 'some key' in line:
>             fout.write(line)
> ```

Any number of context manager items may be listed, and multiple items work the same as nested with statements. In Pythons that support this, the following code:
> 
> > ```python
> > with A() as a, B() as b:
> >     ...statements...
> > ```
> 
> is equivalent to the following, which also works in 3.0 and 2.6:
> > ```python
> > with A() as a:
> >     with B() as b:
> >         ...statements...
> > ```
> 

Python 3.1's release notes have additional details, but here's a quick look at the extension in action -- to implement a parallel lines scan of two files, the following uses with to open two files at once and zip together their lines, without having to manually close when finished (assuming manual closes are required):
> ```python
> >>> with open('script1.py') as f1, open('script2.py') as f2:
> ...     for pair in zip(f1, f2):
> ...         print(pair)
> ...
> ('# A first Python script\n', 'import sys\n')
> ('import sys # Load a library module\n', 'print(sys.path)\n')
> ('print(sys.platform)\n', 'x = 2\n')
> ('print(2 ** 32) # Raise 2 to a power\n', 'print(x ** 32)\n')
> ```

You might use this coding structure to do a line-by-line comparison of two text files, for example -- replace the print with an if for a simple file comparison operation, and use enumerate for line numbers:
> ```python
> with open('script1.py') as f1, open('script2.py') as f2:
>     for (linenum, (line1, line2)) in enumerate(zip(f1, f2)):
>         if line1 != line2:
>             print('%s\n%r\n%r' % (linenum, line1, line2))
> ```

Still, the preceding technique isn't all that useful in CPython, because input file objects don't require a buffer flush, and file objects are closed automatically when reclaimed if still open. In CPython, the files would be reclaimed immediately if the parallel scan were coded the following simpler way:
> ```python
> for pair in zip(open('script1.py'), open('script2.py')):       # Same effect, auto close
>     print(pair)
> ```

On the other hand, alternative implementations such as PyPy and Jython may require more direct closure inside loops to avoid taxing system resources, due to differing garbage collectors. Even more usefully, the following automatically closes the output file on statement exit, to ensure that any buffered text is transferred to disk immediately:
> ```python
> >>> with open('script2.py') as fin, open('upper.py', 'w') as fout:
> ...     for line in fin:
> ...         fout.write(line.upper())
> ...
> >>> print(open('upper.py').read())
> IMPORT SYS
> PRINT(SYS.PATH)
> X = 2
> PRINT(X ** 32)
> ```

In both cases, we can instead simply open files in individual statements and close after processing if needed, and in some scripts we probably should -- there's no point in using statements that catch an exception if it means your program is out of business anyhow!
> ```python
> fin = open('script2.py')
> fout = open('upper.py', 'w')
> for line in fin: 					# Same effect as preceding code, auto close
>     fout.write(line.upper())
> ```

However, in cases where programs must continue after exceptions, the with forms also implicitly catch exceptions, and thereby also avoid a try/finally in cases where close is required. The equivalent without with is more explicit, but requires noticeably more code:
> ```python
> fin = open('script2.py')
> fout = open('upper.py', 'w')
> try: 								# Same effect but explicit close on error
>     for line in fin:
>         fout.write(line.upper())
> finally:
>     fin.close()
>     fout.close()
> ```

On the other hand, the try/finally is a single tool that applies to all finalization cases, whereas the with adds a second tool that can be more concise, but applies to only certain objects types, and doubles the required knowledge base of programmers. As usual, you'll have to weigh the tradeoffs for yourself.
