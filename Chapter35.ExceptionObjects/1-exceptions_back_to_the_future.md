# Exceptions: Back to the Future
Once upon a time (well, prior to Python 2.6 and 3.0), it was possible to define exceptions in two different ways. This complicated try statements, raise statements, and Python in general. Today, there is only one way to do it. This is a good thing: it removes from the language substantial cruft accumulated for the sake of backward compatibility. Because the old way helps explain why exceptions are as they are today, though, and because it's not really possible to completely erase the history of something that has been used by on the order of a million people over the course of nearly two decades, let's begin our exploration of the present with a brief look at the past.

## String Exceptions Are Right Out!
Prior to Python 2.6 and 3.0, it was possible to define exceptions with both class instances and string objects. String-based exceptions began issuing deprecation warnings in 2.5 and were removed in 2.6 and 3.0, so today you should use class-based exceptions, as shown in this book. If you work with legacy code, though, you might still come across string exceptions. They might also appear in books, tutorials, and web resources written a few years ago (which qualifies as an eternity in Python years!).

String exceptions were straightforward to use -- any string would do, and they matched by object identity, not value (that is, using is, not ==):
> ```python
> C:\code> C:\Python25\python
> >>> myexc = "My exception string" # Were we ever this young?...
> >>> try:
> ...     raise myexc
> ... except myexc:
> ...     print('caught')
> ...
> 
> caught
> ```

This form of exception was removed because it was not as good as classes for larger programs and code maintenance. In modern Pythons, string exceptions trigger exceptions instead:
> ```powershell
> C:\code> py −3
> >>> raise 'spam'
> TypeError: exceptions must derive from BaseException
> 
> C:\code> py −2
> >>> raise 'spam'
> TypeError: exceptions must be old-style classes or derived from BaseException, ...etc
> ```

Although you can't use string exceptions today, they actually provide a natural vehicle for introducing the class-based exceptions model.

## Class-Based Exceptions
Strings were a simple way to define exceptions. As described earlier, however, classes have some added advantages that merit a quick look. Most prominently, they allow us to identify exception categories that are more flexible to use and maintain than simple strings. Moreover, classes naturally allow for attached exception details and support inheritance. Because they are seen by many as the better approach, they are now required.

Coding details aside, the chief difference between string and class exceptions has to do with the way that exceptions raised are matched against except clauses in try statements:
- String exceptions were matched by simple object identity: the raised exception was matched to except clauses by Python's is test.
- Class exceptions are matched by superclass relationships: the raised exception matches an except clause if that except clause names the exception instance's class or any superclass of it.

That is, when a try statement's except clause lists a superclass, it catches instances of that superclass, as well as instances of all its subclasses lower in the class tree. The net effect is that class exceptions naturally support the construction of exception hierarchies: superclasses become category names, and subclasses become specific kinds of exceptions within a category. By naming a general exception superclass, an except clause can catch an entire category of exceptions -- any more specific subclass will match.

String exceptions had no such concept: because they were matched by simple object identity, there was no direct way to organize exceptions into more flexible categories or groups. The net result was that exception handlers were coupled with exception sets in a way that made changes difficult.

In addition to this category idea, class-based exceptions better support exception state information (attached to instances) and allow exceptions to participate in inheritance hierarchies (to obtain common behaviors). Because they offer all the benefits of classes and OOP in general, they provide a more powerful alternative to the now-defunct string-based exceptions model in exchange for a small amount of additional code.

## Coding Exceptions Classes
Let's look at an example to see how class exceptions translate to code. In the following file, classexc.py, we define a superclass called General and two subclasses called Specific1 and Specific2. This example illustrates the notion of exception categories -- General is a category name, and its two subclasses are specific types of exceptions within the category. Handlers that catch General will also catch any subclasses of it, including Specific1 and Specific2:
> 
> > ```python
> > class General(Exception): pass
> > class Specific1(General): pass
> > class Specific2(General): pass
> > 
> > def raiser0():
> >     X = General() # Raise superclass instance
> >     raise X
> > 
> > def raiser1():
> >     X = Specific1() # Raise subclass instance
> >     raise X
> > 
> > def raiser2():
> >     X = Specific2() # Raise different subclass instance
> >     raise X
> > 
> > for func in (raiser0, raiser1, raiser2):
> >     try:
> >         func()
> >     except General: # Match General or any subclass of it
> >         import sys
> >         print('caught: %s' % sys.exc_info()[0])
> > ```
> 
> > ```powershell
> > C:\code> python classexc.py
> > caught: <class '__main__.General'>
> > caught: <class '__main__.Specific1'>
> > caught: <class '__main__.Specific2'>
> > ```
> 

This code is mostly straightforward, but here are a few points to notice:
- **Exception superclass**
  Classes used to build exception category trees have very few requirements -- in fact, in this example they are mostly empty, with bodies that do nothing but pass. Notice, though, how the top-level class here inherits from the built-in Exception class. This is required in Python 3.X; Python 2.X allows standalone classic classes to serve as exceptions too, but it requires new-style classes to be derived from built-in exception classes just as in 3.X. Although we don't employ it here, because Exception provides some useful behavior we'll meet later, it's a good idea to inherit from it in either Python.
- **Raising instances**
  In this code, we call classes to make instances for the raise statements. In the class exception model, we always raise and catch a class instance object. If we list a class name without parentheses in a raise, Python calls the class with no constructor argument to make an instance for us. Exception instances can be created before the raise, as done here, or within the raise statement itself.
- **Catching categories**
  This code includes functions that raise instances of all three of our classes as exceptions, as well as a top-level try that calls the functions and catches General exceptions. The same try also catches the two specific exceptions, because they are subclasses of General -- members of its category.
- **Exception details**
  The exception handler here uses the `sys.exc_info` call -- as we'll see in more detail in the next chapter, it's how we can grab hold of the most recently raised exception in a generic fashion. Briefly, the first item in its result is the class of the exception raised, and the second is the actual instance raised. In a general except clause like the one here that catches all classes in a category, `sys.exc_info` is one way to determine exactly what's occurred. In this particular case, it's equivalent to fetching the instance's \_\_class\_\_ attribute. As we'll see in the next chapter, the `sys.exc_info` scheme is also commonly used with empty except clauses that catch everything.

The last point merits further explanation. When an exception is caught, we can be sure that the instance raised is an instance of the class listed in the except, or one of its more specific subclasses. Because of this, the \_\_class\_\_ attribute of the instance also gives the exception type. The following variant in classexc2.py, for example, works the same as the prior example -- it uses the as extension in its except clause to assign a variable to the instance actually raised:
> ```python
> class General(Exception): pass
> class Specific1(General): pass
> class Specific2(General): pass
> 
> def raiser0(): raise General()
> def raiser1(): raise Specific1()
> def raiser2(): raise Specific2()
> 
> for func in (raiser0, raiser1, raiser2):
>     try:
>         func()
>     except General as X: 								# X is the raised instance
>         print('caught: %s' % X.__class__) 			# Same as sys.exc_info()[0]

Because \_\_class\_\_ can be used like this to determine the specific type of exception raised, `sys.exc_info` is more useful for empty except clauses that do not otherwise have a way to access the instance or its class. Furthermore, more realistic programs usually should not have to care about which specific exception was raised at all -- by calling methods of the exception class instance generically, we automatically dispatch to behavior tailored for the exception raised.

More on this and `sys.exc\_info` in the next chapter; also see Chapter 29 and Part VI at large if you've forgotten what \_\_class\_\_ means in an instance, and the prior chapter for a review of the as used here.

