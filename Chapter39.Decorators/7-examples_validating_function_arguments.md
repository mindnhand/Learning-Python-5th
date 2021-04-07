# Example: Validating Function Arguments
As a final example of the utility of decorators, this section develops a function decorator that automatically tests whether arguments passed to a function or method are within a valid numeric range. It's designed to be used during either development or production, and it can be used as a template for similar tasks (e.g., argument type testing, if you must). Because this chapter's size limits have been broached, this example's code is largely self-study material, with limited narrative; as usual, browse the code for more details.

## The Goal
In the object-oriented tutorial of Chapter 28, we wrote a class that gave a pay raise to objects representing people based upon a passed-in percentage:
> ```python
> class Person:
>     ...
>     def giveRaise(self, percent):
>         self.pay = int(self.pay * (1 + percent))
> ```

There, we noted that if we wanted the code to be robust it would be a good idea to check the percentage to make sure it's not too large or too small. We could implement such a check with either if or assert statements in the method itself, using inline tests:
> ```python
> class Person:
>     def giveRaise(self, percent): 			# Validate with inline code
>         if percent < 0.0 or percent > 1.0:
>             raise TypeError, 'percent invalid'
>         self.pay = int(self.pay * (1 + percent))
> 
> class Person: 								# Validate with asserts
>     def giveRaise(self, percent):
>         assert percent >= 0.0 and percent <= 1.0, 'percent invalid'
>         self.pay = int(self.pay * (1 + percent))
> ```

