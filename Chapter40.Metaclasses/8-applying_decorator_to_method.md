# Example: Applying Decorators to Methods
As we saw in the prior section, because they are both run at the end of a class statement, metaclasses and decorators can often be used interchangeably, albeit with different syntax. The choice between the two is arbitrary in many contexts. It's also possible to use them in combination, as complementary tools. In this section, we'll explore an example of just such a combination -- applying a function decorator to all the methods of a class.

## Tracing with Decoration Manually
In the prior chapter we coded two function decorators, one that traced and counted all calls made to a decorated function and another that timed such calls. They took various forms there, some of which were applicable to both functions and methods and some of which were not. The following collects both decorators' final forms into a module file for reuse and reference here:
> ```python
> # File decotools.py: assorted decorator tools
> import time
> 
> def tracer(func): 				# Use function, not class with __call__
>     calls = 0 					# Else self is decorator instance only
>     def onCall(*args, **kwargs):
>         nonlocal calls
>         calls += 1
>         print('call %s to %s' % (calls, func.__name__))
>         return func(*args, **kwargs)
>     return onCall
> 
> def timer(label='', trace=True): 	# On decorator args: retain args
>     def onDecorator(func): 		# On @: retain decorated func
>         def onCall(*args, **kargs): 		# On calls: call original
>             start = time.clock() 			# State is scopes + func attr
>             result = func(*args, **kargs)
>             elapsed = time.clock() - start
>             onCall.alltime += elapsed
>             if trace:
>                 format = '%s%s: %.5f, %.5f'
>                 values = (label, func.__name__, elapsed, onCall.alltime)
>                 print(format % values)
>             return result
>         onCall.alltime = 0
>         return onCall
>     return onDecorator
> ```

As we learned in the prior chapter, to use these decorators manually, we simply import them from the module and code the decoration @ syntax before each method we wish to trace or time:
> 
> > ```python
> > from decotools import tracer
> > 
> > class Person:
> >     @tracer
> >     def __init__(self, name, pay):
> >         self.name = name
> >         self.pay = pay
> > 
> >     @tracer
> >     def giveRaise(self, percent): 			# giveRaise = tracer(giverRaise)
> >         self.pay *= (1.0 + percent) 			# onCall remembers giveRaise
> > 
> >     @tracer
> >     def lastName(self): 						# lastName = tracer(lastName)
> >         return self.name.split()[-1]
> > 
> > bob = Person('Bob Smith', 50000)
> > sue = Person('Sue Jones', 100000)
> > print(bob.name, sue.name)
> > sue.giveRaise(.10) 							# Runs onCall(sue, .10)
> > print('%.2f' % sue.pay)
> > print(bob.lastName(), sue.lastName()) 		# Runs onCall(bob), remembers lastName
> > ```
> 
> When this code is run, we get the following output -- calls to decorated methods are routed to logic that intercepts and then delegates the call, because the original method names have been bound to the decorator:
> 
> > ```python
> > c:\code> py -3 decoall-manual.py
> > call 1 to __init__
> > call 2 to __init__
> > Bob Smith Sue Jones
> > call 1 to giveRaise
> > 110000.00
> > call 1 to lastName
> > call 2 to lastName
> > Smith Jones
> > ```
> 

## Tracing with Metaclasses and Decorators
The manual decoration scheme of the prior section works, but it requires us to add decoration syntax before each method we wish to trace and to later remove that syntax when we no longer desire tracing. If we want to trace every method of a class, this can become tedious in larger programs. In more dynamic contexts where augmentations depend upon runtime parameters, it may not be possible at all. It would be better if we could somehow apply the tracer decorator to all of a class's methods automatically.

With metaclasses, we can do exactly that -- because they are run when a class is constructed, they are a natural place to add decoration wrappers to a class's methods. By scanning the class's attribute dictionary and testing for function objects there, we can automatically run methods through the decorator and rebind the original names to the results. The effect is the same as the automatic method name rebinding of decorators, but we can apply it more globally:
> 
> > ```python
> > # Metaclass that adds tracing decorator to every method of a client class
> > from types import FunctionType
> > from decotools import tracer
> > 
> > class MetaTrace(type):
> >     def __new__(meta, classname, supers, classdict):
> >         for attr, attrval in classdict.items():
> >             if type(attrval) is FunctionType: 							# Method?
> >                 classdict[attr] = tracer(attrval) 						# Decorate it
> >         return type.__new__(meta, classname, supers, classdict) 		# Make class
> > 
> > class Person(metaclass=MetaTrace):
> >     def __init__(self, name, pay):
> >         self.name = name
> >         self.pay = pay
> > 
> >     def giveRaise(self, percent):
> >         self.pay *= (1.0 + percent)
> > 
> >     def lastName(self):
> >         return self.name.split()[-1]
> > 
> > bob = Person('Bob Smith', 50000)
> > sue = Person('Sue Jones', 100000)
> > print(bob.name, sue.name)
> > sue.giveRaise(.10)
> > print('%.2f' % sue.pay)
> > print(bob.lastName(), sue.lastName())
> > ```
> 
> When this code is run, the results are the same as before -- calls to methods are routed to the tracing decorator first for tracing, and then propagated on to the original method:
> 
> > ```powershell
> > c:\code> py -3 decoall-meta.py
> > call 1 to __init__
> > call 2 to __init__
> > Bob Smith Sue Jones
> > call 1 to giveRaise
> > 110000.00
> > call 1 to lastName
> > call 2 to lastName
> > Smith Jones
> > ```
> 

