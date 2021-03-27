# Unified try/except/finally
In all versions of Python prior to release 2.5 (for its first 15 years of life, more or less), the try statement came in two flavors and was really two separate statements -- we could either use a finally to ensure that cleanup code was always run, or write except blocks to catch and recover from specific exceptions and optionally specify an else clause to be run if no exceptions occurred.

That is, the finally clause could not be mixed with except and else. This was partly because of implementation issues, and partly because the meaning of mixing the two seemed obscure -- catching and recovering from exceptions seemed a disjoint concept from performing cleanup actions.

In Python 2.5 and later, though, the two statements have merged. Today, we can mix finally, except, and else clauses in the same statement -- in part because of similar utility in the Java language. That is, we can now write a statement of this form:
> ```python
> try: 						# Merged form
>     main-action
> except Exception1:
>     handler1
> except Exception2: 		# Catch exceptions
>     handler2
>     ...
> else: 					# No-exception handler
>     else-block
> finally: 					# The finally encloses all else
>     finally-block
> ```

The code in this statement's main-action block is executed first, as usual. If that code raises an exception, all the except blocks are tested, one after another, looking for a match to the exception raised. If the exception raised is Exception1, the handler1 block is executed; if it's Exception2, handler2 is run, and so on. If no exception is raised, the else-block is executed.

No matter what's happened previously, the finally-block is executed once the main action block is complete and any raised exceptions have been handled. In fact, the code in the finally-block will be run even if there is an error in an exception handler or the else-block and a new exception is raised.

As always, the finally clause does not end the exception -- if an exception is active when the finally-block is executed, it continues to be propagated after the finallyblock runs, and control jumps somewhere else in the program (to another try, or to the default top-level handler). If no exception is active when the finally is run, control resumes after the entire try statement.

The net effect is that the finally is always run, regardless of whether:
- An exception occurred in the main action and was handled.
- An exception occurred in the main action and was not handled.
- No exceptions occurred in the main action.
- A new exception was triggered in one of the handlers.

Again, the finally serves to specify cleanup actions that must always occur on the way out of the try, regardless of what exceptions have been raised or handled.

## Unified try Statement Syntax
When combined like this, the try statement must have either an except or a finally, and the order of its parts must be like this:
> try -> except -> else -> finally
where the else and finally are optional, and there may be zero or more excepts, but there must be at least one except if an else appears. Really, the try statement consists of two parts: excepts with an optional else, and/or the finally.

In fact, it's more accurate to describe the merged statement's syntactic form this way (square brackets mean optional and star means zero-or-more here):
> 
> # Format 1
> > ```python
> > try: 					
> >     statements
> > except [type [as value]]: 		# [type [, value]] in Python 2.X
> >     statements
> > [except [type [as value]]:
> >     statements]*
> > [else:
> >     statements]
> > [finally:
> >     statements]
> > ```
> 
> # Format 2
> > ```python
> > try: 
> >     statements
> > finally:
> >     statements
> > ```
> 

Because of these rules, the else can appear only if there is at least one except, and it's always possible to mix except and finally, regardless of whether an else appears or not. It's also possible to mix finally and else, but only if an except appears too (though the except can omit an exception name to catch everything and run a raise statement, described later, to reraise the current exception). If you violate any of these ordering rules, Python will raise a syntax error exception before your code runs.

## Combining finally and except by Nesting
Prior to Python 2.5, it is actually possible to combine finally and except clauses in a try by syntactically nesting a try/except in the try block of a try/finally statement. We'll explore this technique more fully in Chapter 36, but the basics may help clarify the meaning of a combined try -- the following has the same effect as the new merged form shown at the start of this section:
> ```python
> try: 						# Nested equivalent to merged form
>     try:
>         main-action
>     except Exception1:
>         handler1
>     except Exception2:
>         handler2
>         ...
>     else:
>         no-error
> 
> finally:
>     cleanup
> ```

Again, the finally block is always run on the way out, regardless of what happened in the main action and regardless of any exception handlers run in the nested try (trace through the four cases listed previously to see how this works the same). Since an else always requires an except, this nested form even sports the same mixing constraints of the unified statement form outlined in the preceding section.

However, this nested equivalent seems more obscure to some, and requires more code than the new merged form -- though just one four-character line plus extra indentation. Mixing finally into the same statement makes your code arguably easier to write and read, and is a generally preferred technique today.

## Unified try Example
Here's a demonstration of the merged try statement form at work. The following file, mergedexc.py, codes four common scenarios, with print statements that describe the meaning of each:
> # File mergedexc.py (Python 3.X + 2.X)
> sep = '-' * 45 + '\n'
> 
> print(sep + 'EXCEPTION RAISED AND CAUGHT')
> try:
>     x = 'spam'[99]
> except IndexError:
>     print('except run')
> finally:
>     print('finally run')
> 
> print('after run')
> 
> 
> print(sep + 'NO EXCEPTION RAISED')
> try:
>     x = 'spam'[3]
> except IndexError:
>     print('except run')
> finally:
>     print('finally run')
> 
> print('after run')
> 
> 
> print(sep + 'NO EXCEPTION RAISED, WITH ELSE')
> try:
>     x = 'spam'[3]
> except IndexError:
>     print('except run')
> else:
>     print('else run')
> finally:
>     print('finally run')
> 
> print('after run')
> 
> 
> print(sep + 'EXCEPTION RAISED BUT NOT CAUGHT')
> try:
>     x = 1 / 0
> except IndexError:
>     print('except run')
> finally:
>     print('finally run')
> 
> print('after run')
> ```

When this code is run, the following output is produced in Python 3.3; in 2.X, its behavior and output are the same because the print calls each print a single item, though the error message text varies slightly. Trace through the code to see how exception handling produces the output of each of the four tests here:
> ```python
> c:\code> py −3 mergedexc.py
> ---------------------------------------------
> EXCEPTION RAISED AND CAUGHT
> except run
> finally run
> after run
> ---------------------------------------------
> NO EXCEPTION RAISED
> finally run
> after run
> ---------------------------------------------
> NO EXCEPTION RAISED, WITH ELSE
> else run
> finally run
> after run
> ---------------------------------------------
> EXCEPTION RAISED BUT NOT CAUGHT
> finally run
> Traceback (most recent call last):
> File "mergedexc.py", line 39, in <module>
> x = 1 / 0
> ZeroDivisionError: division by zero
> ```

This example uses built-in operations in the main action to trigger exceptions (or not), and it relies on the fact that Python always checks for errors as code is running. The next section shows how to raise exceptions manually instead.


