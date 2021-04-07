# The Basics
Let's get started with a first-pass look at decoration behavior from a symbolic perspective. We'll write real and more substantial code soon, but since most of the magic of decorators boils down to an automatic rebinding operation, it's important to understand this mapping first.

## Function Decorators
Function decorators have been available in Python since version 2.4. As we saw earlier in this book, they are largely just syntactic sugar that runs one function through another at the end of a def statement, and rebinds the original function name to the result.

### Usage
A function decorator is a kind of runtime declaration about the function whose definition follows. The decorator is coded on a line just before the def statement that defines a function or method, and it consists of the @ symbol followed by a reference to a metafunction -- a function (or other callable object) that manages another function. In terms of code, function decorators automatically map the following syntax:
> 
> > ```python
> > @decorator 		# Decorate function
> > def F(arg):
> >     ...
> > F(99) 			# Call function
> > ```
> 
> into this equivalent form, where decorator is a one-argument callable object that returns a callable object with the same number of arguments as F (in not F itself):
> 
> > ```python
> > def F(arg):
> >     ...
> > F = decorator(F) 		# Rebind function name to decorator result
> > F(99) 				# Essentially calls decorator(F)(99)
> > ```
> 

This automatic name rebinding works on any def statement, whether it's for a simple function or a method within a class. When the function F is later called, it's actually calling the object returned by the decorator, which may be either another object that implements required wrapping logic, or the original function itself.

In other words, decoration essentially maps the first of the following into the second -- though the decorator is really run only once, at decoration time:
> ```python
> func(6, 7)
> decorator(func)(6, 7)
> ```

This automatic name rebinding accounts for the static method and property decoration syntax we met earlier in the book:
> ```python
> class C:
>     @staticmethod
>     def meth(...): ... 		# meth = staticmethod(meth)
> class C:
>     @property
>     def name(self): ... 		# name = property(name)
> ```

In both cases, the method name is rebound to the result of a built-in function decorator, at the end of the def statement. Calling the original name later invokes whatever object the decorator returns. In these specific cases, the original names are rebound to a static method router and property descriptor, but the process is much more general than this -- as the next section explains.

### Implementation
A decorator itself is a callable that returns a callable. That is, it returns the object to be called later when the decorated function is invoked through its original name -- either a wrapper object to intercept later calls, or the original function augmented in someway. In fact, decorators can be any type of callable and return any type of callable: any combination of functions and classes may be used, though some are better suited to certain contexts.

For example, to tap into the decoration protocol in order to manage a function just after it is created, we might code a decorator of this form:
> ```python
> def decorator(F):
>     # Process function F
>     return F
> 
> @decorator
> def func(): ... # func = decorator(func)
> ```

Because the original decorated function is assigned back to its name, this simply adds a post-creation step to function definition. Such a structure might be used to register a function to an API, assign function attributes, and so on. In more typical use, to insert logic that intercepts later calls to a function, we might code a decorator to return a different object than the original function -- a proxy for later calls:
> ```python
> def decorator(F):
>     # Save or use function F
>     # Return a different callable: nested def, class with __call__, etc.
> 
> @decorator
> def func(): ... # func = decorator(func)
> ```

This decorator is invoked at decoration time, and the callable it returns is invoked when the original function name is later called. The decorator itself receives the decorated function; the callable returned receives whatever arguments are later passed to the decorated function's name. When coded properly, this works the same for class-level methods: the implied instance object simply shows up in the first argument of the returned callable.

In skeleton terms, here's one common coding pattern that captures this idea -- the decorator returns a wrapper that retains the original function in an enclosing scope:
> ```python
> def decorator(F): 				# On @ decoration
>     def wrapper(*args): 			# On wrapped function call
>         # Use F and args
>         # F(*args) calls original function
>     return wrapper
> 
> @decorator 			# func = decorator(func)
> def func(x, y): 		# func is passed to decorator's F
>     ...
> 
> func(6, 7) 			# 6, 7 are passed to wrapper's *args
> ```

When the name func is later called, it really invokes the wrapper function returned by decorator; the wrapper function can then run the original func because it is still available in an enclosing scope. When coded this way, each decorated function produces a new scope to retain state.

To do the same with classes, we can overload the call operation and use instance attributes instead of enclosing scopes:
> ```python
> class decorator:
>     def __init__(self, func): 			# On @ decoration
>     self.func = func
>     def __call__(self, *args): 			# On wrapped function call
>         # Use self.func and args
>         # self.func(*args) calls original function
> 
> @decorator
> def func(x, y): 		# func = decorator(func)
>     ... 				# func is passed to __init__
> 
> func(6, 7) 			# 6, 7 are passed to __call__'s *args
> ```

