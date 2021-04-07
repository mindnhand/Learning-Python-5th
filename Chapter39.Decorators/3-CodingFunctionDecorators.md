# Coding Function Decorators
On to the code -- in the rest of this chapter, we are going to study working examples that demonstrate the decorator concepts we just explored. This section presents a handful of function decorators at work, and the next shows class decorators in action. Following that, we'll close out with some larger case studies of class and function decorator usage -- complete implementations of class privacy and argument range tests.

## Tracing Calls
To get started, let's revive the call tracer example we met in Chapter 32. The following defines and applies a function decorator that counts the number of calls made to the decorated function and prints a trace message for each call:
> ```python
> # File decorator1.py
> class tracer:
>     def __init__(self, func): 		# On @ decoration: save original func
>         self.calls = 0
>         self.func = func
>     def __call__(self, *args): 		# On later calls: run original func
>         self.calls += 1
>         print('call %s to %s' % (self.calls, self.func.__name__))
>         self.func(*args)
> 
> @tracer
> def spam(a, b, c): 		# spam = tracer(spam)
>     print(a + b + c) 		# Wraps spam in a decorator object
> ```

Notice how each function decorated with this class will create a new instance, with its own saved function object and calls counter. Also observe how the *args argument syntax is used to pack and unpack arbitrarily many passed-in arguments. This generality enables this decorator to be used to wrap any function with any number of positional arguments; this version doesn't yet work on keyword arguments or class-level methods, and doesn't return results, but we'll fix these shortcomings later in this section.

Now, if we import this module's function and test it interactively, we get the following sort of behavior -- each call generates a trace message initially, because the decorator class intercepts it. This code runs as is under both Python 2.X and 3.X, as does all code in this chapter unless otherwise noted (I've made prints version-neutral, and decorators do not require new-style classes; some hex addresses have also been shortened to protect the sighted):
> ```python
> >>> from decorator1 import spam
> >>> spam(1, 2, 3) 		# Really calls the tracer wrapper object
> call 1 to spam
> 6
> >>> spam('a', 'b', 'c') 	# Invokes __call__ in class
> call 2 to spam
> abc
> >>> spam.calls 			# Number calls in wrapper state information
> 2
> >>> spam
> <decorator1.tracer object at 0x02D9A730>
> ```