The result you see here is a combination of decorator and metaclass work -- the metaclass automatically applies the function decorator to every method at class creation time, and the function decorator automatically intercepts method calls in order to print the trace messages in this output. The combination "just works," thanks to the generality of both tools.

## Applying Any Decorator to Methods
The prior metaclass example works for just one specific function decorator -- tracing. However, it's trivial to generalize this to apply any decorator to all the methods of a class. All we have to do is add an outer scope layer to retain the desired decorator, much like we did for decorators in the prior chapter. The following, for example, codes such a generalization and then uses it to apply the tracer decorator again:
> 
> > ```python
> > # Metaclass factory: apply any decorator to all methods of a class
> > from types import FunctionType
> > from decotools import tracer, timer
> > 
> > def decorateAll(decorator):
> >     class MetaDecorate(type):
> >         def __new__(meta, classname, supers, classdict):
> >             for attr, attrval in classdict.items():
> >                 if type(attrval) is FunctionType:
> >                     classdict[attr] = decorator(attrval)
> >             return type.__new__(meta, classname, supers, classdict)
> >     return MetaDecorate
> > 
> > class Person(metaclass=decorateAll(tracer)): 			# Apply a decorator to all
> >     def __init__(self, name, pay):
> >         self.name = name
> >         self.pay = pay
> >     def giveRaise(self, percent):
> >         self.pay *= (1.0 + percent)
> >     def lastName(self):
> >         return self.name.split()[-1]
> > 
> > bob = Person('Bob Smith', 50000)
> > sue = Person('Sue Jones', 100000)
> > print(bob.name, sue.name)
> > sue.giveRaise(.10)
> > print('%.2f' % sue.pay)
> > print(bob.lastName(), sue.lastName())
> > ```
> 
> When this code is run as it is, the output is again the same as that of the previous examples -- we're still ultimately decorating every method in a client class with the tracer function decorator, but we're doing so in a more generic fashion:
> 
> > ```powershell
> > c:\code> py -3 decoall-meta-any.py
> > call 1 to __init__
> > call 2 to __init__
> > Bob Smith Sue Jones
> > call 1 to giveRaise
> > 110000.00
> > call 1 to lastName
> > call 2 to lastName
> > Smith Jones
> > ```
> 

Now, to apply a different decorator to the methods, we can simply replace the decorator name in the class header line. To use the timer function decorator shown earlier, for example, we could use either of the last two header lines in the following when defining our class -- the first accepts the timer's default arguments, and the second specifies label text:
> 
> > ```python
> > class Person(metaclass=decorateAll(tracer)): 					# Apply tracer
> > class Person(metaclass=decorateAll(timer())): 					# Apply timer, defaults
> > class Person(metaclass=decorateAll(timer(label='**'))): 		# Decorator arguments
> > ```
> 
> Notice that this scheme cannot support nondefault decorator arguments differing per method in the client class, but it can pass in decorator arguments that apply to all such methods, as done here. To test, use the last of these metaclass declarations to apply the timer, and add the following lines at the end of the script to see the timer's extra informational attributes:
> 
> > ```python
> > # If using timer: total time per method
> > print('-'*40)
> > print('%.5f' % Person.__init__.alltime)
> > print('%.5f' % Person.giveRaise.alltime)
> > print('%.5f' % Person.lastName.alltime)
> > ```
> 
> The new output is as follows -- the metaclass wraps methods in timer decorators now, so we can tell how long each and every call takes, for every method of the class:
> 
> > ```powershell
> > c:\code> py -3 decoall-meta-any2.py
> > **__init__: 0.00001, 0.00001
> > **__init__: 0.00001, 0.00001
> > Bob Smith Sue Jones
> > **giveRaise: 0.00002, 0.00002
> > 110000.00
> > **lastName: 0.00002, 0.00002
> > **lastName: 0.00002, 0.00004
> > Smith Jones
> > ----------------------------------------
> > 0.00001
> > 0.00002
> > 0.00004
> > ```
> 

