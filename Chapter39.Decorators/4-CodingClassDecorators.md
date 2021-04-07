# Coding Class Decorators
So far we've been coding function decorators to manage function calls, but as we've seen, decorators have been extended to work on classes too as of Python 2.6 and 3.0. As described earlier, while similar in concept to function decorators, class decorators are applied to classes instead -- they may be used either to manage classes themselves, or to intercept instance creation calls in order to manage instances. Also like function decorators, class decorators are really just optional syntactic sugar, though many believe that they make a programmer's intent more obvious and minimize erroneous or missed calls.

## Singleton Classes
Because class decorators may intercept instance creation calls, they can be used to either manage all the instances of a class, or augment the interfaces of those instances. To demonstrate, here's a first class decorator example that does the former -- managing all instances of a class. This code implements the classic singleton coding pattern, where at most one instance of a class ever exists. Its singleton function defines and returns a function for managing instances, and the @ syntax automatically wraps up a subject class in this function:
> ```python
> # 3.X and 2.X: global table
> instances = {}
> def singleton(aClass): 					# On @ decoration
>     def onCall(*args, **kwargs): 			# On instance creation
>         if aClass not in instances: 		# One dict entry per class
>             instances[aClass] = aClass(*args, **kwargs)
>         return instances[aClass]
>     return onCall
> ```

To use this, decorate the classes for which you want to enforce a single-instance model (for reference, all the code in this section is in the file singletons.py):
> ```python
> @singleton 				# Person = singleton(Person)
> class Person: 			# Rebinds Person to onCall
>     def __init__(self, name, hours, rate): 	# onCall remembers Person
>         self.name = name
>         self.hours = hours
>         self.rate = rate
>     def pay(self):
>         return self.hours * self.rate
> 
> @singleton 				# Spam = singleton(Spam)
> class Spam: 				# Rebinds Spam to onCall
>     def __init__(self, val): 	# onCall remembers Spam
>         self.attr = val
> 
> bob = Person('Bob', 40, 10) 	# Really calls onCall
> print(bob.name, bob.pay())
> 
> sue = Person('Sue', 50, 20) 	# Same, single object
> print(sue.name, sue.pay())
> 
> X = Spam(val=42) # One Person, one Spam
> Y = Spam(99)
> print(X.attr, Y.attr)
> ```

Now, when the Person or Spam class is later used to create an instance, the wrapping logic layer provided by the decorator routes instance construction calls to onCall, which in turn ensures a single instance per class, regardless of how many construction calls are made. Here's this code's output (2.X prints extra tuple parentheses):
> ```powershell
> c:\code> python singletons.py
> Bob 400
> Bob 400
> 42 42
> ```

### Coding alternatives
Interestingly, you can code a more self-contained solution here if you're able to use the nonlocal statement (available in Python 3.X only) to change enclosing scope names, as described earlier -- the following alternative achieves an identical effect, by using one enclosing scope per class, instead of one global table entry per class. It works the same, but it does not depend on names in the global scope outside the decorator (note that the None check could use is instead of == here, but it’s a trivial test either way):
> ```python
> # 3.X only: nonlocal
> def singleton(aClass): 				# On @ decoration
>     instance = None
>     def onCall(*args, **kwargs): 		# On instance creation
>         nonlocal instance 			# 3.X and later nonlocal
>         if instance == None:
>             instance = aClass(*args, **kwargs) 		# One scope per class
>         return instance
>     return onCall
> ```

In either Python 3.X or 2.X (2.6 and later), you can also code a self-contained solution with either function attributes or a class instead. The first of the following codes the former, leveraging the fact that there will be one onCall function per decoration -- the object namespace serves the same role as an enclosing scope. The second uses one instance per decoration, rather than an enclosing scope, function object, or global table.

In fact, the second relies on the same coding pattern that we will later see is a common decorator class blunder -- here we want just one instance, but that's not usually the case:
> ```python
> # 3.X and 2.X: func attrs, classes (alternative codings)
> def singleton(aClass): 				# On @ decoration
>     def onCall(*args, **kwargs): 		# On instance creation
>         if onCall.instance == None:
>             onCall.instance = aClass(*args, **kwargs) 		# One function per class
>         return onCall.instance
>     onCall.instance = None
>     return onCall
> 
> class singleton:
>     def __init__(self, aClass): 		# On @ decoration
>         self.aClass = aClass
>         self.instance = None
>     def __call__(self, *args, **kwargs): 		# On instance creation
>         if self.instance == None:
>             self.instance = self.aClass(*args, **kwargs) 		# One instance per class
>         return self.instance
> ```

