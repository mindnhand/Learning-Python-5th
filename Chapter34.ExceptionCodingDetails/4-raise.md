# The raise Statement
To trigger exceptions explicitly, you can code raise statements. Their general form is simple -- a raise statement consists of the word raise, optionally followed by the class to be raised or an instance of it:
> ```python
> raise instance 			# Raise instance of class
> raise class 				# Make and raise instance of class: makes an instance
> raise 					# Reraise the most recent exception
> ```

As mentioned earlier, exceptions are always instances of classes in Python 2.6, 3.0, and later. Hence, the first raise form here is the most common -- we provide an instance directly, either created before the raise or within the raise statement itself. If we pass a class instead, Python calls the class with no constructor arguments, to create an instance to be raised; this form is equivalent to adding parentheses after the class reference. The last form reraises the most recently raised exception; it's commonly used in exception handlers to propagate exceptions that have been caught.

> **Version skew note:** Python 3.X no longer supports the raise Exc, Args form that is still available in Python 2.X. In 3.X, use the raise Exc(Args) instance-creation call form described in this book instead. The equivalent comma form in 2.X is legacy syntax provided for compatibility with the now-defunct string-based exceptions model, and it's deprecated in 2.X. If used, it is converted to the 3.X call form.
> 
> As in earlier releases, a raise Exc form is also allowed to name a class -- it is converted to raise Exc() in both versions, calling the class constructor with no arguments. Besides its defunct comma syntax, Python 2.X's raise also allowed for either string or class exceptions, but the former is removed in 2.6, deprecated in 2.5, and not covered here except for a brief mention in the next chapter. Use classes for new exceptions today.

## Raising Exceptions
To make this clearer, let's look at some examples. With built-in exceptions, the following two forms are equivalent -- both raise an instance of the exception class named, but the first creates the instance implicitly:
> ```python
> raise IndexError 				# Class (instance created)
> raise IndexError() 			# Instance (created in statement)
> ```

We can also create the instance ahead of time -- because the raise statement accepts any kind of object reference, the following two examples raise IndexError just like the prior two:
> ```python
> exc = IndexError() 				# Create instance ahead of time
> raise exc
> excs = [IndexError, TypeError]
> raise excs[0]
> ```

When an exception is raised, Python sends the raised instance along with the exception. If a try includes an except name as X: clause, the variable X will be assigned the instance provided in the raise:
> ```python
> try:
>     ...
> except IndexError as X: 			# X assigned the raised instance object
>     ...
> ```

