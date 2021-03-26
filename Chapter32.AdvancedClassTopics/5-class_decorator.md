# Decorators and Metaclasses: Part 1
Because the staticmethod and classmethod call technique described in the prior section initially seemed obscure to some observers, a device was eventually added to make the operation simpler. Python decorators -- similar to the notion and syntax of annotations in Java -- both addressed this specific need and provided a general tool for adding logic that manages both functions and classes, or later calls to them.

This is called a "decoration," but in more concrete terms is really just a way to run extra processing steps at function and class definition time with explicit syntax. It comes in two flavors:
- Function decorators -- the initial entry in this set, added in Python 2.4 -- augment function definitions. They specify special operation modes for both simple functions and classes' methods by wrapping them in an extra layer of logic implemented as another function, usually called a metafunction.
- Class decorators -- a later extension, added in Python 2.6 and 3.0 -- augment class definitions. They do the same for classes, adding support for management of whole objects and their interfaces. Though perhaps simpler, they often overlap in roles with metaclasses.

Function decorators turn out to be very general tools: they are useful for adding many types of logic to functions besides the static and class method use cases. For instance, they may be used to augment functions with code that logs calls made to them, checks the types of passed arguments during debugging, and so on. Function decorators can be used to manage either functions themselves or later calls to them. In the latter mode, function decorators are similar to the delegation design pattern we explored in Chapter 31, but they are designed to augment a specific function or method call, not an entire object interface.

Python provides a few built-in function decorators for operations such as marking static and class methods and defining properties (as sketched earlier, the property built-in works as a decorator automatically), but programmers can also code arbitrary decorators of their own. Although they are not strictly tied to classes, user-defined function decorators often are coded as classes to save the original functions for later dispatch, along with other data as state information.

This proved such a useful hook that it was extended in Python 2.6, 2.7, and 3.X -- class decorators bring augmentation to classes too, and are more directly tied to the class model. Like their function cohorts, class decorators may manage classes themselves or later instance creation calls, and often employ delegation in the latter mode. As we'll find, their roles also often overlap with metaclasses; when they do, the newer class decorators may offer a more lightweight way to achieve the same goals.

## Function Decorator Basics
Syntactically, a function decorator is a sort of runtime declaration about the function that follows. A function decorator is coded on a line by itself just before the def statement that defines a function or method. It consists of the @ symbol, followed by what we call a metafunction -- a function (or other callable object) that manages another function. Static methods since Python 2.4, for example, may be coded with decorator syntax like this:
> ```python
> class C:
>     @staticmethod 				# Function decoration syntax
>     def meth():
>         ...
> ```

Internally, this syntax has the same effect as the following -- passing the function through the decorator and assigning the result back to the original name:
> ```python
> class C:
>     def meth():
>         ...
>     meth = staticmethod(meth) 	# Name rebinding equivalent
> ```

Decoration rebinds the method name to the decorator's result. The net effect is that calling the method function's name later actually triggers the result of its static method decorator first. Because a decorator can return any sort of object, this allows the decorator to insert a layer of logic to be run on every call. The decorator function is free to return either the original function itself, or a new proxy object that saves the original function passed to the decorator to be invoked indirectly after the extra logic layer runs.

With this addition, here's a better way to code our static method example from the prior section in either Python 2.X or 3.X:
> ```python
> class Spam:
>     numInstances = 0
>     def __init__(self):
>         Spam.numInstances = Spam.numInstances + 1
> 
>     @staticmethod
>     def printNumInstances():
>         print("Number of instances created: %s" % Spam.numInstances)
> ```

> ```python
> >>> from spam_static_deco import Spam
> >>> a = Spam()
> >>> b = Spam()
> >>> c = Spam()
> >>> Spam.printNumInstances() 				# Calls from classes and instances work
> Number of instances created: 3
> >>> a.printNumInstances()
> Number of instances created: 3
> ```

Because they also accept and return functions, the classmethod and property built-in functions may be used as decorators in the same way -- as in the following mutation of the prior bothmethods.py:
> ```python
> # File bothmethods_decorators.py
> class Methods(object): 				# object needed in 2.X for property setters
>     def imeth(self, x): 				# Normal instance method: passed a self
>         print([self, x])
> 
>     @staticmethod
>     def smeth(x): 					# Static: no instance passed
>         print([x])
> 
>     @classmethod
>     def cmeth(cls, x): 				# Class: gets class, not instance
>         print([cls, x])
> 
>     @property 						# Property: computed on fetch
>     def name(self):
>         return 'Bob ' + self.__class__.__name__
> ```