When the name func is later called now, it really invokes the \_\_call\_\_ operator overloading method of the instance created by decorator; the \_\_call\_\_ method can then run the original func because it is still available in an instance attribute. When coded this way, each decorated function produces a new instance to retain state.

### Supporting method decoration
One subtle point about the prior class-based coding is that while it works to intercept simple function calls, it does not quite work when applied to class-level method functions:
> ```python
> class decorator:
>     def __init__(self, func): 		# func is method without instance
>         self.func = func
>     def __call__(self, *args): 		# self is decorator instance
>         # self.func(*args) fails! 	# C instance not in args!
> 
> class C:
>     @decorator
>     def method(self, x, y): 			# method = decorator(method)
>         ... 				# Rebound to decorator instance
> ```

When coded this way, the decorated method is rebound to an instance of the decorator class, instead of a simple function. The problem with this is that the self in the decorator's \_\_call\_\_ receives the decorator class instance when the method is later run, and the instance of class C is never included in *args. This makes it impossible to dispatch the call to the original method -- the decorator object retains the original method function, but it has no instance to pass to it.

To support both functions and methods, the nested function alternative works better:
> ```python
> def decorator(F): 			# F is func or method without instance
>     def wrapper(*args): 		# class instance in args[0] for method
>         # F(*args) runs func or method
>         return wrapper
> 
> @decorator
> def func(x, y): 		# func = decorator(func)
>     ...
> 
> func(6, 7) 			# Really calls wrapper(6, 7)
> 
> class C:
>     @decorator
>     def method(self, x, y): 		# method = decorator(method)
>         ... 			# Rebound to simple function
> 
> X = C()
> X.method(6, 7) 		# Really calls wrapper(X, 6, 7)
> ```

When coded this way wrapper receives the C class instance in its first argument, so it can dispatch to the original method and access state information.

Technically, this nested-function version works because Python creates a bound method object and thus passes the subject class instance to the self argument only when a method attribute references a simple function; when it references an instance of a callable class instead, the callable class's instance is passed to self to give the callable class access to its own state information. We'll see how this subtle difference can matter in more realistic examples later in this chapter.

Also note that nested functions are perhaps the most straightforward way to support decoration of both functions and methods, but not necessarily the only way. The prior chapter's descriptors, for example, receive both the descriptor and subject class instance when called. Though more complex, later in this chapter we'll see how this tool can be leveraged in this context as well.

## Class Decorators
Function decorators proved so useful that the model was extended to allow class decoration as of Python 2.6 and 3.0. They were initially resisted because of role overlap with metaclasses; in the end, though, they were adopted because they provide a simpler way to achieve many of the same goals.

Class decorators are strongly related to function decorators; in fact, they use the same syntax and very similar coding patterns. Rather than wrapping individual functions or methods, though, class decorators are a way to manage classes, or wrap up instance construction calls with extra logic that manages or augments instances created from a class. In the latter role, they may manage full object interfaces.

### Usage
Syntactically, class decorators appear just before class statements, in the same way that function decorators appear just before def statements. In symbolic terms, for a decorator that must be a one-argument callable that returns a callable, the class decorator syntax:
> 
> > ```python
> > @decorator 		# Decorate class
> > class C:
> >     ...
> > 
> > x = C(99) 		# Make an instance
> > ```
> 
> is equivalent to the following -- the class is automatically passed to the decorator function, and the decorator's result is assigned back to the class name:
> 
> > ```python
> > class C:
> >     ...
> > 
> > C = decorator(C) 		# Rebind class name to decorator result
> > x = C(99) 		# Essentially calls decorator(C)(99)
> > ```
> 

The net effect is that calling the class name later to create an instance winds up triggering the callable returned by the decorator, which may or may not call the original class itself.

### Implementation
New class decorators are coded with many of the same techniques used for function decorators, though some may involve two levels of augmentation -- to manage both instance construction calls, as well as instance interface access. Because a class decorator is also a callable that returns a callable, most combinations of functions and classes suffice.

However it's coded, the decorator's result is what runs when an instance is later created. For example, to simply manage a class just after it is created, return the original class itself:
> ```python
> def decorator(C):
>     # Process class C
>     return C
> 
> @decorator
> class C: ... 			# C = decorator(C)
> ```