To make this decorator a fully general-purpose tool, choose one, store it in an importable module file, and indent the self-test code under a \_\_name\_\_ check -- steps we'll leave as suggested exercise. The final class-based version offers a portability and explicit option, with extra structure that may better support later evolution, but OOP might not be warranted in all contexts.

## Tracing Object Interfaces
The singleton example of the prior section illustrated using class decorators to manage all the instances of a class. Another common use case for class decorators augments the interface of each generated instance. Class decorators can essentially install on instances a wrapper or "proxy" logic layer that manages access to their interfaces in some way.

For example, in Chapter 31, the \_\_getattr\_\_ operator overloading method is shown as a way to wrap up entire object interfaces of embedded instances, in order to implement the delegation coding pattern. We saw similar examples in the managed attribute coverage of the prior chapter. Recall that \_\_getattr\_\_ is run when an undefined attribute name is fetched; we can use this hook to intercept method calls in a controller class and propagate them to an embedded object.

For reference, here's the original nondecorator delegation example, working on two built-in type objects:
> ```python
> class Wrapper:
>     def __init__(self, object):
>         self.wrapped = object 			# Save object
>     def __getattr__(self, attrname):
>         print('Trace:', attrname) 		# Trace fetch
>         return getattr(self.wrapped, attrname) 		# Delegate fetch
> 
> >>> x = Wrapper([1,2,3]) 			# Wrap a list
> >>> x.append(4) 					# Delegate to list method
> Trace: append
> >>> x.wrapped 					# Print my member
> [1, 2, 3, 4]
> >>> x = Wrapper({"a": 1, "b": 2}) # Wrap a dictionary
> >>> list(x.keys()) 				# Delegate to dictionary method
> Trace: keys 						# Use list() in 3.X
> ['a', 'b']
> ```

In this code, the Wrapper class intercepts access to any of the wrapped object's named attributes, prints a trace message, and uses the getattr built-in to pass off the request to the wrapped object. Specifically, it traces attribute accesses made outside the wrapped object's class; accesses inside the wrapped object's methods are not caught and run normally by design. This whole-interface model differs from the behavior of function decorators, which wrap up just one specific method.

### Tracing interfaces with class decorators
Class decorators provide an alternative and convenient way to code this \_\_getattr\_\_ technique to wrap an entire interface. As of both 2.6 and 3.0, for example, the prior class example can be coded as a class decorator that triggers wrapped instance creation, instead of passing a premade instance into the wrapper's constructor (also augmented here to support keyword arguments with \*\*kargs and to count the number of accesses made to illustrate changeable state):
> ```python
> def Tracer(aClass): 			# On @ decorator
>     class Wrapper:
>         def __init__(self, *args, **kargs): 			# On instance creation
>             self.fetches = 0
>             self.wrapped = aClass(*args, **kargs) 	# Use enclosing scope name
>         def __getattr__(self, attrname):
>             print('Trace: ' + attrname) 				# Catches all but own attrs
>             self.fetches += 1
> 			  # This will trigger an infinite loop
>             return getattr(self.wrapped, attrname) 	# Delegate to wrapped obj, WARNING: THIS WILL TRIGGER AN INFINIT LOOP!!!
>     return Wrapper
> 
> if __name__ == '__main__':
>     @Tracer
>     class Spam: 				# Spam = Tracer(Spam)
>         def display(self): 		# Spam is rebound to Wrapper
>             print('Spam!' * 8)
> 
>     @Tracer
>     class Person: 			# Person = Tracer(Person)
>         def __init__(self, name, hours, rate): 		# Wrapper remembers Person
>             self.name = name
>             self.hours = hours
>             self.rate = rate
>         def pay(self): 		# Accesses outside class traced
>             return self.hours * self.rate 			# In-method accesses not traced
> 
>     food = Spam() 			# Triggers Wrapper()
>     food.display() 			# Triggers __getattr__
>     print([food.fetches])
>     bob = Person('Bob', 40, 50) 		# bob is really a Wrapper
>     print(bob.name) 			# Wrapper embeds a Person
>     print(bob.pay())
>     print('')
>     sue = Person('Sue', rate=100, hours=60) 			# sue is a different Wrapper
>     print(sue.name) 			# with a different Person
>     print(sue.pay())
>     print(bob.name) 			# bob has different state
>     print(bob.pay())
>     print([bob.fetches, sue.fetches]) 				# Wrapper attrs not traced
> ```