When run, the tracer class saves away the decorated function, and intercepts later calls to it, in order to add a layer of logic that counts and prints each call. Notice how the total number of calls shows up as an attribute of the decorated function -- spam is really an instance of the tracer class when decorated, a finding that may have ramifications for programs that do type checking, but is generally benign (decorators might copy the original function's \_\_name\_\_, but such forgery is limited, and could lead to confusion).

For function calls, the @ decoration syntax can be more convenient than modifying each call to account for the extra logic level, and it avoids accidentally calling the original function directly. Consider a nondecorator equivalent such as the following:
> ```python
> calls = 0
> def tracer(func, *args):
>     global calls
>     calls += 1
>     print('call %s to %s' % (calls, func.__name__))
>     func(*args)
> 
> def spam(a, b, c):
>     print(a, b, c)
> 
> >>> spam(1, 2, 3) 			# Normal nontraced call: accidental?
> 1 2 3
> >>> tracer(spam, 1, 2, 3) 	# Special traced call without decorators
> call 1 to spam
> 1 2 3
> ```

This alternative can be used on any function without the special @ syntax, but unlike the decorator version, it requires extra syntax at every place where the function is called in your code. Furthermore, its intent may not be as obvious, and it does not ensure that the extra layer will be invoked for normal calls. Although decorators are never required (we can always rebind names manually), they are often the most convenient and uniform option.

## Decorator State Retention Options
The last example of the prior section raises an important issue. Function decorators have a variety of options for retaining state information provided at decoration time, for use during the actual function call. They generally need to support multiple decorated objects and multiple calls, but there are a number of ways to implement these goals: instance attributes, global variables, nonlocal closure variables, and function attributes can all be used for retaining state.

### Class instance attributes
For example, here is an augmented version of the prior example, which adds support for keyword arguments with \*\* syntax, and returns the wrapped function's result to support more use cases (for nonlinear readers, we first studied keyword arguments in Chapter 18, and for readers working with the book examples package, some filenames in this chapter are again implied by the command-lines that follow their listings):
> 
> > ```python
> > class tracer: 			# State via instance attributes
> >     def __init__(self, func): 		# On @ decorator
> >         self.calls = 0 		# Save func for later call
> >         self.func = func
> >     def __call__(self, *args, **kwargs): 		# On call to original function
> >         self.calls += 1
> >         print('call %s to %s' % (self.calls, self.func.__name__))
> >         return self.func(*args, **kwargs)
> > 
> > @tracer
> > def spam(a, b, c): 		# Same as: spam = tracer(spam)
> >     print(a + b + c) 		# Triggers tracer.__init__
> > 
> > @tracer
> > def eggs(x, y): 			# Same as: eggs = tracer(eggs)
> >     print(x ** y) 		# Wraps eggs in a tracer object
> > 
> > spam(1, 2, 3) 			# Really calls tracer instance: runs tracer.__call__
> > spam(a=4, b=5, c=6) 		# spam is an instance attribute
> > 
> > eggs(2, 16) 				# Really calls tracer instance, self.func is eggs
> > eggs(4, y=4) 				# self.calls is per-decoration here
> > ```
> 
> Like the original, this uses class instance attributes to save state explicitly. Both the wrapped function and the calls counter are per-instance information -- each decoration gets its own copy. When run as a script under either 2.X or 3.X, the output of this version is as follows; notice how the spam and eggs functions each have their own calls counter, because each decoration creates a new class instance:
> 
> > ```powershell
> > c:\code> python decorator2.py
> > call 1 to spam
> > 6
> > call 2 to spam
> > 15
> > call 1 to eggs
> > 65536
> > call 2 to eggs
> > 256
> > ```
> 

While useful for decorating functions, this coding scheme still has issues when applied to methods -- a shortcoming we'll address in a later revision.

### Enclosing scopes and globals
Closure functions -- with enclosing def scope references and nested defs -- can often achieve the same effect, especially for static data like the decorated original function. In this example, though, we would also need a counter in the enclosing scope that changes on each call, and that's not possible in Python 2.X (recall from Chapter 17 that the nonlocal statement is 3.X-only).

In 2.X, we can still use either classes and attributes per the prior section, or other options. Moving state variables out to the global scope with declarations is one candidate, and works in both 2.X and 3.X:
> 
> > ```python
> > calls = 0
> > def tracer(func): 					# State via enclosing scope and global
> >     def wrapper(*args, **kwargs): 	# Instead of class attributes
> >         global calls 					# calls is global, not per-function, so different function decorated 
>                                         # by this decorator will share the same call counter
> >         calls += 1
> >         print('call %s to %s' % (calls, func.__name__))
> >         return func(*args, **kwargs)
> >     return wrapper
> > 
> > @tracer
> > def spam(a, b, c): 			# Same as: spam = tracer(spam)
> >     print(a + b + c)
> > 
> > @tracer
> > def eggs(x, y): 				# Same as: eggs = tracer(eggs)
> >     print(x ** y)
> > 
> > spam(1, 2, 3) 				# Really calls wrapper, assigned to spam
> > spam(a=4, b=5, c=6) 			# wrapper calls spam
> > 
> > eggs(2, 16) 			# Really calls wrapper, assigned to eggs
> > eggs(4, y=4) 			# Global calls is not per-decoration here!
> > ```
> 
> Unfortunately, moving the counter out to the common global scope to allow it to be changed like this also means that it will be shared by every wrapped function. Unlike class instance attributes, global counters are cross-program, not per-function -- the counter is incremented for any traced function call. You can tell the difference if you compare this version's output with the prior version's -- the single, shared global call counter is incorrectly updated by calls to every decorated function:
> 
> > ```python
> > c:\code> python decorator3.py
> > call 1 to spam
> > 6
> > call 2 to spam
> > 15
> > call 3 to eggs
> > 65536
> > call 4 to eggs
> > 256
> > ```
> 

### Enclosing scopes and nonlocals
Shared global state may be what we want in some cases. If we really want a per-function counter, though, we can either use classes as before, or make use of closure (a.k.a. factory) functions and the nonlocal statement in Python 3.X, described in Chapter 17. Because this new statement allows enclosing function scope variables to be changed, they can serve as per-decoration and changeable data. In 3.X only:
> 
> > ```python
> > def tracer(func): 			# State via enclosing scope and nonlocal
> >     calls = 0 					# Instead of class attrs or global
> >     def wrapper(*args, **kwargs): # calls is per-function, not global
> >         nonlocal calls
> >         calls += 1
> >         print('call %s to %s' % (calls, func.__name__))
> >         return func(*args, **kwargs)
> >     return wrapper
> > 
> > @tracer
> > def spam(a, b, c): 			# Same as: spam = tracer(spam)
> >     print(a + b + c)
> > 
> > @tracer
> > def eggs(x, y): 				# Same as: eggs = tracer(eggs)
> >     print(x ** y)
> > 
> > spam(1, 2, 3) 				# Really calls wrapper, bound to func
> > spam(a=4, b=5, c=6) 			# wrapper calls spam
> > 
> > eggs(2, 16) 					# Really calls wrapper, bound to eggs
> > eggs(4, y=4) 					# Nonlocal calls _is_ per-decoration here
> > ```
> 
> Now, because enclosing scope variables are not cross-program globals, each wrapped function gets its own counter again, just as for classes and attributes. Here's the new output when run under 3.X:
> 
> > ```python
> > c:\code> py -3 decorator4.py
> > call 1 to spam
> > 6
> > call 2 to spam
> > 15
> > call 1 to eggs
> > 65536
> > call 2 to eggs
> > 256
> > ```
> 

### Function attributes
Finally, if you are not using Python 3.X and don't have a nonlocal statement -- or you want your code to work portably on both 3.X and 2.X -- you may still be able to avoid globals and classes by making use of function attributes for some changeable state instead.

In all Pythons since 2.1, we can assign arbitrary attributes to functions to attach them, with func.attr=value. Because a factory function makes a new function on each call, its attributes become per-call state. Moreover, you need to use this technique only for state variables that must change; enclosing scope references are still retained and work normally.

In our example, we can simply use wrapper.calls for state. The following works the same as the preceding nonlocal version because the counter is again per-decoratedfunction, but it also runs in Python 2.X:
> 
> > ```python
> > def tracer(func): 					# State via enclosing scope and func attr
> >     def wrapper(*args, **kwargs): 	# calls is per-function, not global
> >         wrapper.calls += 1
> >         print('call %s to %s' % (wrapper.calls, func.__name__))
> >         return func(*args, **kwargs)
> >     wrapper.calls = 0
> >     return wrapper
> > 
> > @tracer
> > def spam(a, b, c): 			# Same as: spam = tracer(spam)
> >     print(a + b + c)
> > 
> > @tracer
> > def eggs(x, y): 				# Same as: eggs = tracer(eggs)
> >     print(x ** y)
> > 
> > spam(1, 2, 3) 				# Really calls wrapper, assigned to spam
> > spam(a=4, b=5, c=6) 			# wrapper calls spam
> > 
> > eggs(2, 16) 					# Really calls wrapper, assigned to eggs
> > eggs(4, y=4) 					# wrapper.calls _is_ per-decoration here
> > ```
> 
> As we learned in Chapter 17, this works only because the name wrapper is retained in the enclosing tracer function's scope. When we later increment wrapper.calls, we are not changing the name wrapper itself, so no nonlocal declaration is required. This version runs in either Python line:
> 
> > ```powershell
> > c:\code> py -2 decorator5.py
> > ...same output as prior version, but works on 2.X too...
> > ```
> 

This scheme was almost relegated to a footnote, because it may be more obscure than nonlocal in 3.X and might be better saved for cases where other schemes don't help. However, function attributes also have substantial advantages. For one, they allow access to the saved state from outside the decorator's code; nonlocals can only be seen inside the nested function itself, but function attributes have wider visibility. For another, they are far more portable; this scheme also works in 2.X, making it versionneutral.

We will employ function attributes again in an answer to one of the end-of-chapter questions, where their visibility outside callables becomes an asset. As changeable state associated with a context of use, they are equivalent to enclosing scope nonlocals. As usual, choosing from multiple tools is an inherent part of the programming task.

Because decorators often imply multiple levels of callables, you can combine functions with enclosing scopes, classes with attributes, and function attributes to achieve a variety of coding structures. As we'll see later, though, this sometimes may be subtler than you expect -- each decorated function should have its own state, and each decorated class may require state both for itself and for each generated instance.

In fact, as the next section will explain in more detail, if we want to apply function decorators to class-level methods, too, we also have to be careful about the distinction Python makes between decorators coded as callable class instance objects and decorators coded as functions.

## Class Blunders I: Decorating Methods
When I wrote the first class-based tracer function decorator in decorator1.py earlier, I naively assumed that it could also be applied to any method -- decorated methods should work the same, I reasoned, but the automatic self instance argument would simply be included at the front of *args. The only real downside to this assumption is that it is completely wrong! When applied to a class's method, the first version of the tracer fails, because self is the instance of the decorator class and the instance of the decorated subject class is not included in *args at all. This is true in both Python 3.X and 2.X.

I introduced this phenomenon earlier in this chapter, but now we can see it in the context of realistic working code. Given the class-based tracing decorator:
> 
> > ```python
> > class tracer:
> >     def __init__(self, func): 			# On @ decorator
> >         self.calls = 0 					# Save func for later call
> >         self.func = func
> >     def __call__(self, *args, **kwargs): # On call to original function
> >         self.calls += 1
> >         print('call %s to %s' % (self.calls, self.func.__name__))
> >         return self.func(*args, **kwargs)
> > ```
> 
> decoration of simple functions works as advertised earlier:
> 
> > ```powershell
> > @tracer
> > def spam(a, b, c): 			# spam = tracer(spam)
> >     print(a + b + c) 		# Triggers tracer.__init__
> > >>> spam(1, 2, 3) 			# Runs tracer.__call__
> > call 1 to spam
> > 6
> > >>> spam(a=4, b=5, c=6) 	# spam saved in an instance attribute
> > call 2 to spam
> > 15
> > ```
> 

However, decoration of class-level methods fails (more lucid sequential readers might recognize this as an adaptation of our Person class resurrected from the object-oriented tutorial in Chapter 28):
> ```python
> class Person:
>     def __init__(self, name, pay):
>         self.name = name
>         self.pay = pay
> 
>     @tracer
>     def giveRaise(self, percent): 			# giveRaise = tracer(giveRaise)
>         self.pay *= (1.0 + percent)
> 
>     @tracer
>     def lastName(self): 						# lastName = tracer(lastName)
>         return self.name.split()[-1]
> 
> >>> bob = Person('Bob Smith', 50000) 			# tracer remembers method funcs
> >>> bob.giveRaise(.25) 						# Runs tracer.__call__(???, .25)
> call 1 to giveRaise
> TypeError: giveRaise() missing 1 required positional argument: 'percent'
> >>> print(bob.lastName()) 					# Runs tracer.__call__(???)
> call 1 to lastName
> TypeError: lastName() missing 1 required positional argument: 'self'
> ```


The root of the problem here is in the self argument of the tracer class's \_\_call\_\_ method -- is it a tracer instance or a Person instance? We really need both as it's coded: the tracer for decorator state, and the Person for routing on to the original method. Really, self must be the tracer object, to provide access to tracer's state information (its calls and func); this is true whether decorating a simple function or a method.

Unfortunately, when our decorated method name is rebound to a class instance object with a \_\_call\_\_, Python passes only the tracer instance to self; it doesn't pass along the Person subject in the arguments list at all. Moreover, because the tracer knows nothing about the Person instance we are trying to process with method calls, there's no way to create a bound method with an instance, and thus no way to correctly dispatch the call. This isn't a bug, but it's wildly subtle.

In the end, the prior listing winds up passing too few arguments to the decorated method, and results in an error. Add a line to the decorator's \_\_call\_\_ to print all its arguments to verify this -- as you can see, self is the tracer instance, and the Person instance is entirely absent:
> ```python
> >>> bob.giveRaise(.25)
> <__main__.tracer object at 0x02A486D8> (0.25,) {}
> call 1 to giveRaise
> Traceback (most recent call last):
> File "<stdin>", line 1, in <module>
> File "<stdin>", line 9, in __call__
> TypeError: giveRaise() missing 1 required positional argument: 'percent'
> ```

As mentioned earlier, this happens because Python passes the implied subject instance to self when a method name is bound to a simple function only; when it is an instance of a callable class, that class's instance is passed instead. Technically, Python makes a bound method object containing the subject instance only when the method is a simple function, not when it is a callable instance of another class.

### Using nested functions to decorate methods
If you want your function decorators to work on both simple functions and class-level methods, the most straightforward solution lies in using one of the other state retention solutions described earlier -- code your function decorator as nested defs, so that you don't depend on a single self instance argument to be both the wrapper class instance and the subject class instance.

The following alternative applies this fix using Python 3.X nonlocals; recode this to use function attributes for the changeable calls to use in 2.X. Because decorated methods are rebound to simple functions instead of instance objects, Python correctly passes the Person object as the first argument, and the decorator propagates it on in the first item of *args to the self argument of the real, decorated methods:
> 
> > ```python
> > # A call tracer decorator for both functions and methods
> > def tracer(func): 					# Use function, not class with __call__
> >     calls = 0 						# Else "self" is decorator instance only!
> >     def onCall(*args, **kwargs): 		# Or in 2.X+3.X: use [onCall.calls += 1]
> >         nonlocal calls
> >         calls += 1
> >         print('call %s to %s' % (calls, func.__name__))
> >         return func(*args, **kwargs)
> >     return onCall
> > 
> > 
> > if __name__ == '__main__':
> >     # Applies to simple functions
> >     @tracer
> >     def spam(a, b, c): 			# spam = tracer(spam)
> >         print(a + b + c) 			# onCall remembers spam
> > 
> >     @tracer
> >     def eggs(N):
> >         return 2 ** N
> > 
> >     spam(1, 2, 3) 				# Runs onCall(1, 2, 3)
> >     spam(a=4, b=5, c=6)
> >     print(eggs(32))
> > 
> >     # Applies to class-level method functions too!
> >     class Person:
> >         def __init__(self, name, pay):
> >             self.name = name
> >             self.pay = pay
> > 
> >         @tracer
> >         def giveRaise(self, percent): 			# giveRaise = tracer(giveRaise)
> >             self.pay *= (1.0 + percent) 			# onCall remembers giveRaise
> > 
> >         @tracer
> >         def lastName(self): 		# lastName = tracer(lastName)
> >             return self.name.split()[-1]
> > 
> >     print('methods...')
> >     bob = Person('Bob Smith', 50000)
> >     sue = Person('Sue Jones', 100000)
> >     print(bob.name, sue.name)
> >     sue.giveRaise(.10) 						# Runs onCall(sue, .10)
> >     print(int(sue.pay))
> >     print(bob.lastName(), sue.lastName()) 	# Runs onCall(bob), lastName in scopes
> > ```
> 
> We've also indented the file's self-test code under a \_\_name\_\_ test so the decorator can be imported and used elsewhere. This version works the same on both functions and methods, but runs in 3.X only due to its nonlocal:
> 
> > ```powershell
> c:\code> py -3 calltracer.py
> call 1 to spam
> 6
> call 2 to spam
> 15
> call 1 to eggs
> 4294967296
> methods...
> Bob Smith Sue Jones
> call 1 to giveRaise
> 110000
> call 1 to lastName
> call 2 to lastName
> Smith Jones
> > ```
> 

Trace through these results to make sure you have a handle on this model; the next section provides an alternative to it that supports classes, but is also substantially more complex.

### Using descriptors to decorate methods
Although the nested function solution illustrated in the prior section is the most straightforward way to support decorators that apply to both functions and class-level methods, other schemes are possible. The descriptor feature we explored in the prior chapter, for example, can help here as well.

Recall from our discussion in that chapter that a descriptor is normally a class attribute assigned to an object with a \_\_get\_\_ method run automatically whenever that attribute is referenced and fetched; new-style class object derivation is required for descriptors in Python 2.X, but not 3.X:
> ```python
> class Descriptor(object):
>     def __get__(self, instance, owner): ...
> 
> class Subject:
>     attr = Descriptor()
> 
> X = Subject()
> X.attr 			# Roughly runs Descriptor.__get__(Subject.attr, X, Subject)
> ```

Descriptors may also have \_\_set\_\_ and \_\_del\_\_ access methods, but we don't need them here. More relevant to this chapter's topic, because the descriptor's \_\_get\_\_ method receives both the descriptor class instance and subject class instance when invoked, it's well suited to decorating methods when we need both the decorator's state and the original class instance for dispatching calls. Consider the following alternative tracing decorator, which also happens to be a descriptor when used for a class-level method:
> ```python
> class tracer(object): 			# A decorator+descriptor
>     def __init__(self, func): 		# On @ decorator
>         self.calls = 0 					# Save func for later call
>         self.func = func
>     def __call__(self, *args, **kwargs): 	# On call to original func
>         self.calls += 1
>         print('call %s to %s' % (self.calls, self.func.__name__))
>         return self.func(*args, **kwargs)
>     def __get__(self, instance, owner): 	# On method attribute fetch
>         return wrapper(self, instance)
> 
> class wrapper:
>     def __init__(self, desc, subj): 		# Save both instances
>         self.desc = desc 					# Route calls back to deco/desc
>         self.subj = subj
>     def __call__(self, *args, **kwargs):
>         return self.desc(self.subj, *args, **kwargs) 		# Runs tracer.__call__
> 
> @tracer
> def spam(a, b, c): 			# spam = tracer(spam)
>     ...same as prior... 		# Uses __call__ only
> 
> class Person:
>     @tracer
>     def giveRaise(self, percent): 		# giveRaise = tracer(giveRaise)
>         ...same as prior... 				# Makes giveRaise a descriptor
> ```

This works the same as the preceding nested function coding. Its operation varies by usage context:
- Decorated functions invoke only its \_\_call\_\_, and never invoke its \_\_get\_\_.
- Decorated methods invoke its \_\_get\_\_ first to resolve the method name fetch (on I.method); the object returned by \_\_get\_\_ retains the subject class instance and is then invoked to complete the call expression, thereby triggering the decorator's \_\_call\_\_ (on ()).

For example, the test code's call to:
> ```python
> sue.giveRaise(.10) 		# Runs __get__ then __call__
> ```
runs tracer.\_\_get\_\_ first, because the giveRaise attribute in the Person class has been rebound to a descriptor by the method function decorator. The call expression then triggers the \_\_call\_\_ method of the returned wrapper object, which in turn invokes tracer.\_\_call\_\_. In other words, decorated method calls trigger a four-step process:
> ```python
> tracer.__get__, followed by three call operations -- wrapper.__call__,
> tracer.__call__, and finally the original wrapped method.
> ```

The wrapper object retains both descriptor and subject instances, so it can route control back to the original decorator/descriptor class instance. In effect, the wrapper object saves the subject class instance available during method attribute fetch and adds it to the later call's arguments list, which is passed to the decorator\_\_call\_\_. Routing the call back to the descriptor class instance this way is required in this application so that all calls to a wrapped method use the same calls counter state information in the descriptor instance object.

Alternatively, we could use a nested function and enclosing scope references to achieve the same effect -- the following version works the same as the preceding one, by swapping a class and object attributes for a nested function and scope references. It requires noticeably less code, but follows the same four-step process on each decorated method call:
> ```python
> class tracer(object):
>     def __init__(self, func): 			# On @ decorator
>         self.calls = 0 					# Save func for later call
>         self.func = func
> 
>     def __call__(self, *args, **kwargs): 	# On call to original func
>         self.calls += 1
>         print('call %s to %s' % (self.calls, self.func.__name__))
>         return self.func(*args, **kwargs)
> 
>     def __get__(self, instance, owner): 	# On method fetch
>         def wrapper(*args, **kwargs): 	# Retain both inst
>             return self(instance, *args, **kwargs) 		# Runs __call__
>         return wrapper
> ```

Add print statements to these alternatives' methods to trace the multistep get/call process on your own, and run them with the same test code as in the nested function alternative shown earlier (see file calltracer-descr.py for their source). In either coding, this descriptor-based scheme is also substantially subtler than the nested function option, and so is probably a second choice here. To be more blunt, if its complexity doesn't send you screaming into the night, its performance costs probably should! Still, this may be a useful coding pattern in other contexts.

It's also worth noting that we might code this descriptor-based decorator more simply as follows, but it would then apply only to methods, not to simple functions -- an intrinsic limitation of attribute descriptors (and just the inverse of the problem we're trying to solve: application to both functions and methods)
> ```python
> class tracer(object): 			# For methods, but not functions!
>     def __init__(self, meth): 	# On @ decorator
>         self.calls = 0
>         self.meth = meth
> 
>     def __get__(self, instance, owner): 		# On method fetch
>         def wrapper(*args, **kwargs): 		# On method call: proxy with self+inst
>             self.calls += 1
>             print('call %s to %s' % (self.calls, self.meth.__name__))
>             return self.meth(instance, *args, **kwargs)
>         return wrapper
> 
> class Person:
>     @tracer 			# Applies to class methods
>     def giveRaise(self, percent): 			# giveRaise = tracer(giveRaise)
>         ... 			# Makes giveRaise a descriptor
> 
> @tracer 				# But fails for simple functions
> def spam(a, b, c): 	# spam = tracer(spam)
>     ... 				# No attribute fetch occurs here
> ```