> ```python
> >>> from bothmethods_decorators import Methods
> >>> obj = Methods()
> >>> obj.imeth(1)
> [<bothmethods_decorators.Methods object at 0x0000000002A256A0>, 1]
> >>> obj.smeth(2)
> [2]
> >>> obj.cmeth(3)
> [<class 'bothmethods_decorators.Methods'>, 3]
> >>> obj.name
> 'Bob Methods'
> ```

Keep in mind that staticmethod and its kin here are still built-in functions; they may be used in decoration syntax, just because they take a function as an argument and return a callable to which the original function name can be rebound. In fact, any such function can be used in this way -- even user-defined functions we code ourselves, as the next section explains.

## A First Look at User-Defined Function Decorators
Although Python provides a handful of built-in functions that can be used as decorators, we can also write custom decorators of our own. Because of their wide utility, we're going to devote an entire chapter to coding decorators in the final part of this book. As a quick example, though, let's look at a simple user-defined decorator at work.

Recall from Chapter 30 that the \_\_call\_\_ operator overloading method implements a function-call interface for class instances. The following code uses this to define a call proxy class that saves the decorated function in the instance and catches calls to the original name. Because this is a class, it also has state information -- a counter of calls made:
> ```python
> class tracer:
>     def __init__(self, func): 			# Remember original, init counter
>         self.calls = 0
>         self.func = func
> 
>     def __call__(self, *args): 			# On later calls: add logic, run original
>         self.calls += 1
>         print('call %s to %s' % (self.calls, self.func.__name__))
>         return self.func(*args)
> 
> @tracer 					# Same as spam = tracer(spam)
> def spam(a, b, c): 		# Wrap spam in a decorator object
>     return a + b + c
> 
> print(spam(1, 2, 3)) 		# Really calls the tracer wrapper object
> print(spam('a', 'b', 'c')) 		# Invokes __call__ in class
> ```

Because the spam function is run through the tracer decorator, when the original spam name is called it actually triggers the \_\_call\_\_ method in the class. This method counts and logs the call, and then dispatches it to the original wrapped function. Note how the *name argument syntax is used to pack and unpack the passed-in arguments; because of this, this decorator can be used to wrap any function with any number of positional arguments.

The net effect, again, is to add a layer of logic to the original spam function. Here is the script's 3.X and 2.X output -- the first line comes from the tracer class, and the second gives the return value of the spam function itself:
> ```powershell
> c:\code> python tracer1.py
> call 1 to spam
> 6
> call 2 to spam
> abc
> ```

Trace through this example's code for more insight. As it is, this decorator works for any function that takes positional arguments, but it does not handle keyword arguments, and cannot decorate class-level method functions (in short, for methods its \_\_call\_\_ would be passed a tracer instance only). As we'll see in Part VIII, there are a variety of ways to code function decorators, including nested def statements; some of the alternatives are better suited to methods than the version shown here.

For example, by using nested functions with enclosing scopes for state, instead of callable class instances with attributes, function decorators often become more broadly applicable to class-level methods too. We'll postpone the full details on this, but here's a brief look at this closure based coding model; it uses function attributes for counter state for portability, but could leverage variables and nonlocal instead in 3.X only:
> ```python
> def tracer(func): 				# Remember original
>     def oncall(*args): 				# On later calls
>         oncall.calls += 1
>         print('call %s to %s' % (oncall.calls, func.__name__))
>         return func(*args)
>     oncall.calls = 0
>     return oncall
> 
> class C:
>     @tracer
>     def spam(self,a, b, c): return a + b + c
> 
> x = C()
> print(x.spam(1, 2, 3))
> print(x.spam('a', 'b', 'c')) 			# Same output as tracer1 (in tracer2.py)
> ```

## A First Look at Class Decorators and Metaclasses
Function decorators turned out to be so useful that Python 2.6 and 3.0 expanded the model, allowing decorators to be applied to classes as well as functions. In short, class decorators are similar to function decorators, but they are run at the end of a class statement to rebind a class name to a callable. As such, they can be used to either manage classes just after they are created, or insert a layer of wrapper logic to manage instances when they are later created. Symbolically, the code structure:
>
> > ```python
> > def decorator(aClass): ...
> > 
> > @decorator 				# Class decoration syntax
> > class C: ...
> > ```
> 
> is mapped to the following equivalent:
> 
> > ```python
> > def decorator(aClass): ...
> > 
> > class C: ... 			# Name rebinding equivalent
> > C = decorator(C)
> > ```
> 