It's important to note that this is very different from the tracer decorator we met earlier (despite the name!). In "Coding Function Decorators", we looked at decorators that enabled us to trace and time calls to a given function or method. In contrast, by intercepting instance creation calls, the class decorator here allows us to trace an entire object interface -- that is, accesses to any of the instance's attributes. The following is the output produced by this code under both 3.X and 2.X (2.6 and later): attribute fetches on instances of both the Spam and Person classes invoke the \_\_getattr\_\_ logic in the Wrapper class, because food and bob are really instances of Wrapper, thanks to the decorator's redirection of instance creation calls:
> ```powershell
> c:\code> python interfacetracer.py
> Trace: display
> Spam!Spam!Spam!Spam!Spam!Spam!Spam!Spam!
> [1]
> Trace: name
> Bob
> Trace: pay
> 2000
> Trace: name
> Sue
> Trace: pay
> 6000
> Trace: name
> Bob
> Trace: pay
> 2000
> [4, 2]
> ```

Notice how there is one Wrapper class with state retention per decoration, generated by the nested class statement in the Tracer function, and how each instance gets its own fetches counter by virtue of generating a new Wrapper instance. As we'll see ahead, orchestrating this is trickier than you may expect.

### Applying class decorators to built-in types
Also notice that the preceding decorates a user-defined class. Just like in the original example in Chapter 31, we can also use the decorator to wrap up a built-in type such as a list, as long as we either subclass to allow decoration syntax or perform the decoration manually -- decorator syntax requires a class statement for the @ line. In the following, x is really a Wrapper again due to the indirection of decoration:
> ```python
> >>> from interfacetracer import Tracer
> >>> @Tracer
> ... class MyList(list): pass 			# MyList = Tracer(MyList)
> >>> x = MyList([1, 2, 3]) 			# Triggers Wrapper()
> >>> x.append(4) 						# Triggers __getattr__, append
> Trace: append
> >>> x.wrapped
> [1, 2, 3, 4]
> >>> WrapList = Tracer(list) 			# Or perform decoration manually
> >>> x = WrapList([4, 5, 6]) 			# Else subclass statement required
> >>> x.append(7)
> Trace: append
> >>> x.wrapped
> [4, 5, 6, 7]
> ```

The decorator approach allows us to move instance creation into the decorator itself, instead of requiring a premade object to be passed in. Although this seems like a minor difference, it lets us retain normal instance creation syntax and realize all the benefits of decorators in general. Rather than requiring all instance creation calls to route objects through a wrapper manually, we need only augment class definitions with decorator syntax:
> ```python
> @Tracer 					# Decorator approach
> class Person: ...
> bob = Person('Bob', 40, 50)
> sue = Person('Sue', rate=100, hours=60)
> class Person: ... 		# Nondecorator approach
> bob = Wrapper(Person('Bob', 40, 50))
> sue = Wrapper(Person('Sue', rate=100, hours=60))
> ```

Assuming you will make more than one instance of a class, and want to apply the augmentation to every instance of a class, decorators will generally be a net win in terms of both code size and code maintenance.

> **Attribute version skew note:** The preceding tracer decorator works for explicitly accessed attribute names on all Pythons. As we learned in Chapter 38, Chapter 32, and elsewhere, though, \_\_getattr\_\_ intercepts built-ins' implicit accesses to operator overloading methods like \_\_str\_\_ and \_\_repr\_\_ in Python 2.X's default classic classes, but not in 3.X's new-style classes. In Python 3.X's classes, instances inherit defaults for some, but not all of these names from the class (really, from the object superclass). Moreover, in 3.X, implicitly invoked attributes for built-in operations like printing and + are not routed through \_\_getattr\_\_, or its cousin, \_\_getattribute\_\_. In new-style classes, built-ins start such searches at classes and skip the normal instance lookup entirely.  Here, this means that the \_\_getattr\_\_ based tracing wrapper will automatically trace and propagate operator overloading calls for built-ins in 2.X as coded, but not in 3.X. To see this, display "x" directly at the end of the preceding interactive session -- in 2.X the attribute \_\_repr\_\_ is traced and the list prints as expected, but in 3.X no trace occurs and the list prints using a default display for the Wrapper class:
> ```python
> >>> x 			# 2.X
> Trace: __repr__
> [4, 5, 6, 7]
> >>> x 			# 3.X
> <interfacetracer.Tracer.<locals>.Wrapper object at 0x02946358>
> ```

To work the same in 3.X, operator overloading methods generally must be redefined redundantly in the wrapper class, either by hand, by tools, or by definition in superclasses. We'll see this at work again in a Private decorator later in this chapter -- where we'll also study ways to add the methods required of such code in 3.X.

