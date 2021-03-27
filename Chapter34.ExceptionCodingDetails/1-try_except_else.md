# The try/except/else Statement
Now that we've seen the basics, it's time for the details. In the following discussion, I'll first present try/except/else and try/finally as separate statements, because in versions of Python prior to 2.5 they serve distinct roles and cannot be combined, and still are at least logically distinct today. Per the preceding note, in Python 2.5 and later except and finally can be mixed in a single try statement; we'll see the implications of that merging after we've explored the two original forms in isolation.

Syntactically, the try is a compound, multipart statement. It starts with a try header line, followed by a block of (usually) indented statements; then one or more except clauses that identify exceptions to be caught and blocks to process them; and an optional else clause and block at the end. You associate the words try, except, and else by indenting them to the same level (i.e., lining them up vertically). For reference, here's the general and most complete format in Python 3.X:
> ```python
> try:
>     statements 			# Run this main action first
> except name1:
>     statements 			# Run if name1 is raised during try block
> except (name2, name3):
>     statements 			# Run if any of these exceptions occur
> except name4 as var:
>     statements 			# Run if name4 is raised, assign instance raised to var
> except:
>     statements 			# Run for all other exceptions raised
> else:
>     statements 			# Run if no exception was raised during try block
> ```

Semantically, the block under the try header in this statement represents the main action of the statement -- the code you're trying to run and wrap in error processing logic. The except clauses define handlers for exceptions raised during the try block, and the else clause (if coded) provides a handler to be run if no exceptions occur. The var entry here has to do with a feature of raise statements and exception classes, which we will discuss in full later in this chapter.

## How try Statements Work
Operationally, here's how try statements are run. When a try statement is entered, Python marks the current program context so it can return to it if an exception occurs.  The statements nested under the try header are run first. What happens next depends on whether exceptions are raised while the try block's statements are running, and whether they match those that the try is watching for:
- If an exception occurs while the try block's statements are running, and the exception matches one that the statement names, Python jumps back to the try and runs the statements under the first except clause that matches the raised exception, after assigning the raised exception object to the variable named after the as keyword in the clause (if present). After the except block runs, control then resumes below the entire try statement (unless the except block itself raises another exception, in which case the process is started anew from this point in the code).
- If an exception occurs while the try block's statements are running, but the exception does not match one that the statement names, the exception is propagated up to the next most recently entered try statement that matches the exception; if no such matching try statement can be found and the search reaches the top level of the process, Python kills the program and prints a default error message.

- If an exception does not occur while the try block's statements are running, Python runs the statements under the else line (if present), and control then resumes below the entire try statement.

In other words, except clauses catch any matching exceptions that happen while the try block is running, and the else clause runs only if no exceptions happen while the try block runs. Exceptions raised are matched to exceptions named in except clauses by superclass relationships we'll explore in the next chapter, and the empty except clause (with no exception name) matches all (or all other) exceptions.

The except clauses are focused exception handlers -- they catch exceptions that occur only within the statements in the associated try block. However, as the try block's statements can call functions coded elsewhere in a program, the source of an exception may be outside the try statement itself.

In fact, a try block might invoke arbitrarily large amounts of program code -- including code that may have try statements of its own, which will be searched first when exceptions occur. That is, try statements can nest at runtime, a topic I'll have more to say about in Chapter 36.

## try Statement Clauses
When you write a try statement, a variety of clauses can appear after the try header. Table 34-1 summarizes all the possible forms -- you must use at least one. We've already met some of these: as you know, except clauses catch exceptions, finally clauses run on the way out, and else clauses run if no exceptions are encountered.

Formally, there may be any number of except clauses, but you can code else only if there is at least one except, and there can be only one else and one finally. Through Python 2.4, the finally clause must appear alone (without else or except); the try/finally is really a different statement. As of Python 2.5, however, a finally can appear in the same statement as except and else (more on the ordering rules later in this chapter when we meet the unified try statement).