In the rest of this chapter we're going to be fairly casual about using classes or functions to code our function decorators, as long as they are applied only to functions. Some decorators may not require the instance of the original class, and will still work on both functions and methods if coded as a class -- something like Python's own `staticmethod` decorator, for example, wouldn't require an instance of the subject class (indeed, its whole point is to remove the instance from the call).

The moral of this story, though, is that if you want your decorators to work on both simple functions and methods, you're probably better off using the nested-functionbased coding pattern outlined here instead of a class with call interception.

## Timing Calls
To sample the fuller flavor of what function decorators are capable of, let's turn to a different use case. Our next decorator times calls made to a decorated function -- both the time for one call, and the total time among all calls. The decorator is applied to two functions, in order to compare the relative speed of list comprehensions and the map built-in call:
> ```python
> # File timerdeco1.py
> # Caveat: range still differs - a list in 2.X, an iterable in 3.X
> # Caveat: timer won't work on methods as coded (see quiz solution)
> import time, sys
> force = list if sys.version_info[0] == 3 else (lambda X: X)
> class timer:
>     def __init__(self, func):
>         self.func = func
>         self.alltime = 0
>     def __call__(self, *args, **kargs):
>         start = time.clock()
>         result = self.func(*args, **kargs)
>         elapsed = time.clock() - start
>         self.alltime += elapsed
>         print('%s: %.5f, %.5f' % (self.func.__name__, elapsed, self.alltime))
>         return result
> 
> @timer
> def listcomp(N):
>     return [x * 2 for x in range(N)]
> 
> @timer
> def mapcall(N):
>     return force(map((lambda x: x * 2), range(N)))
> 
> result = listcomp(5) 				# Time for this call, all calls, return value
> listcomp(50000)
> listcomp(500000)
> listcomp(1000000)
> print(result)
> print('allTime = %s' % listcomp.alltime) 			# Total time for all listcomp calls
> print('')
> result = mapcall(5)
> mapcall(50000)
> mapcall(500000)
> mapcall(1000000)
> print(result)
> print('allTime = %s' % mapcall.alltime) 			# Total time for all mapcall calls
> print('\nmapcomp = %s' % round(mapcall.alltime / listcomp.alltime, 3))
> ```