To instead insert a wrapper layer that intercepts later instance creation calls, return a different callable object:
> ```python
> def decorator(C):
>     # Save or use class C
>     # Return a different callable: nested def, class with __call__, etc.
> 
> @decorator
> class C: ... 			# C = decorator(C)
> ```

The callable returned by such a class decorator typically creates and returns a new instance of the original class, augmented in some way to manage its interface. For example, the following inserts an object that intercepts undefined attributes of a class instance:
> ```python
> def decorator(cls): 		# On @ decoration
>     class Wrapper:
>         def __init__(self, *args): 		# On instance creation
>             self.wrapped = cls(*args)
>         def __getattr__(self, name): 		# On attribute fetch
>             return getattr(self.wrapped, name)
>     return Wrapper
> 
> @decorator
> class C: 		# C = decorator(C)
>     def __init__(self, x, y): 	# Run by Wrapper.__init__
>         self.attr = 'spam'
> 
> x = C(6, 7) 			# Really calls Wrapper(6, 7)
> print(x.attr) 		# Runs Wrapper.__getattr__, prints "spam"
> ```

In this example, the decorator rebinds the class name to another class, which retains the original class in an enclosing scope and creates and embeds an instance of the original class when it's called. When an attribute is later fetched from the instance, it is intercepted by the wrapper's \_\_getattr\_\_ and delegated to the embedded instance of the original class. Moreover, each decorated class creates a new scope, which remembers the original class. We'll flesh out this example into some more useful code later in this chapter.

Like function decorators, class decorators are commonly coded as either "factory" functions that create and return callables, classes that use \_\_init\_\_ or \_\_call\_\_ methods to intercept call operations, or some combination thereof. Factory functions typically retain state in enclosing scope references, and classes in attributes.

### Supporting multiple instances
As for function decorators, some callable type combinations work better for class decorators than others. Consider the following invalid alternative to the class decorator of the prior example:
> ```python
> class Decorator:
>     def __init__(self, C): 			# On @ decoration
>         self.C = C
>     def __call__(self, *args): 			# On instance creation
>         self.wrapped = self.C(*args)
>         return self
>     def __getattr__(self, attrname): 			# On atrribute fetch
>         return getattr(self.wrapped, attrname)
> 
> @Decorator
> class C: ... 		# C = Decorator(C)
> 
> x = C()
> y = C() 			# Overwrites x!
> ```

This code handles multiple decorated classes (each makes a new Decorator instance) and will intercept instance creation calls (each runs \_\_call\_\_). Unlike the prior version, however, this version fails to handle multiple instances of a given class -- each instance creation call overwrites the prior saved instance. The original version does support multiple instances, because each instance creation call makes a new independent wrapper object. More generally, either of the following patterns supports multiple wrapped instances:
> ```python
> def decorator(C): 			# On @ decoration
>     class Wrapper:
>         def __init__(self, *args): 		# On instance creation: new Wrapper
>             self.wrapped = C(*args) 		# Embed instance in instance
>     return Wrapper
> 
> class Wrapper: ...
> def decorator(C): 			# On @ decoration
>     def onCall(*args): 			# On instance creation: new Wrapper
>         return Wrapper(C(*args)) 			# Embed instance in instance
>     return onCall
> ```

We'll study this phenomenon in a more realistic context later in the chapter too; in practice, though, we must be careful to combine callable types properly to support our intent, and choose state policies wisely.

## Decorator Nesting
Sometimes one decorator isn't enough. For instance, suppose you've coded two function decorators to be used during development -- one to test argument types before function calls, and another to test return value types after function calls. You can use either independently, but what to do if you want to employ both on a single function? What you really need is a way to nest the two, such that the result of one decorator is the function decorated by the other. It's irrelevant which is nested, as long as both steps run on later calls.

To support multiple nested steps of augmentation this way, decorator syntax allows you to add multiple layers of wrapper logic to a decorated function or method. When this feature is used, each decorator must appear on a line of its own. Decorator syntax of this form:
> 
> > ```python
> > @A
> > @B
> > @C
> > def f(...):
> >     ...
> > ```
> 
> runs the same as the following:
> 
> > ```python
> > def f(...):
> >     ...
> > 
> > f = A(B(C(f)))
> > ```
> 

Here, the original function is passed through three different decorators, and the resulting callable object is assigned back to the original name. Each decorator processes the result of the prior, which may be the original function or an inserted wrapper. If all the decorators insert wrappers, the net effect is that when the original function name is called, three different layers of wrapping object logic will be invoked, to augment the original function in three different ways. The last decorator listed is the first applied, and is the most deeply nested when the original function name is later called (insert joke about Python "interior decorators" here).

