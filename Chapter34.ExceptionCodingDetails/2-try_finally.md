# The try/finally Statement
The other flavor of the try statement is a specialization that has to do with finalization (a.k.a. termination) actions. If a finally clause is included in a try, Python will always run its block of statements "on the way out" of the try statement, whether an exception occurred while the try block was running or not. Its general form is:
> ```python
> try:
>     statements 			# Run this action first
> finally:
>     statements 			# Always run this code on the way out
> ```

With this variant, Python begins by running the statement block associated with the try header line as usual. What happens next depends on whether an exception occurs during the try block:
- If an exception does not occur while the try block is running, Python continues on to run the finally block, and then continues execution past the try statement.
- If an exception does occur during the try block's run, Python still comes back and runs the finally block, but it then propagates the exception up to a previously entered try or the top-level default handler; the program does not resume execution below the finally clause's try statement. That is, the finally block is run even if an exception is raised, but unlike an except, the finally does not terminate the exception -- it continues being raised after the finally block runs.

The try/finally form is useful when you want to be completely sure that an action will happen after some code runs, regardless of the exception behavior of the program. In practice, it allows you to specify cleanup actions that always must occur, such as file closes and server disconnects where required.

> **Note:**
As we'll also see later in this chapter, as of Python 2.6 and 3.0, the new with statement and its context managers provide an object-based way to do similar work for exit actions. Unlike finally, this new statement also supports entry actions, but it is limited in scope to objects that implement the context manager protocol it leverages.

## Example: Coding Termination Actions with try/finally
We saw some simple try/finally examples in the prior chapter. Here's a more realistic example that illustrates a typical role for this statement:
> ```python
> class MyError(Exception): pass
> 
> def stuff(file):
>     raise MyError()
>     file = open('data', 'w') 			# Open an output file (this can fail too)
>     try:
>         stuff(file) 					# Raises exception
>     finally:
>         file.close() 					# Always close file to flush output buffers
> print('not reached') 					# Continue here only if no exception
> ```

When the function in this code raises its exception, the control flow jumps back and runs the finally block to close the file. The exception is then propagated on to either another try or the default top-level handler, which prints the standard error message and shuts down the program. Hence, the statement after this try is never reached. If the function here did not raise an exception, the program would still execute the finally block to close the file, but it would then continue below the entire try statement.

In this specific case, we've wrapped a call to a file-processing function in a try with a finally clause to make sure that the file is always closed, and thus finalized, whether the function triggers an exception or not. This way, later code can be sure that the file's output buffer's content has been flushed from memory to disk. A similar code structure can guarantee that server connections are closed, and so on.

As we learned in Chapter 9, file objects are automatically closed on garbage collection in standard Python (CPython); this is especially useful for temporary files that we don't assign to variables. However, it's not always easy to predict when garbage collection will occur, especially in larger programs or alternative Python implementations with differing garbage collection policies (e.g., Jython, PyPy). The try statement makes file closes more explicit and predictable and pertains to a specific block of code. It ensures that the file will be closed on block exit, regardless of whether an exception occurs or not.

This particular example's function isn't all that useful (it just raises an exception), but wrapping calls in try/finally statements is a good way to ensure that your closing-time termination activities always run. Again, Python always runs the code in your finally blocks, regardless of whether an exception happens in the try block.

Notice how the user-defined exception here is again defined with a class -- as we'll see more formally in the next chapter, exceptions today must all be class instances in 2.6, 3.0, and later releases in both lines.