When run in either Python 3.X or 2.X, the output of this file's self-test code is as follows -- giving for each function call the function name, time for this call, and time for all calls so far, along with the first call's return value, cumulative time for each function, and the map-to-comprehension time ratio at the end:
> ```powershell
> c:\code> py -3 timerdeco1.py
> listcomp: 0.00001, 0.00001
> listcomp: 0.00499, 0.00499
> listcomp: 0.05716, 0.06215
> listcomp: 0.11565, 0.17781
> [0, 2, 4, 6, 8]
> allTime = 0.17780527629411225
> mapcall: 0.00002, 0.00002
> mapcall: 0.00988, 0.00990
> mapcall: 0.10601, 0.11591
> mapcall: 0.21690, 0.33281
> [0, 2, 4, 6, 8]
> allTime = 0.3328064956447921
> **map/comp = 1.872
> ```

Times vary per Python line and test machine, of course, and cumulative time is available as a class instance attribute here. As usual, map calls are almost twice as slow as list comprehensions when the latter can avoid a function call (or equivalently, its requirement of function calls can make map slower).

### Decorators versus per-call timing
For comparison, see Chapter 21 for a nondecorator approach to timing iteration alternatives like these. As a review, we saw two per-call timing techniques there, homegrown and library -- here deployed to time the 1M list comprehension case of the decorator's test code, though incurring extra costs for management code including an outer loop and function calls:
> ```python
> >>> def listcomp(N): [x * 2 for x in range(N)]
> >>> import timer 				# Chapter 21 techniques
> >>> timer.total(1, listcomp, 1000000)
> (0.1461295268088542, None)
> >>> import timeit
> >>> timeit.timeit(number=1, stmt=lambda: listcomp(1000000))
> 0.14964829430189397
> ```