Just as for functions, multiple class decorators result in multiple nested function calls, and possibly multiple levels and steps of wrapper logic around instance creation calls. For example, the following code:
> 
> > ```python
> > @spam
> > @eggs
> > class C:
> >     ...
> > 
> > X = C()
> > ```python
> 
> is equivalent to the following:
> 
> > class C:
> >     ...
> > 
> > C = spam(eggs(C))
> > X = C()
> > ```
> 

Again, each decorator is free to return either the original class or an inserted wrapper object. With wrappers, when an instance of the original C class is finally requested, the call is redirected to the wrapping layer objects provided by both the spam and eggs decorators, which may have arbitrarily different roles -- they might trace and validate attribute access, for example, and both steps would be run on later requests.

> def d1(F): return F
> def d2(F): return F
> def d3(F): return F
> 
> @d1
> @d2
> @d3
> def func(): 		# func = d1(d2(d3(func)))
>     print('spam')
> 
> func() # Prints "spam"
> ```

The same syntax works on classes, as do these same do-nothing decorators. When decorators insert wrapper function objects, though, they may augment the original function when called -- the following concatenates to its result in the decorator layers, as it runs the layers from inner to outer:
> ```python
> def d1(F): return lambda: 'X' + F()
> def d2(F): return lambda: 'Y' + F()
> def d3(F): return lambda: 'Z' + F()
> 
> @d1
> @d2
> @d3
> def func(): 			# func = d1(d2(d3(func)))
>     return 'spam'
> print(func()) 		# Prints "XYZspam"
> ```

We use lambda functions to implement wrapper layers here (each retains the wrapped function in an enclosing scope); in practice, wrappers can take the form of functions, callable classes, and more. When designed well, decorator nesting allows us to combine augmentation steps in a wide variety of ways.

## Decorator Arguments
Both function and class decorators can also seem to take arguments, although really these arguments are passed to a callable that in effect returns the decorator, which in turn returns a callable. By nature, this usually sets up multiple levels of state retention. The following, for instance:
> 
> > ```python
> > @decorator(A, B)
> > def F(arg):
> >     ...
> > 
> > F(99)
> > ```
> 
> is automatically mapped into this equivalent form, where decorator is a callable that returns the actual decorator. The returned decorator in turn returns the callable run later for calls to the original function name:
> 
> > ```python
> > def F(arg):
> >     ...
> > 
> > F = decorator(A, B)(F) 			# Rebind F to result of decorator's return value
> > F(99) 				# Essentially calls decorator(A, B)(F)(99)
> > ```
> 

Decorator arguments are resolved before decoration ever occurs, and they are usually used to retain state information for use in later calls. The decorator function in this example, for instance, might take a form like the following:
> ```python
> def decorator(A, B):
>     # Save or use A, B
>     def actualDecorator(F):
>         # Save or use function F
>         # Return a callable: nested def, class with __call__, etc.
>         return callable
>     return actualDecorator
> ```

The outer function in this structure generally saves the decorator arguments away as state information, for use in the actual decorator, the callable it returns, or both. This code snippet retains the state information argument in enclosing function scope references, but class attributes are commonly used as well.

In other words, decorator arguments often imply three levels of callables: a callable to accept decorator arguments, which returns a callable to serve as decorator, which returns a callable to handle calls to the original function or class. Each of the three levels may be a function or class and may retain state in the form of scopes or class attributes.

Decorator arguments can be used to provide attribute initialization values, call trace message labels, attribute names to be validated, and much more -- any sort of configuration parameter for objects or their proxies is a candidate. We'll see concrete examples of decorator arguments employed later in this chapter.

## Decorators Manage Functions and Classes, Too
Although much of the rest of this chapter focuses on wrapping later calls to functions and classes, it's important to remember that the decorator mechanism is more general than this -- it is a protocol for passing functions and classes through any callable immediately after they are created. As such, it can also be used to invoke arbitrary postcreation processing:
> ```python
> def decorator(O):
>     # Save or augment function or class O
>     return O
> 
> @decorator
> def F(): ... 			# F = decorator(F)
> 
> @decorator
> class C: ... 			# C = decorator(C)
> ```

As long as we return the original decorated object this way instead of a proxy, we can manage functions and classes themselves, not just later calls to them. We'll see more realistic examples later in this chapter that use this idea to register callable objects to an API with decoration and assign attributes to functions when they are created.