The class decorator is free to augment the class itself, or return a proxy object that intercepts later instance construction calls. For example, in the code of the section "Counting instances per class with class methods" on page 1033, we could use this hook to automatically augment the classes with instance counters and any other data required:
> ```python
> def count(aClass):
>     aClass.numInstances = 0
>     return aClass 				# Return class itself, instead of a wrapper
> 
> @count
> class Spam: ... 					# Same as Spam = count(Spam)
> 
> @count
> class Sub(Spam): ... 				# numInstances = 0 not needed here
> 
> @count
> class Other(Spam): ...
> ```

In fact, as coded, this decorator can be applied to class or functions -- it happily returns the object being defined in either context after initializing the object's attribute: 
> ```python
> @count
> def spam(): pass 					# Like spam = count(spam)
> 
> @count
> class Other: pass 				# Like Other = count(Other)
> 
> spam.numInstances 				# Both are set to zero
> Other.numInstances
> 

Though this decorator manages a function or class itself, as we'll see later in this book, class decorators can also manage an object's entire interface by intercepting construction calls, and wrapping the new instance object in a proxy that deploys attribute accessor tools to intercept later requests -- a multilevel coding technique we'll use to implement class attribute privacy in Chapter 39. Here's a preview of the model:
> ```python
> def decorator(cls): 				# On @ decoration
>     class Proxy:
>         def __init__(self, *args): 	# On instance creation: make a cls
>             self.wrapped = cls(*args)
>         def __getattr__(self, name): 	# On attribute fetch: extra ops here
>             return getattr(self.wrapped, name)
>     return Proxy
> 
> @decorator
> class C: ... 						# Like C = decorator(C)
> X = C() 							# Makes a Proxy that wraps a C, and catches later X.attr
> ```

Metaclasses, mentioned briefly earlier, are a similarly advanced class-based tool whose roles often intersect with those of class decorators. They provide an alternate model, which routes the creation of a class object to a subclass of the top-level type class, at the conclusion of a class statement:
> ```python
> class Meta(type):
>     def __new__(meta, classname, supers, classdict):
>         ...extra logic + class creation via type call...
> 
> class C(metaclass=Meta):
>     ...my creation routed to Meta... 				# Like C = Meta('C', (), {...})
> ```

In Python 2.X, the effect is the same, but the coding differs -- use a class attribute instead of a keyword argument in the class header:
> ```python
> class C:
>     __metaclass__ = Meta
>     ... my creation routed to Meta...
> ```

In either line, Python calls a class's metaclass to create the new class object, passing in the data defined during the class statement's run; in 2.X, the metaclass simply defaults to the classic class creator:
> ```python
> classname = Meta(classname, superclasses, attributedict)
> ```

To assume control of the creation or initialization of a new class object, a metaclass generally redefines the \_\_new\_\_ or \_\_init\_\_ method of the type class that normally intercepts this call. The net effect, as with class decorators, is to define code to be run automatically at class creation time. Here, this step binds the class name to the result of a call to a user-defined metaclass. In fact, a metaclass need not be a class at all -- a possibility we'll explore later that blurs some of the distinction between this tool and decorators, and may even qualify the two as functionally equivalent in many roles.

Both schemes, class decorators and metaclasses, are free to augment a class or return an arbitrary object to replace it -- a protocol with almost limitless class-based customization possibilities. As we'll see later, metaclasses may also define methods that process their instance classes, rather than normal instances of them -- a technique that's similar to class methods, and might be emulated in spirit by methods and data in class decorator proxies, or even a class decorator that returns a metaclass instance. Such mindbinding concepts will require Chapter 40's conceptual groundwork (and quite possibly sedation!).

## For More Details
Naturally, there's much more to the decorator and metaclass stories than I've shown here. Although they are a general mechanism whose usage may be required by some packages, coding new user-defined decorators and metaclasses is an advanced topic of interest primarily to tool writers, not application programmers. Because of this, we'll defer additional coverage until the final and optional part of this book:
- Chapter 38 shows how to code properties using function decorator syntax in more depth.
- Chapter 39 has much more on decorators, including more comprehensive examples.
- Chapter 40 covers metaclasses, and more on the class and instance management story.

Although these chapters cover advanced topics, they'll also provide us with a chance to see Python at work in more substantial examples than much of the rest of the book was able to provide. For now, let's move on to our final class-related topic.