However, this approach clutters up the method with inline tests that will probably be useful only during development. For more complex cases, this can become tedious (imagine trying to inline the code needed to implement the attribute privacy provided by the last section's decorator). Perhaps worse, if the validation logic ever needs to change, there may be arbitrarily many inline copies to find and update.

A more useful and interesting alternative would be to develop a general tool that can perform range tests for us automatically, for the arguments of any function or method we might code now or in the future. A decorator approach makes this explicit and convenient:
> ```python
> class Person:
>     @rangetest(percent=(0.0, 1.0)) 			# Use decorator to validate
>     def giveRaise(self, percent):
>         self.pay = int(self.pay * (1 + percent))
> ```

Isolating validation logic in a decorator simplifies both clients and future maintenance.

Notice that our goal here is different than the attribute validations coded in the prior chapter's final example. Here, we mean to validate the values of function arguments when passed, rather than attribute values when set. Python's decorator and introspection tools allow us to code this new task just as easily.

## A Basic Range-Testing Decorator for Positional Arguments
Let's start with a basic range test implementation. To keep things simple, we'll begin by coding a decorator that works only for positional arguments and assumes they always appear at the same position in every call; they cannot be passed by keyword name, and we don't support additional \*\*args keywords in calls because this can invalidate the positions declared in the decorator. Code the following in a file called rangetest1.py:
> ```python
> def rangetest(*argchecks): 				# Validate positional arg ranges
>     def onDecorator(func):
>         if not __debug__: 				# True if "python -O main.py args..."
>             return func 					# No-op: call original directly
>         else: 							# Else wrapper while debugging
>             def onCall(*args):
>                 for (ix, low, high) in argchecks:
>                     if args[ix] < low or args[ix] > high:
>                         errmsg = 'Argument %s not in %s..%s' % (ix, low, high)
>                         raise TypeError(errmsg)
>                 return func(*args)
>             return onCall
>     return onDecorator
> ```

As is, this code is mostly a rehash of the coding patterns we explored earlier: we use decorator arguments, nested scopes for state retention, and so on.

We also use nested def statements to ensure that this works for both simple functions and methods, as we learned earlier. When used for a class's method, onCall receives the subject class's instance in the first item in \*args and passes this along to self in the original method function; argument numbers in range tests start at 1 in this case, not 0.

New here, notice this code's use of the \_\_debug\_\_ built-in variable -- Python sets this to True, unless it's being run with the `-O` optimize command-line flag (e.g., `python -O main.py`). When \_\_debug\_\_ is False, the decorator returns the origin function unchanged, to avoid extra later calls and their associated performance penalty. In other words, the decorator automatically removes its augmentation logic when `-O` is used, without requiring you to physically remove the decoration lines in your code. This first iteration solution is used as follows:
> ```python
> # File rangetest1_test.py
> from __future__ import print_function 				# 2.X
> from rangetest1 import rangetest
> print(__debug__) 						# False if "python -O main.py"
> @rangetest((1, 0, 120)) 				# persinfo = rangetest(...)(persinfo)
> def persinfo(name, age): 				# age must be in 0..120
>     print('%s is %s years old' % (name, age))
> 
> @rangetest([0, 1, 12], [1, 1, 31], [2, 0, 2009])
> def birthday(M, D, Y):
>     print('birthday = {0}/{1}/{2}'.format(M, D, Y))
> 
> class Person:
>     def __init__(self, name, job, pay):
>         self.job = job
>         self.pay = pay
> 
>     @rangetest([1, 0.0, 1.0]) 		# giveRaise = rangetest(...)(giveRaise)
>     def giveRaise(self, percent): 	# Arg 0 is the self instance here
>         self.pay = int(self.pay * (1 + percent))
> 
> # Comment lines raise TypeError unless "python -O" used on shell command line
> persinfo('Bob Smith', 45) 			# Really runs onCall(...) with state
> #persinfo('Bob Smith', 200) 			# Or person if -O cmd line argument
> 
> birthday(5, 31, 1963)
> #birthday(5, 32, 1963)
> 
> sue = Person('Sue Jones', 'dev', 100000)
> sue.giveRaise(.10) 					# Really runs onCall(self, .10)
> print(sue.pay) 						# Or giveRaise(self, .10) if -O
> #sue.giveRaise(1.10)
> #print(sue.pay)
> ```

When run, valid calls in this code produce the following output (all the code in this section works the same under Python 2.X and 3.X, because function decorators are supported in both, we're not using attribute delegation, and we use version-neutral exception construction and printing techniques):
> ```powershell
> C:\code> python rangetest1_test.py
> True
> Bob Smith is 45 years old
> birthday = 5/31/1963
> 110000
> ```

Uncommenting any of the invalid calls causes a TypeError to be raised by the decorator. Here's the result when the last two lines are allowed to run (as usual, I've omitted some of the error message text here to save space):
> ```powershell
> C:\code> python rangetest1_test.py
> True
> Bob Smith is 45 years old
> birthday = 5/31/1963
> 110000
> TypeError: Argument 1 not in 0.0..1.0

Running Python with its -O flag at a system command line will disable range testing, but also avoid the performance overhead of the wrapping layer -- we wind up calling the original undecorated function directly. Assuming this is a debugging tool only, you can use this flag to optimize your program for production use:
> ```python
> C:\code> python -O rangetest1_test.py
> False
> Bob Smith is 45 years old
> birthday = 5/31/1963
> 110000
> 231000
> ```

## Generalizing for Keywords and Defaults, Too
The prior version illustrates the basics we need to employ, but it's fairly limited -- it supports validating arguments passed by position only, and it does not validate keyword arguments (in fact, it assumes that no keywords are passed in a way that makes argument position numbers incorrect). Additionally, it does nothing about arguments with defaults that may be omitted in a given call. That's fine if all your arguments are passed by position and never defaulted, but less than ideal in a general tool. Python supports much more flexible argument-passing modes, which we're not yet addressing.

The mutation of our example shown next does better. By matching the wrapped function's expected arguments against the actual arguments passed in a call, it supports range validations for arguments passed by either position or keyword name, and it skips testing for default arguments omitted in the call. In short, arguments to be validated are specified by keyword arguments to the decorator, which later steps through both the \*pargs positionals tuple and the \*\*kargs keywords dictionary to validate.
> ```python
> """
> File rangetest.py: function decorator that performs range-test
> validation for arguments passed to any function or method.
> Arguments are specified by keyword to the decorator. In the actual
> call, arguments may be passed by position or keyword, and defaults
> may be omitted. See rangetest_test.py for example use cases.
> """
> trace = True
> def rangetest(**argchecks): 			# Validate ranges for both+defaults
>     def onDecorator(func): 			# onCall remembers func and argchecks
>         if not __debug__: 			# True if "python -O main.py args..."
>             return func 				# Wrap if debugging; else use original
>         else:
>             code = func.__code__
>             allargs = code.co_varnames[:code.co_argcount]
>             funcname = func.__name__
>             def onCall(*pargs, **kargs):
>                 # All pargs match first N expected args by position
>                 # The rest must be in kargs or be omitted defaults
>                 expected = list(allargs)
>                 positionals = expected[:len(pargs)]
> 
>                 for (argname, (low, high)) in argchecks.items():
>                     # For all args to be checked
>                     if argname in kargs:
>                         # Was passed by name
>                         if kargs[argname] < low or kargs[argname] > high:
>                             errmsg = '{0} argument "{1}" not in {2}..{3}'
>                             errmsg = errmsg.format(funcname, argname, low, high)
>                             raise TypeError(errmsg)
>                     elif argname in positionals:
>                         # Was passed by position
>                         position = positionals.index(argname)
>                         if pargs[position] < low or pargs[position] > high:
>                             errmsg = '{0} argument "{1}" not in {2}..{3}'
>                             errmsg = errmsg.format(funcname, argname, low, high)
>                             raise TypeError(errmsg)
>                     else:
>                         # Assume not passed: default
>                         if trace:
>                             print('Argument "{0}" defaulted'.format(argname))
>                 return func(*pargs, **kargs) # OK: run original call
>             return onCall
>     return onDecorator
> ```

The following test script shows how the decorator is used -- arguments to be validated are given by keyword decorator arguments, and at actual calls we can pass by name or position and omit arguments with defaults even if they are to be validated otherwise:
> ```python
> """
> File rangetest_test.py (3.X + 2.X)
> Comment lines raise TypeError unless "python -O" used on shell command line
> """
> 
> from __future__ import print_function # 2.X
> from rangetest import rangetest
> # Test functions, positional and keyword
> 
> @rangetest(age=(0, 120)) # persinfo = rangetest(...)(persinfo)
> def persinfo(name, age):
>     print('%s is %s years old' % (name, age))
> 
> @rangetest(M=(1, 12), D=(1, 31), Y=(0, 2013))
> def birthday(M, D, Y):
>     print('birthday = {0}/{1}/{2}'.format(M, D, Y))
> 
> persinfo('Bob', 40)
> persinfo(age=40, name='Bob')
> birthday(5, D=1, Y=1963)
> #persinfo('Bob', 150)
> #persinfo(age=150, name='Bob')
> #birthday(5, D=40, Y=1963)
> 
> # Test methods, positional and keyword
> class Person:
>     def __init__(self, name, job, pay):
>         self.job = job
>         self.pay = pay
> 
>     # giveRaise = rangetest(...)(giveRaise)
>     @rangetest(percent=(0.0, 1.0)) 			# percent passed by name or position
>     def giveRaise(self, percent):
>         self.pay = int(self.pay * (1 + percent))
> 
> bob = Person('Bob Smith', 'dev', 100000)
> sue = Person('Sue Jones', 'dev', 100000)
> bob.giveRaise(.10)
> sue.giveRaise(percent=.20)
> print(bob.pay, sue.pay)
> #bob.giveRaise(1.10)
> #bob.giveRaise(percent=1.20)
> 
> # Test omitted defaults: skipped
> @rangetest(a=(1, 10), b=(1, 10), c=(1, 10), d=(1, 10))
> def omitargs(a, b=7, c=8, d=9):
>     print(a, b, c, d)
> 
> omitargs(1, 2, 3, 4)
> omitargs(1, 2, 3)
> omitargs(1, 2, 3, d=4)
> omitargs(1, d=4)
> omitargs(d=4, a=1)
> omitargs(1, b=2, d=4)
> omitargs(d=8, c=7, a=1)
> #omitargs(1, 2, 3, 11) # Bad d
> #omitargs(1, 2, 11) # Bad c
> #omitargs(1, 2, 3, d=11) # Bad d
> #omitargs(11, d=4) # Bad a
> #omitargs(d=4, a=11) # Bad a
> #omitargs(1, b=11, d=4) # Bad b
> #omitargs(d=8, c=7, a=11) # Bad a
> ```

When this script is run, out-of-range arguments raise an exception as before, but arguments may be passed by either name or position, and omitted defaults are not validated. This code runs on both 2.X and 3.X. Trace its output and test this further on your own to experiment; it works as before, but its scope has been broadened:
> ```powershell
> C:\code> python rangetest_test.py
> Bob is 40 years old
> Bob is 40 years old
> birthday = 5/1/1963
> 110000 120000
> 1 2 3 4
> Argument "d" defaulted
> 1 2 3 9
> 1 2 3 4
> Argument "c" defaulted
> Argument "b" defaulted
> 1 7 8 4
> Argument "c" defaulted
> Argument "b" defaulted
> 1 7 8 4
> Argument "c" defaulted
> 1 2 8 4
> Argument "b" defaulted
> 1 7 7 8
> ```

On validation errors, we get an exception as before when one of the method test lines is uncommented, unless the -O command-line argument is passed to Python to disable the decorator's logic:
> ```python
> TypeError: giveRaise argument "percent" not in 0.0..1.0
> ```

## Implementation Details
This decorator's code relies on both introspection APIs and subtle constraints of argument passing. To be fully general we could in principle try to mimic Python's argument matching logic in its entirety to see which names have been passed in which modes, but that's far too much complexity for our tool. It would be better if we could somehow match arguments passed by name against the set of all expected arguments' names, in order to determine which position arguments actually appear in during a given call.

### Function introspection
It turns out that the introspection API available on function objects and their associated code objects has exactly the tool we need. This API was briefly introduced in Chapter 19, but we'll actually put it to use here. The set of expected argument names is simply the first N variable names attached to a function's code object:
> ```python
> # In Python 3.X (and 2.6+ for compatibility)
> >>> def func(a, b, c, e=True, f=None): 			# Args: three required, two defaults
>         x = 1 						# Plus two more local variables
>         y = 2
> >>> code = func.__code__ 		# Code object of function object
> >>> code.co_nlocals
> 7
> >>> code.co_varnames 			# All local variable names
> ('a', 'b', 'c', 'e', 'f', 'x', 'y')
> >>> code.co_varnames[:code.co_argcount] 			# <== First N locals are expected args
> ('a', 'b', 'c', 'e', 'f')
> ```

And as usual, starred-argument names in the call proxy allow it to collect arbitrarily many arguments to be matched against the expected arguments so obtained from the function's introspection API:
> ```python
> >>> def catcher(*pargs, **kargs): print('%s, %s' % (pargs, kargs))
> >>> catcher(1, 2, 3, 4, 5)
> (1, 2, 3, 4, 5), {}
> >>> catcher(1, 2, c=3, d=4, e=5) 		# Arguments at calls
> (1, 2), {'d': 4, 'e': 5, 'c': 3}
> ```

The function object's API is available in older Pythons, but the func.\_\_code\_\_ attribute is named func.func\_code in 2.5 and earlier; the newer \_\_code\_\_ attribute is also redundantly available in 2.6 and later for portability. Run a dir call on function and code objects for more details. Code like the following would support 2.5 and earlier, though the sys.version\_info result itself is similarly nonportable -- it's a named tuple in recent Pythons, but we can use offsets on newer and older Pythons alike:
> ```python
> >>> import sys 					# For backward compatibility
> >>> tuple(sys.version_info) 		# [0] is major release number
> (3, 3, 0, 'final', 0)
> >>> code = func.__code__ if sys.version_info[0] == 3 else func.func_code
> ```

### Argument assumptions
Given the decorated function's set of expected argument names, the solution relies upon two constraints on argument passing order imposed by Python (these still hold true in both 2.X and 3.X current releases):
- At the call, all positional arguments appear before all keyword arguments.
- In the def, all nondefault arguments appear before all default arguments.

That is, a nonkeyword argument cannot generally follow a keyword argument at a call, and a nondefault argument cannot follow a default argument at a definition. All "name=value" syntax must appear after any simple "name" in both places. As we've also learned, Python matches argument values passed by position to argument names in function headers from left to right, such that these values always match the leftmost names in headers. Keywords match by name instead, and a given argument can receive only one value.

To simplify our work, we can also make the assumption that a call is valid in general
- that is, that all arguments either will receive values (by name or position), or will be omitted intentionally to pick up defaults. This assumption won't necessarily hold, because the function has not yet actually been called when the wrapper logic tests validity
- the call may still fail later when invoked by the wrapper layer, due to incorrect argument passing. As long as that doesn't cause the wrapper to fail any more badly, though, we can finesse the validity of the call. This helps, because validating calls before they are actually made would require us to emulate Python's argument-matching algorithm in full -- again, too complex a procedure for our tool.

### Matching algorithm
Now, given these constraints and assumptions, we can allow for both keywords and omitted default arguments in the call with this algorithm. When a call is intercepted, we can make the following assumptions and deductions:
1. Let N be the number of passed positional arguments, obtained from the length of the \*pargs tuple.
2. All N positional arguments in \*pargs must match the first N expected arguments obtained from the function's code object. This is true per Python's call ordering rules, outlined earlier, since all positionals precede all keywords in a call.
3. To obtain the names of arguments actually passed by position, we can slice the list of all expected arguments up to the length N of the \*pargs passed positionals tuple.
4. Any arguments after the first N expected arguments either were passed by keyword or were defaulted by omission at the call.
5. For each argument name to be validated by the decorator:
  a. If the name is in \*\*kargs, it was passed by name -- indexing \*\*kargs gives its passed value.
  b. If the name is in the first N expected arguments, it was passed by position -- its relative position in the expected list gives its relative position in \*pargs.
  c. Otherwise, we can assume it was omitted in the call and defaulted, and need not be checked.

In other words, we can skip tests for arguments that were omitted in a call by assuming that the first N actually passed positional arguments in \*pargs must match the first N argument names in the list of all expected arguments, and that any others must either have been passed by keyword and thus be in \*\*kargs, or have been defaulted. Under this scheme, the decorator will simply skip any argument to be checked that was omitted between the rightmost positional argument and the leftmost keyword argument; between keyword arguments; or after the rightmost positional in general. Trace through the decorator and its test script to see how this is realized in code.

## Open Issues
Although our range-testing tool works as planned, three caveats remain -- it doesn't detect invalid calls, doesn't handle some arbitrary-argument signatures, and doesn't fully support nesting. Improvements may require extension or altogether different approaches. Here's a quick rundown of the issues.

### Invalid calls
First, as mentioned earlier, calls to the original function that are not valid still fail in our final decorator. The following both trigger exceptions, for example:
> ```python
> omitargs()
> omitargs(d=8, c=7, b=6)
> ```

These only fail, though, where we try to invoke the original function, at the end of the wrapper. While we could try to imitate Python's argument matching to avoid this, there's not much reason to do so -- since the call would fail at this point anyhow, we might as well let Python's own argument-matching logic detect the problem for us.

### Arbitrary arguments
Second, although our final version handles positional arguments, keyword arguments, and omitted defaults, it still doesn't do anything explicit about \*pargs and \*\*kargs starred-argument names that may be used in a decorated function that accepts arbitrarily many arguments itself. We probably don't need to care for our purposes, though:
- If an extra keyword argument is passed, its name will show up in \*\*kargs and can be tested normally if mentioned to the decorator.
- If an extra keyword argument is not passed, its name won't be in either \*\*kargs or the sliced expected positionals list, and it will thus not be checked -- it is treated as though it were defaulted, even though it is really an optional extra argument.
- If an extra positional argument is passed, there's no way to reference it in the decorator  anyhow -- its name won't be in either \*\*kargs or the sliced expected arguments list, so it will simply be skipped. Because such arguments are not listed in the function's definition, there's no way to map a name given to the decorator back to an expected relative position.

In other words, as it is the code supports testing arbitrary keyword arguments by name, but not arbitrary positionals that are unnamed and hence have no set position in the function's argument signature. In terms of the function object's API, here's the effect of these tools in decorated functions:
> ```python
> >>> def func(*kargs, **pargs): pass
> >>> code = func.__code__
> >>> code.co_nlocals, code.co_varnames
> (2, ('kargs', 'pargs'))
> >>> code.co_argcount, code.co_varnames[:code.co_argcount]
> (0, ())
> >>> def func(a, b, *kargs, **pargs): pass
> >>> code = func.__code__
> >>> code.co_argcount, code.co_varnames[:code.co_argcount]
> (2, ('a', 'b'))
> ```

Because starred-argument names show up as locals but not as expected arguments, they won't be a factor in our matching algorithm -- names preceding them in function headers can be validated as usual, but not any extra positional arguments passed. In principle, we could extend the decorator's interface to support \*pargs in the decorated function, too, for the rare cases where this might be useful (e.g., a special argument name with a test to apply to all arguments in the wrapper's \*pargs beyond the length of the expected arguments list), but we'll pass on such an extension here.

### Decorator nesting
Finally, and perhaps most subtly, this code's approach does not fully support use of decorator nesting to combine steps. Because it analyzes arguments using names in function definitions, and the names of the call proxy function returned by a nested decoration won't correspond to argument names in either the original function or decorator arguments, it does not fully support use in nested mode.

Technically, when nested, only the most deeply nested appearance's validations are run in full; all other nesting levels run tests on arguments passed by keyword only. Trace the code to see why; because the onCall proxy's call signature expects no named positional arguments, any to-be-validated arguments passed to it by position are treated as if they were omitted and hence defaulted, and are thus skipped.

This may be inherent in this tool's approach -- proxies change the argument name signatures at their levels, making it impossible to directly map names in decorator arguments to positions in passed argument sequences. When proxies are present, argument names ultimately apply to keywords only; by contrast, the first-cut solution's argument positions may support proxies better, but do not fully support keywords.

In lieu of this nesting capability, we'll generalize this decorator to support multiple types of validations in a single decoration in an end-of-chapter quiz solution, which also gives examples of the nesting limitation in action. Since we've already neared the space allocation for this example, though, if you care about these or any other further improvements, you've officially crossed over into the realm of suggested exercises.

## Decorator Arguments Versus Function Annotations
Interestingly, the function annotation feature introduced in Python 3.X (3.0 and later) could provide an alternative to the decorator arguments used by our example to specify range tests. As we learned in Chapter 19, annotations allow us to associate expressions with arguments and return values, by coding them in the def header line itself; Python collects annotations in a dictionary and attaches it to the annotated function.

We could use this in our example to code range limits in the header line, instead of in decorator arguments. We would still need a function decorator to wrap the function in order to intercept later calls, but we would essentially trade decorator argument syntax:
> 
> > ```python
> > @rangetest(a=(1, 5), c=(0.0, 1.0))
> > def func(a, b, c): 				# func = rangetest(...)(func)
> >     print(a + b + c)
> 
> for annotation syntax like this:
> 
> > 
> > @rangetest
> > def func(a:(1, 5), b, c:(0.0, 1.0)):
> >     print(a + b + c)
> > ```
> 

That is, the range constraints would be moved into the function itself, instead of being coded externally. The following script illustrates the structure of the resulting decorators under both schemes, in incomplete skeleton code for brevity. The decorator arguments code pattern is that of our complete solution shown earlier; the annotation alternative requires one less level of nesting, because it doesn't need to retain decorator arguments as state:
> 
> > ```python
> > # Using decorator arguments (3.X + 2.X)
> > def rangetest(**argchecks):
> >     def onDecorator(func):
> >         def onCall(*pargs, **kargs):
> >             print(argchecks)
> >             for check in argchecks:
> >                 pass 					# Add validation code here
> >             return func(*pargs, **kargs)
> >         return onCall
> >     return onDecorator
> > 
> > @rangetest(a=(1, 5), c=(0.0, 1.0))
> > def func(a, b, c): 					# func = rangetest(...)(func)
> >     print(a + b + c)
> > 
> > func(1, 2, c=3) 					# Runs onCall, argchecks in scope
> > 
> > # Using function annotations (3.X only)
> > def rangetest(func):
> >     def onCall(*pargs, **kargs):
> >         argchecks = func.__annotations__
> >         print(argchecks)
> >         for check in argchecks:
> >             pass 						# Add validation code here
> >         return func(*pargs, **kargs)
> >     return onCall
> > 
> > @rangetest
> > def func(a:(1, 5), b, c:(0.0, 1.0)): 	# func = rangetest(func)
> >     print(a + b + c)
> > 
> > func(1, 2, c=3) 						# Runs onCall, annotations on func
> > ```
> 
> When run, both schemes have access to the same validation test information, but in different forms -- the decorator argument version's information is retained in an argument in an enclosing scope, and the annotation version's information is retained in an attribute of the function itself. In 3.X only, due to the use of function annotations:
> 
> > ```python
> > C:\code> py -3 decoargs-vs-annotation.py
> > {'a': (1, 5), 'c': (0.0, 1.0)}
> > 6
> > {'a': (1, 5), 'c': (0.0, 1.0)}
> > 6
> > ```
> 

I'll leave fleshing out the rest of the annotation-based version as a suggested exercise; its code would be identical to that of our complete solution shown earlier, because range-test information is simply on the function instead of in an enclosing scope. Really, all this buys us is a different user interface for our tool -- it will still need to match argument names against expected argument names to obtain relative positions as before.

In fact, using annotation instead of decorator arguments in this example actually limits its utility. For one thing, annotation only works under Python 3.X, so 2.X is no longer supported; function decorators with arguments, on the other hand, work in both versions.

More importantly, by moving the validation specifications into the def header, we essentially commit the function to a single role -- since annotation allows us to code only one expression per argument, it can have only one purpose. For instance, we cannot use range-test annotations for any other role.

By contrast, because decorator arguments are coded outside the function itself, they are both easier to remove and more general -- the code of the function itself does not imply a single decoration purpose. Crucially, by nesting decorators with arguments, we can apply multiple augmentation steps to the same function; annotation directly supports only one. With decorator arguments, the function itself also retains a simpler, normal appearance.

Still, if you have a single purpose in mind, and you can commit to supporting 3.X only, the choice between annotation and decorator arguments is largely stylistic and subjective. As is so often true in life, one person's decoration or annotation may well be another's syntactic clutter!

## Other Applications: Type Testing (If You Insist!)
The coding pattern we've arrived at for processing arguments in decorators could be applied in other contexts. Checking argument data types at development time, for example, is a straightforward extension:
> ```python
> def typetest(**argchecks):
>     def onDecorator(func):
>         ...
>         def onCall(*pargs, **kargs):
>             positionals = list(allargs)[:len(pargs)]
>             for (argname, type) in argchecks.items():
>                 if argname in kargs:
>                     if not isinstance(kargs[argname], type):
>                         ...
>                         raise TypeError(errmsg)
>                 elif argname in positionals:
>                     position = positionals.index(argname)
>                     if not isinstance(pargs[position], type):
>                         ...
>                         raise TypeError(errmsg)
>                 else:
>                     # Assume not passed: default
>             return func(*pargs, **kargs)
>         return onCall
>     return onDecorator
> 
> @typetest(a=int, c=float)
> def func(a, b, c, d): 			# func = typetest(...)(func)
>     ...
> 
> func(1, 2, 3.0, 4) 				# OK
> func('spam', 2, 99, 4) 			# Triggers exception correctly
> ```

Using function annotations instead of decorator arguments for such a decorator, as described in the prior section, would make this look even more like type declarations in other languages:
> ```python
> @typetest
> def func(a: int, b, c: float, d): # func = typetest(func)
>     ... 							# Gasp!...
> ```

But we're getting dangerously close to triggering a "flag on the play" here. As you should have learned in this book, this particular role is generally a bad idea in working code, and, much like private declarations, is not at all Pythonic (and is often a symptom of an ex-C++ programmer's first attempts to use Python).

Type testing restricts your function to work on specific types only, instead of allowing it to operate on any types with compatible interfaces. In effect, it limits your code and breaks its flexibility. On the other hand, every rule has exceptions; type checking may come in handy in isolated cases while debugging and when interfacing with code written in more restrictive languages, such as C++.

Still, this general pattern of argument processing might also be applicable in a variety of less controversial roles. We might even generalize further by passing in a test function, much as we did to add Public decorations earlier; a single copy of this sort of code would then suffice for both range and type testing, and perhaps other similar goals. In fact, we will generalize this way in the end-of-chapter quiz coming up, so we'll leave this extension as a cliffhanger here.