The as is optional in a try handler (if it's omitted, the instance is simply not assigned to a name), but including it allows the handler to access both data in the instance and methods in the exception class.

This model works the same for user-defined exceptions we code with classes -- the following, for example, passes to the exception class constructor arguments that become available in the handler through the assigned instance:
> ```python
> class MyExc(Exception): pass
>     ...
> raise MyExc('spam') 				# Exception class with constructor args
>     ...
> try:
>     ...
> except MyExc as X: 				# Instance attributes available in handler
>     print(X.args)
> ```

Because this encroaches on the next chapter's topic, though, I'll defer further details until then.

Regardless of how you name them, exceptions are always identified by class instance objects, and at most one is active at any given time. Once caught by an except clause anywhere in the program, an exception dies (i.e., won't propagate to another try), unless it's reraised by another raise statement or error.

## Scopes and try except Variables
We'll study exception objects in more detail in the next chapter. Now that we've seen the as variable in action, though, we can finally clarify the related version-specific scope issue summarized in Chapter 17. In Python 2.X, the exception reference variable name in an except clause is not localized to the clause itself, and is available after the associated block runs:
> ```powershell
> c:\code> py −2
> >>> try:
> ...     1 / 0
> ... except Exception as X: 					# 2.X does not localize X either way
> ...     print X
> ...
> integer division or modulo by zero
> >>> X
> ZeroDivisionError('integer division or modulo by zero',)
> ```

This is true in 2.X whether we use the 3.X-style as or the earlier comma syntax:
> ```powershell
> >>> try:
> ...     1 / 0
> ... except Exception, X:
> ...     print X
> ...
> integer division or modulo by zero
> >>> X
> ZeroDivisionError('integer division or modulo by zero',)
> ```

By contrast, Python 3.X localizes the exception reference name to the except block -- the variable is not available after the block exits, much like a temporary loop variable in 3.X comprehension expressions (3.X also doesn't accept 2.X's except comma syntax, as noted earlier):
> ```powershell
> c:\code> py −3
> >>> try:
> ...     1 / 0
> ... except Exception, X:
> SyntaxError: invalid syntax
> >>> try:
> ...     1 / 0
> ... except Exception as X: 				# 3.X localizes 'as' names to except block
> ...     print(X)
> ...
> division by zero
> >>> X
> NameError: name 'X' is not defined
> ```

Unlike compression loop variables, though, this variable is removed after the except block exits in 3.X. It does so because it would otherwise retain a reference to the runtime call stack, which would defer garbage collection and thus retain excess memory space. This removal occurs, though, even if you're using the name elsewhere, and is more extreme policy than that used for comprehensions:
> ```python
> >>> X = 99
> >>> try:
> ...     1 / 0
> ... except Exception as X: 				# 3.X localizes _and_ removes on exit!
> ...     print(X)
> ...
> division by zero
> >>> X
> NameError: name 'X' is not defined
> >>> X = 99
> >>> {X for X in 'spam'} 					# 2.X/3.X localizes only: not removed
> {'s', 'a', 'p', 'm'}
> >>> X
> 99
> ```

Because of this, you should generally use unique variable names in your try statement's except clauses, even if they are localized by scope. If you do need to reference the exception instance after the try statement, simply assign it to another name that won't be automatically removed:
> ```python
> >>> try:
> ...     1 / 0
> ... except Exception as X: 				# Python removes this reference
> ...     print(X)
> ...     Saveit = X 						# Assign exc to retain exc if needed
> ...
> division by zero
> >>> X
> NameError: name 'X' is not defined
> >>> Saveit
> ZeroDivisionError('division by zero',)

## Propagating Exceptions with raise
The raise statement is a bit more feature-rich than we've seen thus far. For example, a raise that does not include an exception name or extra data value simply reraises the current exception. This form is typically used if you need to catch and handle an exception but don't want the exception to die in your code:
> ```python
> >>> try:
> ...     raise IndexError('spam') 		# Exceptions remember arguments
> ... except IndexError:
> ...     print('propagating')
> ... raise 							# Reraise most recent exception
> ...
> propagating
> Traceback (most recent call last):
> File "<stdin>", line 2, in <module>
> IndexError: spam
> ```

Running a raise this way reraises the exception and propagates it to a higher handler (or the default handler at the top, which stops the program with a standard error message). Notice how the argument we passed to the exception class shows up in the error messages; you'll learn why this happens in the next chapter.


## Python 3.X Exception Chaining: raise from
Exceptions can sometimes be triggered in response to other exceptions -- both deliberately and by new program errors. To support full disclosure in such cases, Python 3.X (but not 2.X) also allows raise statements to have an optional from clause:
> ```python
> raise newexception from otherexception
> ```

When the from is used in an explicit raise request, the expression following from specifies another exception class or instance to attach to the __cause__ attribute of the new exception being raised. If the raised exception is not caught, Python prints both exceptions as part of the standard error message:
> > ```python
> > >>> try:
> > ...     1 / 0
> > ... except Exception as E:
> > ...     raise TypeError('Bad') from E 				# Explicitly chained exceptions
> > ...
> > Traceback (most recent call last):
> > File "<stdin>", line 2, in <module>
> > ZeroDivisionError: division by zero
> > ```
> 
> The above exception was the direct cause of the following exception:
> 
> > Traceback (most recent call last):
> > File "<stdin>", line 4, in <module>
> > TypeError: Bad
> 

When an exception is raised implicitly by a program error inside an exception handler, a similar procedure is followed automatically: the previous exception is attached to the new exception's __context__ attribute and is again displayed in the standard error message if the exception goes uncaught:
> 
> > ```python
> > >>> try:
> > ...     1 / 0
> > ... except:
> > ...     badname 						# Implicitly chained exceptions
> > ...
> > Traceback (most recent call last):
> > File "<stdin>", line 2, in <module>
> > ZeroDivisionError: division by zero
> 
> During handling of the above exception, another exception occurred:
> > Traceback (most recent call last):
> > File "<stdin>", line 4, in <module>
> > NameError: name 'badname' is not defined
> 

In both cases, because the original exception objects thus attached to new exception objects may themselves have attached causes, the causality chain can be arbitrary long, and is displayed in full in error messages. That is, error messages might give more than two exceptions. The net effect in both explicit and implicit contexts is to allow programmers to know all exceptions involved, when one exception triggers another:
> 
> > ```python
> > >>> try:
> > ...     try:
> > ...         raise IndexError()
> > ...     except Exception as E:
> > ...         raise TypeError() from E
> > ... except Exception as E:
> > ...     raise SyntaxError() from E
> > ...
> > Traceback (most recent call last):
> > File "<stdin>", line 3, in <module>
> > IndexError
> > ```
> 
> The above exception was the direct cause of the following exception:
> > Traceback (most recent call last):
> > File "<stdin>", line 5, in <module>
> > TypeError
> 
> The above exception was the direct cause of the following exception:
> > Traceback (most recent call last):
> > File "<stdin>", line 7, in <module>
> > SyntaxError: None
> 

Code like the following would similarly display three exceptions, though implicitly triggered here:
> ```python
> try:
>     try:
>         1 / 0
>     except:
>         badname
> except:
>     open('nonesuch')
> ```

Like the unified try, chained exceptions are similar to utility in other languages (including Java and C#) though it's not clear which languages were borrowers. In Python, it's a still somewhat obscure extension, so we'll defer to Python's manuals for more details. In fact, Python 3.3 adds a way to stop exceptions from chaining, per the following note.  
> **Note:** Python 3.3 chained exception suppression: raise from None. Python 3.3 introduces a new syntax form—using None as the exception name in the raise from statement:
> > ```python
> > raise newexception from None
> > ```
> This allows the display of the chained exception context described in the preceding section to be disabled. This makes for less cluttered error messages in applications that convert between exception types while processing exception chains.

