# Exception Basics

This part of the book deals with exceptions, which are events that can modify the flow of control through a program. In Python, exceptions are triggered automatically on errors, and they can be triggered and intercepted by your code. They are processed by four statements we'll study in this part, the first of which has two variations (listed separately here) and the last of which was an optional extension until Python 2.6 and 3.0:
- try/except: Catch and recover from exceptions raised by Python, or by you.
- try/finally: Perform cleanup actions, whether exceptions occur or not.
- raise: Trigger an exception manually in your code.
- assert: Conditionally trigger an exception in your code.
- with/as: Implement context managers in Python 2.6, 3.0, and later (optional in 2.5).

This topic was saved until nearly the end of the book because you need to know about classes to code exceptions of your own. With a few exceptions (pun intended), though, you'll find that exception handling is simple in Python because it's integrated into the language itself as another high-level tool.


## Exception Roles
In Python programs, exceptions are typically used for a variety of purposes. Here are some of their most common roles:
- Error handling
  Python raises exceptions whenever it detects errors in programs at runtime. You can catch and respond to the errors in your code, or ignore the exceptions that are raised. If an error is ignored, Python's default exception-handling behavior kicks in: it stops the program and prints an error message. If you don't want this default behavior, code a try statement to catch and recover from the exception -- Python will jump to your try handler when the error is detected, and your program will resume execution after the try.
- Event notification
  Exceptions can also be used to signal valid conditions without you having to pass result flags around a program or test them explicitly. For instance, a search routine might raise an exception on failure, rather than returning an integer result code -- and hoping that the code will never be a valid result!
- Special-case handling
  Sometimes a condition may occur so rarely that it’s hard to justify convoluting your code to handle it in multiple places. You can often eliminate special-case code by handling unusual cases in exception handlers in higher levels of your program. An assert can similarly be used to check that conditions are as expected during development.
- Termination actions
  As you'll see, the try/finally statement allows you to guarantee that required closing-time operations will be performed, regardless of the presence or absence of exceptions in your programs. The newer with statement offers an alternative in this department for objects that support it.
- Unusual control flows
  Finally, because exceptions are a sort of high-level and structured "go to," you can use them as the basis for implementing exotic control flows. For instance, although the language does not explicitly support backtracking, you can implement it in Python by using exceptions and a bit of support logic to unwind assignments. There is no "go to" statement in Python (thankfully!), but exceptions can sometimes serve similar roles; a raise, for instance, can be used to jump out of multiple loops.

We saw some of these roles briefly earlier, and will study typical exception use cases in action later in this part of the book. For now, let's get started with a look at Python's exception-processing tools.

In practice, try/except combinations are useful for catching and recovering from exceptions, and try/finally combinations come in handy to guarantee that termination actions will fire regardless of any exceptions that may occur in the try block's code. For instance, you might use try/except to catch errors raised by code that you import from a third-party library, and try/finally to ensure that calls to close files or terminate server connections are always run. We'll see some such practical examples later in this part of the book.

Although they serve conceptually distinct purposes, as of Python 2.5, we can mix except and finally clauses in the same try statement -- the finally is run on the way out regardless of whether an exception was raised, and regardless of whether the exception was caught by an except clause.

As we'll learn in the next chapter, Python 2.X and 3.X both provide an alternative to try/finally when using some types of objects. The with/as statement runs an object's context management logic to guarantee that termination actions occur, irrespective of any exceptions in its nested block:
> ```python
> >>> with open('lumberjack.txt', 'w') as file: 			# Always close file on exit
>         file.write('The larch!\n')
> ```

Although this option requires fewer lines of code, it's applicable only when processing certain object types, so try/finally is a more general termination structure, and is often simpler than coding a class in cases where with is not already supported. On the other hand, with/as may also run startup actions too, and supports user-defined context management code with access to Python's full OOP toolset.
