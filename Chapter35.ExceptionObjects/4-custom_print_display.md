# Custom Print Displays
As we saw in the preceding section, by default, instances of class-based exceptions display whatever you passed to the class constructor when they are caught and printed:
> ```python
> >>> class MyBad(Exception): pass
> ...
> >>> try:
> ...     raise MyBad('Sorry--my mistake!')
> ... except MyBad as X:
> ...     print(X)
> ...
> Sorry--my mistake!
> ```

This inherited default display model is also used if the exception is displayed as part of an error message when the exception is not caught:
> ```python
> >>> raise MyBad('Sorry--my mistake!')
> Traceback (most recent call last):
> File "<stdin>", line 1, in <module>
> __main__.MyBad: Sorry--my mistake!
> ```

For many roles, this is sufficient. To provide a more custom display, though, you can define one of two string-representation overloading methods in your class (\_\_repr\_\_ or \_\_str\_\_) to return the string you want to display for your exception. The string the method returns will be displayed if the exception either is caught and printed or reaches the default handler:
> 
> > ```python
> > >>> class MyBad(Exception):
> > ...     def __str__(self):
> > ...         return 'Always look on the bright side of life...'
> > ...
> > >>> try:
> > ...     raise MyBad()
> > ... except MyBad as X:
> > ...     print(X)
> > ...
> > ```
> Always look on the bright side of life...
> > ```python
> > >>> raise MyBad()
> > Traceback (most recent call last):
> > File "<stdin>", line 1, in <module>
> > __main__.MyBad: Always look on the bright side of life...
> > ```
> 
Whatever your method returns is included in error messages for uncaught exceptions and used when exceptions are printed explicitly. The method returns a hardcoded string here to illustrate, but it can also perform arbitrary text processing, possibly using state information attached to the instance object. The next section looks at state information options.

> **Note:** A subtle point here: you generally must redefine \_\_str\_\_ for exception display purposes, because the built-in exception superclasses already have a \_\_str\_\_ method, and \_\_str\_\_ is preferred to \_\_repr\_\_ in some contexts -- including error message displays. If you define a \_\_repr\_\_, printing will happily call the built-in superclass's \_\_str\_\_ instead!
> > ```python
> > >>> class E(Exception):
> >         def __repr__(self): return 'Not called!'
> > >>> raise E('spam')
> > ...
> > __main__.E: spam
> > >>> class E(Exception):
> >         def __str__(self): return 'Called!'
> > >>> raise E('spam')
> > ...
> > __main__.E: Called!
> > ```
> See Chapter 30 for more details on these special operator overloading methods.