In this specific case, a nondecorator approach would allow the subject functions to be used with or without timing, but it would also complicate the call signature when timing is desired -- we'd need to add code at every call instead of once at the def. Moreover, in the nondecorator scheme there would be no direct way to guarantee that all list builder calls in a program are routed through timer logic, short of finding and potentially changing them all. This may make it difficult to collect cumulative data for all calls.

In general, decorators may be preferred when functions are already deployed as part of a larger system, and may not be easily passed to analysis functions at calls. On the other hand, because decorators charge each call to a function with augmentation logic, a nondecorator approach may be better if you wish to augment calls more selectively. As usual, different tools serve different roles.

> **Note:** Timer call portability and new options in 3.3: Also see Chapter 21's more complete handling and selection of time module functions, as well as its sidebar concerning the new and improved timer functions in this module available as of Python 3.3 (e.g., perf\_counter). We're taking a simplistic approach here for both brevity and version neutrality, but time.clock may not be best on some platforms even prior to 3.3, and platform or version tests may be required outside Windows.
> 

### Testing subtleties
Notice how this script uses its force setting to make it portable between 2.X and 3.X. As described in Chapter 14, the map built-in returns an iterable that generates results on demand in 3.X, but an actual list in 2.X. Hence, 3.X's map by itself doesn't compare directly to a list comprehension's work. In fact, without wrapping it in a list call to force results production, the map test takes virtually no time at all in 3.X -- it returns an iterable without iterating!