## Class Blunders II: Retaining Multiple Instances
Curiously, the decorator function in this example can almost be coded as a class instead of a function, with the proper operator overloading protocol. The following slightly simplified alternative works similarly because its \_\_init\_\_ is triggered when the @ decorator is applied to the class, and its \_\_call\_\_ is triggered when a subject class instance is created. Our objects are really instances of Tracer this time, and we essentially just trade an enclosing scope reference for an instance attribute here:
> ```python
> class Tracer:
>     def __init__(self, aClass): 					# On @decorator
>         self.aClass = aClass 						# Use instance attribute
>     def __call__(self, *args): 					# On instance creation
>         self.wrapped = self.aClass(*args) 		# ONE (LAST) INSTANCE PER CLASS!
>         return self
>     def __getattr__(self, attrname):
>         print('Trace: ' + attrname)
>         return getattr(self.wrapped, attrname)
> 
> @Tracer 					# Triggers __init__
> class Spam: 				# Like: Spam = Tracer(Spam)
>     def display(self):
>         print('Spam!' * 8)
> 
> ...
> food = Spam() 			# Triggers __call__
> food.display() 			# Triggers __getattr__
> ```

As we saw in the abstract earlier, though, this class-only alternative handles multiple classes as before, but it won't quite work for multiple instances of a given class: each instance construction call triggers \_\_call\_\_, which overwrites the prior instance. The net effect is that Tracer saves just one instance -- the last one created. Experiment with this yourself to see how, but here's an example of the problem:
> 
> > ```python
> > @Tracer
> > class Person: 					# Person = Tracer(Person)
> >     def __init__(self, name): 	# Wrapper bound to Person
> >     self.name = name
> > 
> > bob = Person('Bob') 				# bob is really a Wrapper
> > print(bob.name) 					# Wrapper embeds a Person
> > Sue = Person('Sue')
> > print(sue.name) 					# sue overwrites bob
> > print(bob.name) 					# OOPS: now bob's name is 'Sue'!
> > ```
> 
> This code's output follows -- because this tracer only has a single shared instance, the second overwrites the first:
> 
> > ```python
> > Trace: name
> > Bob
> > Trace: name
> > Sue
> > Trace: name
> > Sue
> > ```
> 

The problem here is bad state retention -- we make one decorator instance per class, but not per class instance, such that only the last instance is retained. The solution, as in our prior class blunder for decorating methods, lies in abandoning class-based decorators. The earlier function-based Tracer version does work for multiple instances, because each instance construction call makes a new Wrapper instance, instead of overwriting the state of a single shared Tracer instance; the original nondecorator version handles multiple instances correctly for the same reason. The moral here: decorators are not only arguably magical, they can also be incredibly subtle!

## Decorators Versus Manager Functions
Regardless of such subtleties, the Tracer class decorator example ultimately still relies on \_\_getattr\_\_ to intercept fetches on a wrapped and embedded instance object. As we saw earlier, all we've really accomplished is moving the instance creation call inside a class, instead of passing the instance into a manager function. With the original nondecorator tracing example, we would simply code instance creation differently:
> ```python
> class Spam: 					# Nondecorator version
>     ... 						# Any class will do
> 
> food = Wrapper(Spam()) 		# Special creation syntax
> 
> @Tracer
> class Spam: 					# Decorator version
>     ... 						# Requires @ syntax at class
> food = Spam() 				# Normal creation syntax
> ```

Essentially, class decorators shift special syntax requirements from the instance creation call to the class statement itself. This is also true for the singleton example earlier in this section -- rather than decorating a class and using normal instance creation calls, we could simply pass the class and its construction arguments into a manager function:
> ```python
> instances = {}
> def getInstance(aClass, *args, **kwargs):
>     if aClass not in instances:
>         instances[aClass] = aClass(*args, **kwargs)
>     return instances[aClass]
> 
> bob = getInstance(Person, 'Bob', 40, 10) 				# Versus: bob = Person('Bob', 40, 10)
> ```

Alternatively, we could use Python's introspection facilities to fetch the class from an already created instance (assuming creating an initial instance is acceptable):
> ```python
> instances = {}
> def getInstance(object):
>     aClass = object.__class__
>     if aClass not in instances:
>         instances[aClass] = object
>     return instances[aClass]
> 
> bob = getInstance(Person('Bob', 40, 10)) 				# Versus: bob = Person('Bob', 40, 10)
> ```