Table 34-1. try statement clause forms
|Clause form|Interpretation|
|:-|:-|
|except:|Catch all (or all other) exception types.|
|except name:|Catch a specific exception only.|
|except name as value:|Catch the listed exception and assign its instance.|
|except (name1, name2):|Catch any of the listed exceptions.|
|except (name1, name2) as value:|Catch any listed exception and assign its instance.|
|else:|Run if no exceptions are raised in the try block.|
|finally:|Always perform this block on exit.|
 
Catching any and all exceptions The first and fourth entries in Table 34-1 are new here:
- except clauses that list no exception name (except:) catch all exceptions not previously listed in the try statement.
- except clauses that list a set of exceptions in parentheses (except (e1, e2, e3):) catch any of the listed exceptions.

Because Python looks for a match within a given try by inspecting the except clauses from top to bottom, the parenthesized version has the same effect as listing each exception in its own except clause, but you have to code the statement body associated with each only once. Here's an example of multiple except clauses at work, which demonstrates just how specific your handlers can be:
> ```python
> try:
>     action()
> except NameError:
>     ...
> except IndexError:
>     ...
> except KeyError:
>     ...
> except (AttributeError, TypeError, SyntaxError):
>     ...
> else:
>     ...
> ```

In this example, if an exception is raised while the call to the action function is running, Python returns to the try and searches for the first except that names the exception raised. It inspects the except clauses from top to bottom and left to right, and runs the statements under the first one that matches. If none match, the exception is propagated past this try. Note that the else runs only when no exception occurs in action -- it does not run when an exception without a matching except is raised.

### Catching all: The empty except and Exception
If you really want a general "catchall" clause, an empty except does the trick:
> ```python
> try:
>     action()
> except NameError:
>     ... 					# Handle NameError
> except IndexError:
>     ... 					# Handle IndexError
> except:
>     ... 					# Handle all other exceptions
> else:
>     ... 					# Handle the no-exception case
> ```

The empty except clause is a sort of wildcard feature -- because it catches everything, it allows your handlers to be as general or specific as you like. In some scenarios, this form may be more convenient than listing all possible exceptions in a try. For example, the following catches everything without listing anything:
> ```python
> try:
>     action()
> except:
>     ... 					# Catch all possible exceptions
> ```

Empty excepts also raise some design issues, though. Although convenient, they may catch unexpected system exceptions unrelated to your code, and they may inadvertently intercept exceptions meant for another handler. For example, even system exit calls and Ctrl-C key combinations in Python trigger exceptions, and you usually want these to pass. Even worse, the empty except may also catch genuine programming mistakes for which you probably want to see an error message. We'll revisit this as a gotcha at the end of this part of the book. For now, I'll just say, "use with care."

Python 3.X more strongly supports an alternative that solves one of these problems -- catching an exception named Exception has almost the same effect as an empty except, but ignores exceptions related to system exits:
> ```python
> try:
>     action()
> except Exception:
>     ... 					# Catch all possible exceptions, except exits
> ```

We'll explore how this form works its voodoo formally in the next chapter when we study exception classes. In short, it works because exceptions match if they are a subclass of one named in an except clause, and Exception is a superclass of all the exceptions you should generally catch this way. This form has most of the same convenience of the empty except, without the risk of catching exit events. Though better, it also has some of the same dangers -- especially with regard to masking programming errors.

### The try else Clause
The purpose of the else clause is not always immediately obvious to Python newcomers. Without it, though, there is no direct way to tell (without setting and checking Boolean flags) whether the flow of control has proceeded past a try statement because no exception was raised, or because an exception occurred and was handled. Either way, we wind up after the try:
> ```python
> try:
>     ...run code...
> except IndexError:
>     ...handle exception...
> ```

# Did we get here because the try failed or not?
Much like the way else clauses in loops make the exit cause more apparent, the else clause provides syntax in a try that makes what has happened obvious and unambiguous:
> ```python
> try:
>     ...run code...
> except IndexError:
>     ...handle exception...
> else:
>     ...no exception occurred...
> ```