## Metaclasses Versus Class Decorators: Round 3 (and Last)
As you might expect, class decorators intersect with metaclasses here, too. The following version replaces the preceding example's metaclass with a class decorator. That is, it defines and uses a class decorator that applies a function decorator to all methods of a class. Although the prior sentence may sound more like a Zen statement than a technical description, this all works quite naturally -- Python's decorators support arbitrary nesting and combinations:
> 
> > ```python
> > # Class decorator factory: apply any decorator to all methods of a class
> > from types import FunctionType
> > from decotools import tracer, timer
> > 
> > def decorateAll(decorator):
> >     def DecoDecorate(aClass):
> >         for attr, attrval in aClass.__dict__.items():
> >             if type(attrval) is FunctionType:
> >                 setattr(aClass, attr, decorator(attrval)) 			# Not __dict__
> >         return aClass
> >     return DecoDecorate
> > 
> > @decorateAll(tracer) 					# Use a class decorator
> > class Person: 						# Applies func decorator to methods
> >     def __init__(self, name, pay): 		# Person = decorateAll(..)(Person)
> >         self.name = name 						# Person = DecoDecorate(Person)
> >         self.pay = pay
> >     def giveRaise(self, percent):
> >         self.pay *= (1.0 + percent)
> >     def lastName(self):
> >         return self.name.split()[-1]
> > 
> > bob = Person('Bob Smith', 50000)
> > sue = Person('Sue Jones', 100000)
> > print(bob.name, sue.name)
> > sue.giveRaise(.10)
> > print('%.2f' % sue.pay)
> > print(bob.lastName(), sue.lastName())
> > ```
> 
> 
> When this code is run as it is, the class decorator applies the tracer function decorator to every method and produces a trace message on calls (the output is the same as that of the preceding metaclass version of this example):
> 
> > ```powershell
> > c:\code> py -3 decoall-deco-any.py
> > call 1 to __init__
> > call 2 to __init__
> > Bob Smith Sue Jones
> > call 1 to giveRaise
> > 110000.00
> > call 1 to lastName
> > call 2 to lastName
> > Smith Jones
> > ```
> 

Notice that the class decorator returns the original, augmented class, not a wrapper layer for it (as is common when wrapping instance objects instead). As for the metaclass version, we retain the type of the original class -- an instance of Person is an instance of Person, not of some wrapper class. In fact, this class decorator deals with class creation only; instance creation calls are not intercepted at all.

This distinction can matter in programs that require type testing for instances to yield the original class, not a wrapper. When augmenting a class instead of an instance, class decorators can retain the original class type. The class's methods are not their original functions because they are rebound to decorators, but this is likely less important in practice, and it's true in the metaclass alternative as well.

Also note that, like the metaclass version, this structure cannot support function decorator arguments that differ per method in the decorated class, but it can handle such arguments if they apply to all such methods. To use this scheme to apply the timer decorator, for example, either of the last two decoration lines in the following will suffice if coded just before our class definition -- the first uses decorator argument defaults, and the second provides one explicitly:
> 
> > ```python
> > @decorateAll(tracer) 						# Decorate all with tracer
> > @decorateAll(timer()) 					# Decorate all with timer, defaults
> > @decorateAll(timer(label='@@')) 			# Same but pass a decorator argument
> > ```
> 
> As before, let's use the last of these decorator lines and add the following at the end of the script to test our example with a different decorator (better schemes are possible on both the testing and timing fronts here, of course, but we're at chapter end; improve as desired):
> 
> > ```python
> > # If using timer: total time per method
> > print('-'*40)
> > print('%.5f' % Person.__init__.alltime)
> > print('%.5f' % Person.giveRaise.alltime)
> > print('%.5f' % Person.lastName.alltime)
> > ```
> 
> The same sort of output appears -- for every method we get timing data for each and all calls, but we've passed a different label argument to the timer decorator:
> 
> > ```powershell
> > c:\code> py -3 decoall-deco-any2.py
> > @@__init__: 0.00001, 0.00001
> > @@__init__: 0.00001, 0.00001
> > Bob Smith Sue Jones
> > @@giveRaise: 0.00002, 0.00002
> > 110000.00
> > @@lastName: 0.00002, 0.00002
> > @@lastName: 0.00002, 0.00004
> > Smith Jones
> > ----------------------------------------
> > 0.00001
> > 0.00002
> > 0.00004
> > ```
> 

Finally, it's possible to combine decorators such that each runs per method call, but it will likely require changes to those we've coded here. As is, nesting calls to them directly winds up tracing or timing the other's creation-time application, listing the two on separate lines results in tracing or timing the other's wrapper before running the original method, and metaclasses seem to fare no better on this front:
> ```python
> @decorateAll(tracer(timer(label='@@'))) 			# Traces applying the timer
> class Person:
> 
> @decorateAll(tracer) 								# Traces onCall wrapper, times methods
> @decorateAll(timer(label='@@'))
> class Person:
> 
> @decorateAll(timer(label='@@'))
> @decorateAll(tracer) 								# Times onCall wrapper, traces methods
> class Person:
> ```

Pondering this further will have to remain suggested study -- both because we're out of space and time, and because this may quite possibly be illegal in some states! As you can see, metaclasses and class decorators are not only often interchangeable, but also commonly complementary. Both provide advanced but powerful ways to customize and manage both class and instance objects, because both ultimately allow you to insert code into the class creation process. Although some more advanced applications may be better coded with one or the other, the way you choose or combine these two tools in many cases is largely up to you.



