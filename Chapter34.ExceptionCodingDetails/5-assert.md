# The assert Statement
As a somewhat special case for debugging purposes, Python includes the assert statement. It is mostly just syntactic shorthand for a common raise usage pattern, and an assert can be thought of as a conditional raise statement. A statement of the form:
> 
> > ```python
> > assert test, data 				# The data part is optional
> > ```
> 
> works like the following code:
> > ```python
> > if __debug__:
> >     if not test:
> >         raise AssertionError(data)
> > ```
> 

In other words, if the test evaluates to false, Python raises an exception: the data item (if it's provided) is used as the exception's constructor argument. Like all exceptions, the AssertionError exception will kill your program if it's not caught with a try, in which case the data item shows up as part of the standard error message.

As an added feature, assert statements may be removed from a compiled program's byte code if the -O Python command-line flag is used, thereby optimizing the program. AssertionError is a built-in exception, and the \_\_debug\_\_ flag is a built-in name that is automatically set to True unless the -O flag is used. Use a command line like `python -O main.py` to run in optimized mode and disable (and hence skip) asserts.

## Example: Trapping Constraints (but Not Errors!)
Assertions are typically used to verify program conditions during development. When displayed, their error message text automatically includes source code line information and the value listed in the assert statement. Consider the file asserter.py:
> ```python
> def f(x):
>     assert x < 0, 'x must be negative'
>     return x ** 2
> ```
> 
> ```powershell
> % python
> >>> import asserter
> >>> asserter.f(1)
> Traceback (most recent call last):
> File "<stdin>", line 1, in <module>
> File ".\asserter.py", line 2, in f
> assert x < 0, 'x must be negative'
> AssertionError: x must be negative
> ```

It's important to keep in mind that assert is mostly intended for trapping user-defined constraints, not for catching genuine programming errors. Because Python traps programming errors itself, there is usually no need to code assert to catch things like outof-bounds indexes, type mismatches, and zero divides:
> ```python
> def reciprocal(x):
>     assert x != 0 			# A generally useless assert!
>     return 1 / x 				# Python checks for zero automatically
> ```

Such assert use cases are usually superfluous -- because Python raises exceptions on errors automatically, you might as well let it do the job for you. As a rule, you don't need to do error checking explicitly in your own code.

Of course, there are exceptions for most rules -- as suggested earlier in the book, if a function has to perform long-running or unrecoverable actions before it reaches the place where an exception will be triggered, you still might want to test for errors. Even in this case, though, be careful not to make your tests overly specific or restrictive, or you will limit your code's utility.

For another example of common assert usage, see the abstract superclass example in Chapter 29; there, we used assert to make calls to undefined methods fail with a message. It's a rare but useful tool.



