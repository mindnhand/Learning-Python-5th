# Common Operator Overloading Methods

Just about everything you can do to built-in objects such as integers and lists has a
corresponding specially named method for overloading in classes. Table 30-1 lists a
few of the most common; there are many more. In fact, many overloading methods
come in multiple versions (e.g., __add__, __radd__, and __iadd__ for addition), which
is one reason there are so many. See other Python books, or the Python language reference
manual, for an exhaustive list of the special method names available.

Table 30-1. Common operator overloading methods
|Method|Implements|Called for|
|-|-|-|
|`__init__`|`Constructor`|`Object creation: X = Class(args)`|
|`__del__`|`Destructor `|`Object reclamation of X`|
|`__add__`|`Operator + `|`X + Y, X += Y if no __iadd__`|
|`__or__`|`Operator \`|` (bitwise OR)`|`X \`|` Y, X \`|`= Y if no __ior__`|
|`__repr__, __str__`|`Printing, conversions`|`print(X), repr(X), str(X)`|
|`__call__`|`Function calls`|`X(*args, **kargs)`|
|`__getattr__`|`Attribute fetch`|`X.undefined`|
|`__setattr__`|`Attribute assignment`|`X.any = value`|
|`__delattr__`|`Attribute deletion`|`del X.any`|
|`__getattribute__`|`Attribute fetch`|`X.any`|
|`__getitem__`|`Indexing, slicing, iteration`|`X[key], X[i:j], for loops and other iterations if no __iter__`|
|`__setitem__`|`Index and slice assignment`|`X[key] = value, X[i:j] = iterable`|
|`__delitem__`|`Index and slice deletion`|`del X[key], del X[i:j]`|
|`__len__`|`Length`|`len(X), truth tests if no __bool__`|
|`__bool__`|`Boolean tests`|`bool(X), truth tests (named __nonzero__ in 2.X)`|
|`__lt__, __gt__, __le__, __ge__, __eq__, __ne__`|`Comparisons`|`X < Y, X > Y, X <= Y, X >= Y, X == Y, X != Y (or else __cmp__ in 2.X only)`|
|`__radd__`|`Right-side operators`|`Other + X`|
|`__iadd__`|`In-place augmented operators`|`X += Y (or else __add__)`|
|`__iter__, __next__`|`Iteration contexts`|`I=iter(X), next(I); for loops, in if no __con tains__, all comprehensions, map(F,X), others (__next__ is named next in 2.X)`|
|`__contains__`|`Membership test`|`item in X (any iterable)`|
|`__index__`|`Integer value`|`hex(X), bin(X), oct(X), O[X], O[X:] (replaces 2.X __oct__, __hex__)`|
|`__enter__, __exit__`|`Context manager (Chapter 34)`|`with obj as var:`|
|`__get__, __set__, __delete__`|`Descriptor attributes (Chapter 38)`|`X.attr, X.attr = value, del X.attr`|
|`__new__`|`Creation (Chapter 40)`|`Object creation, before __init__`|

All overloading methods have names that start and end with two underscores to keep
them distinct from other names you define in your classes. The mappings from special
method names to expressions or operations are predefined by the Python language,
and documented in full in the standard language manual and other reference resources.
For example, the name __add__ always maps to + expressions by Python language definition,
regardless of what an __add__ method’s code actually does.

Operator overloading methods may be inherited from superclasses if not defined, just
like any other methods. Operator overloading methods are also all optional—if you
don’t code or inherit one, that operation is simply unsupported by your class, and
attempting it will raise an exception. Some built-in operations, like printing, have defaults
(inherited from the implied object class in Python 3.X), but most built-ins fail
for class instances if no corresponding operator overloading method is present.

Most overloading methods are used only in advanced programs that require objects to
behave like built-ins, though the __init__ constructor we’ve already met tends to appear
in most classes. Let’s explore some of the additional methods in Table 30-1 by
example.

Although expressions trigger operator methods, be careful not to assume
that there is a speed advantage to cutting out the middleman and
calling the operator method directly. In fact, calling the operator method
directly might be twice as slow, presumably because of the overhead of
a function call, which Python avoids or optimizes in built-in cases.
Here’s the story for len and __len__ using Appendix B’s Windows
launcher and Chapter 21’s timing techniques on Python 3.3 and 2.7: in
both, calling __len__ directly takes twice as long:
> ```powershell
> c:\code> py −3 -m timeit -n 1000 -r 5 -s "L = list(range(100))" "x = L.__len__()"
> 1000 loops, best of 5: 0.134 usec per loop
> c:\code> py −3 -m timeit -n 1000 -r 5 -s "L = list(range(100))" "x = len(L)"
> 1000 loops, best of 5: 0.063 usec per loop
> c:\code> py −2 -m timeit -n 1000 -r 5 -s "L = list(range(100))" "x = L.__len__()"
> 1000 loops, best of 5: 0.117 usec per loop
> c:\code> py −2 -m timeit -n 1000 -r 5 -s "L = list(range(100))" "x = len(L)"
> 1000 loops, best of 5: 0.0596 usec per loop
> ```
> in my computer, the result with python3.8 follows:
> ```shell
> [root@localhost Chapter30.OperatorOverloading]# python3 -m timeit -n 1000 -r 5 -s "L = list(range(100))" "x = L.__len__()"
> 1000 loops, best of 5: 140 nsec per loop
> [root@localhost Chapter30.OperatorOverloading]# python3 -m timeit -n 1000 -r 5 -s "L = list(range(100))" "x = len(L)"
> 1000 loops, best of 5: 65.9 nsec per loop
> ```
This is not as artificial as it may seem—I’ve actually come across recommendations
for using the slower alternative in the name of speed at a noted research institution!