At the same time, adding this list call in 2.X too charges map with an unfair penalty -- the map test's results would include the time required to build two lists, not one. To work around this, the script selects a map enclosing function per the Python version number in sys: in 3.X, picking list, and in 2.X using a no-op function that simply returns its input argument unchanged. This adds a very minor constant time in 2.X, which is probably fully overshadowed by the cost of the inner loop iterations in the timed function.

While this makes the comparison between list comprehensions and map more fair in either 2.X or 3.X, because range is also an iterator in 3.X, the results for 2.X and 3.X won't compare directly unless you also hoist this call out of the timed code. They'll be relatively comparable -- and will reflect best practice code in each line anyhow -- but a range iteration adds extra time in 3.X only. For more on all such things, see Chapter 21's benchmark recreations; producing comparable numbers is often a nontrivial task.

Finally, as we did for the tracer decorator earlier, we could make this timing decorator reusable in other modules by indenting the self-test code at the bottom of the file under a \_\_name\_\_ test so it runs only when the file is run, not when it's imported. We won't do this here, though, because we're about to add another feature to our code.

## Adding Decorator Arguments
The timer decorator of the prior section works, but it would be nice if it were more configurable -- providing an output label and turning trace messages on and off, for instance, might be useful in a general-purpose tool like this. Decorator arguments come in handy here: when they're coded properly, we can use them to specify configuration options that can vary for each decorated function. A label, for instance, might be added as follows:
> ```python
> def timer(label=''):
>     def decorator(func):
>         def onCall(*args): 			# Multilevel state retention:
>             ... 						# args passed to function
>             func(*args) 				# func retained in enclosing scope
>             print(label, ... 			# label retained in enclosing scope
>         return onCall
>     return decorator 					# Returns the actual decorator
> 
> @timer('==>') 						# Like listcomp = timer('==>')(listcomp)
> def listcomp(N): ... 					# listcomp is rebound to new onCall
> 
> listcomp(...) 						# Really calls onCall
> ```