The same holds true for function decorators like the tracer we wrote earlier: rather than decorating a function with logic that intercepts later calls, we could simply pass the function and its arguments into a manager that dispatches the call:
> ```python
> def func(x, y): 				# Nondecorator version
>     ... 						# def tracer(func, args): ... func(*args)
> result = tracer(func, (1, 2)) # Special call syntax
> 
> @tracer
> def func(x, y): 				# Decorator version
>     ... 						# Rebinds name: func = tracer(func)
> result = func(1, 2) 			# Normal call syntax
> ```

Manager function approaches like this place the burden of using special syntax on calls, instead of expecting decoration syntax at function and class definitions, but also allow you to selectively apply augmentation on a call-by-call basis.

## Why Decorators? (Revisited)
So why did I just show you ways to not use decorators to implement singletons? As I mentioned at the start of this chapter, decorators present us with tradeoffs. Although syntax matters, we all too often forget to ask the "why" questions when confronted with new tools. Now that we’ve seen how decorators actually work, let's step back for a minute to glimpse the big picture here before moving on to more code.

Like most language features, decorators have both pros and cons. For example, in the negatives column, decorators may suffer from three potential drawbacks, which can vary per decorator type:
- **Type changes**
  As we've seen, when wrappers are inserted, a decorated function or class does not retain its original type -- it is rebound to a wrapper (proxy) object, which might matter in programs that use object names or test object types. In the singleton example, both the decorator and manager function approaches retain the original class type for instances; in the tracer code, neither approach does, because wrappers are required. Of course, you should avoid type checks in a polymorphic language like Python anyhow, but there are exceptions to most rules.
- **Extra calls**
  A wrapping layer added by decoration incurs the additional performance cost of an extra call each time the decorated object is invoked -- calls are relatively timeexpensive operations, so decoration wrappers can make a program slower. In the tracer code, both approaches require each attribute to be routed through a wrapper layer; the singleton example avoids extra calls by retaining the original class type.
- **All or nothing**
  Because decorators augment a function or class, they generally apply to every later call to the decorated object. That ensures uniform deployment, but can also be a negative if you'd rather apply an augmentation more selectively on a call-by-call basis.

That said, none of these is a very serious issue. For most programs, decorations' uniformity is an asset, the type difference is unlikely to matter, and the speed hit of the extra calls will be insignificant. Furthermore, the latter of these occurs only when wrappers are used, can often be negated if we simply remove the decorator when optimal performance is required, and is also incurred by nondecorator solutions that add wrapping logic (including metaclasses, as we'll see in Chapter 40).

Conversely, as we saw at the start of this chapter, decorators have three main advantages. Compared to the manager (a.k.a. "helper") function solutions of the prior section, decorators offer:
- **Explicit syntax**
  Decorators make augmentation explicit and obvious. Their @ syntax is easier to recognize than special code in calls that may appear anywhere in a source file -- in our singleton and tracer examples, for instance, the decorator lines seem more likely to be noticed than extra code at calls would be. Moreover, decorators allow function and instance creation calls to use normal syntax familiar to all Python programmers.
- **Code maintenance**
  Decorators avoid repeated augmentation code at each function or class call. Because they appear just once, at the definition of the class or function itself, they obviate redundancy and simplify future code maintenance. For our singleton and tracer cases, we need to use special code at each call to use a manager function approach -- extra work is required both initially and for any modifications that must be made in the future.
- **Consistency**
  Decorators make it less likely that a programmer will forget to use required wrapping logic. This derives mostly from the two prior advantages -- because decoration is explicit and appears only once, at the decorated objects themselves, decorators promote more consistent and uniform API usage than special code that must be included at each call. In the singleton example, for instance, it would be easy to forget to route all class creation calls through special code, which would subvert the singleton management altogether.

Decorators also promote code encapsulation to reduce redundancy and minimize future maintenance effort; although other code structuring tools do too, decorators add explicit structure that makes this natural for augmentation tasks.

None of these benefits completely requires decorator syntax to be achieved, though, and decorator usage is ultimately a stylistic choice. That said, most programmers find them to be a net win, especially as a tool for using libraries and APIs correctly.

> **Historic anecdote:** I can recall similar arguments being made both for and against constructor functions in classes -- prior to the introduction of \_\_init\_\_ methods, programmers achieved the same effect by running an instance through a method manually when creating it (e.g., X=Class().init()). Over time, though, despite being fundamentally a stylistic choice, the \_\_init\_\_ syntax came to be universally preferred because it was more explicit, consistent, and maintainable. Although you should be the judge, decorators seem to bring many of the same assets to the table.
> 