You can almost emulate an else clause by moving its code into the try block:
> ```python
> try:
>     ...run code...
>     ...no exception occurred...
> except IndexError:
>     ...handle exception...
> ```

This can lead to incorrect exception classifications, though. If the "no exception occurred" action triggers an IndexError, it will register as a failure of the try block and erroneously trigger the exception handler below the try (subtle, but true!). By using an explicit else clause instead, you make the logic more obvious and guarantee that except handlers will run only for real failures in the code you're wrapping in a try, not for failures in the else no-exception case's action.

## Example: Default Behavior
I've mentioned that exceptions not caught by try statements percolate up to the top level of the Python process and run Python's default exception-handling logic (i.e., Python terminates the running program and prints a standard error message). To illustrate, running the following module file, bad.py, generates a divide-by-zero exception:
> ```python
> def gobad(x, y):
>     return x / y
> def gosouth(x):
>     print(gobad(x, 0))
>     gosouth(1)
> ```

Because the program ignores the exception it triggers, Python kills the program and prints a message:
> ```powershell
> % python bad.py
> Traceback (most recent call last):
> File "bad.py", line 7, in <module>
> gosouth(1)
> File "bad.py", line 5, in gosouth
> print(gobad(x, 0))
> File "bad.py", line 2, in gobad
> return x / y
> ZeroDivisionError: division by zero
> ```

I ran this in a shell window with Python 3.X. The message consists of a stack trace ("Traceback") and the name of and details about the exception that was raised. The stack trace lists all lines active when the exception occurred, from oldest to newest. Note that because we're not working at the interactive prompt, in this case the file and line number information is more useful. For example, here we can see that the bad divide happens at the last entry in the trace -- line 2 of the file bad.py, a return statement.

Because Python detects and reports all errors at runtime by raising exceptions, exceptions are intimately bound up with the ideas of error handling and debugging in general. If you've worked through this book's examples, you've undoubtedly seen an exception or two along the way -- even typos usually generate a SyntaxError or other exception when a file is imported or executed (that's when the compiler is run). By default, you get a useful error display like the one just shown, which helps you track down the problem.

Often, this standard error message is all you need to resolve problems in your code. For more heavy-duty debugging jobs, you can catch exceptions with try statements, or use one of the debugging tools that I introduced in Chapter 3 and will summarize again in Chapter 36, such as the pdb standard library module.

## Example: Catching Built-in Exceptions
Python's default exception handling is often exactly what you want -- especially for code in a top-level script file, an error often should terminate your program immediately. For many programs, there is no need to be more specific about errors in your code.

Sometimes, though, you'll want to catch errors and recover from them instead. If you don't want your program terminated when Python raises an exception, simply catch it by wrapping the program logic in a try. This is an important capability for programs such as network servers, which must keep running persistently. For example, the following code, in the file kaboom.py, catches and recovers from the TypeError Python raises immediately when you try to concatenate a list and a string (remember, the + operator expects the same sequence type on both sides):
> ```python
> def kaboom(x, y):
>     print(x + y) 					# Trigger TypeError
>     try:
>         kaboom([0, 1, 2], 'spam')
>     except TypeError: 			# Catch and recover here
>         print('Hello world!')
> 
> print('resuming here')  			# Continue here if exception or not
> ```

When the exception occurs in the function kaboom, control jumps to the try statement's except clause, which prints a message. Since an exception is "dead" after it's been caught like this, the program continues executing below the try rather than being terminated by Python. In effect, the code processes and clears the error, and your script recovers:
> ```powershell
> % python kaboom.py
> Hello world!
> resuming here
> ```

Keep in mind that once you've caught an error, control resumes at the place where you caught it (i.e., after the try); there is no direct way to go back to the place where the exception occurred (here, in the function kaboom). In a sense, this makes exceptions more like simple jumps than function calls -- there is no way to return to the code that triggered the error.