This code adds an enclosing scope to retain a decorator argument for use on a later actual call. When the listcomp function is defined, Python really invokes decorator -- the result of timer, run before decoration actually occurs -- with the label value available in its enclosing scope. That is, timer returns the decorator, which remembers both the decorator argument and the original function, and returns the callable onCall, which ultimately invokes the original function on later calls. Because this structure creates new decorator and onCall functions, their enclosing scopes are per-decoration state retention.

We can put this structure to use in our timer to allow a label and a trace control flag to be passed in at decoration time. Here's an example that does just that, coded in a module file named timerdeco2.py so it can be imported as a general tool; it uses a class for the second state retention level instead of a nested function, but the net result is similar:
> ```python
> import time
> def timer(label='', trace=True): 				# On decorator args: retain args
>     class Timer:
>         def __init__(self, func): 			# On @: retain decorated func
>             self.func = func
>             self.alltime = 0
>         def __call__(self, *args, **kargs):  	# On calls: call original
>             start = time.clock()
>             result = self.func(*args, **kargs)
>             elapsed = time.clock() - start
>             self.alltime += elapsed
>             if trace:
>                 format = '%s %s: %.5f, %.5f'
>                 values = (label, self.func.__name__, elapsed, self.alltime)
>                 print(format % values)
>             return result
>     return Timer
> ```

