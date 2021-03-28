# Exception Design Tips and Gotchas
I'm lumping design tips and gotchas together in this chapter, because it turns out that the most common gotchas largely stem from design issues. By and large, exceptions are easy to use in Python. The real art behind them is in deciding how specific or general your except clauses should be and how much code to wrap up in try statements. Let's address the second of these concerns first.

## What Should Be Wrapped
In principle, you could wrap every statement in your script in its own try, but that would just be silly (the try statements would then need to be wrapped in try statements!). What to wrap is really a design issue that goes beyond the language itself, and it will become more apparent with use. But for now, here are a few rules of thumb:
- Operations that commonly fail should generally be wrapped in try statements. For example, operations that interface with system state (file opens, socket calls, and the like) are prime candidates for try.
- However, there are exceptions to the prior rule -- in a simple script, you may want failures of such operations to kill your program instead of being caught and ignored. This is especially true if the failure is a showstopper. Failures in Python typically result in useful error messages (not hard crashes), and this is the best outcome some programs could hope for.
- You should implement termination actions in try/finally statements to guarantee their execution, unless a context manager is available as a with/as option. The try/finally statement form allows you to run code whether exceptions occur or not in arbitrary scenarios.
- It is sometimes more convenient to wrap the call to a large function in a single try statement, rather than littering the function itself with many try statements. That way, all exceptions in the function percolate up to the try around the call,
and you reduce the amount of code within the function.

The types of programs you write will probably influence the amount of exception handling you code as well. Servers, for instance, must generally keep running persistently and so will likely require try statements to catch and recover from exceptions. Inprocess testing programs of the kind we saw in this chapter will probably handle exceptions as well. Simpler one-shot scripts, though, will often ignore exception handling completely because failure at any step requires script shutdown.

## Catching Too Much: Avoid Empty except and Exception
As mentioned, exception handler generality is a key design choice. Python lets you pick and choose which exceptions to catch, but you sometimes have to be careful to not be too inclusive. For example, you've seen that an empty except clause catches every exception that might be raised while the code in the try block runs.

That's easy to code, and sometimes desirable, but you may also wind up intercepting an error that's expected by a try handler higher up in the exception nesting structure. For example, an exception handler such as the following catches and stops every exception that reaches it, regardless of whether another handler is waiting for it:
> ```python
> def func():
>     try:
>         ... 				# IndexError is raised in here
>     except:
>         ... 				# But everything comes here and dies!
> 
> try:
>     func()
> except IndexError: 		# Exception should be processed here
>     ...
> ```

Perhaps worse, such code might also catch unrelated system exceptions. Even things like memory errors, genuine programming mistakes, iteration stops, keyboard interrupts, and system exits raise exceptions in Python. Unless you're writing a debugger or similar tool, such exceptions should not usually be intercepted in your code.

For example, scripts normally exit when control falls off the end of the top-level file. However, Python also provides a built-in `sys.exit(statuscode)` call to allow early terminations. This actually works by raising a built-in SystemExit exception to end the program, so that try/finally handlers run on the way out and special types of programs can intercept the event. Because of this, a try with an empty except might unknowingly prevent a crucial exit, as in the following file (exiter.py):
>
> > ```python
> > import sys
> > def bye():
> >     sys.exit(40) 				# Crucial error: abort now!
> > 
> > try:
> >     bye()
> > except:
> >     print('got it') 			# Oops--we ignored the exit
> > 
> > print('continuing...')
> > ```
> 
> > ```powershell
> > % python exiter.py
> > got it
> > continuing...
> > ```
> 

You simply might not expect all the kinds of exceptions that could occur during an operation. Using the built-in exception classes of the prior chapter can help in this particular case, because the Exception superclass is not a superclass of SystemExit:
> ```python
> try:
>     bye()
> except Exception: 			# Won't catch exits, but _will_ catch many others
>     ...
> ```

In other cases, though, this scheme is no better than an empty except clause -- because Exception is a superclass above all built-in exceptions except system-exit events, it still has the potential to catch exceptions meant for elsewhere in the program.

Probably worst of all, both using an empty except and catching the Exception superclass will also catch genuine programming errors, which should be allowed to pass most of the time. In fact, these two techniques can effectively turn off Python's error-reporting machinery, making it difficult to notice mistakes in your code. Consider this code, for example:
> ```python
> mydictionary = {...}
> ...
> try:
>     x = myditctionary['spam'] 			# Oops: misspelled
> except:
>     x = None 								# Assume we got KeyError
> ...continue here with x...
> ```

The coder here assumes that the only sort of error that can happen when indexing a dictionary is a missing key error. But because the name myditctionary is misspelled (it should say mydictionary), Python raises a NameError instead for the undefined name reference, which the handler will silently catch and ignore. The event handler will incorrectly fill in a None default for the dictionary access, masking the program error.

Moreover, catching Exception here will not help -- it would have the exact same effect as an empty except, happily and silently filling in a default and masking a genuine program error you will probably want to know about. If this happens in code that is far removed from the place where the fetched values are used, it might make for a very interesting debugging task!

As a rule of thumb, be as specific in your handlers as you can be -- empty except clauses and Exception catchers are handy, but potentially error-prone. In the last example, for instance, you would be better off saying except KeyError: to make your intentions explicit and avoid intercepting unrelated events. In simpler scripts, the potential for problems might not be significant enough to outweigh the convenience of a catchall, but in general, general handlers are generally trouble.

## Catching Too Little: Use Class-Based Categories
On the other hand, neither should handlers be too specific. When you list specific exceptions in a try, you catch only what you actually list. This isn't necessarily a bad thing, but if a system evolves to raise other exceptions in the future, you may need to go back and add them to exception lists elsewhere in your code.

We saw this phenomenon at work in the prior chapter. For instance, the following handler is written to treat MyExcept1 and MyExcept2 as normal cases and everything else as an error. If you add a MyExcept3 in the future, though, it will be processed as an error unless you update the exception list:
> ```python
> try:
>     ...
> except (MyExcept1, MyExcept2): 				# Breaks if you add a MyExcept3 later
>     ... 										# Nonerrors
> else:
>     ... 										# Assumed to be an error
> ```

Luckily, careful use of the class-based exceptions we discussed in Chapter 34 can make this code maintenance trap go away completely. As we saw, if you catch a general superclass, you can add and raise more specific subclasses in the future without having to extend except clause lists manually -- the superclass becomes an extendible exceptions category:
> ```python
> try:
>     ...
> except SuccessCategoryName: 					# OK if you add a MyExcept3 subclass later
>     ... 										# Nonerrors
> else:
>     ... 										# Assumed to be an error
> ```

In other words, a little design goes a long way. The moral of the story is to be careful to be neither too general nor too specific in exception handlers, and to pick the granularity of your try statement wrappings wisely. Especially in larger systems, exception policies should be a part of the overall design.

