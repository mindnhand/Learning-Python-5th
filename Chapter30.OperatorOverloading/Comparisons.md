# Comparisons: \_\_lt\_\_, \_\_gt\_\_, and Others
Our next batch of overloading methods supports comparisons. As suggested in Table 30-1, classes can define 
methods to catch all six comparison operators: <, >, <=, >=, ==, and !=. These methods are generally 
straightforward to use, but keep the following qualifications in mind:
- Unlike the \_\_add\_\_/\_\_radd\_\_ pairings discussed earlier, there are no right-side variants of comparison 
  methods. Instead, reflective methods are used when only one operand supports comparison (e.g., \_\_lt\_\_ 
  and \_\_gt\_\_ are each other's reflection).
- There are no implicit relationships among the comparison operators. The truth of == does not imply that 
  != is false, for example, so both \_\_eq\_\_ and \_\_ne\_\_ should be defined to ensure that both operators behave 
  correctly.
- In Python 2.X, a \_\_cmp\_\_ method is used by all comparisons if no more specific comparison methods are defined; 
  it returns a number that is less than, equal to, or greater than zero, to signal less than, equal, and 
  greater than results for the comparison of its two arguments (self and another operand). This method often uses
  the cmp(x, y) built-in to compute its result. Both the \_\_cmp\_\_ method and the cmp built-in function are removed 
  in Python 3.X: use the more specific methods instead.

We don't have space for an in-depth exploration of comparison methods, but as a quick introduction, consider 
the following class and test code:
> ```python
> class C:
>     data = 'spam'
>     def __gt__(self, other): 										# 3.X and 2.X version
>         return self.data > other
>     def __lt__(self, other):
>         return self.data < other
> 
> X = C()
> print(X > 'ham') 													# True (runs __gt__)
> print(X < 'ham') 													# False (runs __lt__)
> ```

When run under Python 3.X or 2.X, the prints at the end display the expected results noted in their comments, 
because the class's methods intercept and implement comparison expressions. Consult Python's manuals and other 
reference resources for more details in this category; for example, \_\_lt\_\_ is used for sorts in Python3.X, and 
as for binary expression operators, these methods can also return NotImplemented for unsupported arguments.

## The \_\_cmp\_\_ Method in Python 2.X
In Python 2.X only, the \_\_cmp\_\_ method is used as a fallback if more specific methods are not defined: its integer 
result is used to evaluate the operator being run. The following produces the same result as the prior section's code 
under 2.X, for example, but fails in 3.X because \_\_cmp\_\_ is no longer used:
> ```python
> class C:
>     data = 'spam' 												# 2.X only
>     def __cmp__(self, other): 									# __cmp__ not used in 3.X
>         return cmp(self.data, other) 								# cmp not defined in 3.X
> 
> X = C()
> print(X > 'ham') 													# True (runs __cmp__)
> print(X < 'ham') 													# False (runs __cmp__)
> ```

Notice that this fails in 3.X because \_\_cmp\_\_ is no longer special, not because the cmp built-in function is no 
longer present. If we change the prior class to the following to try to simulate the cmp call, the code still 
works in 2.X but fails in 3.X:
> ```python
> class C:
>     data = 'spam'
>     def __cmp__(self, other):
>         return (self.data > other) - (self.data < other)
> ```

So why, you might be asking, did I just show you a comparison method that is no longer supported in 3.X? While it 
would be easier to erase history entirely, this book is designed to support both 2.X and 3.X readers. Because \_\_cmp\_\_ 
may appear in code 2.X readers must reuse or maintain, it's fair game in this book. Moreover, \_\_cmp\_\_ was removed
more abruptly than the \_\_getslice\_\_ method described earlier, and so may endure longer. If you use 3.X, though, or 
care about running your code under 3.X in the future, don't use \_\_cmp\_\_ anymore: use the more specific comparison 
methods instead.

## Boolean Tests: \_\_bool\_\_ and \_\_len\_\_
The next set of methods is truly useful (yes, pun intended!). As we've learned, every object is inherently true or 
false in Python. When you code classes, you can define what this means for your objects by coding methods that give 
the True or False values of instances on request. The names of these methods differ per Python line; this section 
starts with the 3.X story, then shows 2.X's equivalent.
As mentioned briefly earlier, in Boolean contexts, Python first tries \_\_bool\_\_ to obtain a direct Boolean value; 
if that method is missing, Python tries \_\_len\_\_ to infer a truth value from the object's length. The first of these
generally uses object state or other information to produce a Boolean result. In 3.X:
> ```python
> >>> class Truth:
>         def __bool__(self): return True
> >>> X = Truth()
> >>> if X: print('yes!')
> yes!
> >>> class Truth:
>         def __bool__(self): return False
> >>> X = Truth()
> >>> bool(X)
> False
> ```

If this method is missing, Python falls back on length because a nonempty object is considered true (i.e., a nonzero 
length is taken to mean the object is true, and a zero length means it is false):
> ```python
> >>> class Truth:
>         def __len__(self): return 0
> >>> X = Truth()
> >>> if not X: print('no!')
> no!
> ```

If both methods are present Python prefers \_\_bool\_\_ over \_\_len\_\_, because it is more specific:
> ```python
> >>> class Truth:
>         def __bool__(self): return True							# 3.X tries __bool__ first
>         def __len__(self): return 0 								# 2.X tries __len__ first
> >>> X = Truth()
> >>> if X: print('yes!')
> yes!
> ```

If neither truth method is defined, the object is vacuously considered true (though any potential implications 
for more metaphysically inclined readers are strictly coincidental):
> ```python
> >>> class Truth:
>         pass
> >>> X = Truth()
> >>> bool(X)
> True
> ```

At least that's the Truth in 3.X. These examples won't generate exceptions in 2.X, but some of their results 
there may look a bit odd (and trigger an existential crisis or two) unless you read the next section.

## Boolean Methods in Python 2.X
Alas, it's not nearly as dramatic as billed—Python 2.X users simply use \_\_nonzero\_\_  instead of \_\_bool\_\_ in 
all of the preceding section's code. Python 3.X renamed the 2.X \_\_nonzero\_\_ method to \_\_bool\_\_, but Boolean tests 
work the same otherwise; both 3.X and 2.X use \_\_len\_\_ as a fallback.
Subtly, if you don't use the 2.X name, the first test in the prior section will work the same for you anyhow, 
but only because \_\_bool\_\_ is not recognized as a special method name in 2.X, and objects are considered true by 
default! To witness this version difference live, you need to return False:
> ```powershell
> C:\code> c:\python33\python
> >>> class C:
>         def __bool__(self):
>             print('in bool')
> 			  return False
> >>> X = C()
> >>> bool(X)
> in bool
> False
> >>> if X: print(99)
> in bool
> ```

This works as advertised in 3.X. In 2.X, though, \_\_bool\_\_ is ignored and the object is always considered true by default:
> ```powershell
> C:\code> c:\python27\python
> >>> class C:
>         def __bool__(self):
>             print('in bool')
> 			  return False
> >>> X = C()
> >>> bool(X)
> True
> >>> if X: print(99)
> 99
> ```

The short story here: in 2.X, use \_\_nonzero\_\_ for Boolean values, or return 0 from the \_\_len\_\_ fallback method 
to designate false:
> ```powershell
> C:\code> c:\python27\python
> >>> class C:
>         def __nonzero__(self):
>             print('in nonzero')
>             return False 										# Returns int (or True/False, same as 1/0)
> >>> X = C()
> >>> bool(X)
> in nonzero
> False
> >>> if X: print(99)
> in nonzero
> ```

But keep in mind that \_\_nonzero\_\_ works in 2.X only; if used in 3.X it will be silently ignored and the object will
be classified as true by default—just like using 3.XX's  \_\_bool\_\_ in 2.X!
And now that we've managed to cross over into the realm of philosophy, let's move on to look at one last overloading 
context: object demise.

## Object Destruction: \_\_del\_\_
It's time to close out this chapter—and learn how to do the same for our class objects.  We've seen how the \_\_init\_\_ 
constructor is called whenever an instance is generated (and noted how \_\_new\_\_ is run first to make the object).
Its counterpart, the destructor method \_\_del\_\_, is run automatically when an instance's space is being reclaimed
(i.e., at "garbage collection" time):
> ```python
> >>> class Life:
>         def __init__(self, name='unknown'):
>             print('Hello ' + name)
>             self.name = name
>         def live(self):
>             print(self.name)
> 		  def __del__(self):
> 			  print('Goodbye ' + self.name)
> 
> >>> brian = Life('Brian')
> Hello Brian
> >>> brian.live()
> Brian
> >>> brian = 'loretta'
> Goodbye Brian
> ```

Here, when brian is assigned a string, we lose the last reference to the Life instance and so trigger its destructor 
method. This works, and it may be useful for implementing some cleanup activities, such as terminating a server 
connection. However, destructors are not as commonly used in Python as in some OOP languages, for a number of reasons
that the next section describes.

## Destructor Usage Notes
The destructor method works as documented, but it has some well-known caveats and a few outright dark corners that 
make it somewhat rare to see in Python code:
- Need: For one thing, destructors may not be as useful in Python as they are in some other OOP languages. Because 
  Python automatically reclaims all memory space held by an instance when the instance is reclaimed, destructors are 
  not necessary for space management. In the current CPython implementation of Python, you also don't need to close 
  file objects held by the instance in destructors because they are automatically closed when reclaimed. As mentioned 
  in Chapter 9, though, it's still sometimes best to run file close methods anyhow, because this autoclose behavior
  may vary in alternative Python implementations (e.g., Jython).
- Predictability: For another, you cannot always easily predict when an instance will be reclaimed. In some cases, 
  there may be lingering references to your objects in system tables that prevent destructors from running when your 
  program expects them to be triggered. Python also does not guarantee that destructor methods will be called for objects 
  that still exist when the interpreter exits.
- Exceptions: In fact, \_\_del\_\_ can be tricky to use for even more subtle reasons. Exceptions raised within it, for 
  example, simply print a warning message to sys.stderr (the standard error stream) rather than triggering an exception
  event, because of the unpredictable context under which it is run by the garbage collector —itt's not always possible
  to know where such an exception should be delivered.
- Cycles: In addition, cyclic (a.k.a. circular) references among objects may prevent garbage collection from happening 
  when you expect it to. An optional cycle detector, enabled by default, can automatically collect such objects eventually, 
  but only if they do not have \_\_del\_\_ methods. Since this is relatively obscure, we'll ignore further details here; 
  see Python's standard manuals' coverage of both \_\_del\_\_ and the gc garbage collector module for more information.

Because of these downsides, it's often better to code termination activities in an explicitly called method (e.g., shutdown).
As described in the next part of the book, the try/finally statement also supports termination actions, as does the with 
statement for objects that support its context manager model.