Mostly all we've done here is embed the original Timer class in an enclosing function, in order to create a scope that retains the decorator arguments per deployment. The outer timer function is called before decoration occurs, and it simply returns the Timer class to serve as the actual decorator. On decoration, an instance of Timer is made that remembers the decorated function itself, but also has access to the decorator arguments in the enclosing function scope.

### Timing with decorator arguments
This time, rather than embedding self-test code in this file, we'll run the decorator in a different file. Here's a client of our timer decorator, the module file testseqs.py, applying it to sequence iteration alternatives again:
> ```python
> import sys
> from timerdeco2 import timer
> force = list if sys.version_info[0] == 3 else (lambda X: X)
> 
> @timer(label='[CCC]==>')
> def listcomp(N): 								# Like listcomp = timer(...)(listcomp)
>     return [x * 2 for x in range(N)] 			# listcomp(...) triggers Timer.__call__
> 
> @timer(trace=True, label='[MMM]==>')
> def mapcall(N):
>     return force(map((lambda x: x * 2), range(N)))
> 
> for func in (listcomp, mapcall):
>     result = func(5) 							# Time for this call, all calls, return value
>     func(50000)
>     func(500000)
>     func(1000000)
>     print(result)
>     print('allTime = %s\n' % func.alltime) 	# Total time for all calls
> 
> print('map v.s. comp = %s' % round(mapcall.alltime / listcomp.alltime, 3))
> ```

Again, to make this fair, map is wrapped in a list call in 3.X only. When run as is in 3.X or 2.X, this file prints the following -- each decorated function now has a label of its own defined by decorator arguments, which will be more useful when we need to find trace displays mixed in with a larger program's output:
> ```python
> c:\code> py -3 testseqs.py
> [CCC]==> listcomp: 0.00001, 0.00001
> [CCC]==> listcomp: 0.00504, 0.00505
> [CCC]==> listcomp: 0.05839, 0.06344
> [CCC]==> listcomp: 0.12001, 0.18344
> [0, 2, 4, 6, 8]
> allTime = 0.1834406801777564
> [MMM]==> mapcall: 0.00003, 0.00003
> [MMM]==> mapcall: 0.00961, 0.00964
> [MMM]==> mapcall: 0.10929, 0.11892
> [MMM]==> mapcall: 0.22143, 0.34035
> [0, 2, 4, 6, 8]
> allTime = 0.3403542519173618
> **map/comp = 1.855
> ```

As usual, we can also test interactively to see how the decorator's configuration arguments come into play:
> ```python
> >>> from timerdeco2 import timer
> >>> @timer(trace=False) 			# No tracing, collect total time
> ... def listcomp(N):
> ...     return [x * 2 for x in range(N)]
> ...
> >>> x = listcomp(5000)
> >>> x = listcomp(5000)
> >>> x = listcomp(5000)
> >>> listcomp.alltime
> 0.0037191417530599152
> >>> listcomp
> <timerdeco2.timer.<locals>.Timer object at 0x02957518>
> >>> @timer(trace=True, label='\t=>') 			# Turn on tracing, custom label
> ... def listcomp(N):
> ...     return [x * 2 for x in range(N)]
> ...
> >>> x = listcomp(5000)
> => listcomp: 0.00106, 0.00106
> >>> x = listcomp(5000)
> => listcomp: 0.00108, 0.00214
> >>> x = listcomp(5000)
> => listcomp: 0.00107, 0.00321
> >>> listcomp.alltime
> 0.003208920466562404
> ```

As is, this timing function decorator can be used for any function, both in modules and interactively. In other words, it automatically qualifies as a general-purpose tool for timing code in our scripts. Watch for another example of decorator arguments in the section "Implementing Private Attributes" on page 1314, and again in "A Basic Range-Testing Decorator for Positional Arguments".  

> **Supporting methods:** This section's timer decorator works on any function, but a minor rewrite is required to be able to apply it to class-level methods too. In short, as our earlier section "Class Blunders I: Decorating Methods" on page 1289 illustrated, it must avoid using a nested class. Because this mutation was deliberately reserved to be a subject of one of our end-of-chapter quiz questions, though, I'll avoid giving away the answer completely here.
> 
