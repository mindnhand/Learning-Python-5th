# Example: Adding Methods to Classes
In this and the following section, we're going to study examples of two common use cases for metaclasses: adding methods to a class, and decorating all methods automatically. These are just two of the many metaclass roles, which unfortunately will consume the space we have left for this chapter; again, you should consult the Web for more advanced applications. These examples are representative of metaclasses in action, though, and they suffice to illustrate their application.

Moreover, both give us an opportunity to contrast class decorators and metaclasses -- our first example compares metaclass- and decorator-based implementations of class augmentation and instance wrapping, and the second applies a decorator with a metaclass first and then with another decorator. As you'll see, the two tools are often interchangeable, and even complementary.

## Manual Augmentation
Earlier in this chapter, we looked at skeleton code that augmented classes by adding methods to them in various ways. As we saw, simple class-based inheritance suffices if the extra methods are statically known when the class is coded. Composition via object embedding can often achieve the same effect too. For more dynamic scenarios, though, other techniques are sometimes required -- helper functions can usually suffice, but metaclasses provide an explicit structure and minimize the maintenance costs of changes in the future.

Let's put these ideas in action here with working code. Consider the following example of manual class augmentation -- it adds two methods to two classes, after they have been created:
> 
> > ```python
> > # Extend manually - adding new methods to classes
> > class Client1:
> >     def __init__(self, value):
> >         self.value = value
> >     def spam(self):
> >         return self.value * 2
> > 
> > class Client2:
> >     value = 'ni?'
> > 
> > def eggsfunc(obj):
> >     return obj.value * 4
> > def hamfunc(obj, value):
> >     return value + 'ham'
> > 
> > Client1.eggs = eggsfunc
> > Client1.ham = hamfunc
> > 
> > Client2.eggs = eggsfunc
> > Client2.ham = hamfunc
> > 
> > X = Client1('Ni!')
> > print(X.spam())
> > print(X.eggs())
> > print(X.ham('bacon'))
> > 
> > Y = Client2()
> > print(Y.eggs())
> > print(Y.ham('bacon'))
> > ```
> 
> This works because methods can always be assigned to a class after it's been created, as long as the methods assigned are functions with an extra first argument to receive the subject self instance -- this argument can be used to access state information accessible from the class instance, even though the function is defined independently of the class.
> 
> When this code runs, we receive the output of a method coded inside the first class, as well as the two methods added to the classes after the fact:
> 
> > ```powershell
> > c:\code> py -3 extend-manual.py
> > Ni!Ni!
> > Ni!Ni!Ni!Ni!
> > baconham
> > ni?ni?ni?ni?
> > baconham
> > ```
> 

This scheme works well in isolated cases and can be used to fill out a class arbitrarily at runtime. It suffers from a potentially major downside, though: we have to repeat the augmentation code for every class that needs these methods. In our case, it wasn't too onerous to add the two methods to both classes, but in more complex scenarios this approach can be time-consuming and error-prone. If we ever forget to do this consistently, or we ever need to change the augmentation, we can run into problems.

## Metaclass-Based Augmentation
Although manual augmentation works, in larger programs it would be better if we could apply such changes to an entire set of classes automatically. That way, we'd avoid the chance of the augmentation being botched for any given class. Moreover, coding the augmentation in a single location better supports future changes -- all classes in the set will pick up changes automatically.

One way to meet this goal is to use metaclasses. If we code the augmentation in a metaclass, every class that declares that metaclass will be augmented uniformly and correctly and will automatically pick up any changes made in the future. The following code demonstrates:
> 
> > ```python
> > # Extend with a metaclass - supports future changes better
> > def eggsfunc(obj):
> >     return obj.value * 4
> > 
> > def hamfunc(obj, value):
> >     return value + 'ham'
> > 
> > class Extender(type):
> >     def __new__(meta, classname, supers, classdict):
> >         classdict['eggs'] = eggsfunc
> >         classdict['ham'] = hamfunc
> >         return type.__new__(meta, classname, supers, classdict)
> > 
> > class Client1(metaclass=Extender):
> >     def __init__(self, value):
> >         self.value = value
> >     def spam(self):
> >         return self.value * 2
> > 
> > class Client2(metaclass=Extender):
> >     value = 'ni?'
> > 
> > X = Client1('Ni!')
> > print(X.spam())
> > print(X.eggs())
> > print(X.ham('bacon'))
> > 
> > Y = Client2()
> > print(Y.eggs())
> > print(Y.ham('bacon'))
> > ```
> 
> This time, both of the client classes are extended with the new methods because they are instances of a metaclass that performs the augmentation. When run, this version's output is the same as before -- we haven't changed what the code does, we've just refactored it to encapsulate the augmentation more cleanly:
> 
> > ```python
> > c:\code> py -3 extend-meta.py
> > Ni!Ni!
> > Ni!Ni!Ni!Ni!
> > baconham
> > ni?ni?ni?ni?
> > baconham
> > ```
> 

Notice that the metaclass in this example still performs a fairly static task: adding two known methods to every class that declares it. In fact, if all we need to do is always add the same two methods to a set of classes, we might as well code them in a normal superclass and inherit in subclasses. In practice, though, the metaclass structure supports much more dynamic behavior. For instance, the subject class might also be configured based upon arbitrary logic at runtime:
> ```python
> # Can also configure class based on runtime tests
> class MetaExtend(type):
>     def __new__(meta, classname, supers, classdict):
>         if sometest():
>             classdict['eggs'] = eggsfunc1
>         else:
>             classdict['eggs'] = eggsfunc2
>         if someothertest():
>             classdict['ham'] = hamfunc
>         else:
>             classdict['ham'] = lambda *args: 'Not supported'
>         return type.__new__(meta, classname, supers, classdict)
> ```

## Metaclasses Versus Class Decorators: Round 2
Keep in mind again that the prior chapter's class decorators often overlap with this chapter's metaclasses in terms of functionality. This derives from the fact that:
- Class decorators rebind class names to the result of a function at the end of a class statement, after the new class has been created.
- Metaclasses work by routing class object creation through an object at the end of a class statement, in order to create the new class.

Although these are slightly different models, in practice they can often achieve the same goals, albeit in different ways. As you've now seen, class decorators correspond directly to metaclass \_\_init\_\_ methods called to initialize newly created classes. Decorators have no direct analog to the metaclass \_\_new\_\_ (called to make classes in the first place) or to metaclass methods (used to process instance classes), but many or most use cases for these tools do not require these extra steps.

Because of this, both tools in principle can be used to manage both instances of a class and the class itself. In practice, though, metaclasses incur extra steps to manage instances, and decorators incur extra steps to create new classes. Hence, while their roles often overlap, metaclasses are probably best used for class object management. Let's translate these ideas to code.

### Decorator-based augmentation
In pure augmentation cases, decorators can often stand in for metaclasses. For example, the prior section's metaclass example, which adds methods to a class on creation, can also be coded as a class decorator; in this mode, decorators roughly correspond to the \_\_init\_\_ method of metaclasses, since the class object has already been created by the time the decorator is invoked. Also as for metaclasses, the original class type is retained, since no wrapper object layer is inserted. The output of the following, file extenddeco.py, is the same as that of the prior metaclass code:
> ```python
> # Extend with a decorator: same as providing __init__ in a metaclass
> def eggsfunc(obj):
>     return obj.value * 4
> 
> def hamfunc(obj, value):
>     return value + 'ham'
> 
> def Extender(aClass):
>     aClass.eggs = eggsfunc 			# Manages class, not instance
>     aClass.ham = hamfunc 				# Equiv to metaclass __init__
>     return aClass
> 
> @Extender
> class Client1: 						# Client1 = Extender(Client1)
>     def __init__(self, value): 		# Rebound at end of class stmt
>         self.value = value
>     def spam(self):
>         return self.value * 2
> 
> @Extender
> class Client2:
>     value = 'ni?'
>  
> X = Client1('Ni!') 					# X is a Client1 instance
> print(X.spam())
> print(X.eggs())
> print(X.ham('bacon'))
> 
> Y = Client2()
> print(Y.eggs())
> print(Y.ham('bacon'))
> ```

In other words, at least in certain cases, decorators can manage classes as easily as metaclasses. The converse isn't quite so straightforward, though; metaclasses can be used to manage instances, but only with a certain amount of extra magic. The next section demonstrates.

### Managing instances instead of classes
As we've just seen, class decorators can often serve the same class-management role as metaclasses. Metaclasses can often serve the same instance-management role as decorators, too, but this requires extra code and may seem less natural. That is:
- Class decorators can manage both classes and instances, but don't create classes normally.
- Metaclasses can manage both classes and instances, but instances require extra work.

That said, certain applications may be better coded in one or the other. For example, consider the following class decorator example from the prior chapter; it's used to print a trace message whenever any normally named attribute of a class instance is fetched:
> 
> > ```python
> > # Class decorator to trace external instance attribute fetches
> > def Tracer(aClass): 								# On @ decorator
> >     class Wrapper:
> >         def __init__(self, *args, **kargs): 		# On instance creation
> >             self.wrapped = aClass(*args, **kargs) # Use enclosing scope name
> > 
> >         def __getattr__(self, attrname):
> >             print('Trace:', attrname) 			# Catches all but .wrapped
> >             return getattr(self.wrapped, attrname) 		# Delegate to wrapped object
> >     return Wrapper
> > 
> > @Tracer
> > class Person: 				# Person = Tracer(Person)
> >     def __init__(self, name, hours, rate): 		# Wrapper remembers Person
> >         self.name = name
> >         self.hours = hours
> >         self.rate = rate 		# In-method fetch not traced
> >     def pay(self):
> >         return self.hours * self.rate
> > 
> > bob = Person('Bob', 40, 50) 						# bob is really a Wrapper
> > print(bob.name) 				# Wrapper embeds a Person
> > print(bob.pay()) 				# Triggers __getattr__
> > ```
> 
> When this code is run, the decorator uses class name rebinding to wrap instance objects in an object that produces the trace lines in the following output:
> 
> > ```python
> > c:\code> py -3 manage-inst-deco.py
> > Trace: name
> > Bob
> > Trace: pay
> > 2000
> > ```
> 

Although it's possible for a metaclass to achieve the same effect, it seems less straightforward conceptually. Metaclasses are designed explicitly to manage class object creation, and they have an interface tailored for this purpose. To use a metaclass just to manage instances, we have to also take on responsibility for creating the class too -- an extra step if normal class creation would otherwise suffice. The following metaclass, in file manage-inst-meta.py, has the same effect as the prior decorator:
> 
> > ```python
> > # Manage instances like the prior example, but with a metaclass
> > def Tracer(classname, supers, classdict): 				# On class creation call
> >     aClass = type(classname, supers, classdict) 			# Make client class
> >     class Wrapper:
> >         def __init__(self, *args, **kargs): 				# On instance creation
> >             self.wrapped = aClass(*args, **kargs)
> >         def __getattr__(self, attrname):
> >             print('Trace:', attrname) 					# Catches all but .wrapped
> >             return getattr(self.wrapped, attrname) 		# Delegate to wrapped object
> >     return Wrapper
> > 
> > class Person(metaclass=Tracer): 							# Make Person with Tracer
> >     def __init__(self, name, hours, rate): 				# Wrapper remembers Person
> >         self.name = name
> >         self.hours = hours
> >         self.rate = rate 									# In-method fetch not traced
> >     def pay(self):
> >         return self.hours * self.rate
> > 
> > bob = Person('Bob', 40, 50) 								# bob is really a Wrapper
> > print(bob.name) 											# Wrapper embeds a Person
> > print(bob.pay()) 											# Triggers __getattr__
> > ```
> 
> This works, but it relies on two tricks. First, it must use a simple function instead of a class, because type subclasses must adhere to object creation protocols. Second, it must manually create the subject class by calling type manually; it needs to return an instance wrapper, but metaclasses are also responsible for creating and returning the subject class. Really, we're using the metaclass protocol to imitate decorators in this example, rather than vice versa; because both run at the conclusion of a class statement, in many roles they are just variations on a theme. This metaclass version produces the same output as the decorator when run live:
> 
> > ```python
> > c:\code> py -3 manage-inst-meta.py
> > Trace: name
> > Bob
> > Trace: pay
> > 2000
> > ```
> 

You should study both versions of these examples for yourself to weigh their tradeoffs. In general, though, metaclasses are probably best suited to class management, due to their design; class decorators can manage either instances or classes, though they may not be the best option for more advanced metaclass roles that we don't have space to cover in this book. See the Web for more metaclass examples, but keep in mind that some are more appropriate than others (and some of their authors may know less of Python than you do!).

### Metaclass and class decorator equivalence?
The preceding section illustrated that metaclasses incur an extra step to create the class when used in instance management roles, and hence can't quite subsume decorators in all use cases. But what about the inverse -- are decorators a replacement for metaclasses?

Just in case this chapter has not yet managed to make your head explode, consider the following metaclass coding alternative too -- a class decorator that returns a metaclass instance:
> ```python
> # A decorator can call a metaclass, though not vice versa without type()
> >>> class Metaclass(type):
>         def __new__(meta, clsname, supers, attrdict):
>             print('In M.__new__:')
>             print([clsname, supers, list(attrdict.keys())])
>             return type.__new__(meta, clsname, supers, attrdict)
> 
> >>> def decorator(cls):
>         return Metaclass(cls.__name__, cls.__bases__, dict(cls.__dict__))
> 
> >>> class A:
>         x = 1
> >>> @decorator
>     class B(A):
>         y = 2
>         def m(self): 
>             return self.x + self.y
> 
> In M.__new__:
> ['B', (<class '__main__.A'>,), ['__qualname__', '__doc__', 'm', 'y', '__module__']]
> >>> B.x, B.y
> (1, 2)
> >>> I = B()
> >>> I.x, I.y, I.m()
> (1, 2, 3)
> ```

This nearly proves the equivalence of the two tools, but really just in terms of dispatch at class construction time. Again, decorators essentially serve the same role as metaclass \_\_init\_\_ methods. Because this decorator returns a metaclass instance, metaclasses -- or at least their type superclass -- are still assumed here. Moreover, this winds up triggering an additional metaclass call after the class is created, and isn't an ideal scheme in real code -- you might as well move this metaclass to the first creation step:
> ```python
> >>> class B(A, metaclass=Metaclass): ... 				# Same effect, but makes just one class
> ```

Still, there is some tool redundancy here, and decorator and metaclass roles often overlap in practice. And although decorators don't directly support the notion of class-level methods in metaclasses discussed earlier, methods and state in proxy objects created by decorators can achieve similar effects, though for space we'll leave this last observation in the suggested explorations column.

The inverse may not seem applicable -- a metaclass can't generally defer to a nonmetaclass decorator, because the class doesn't yet exist until the metaclass call completes -- although a metaclass can take the form of a simple callable that invokes type to create the class directly and passes it on to the decorator. In other words, the crucial hook in the model is the type call issued for class construction. Given that, metaclasses and class decorators are often functionally equivalent, with varying dispatch protocol models:
> ```python
> >>> def Metaclass(clsname, supers, attrdict):
>         return decorator(type(clsname, supers, attrdict))
> >>> def decorator(cls): ...
> >>> class B(A, metaclass=Metaclass): ... 				# Metas can call decos and vice versa
> ```

In fact, metaclasses need not necessarily return a type instance either -- any object compatible with the class coder's expectations will do—and this further blurs the decorator/metaclass distinction:
> ```python
> >>> def func(name, supers, attrs):
>         return 'spam'
> 
> >>> class C(metaclass=func): 		# A class whose metaclass makes it a string!
>         attr = 'huh?'
> 
> >>> C, C.upper()
> ('spam', 'SPAM')
> 
> >>> def func(cls):
>         return 'spam'
> 
> >>> @func
>     class C: 						# A class whose decorator makes it a string!
>         attr = 'huh?'
> 
> >>> C, C.upper()
> ('spam', 'SPAM')
> ```

Odd metaclass and decorator tricks like these aside, timing often determines roles in practice, as stated earlier:
- Because decorators run after a class is created, they incur an extra runtime step in class creation roles.
- Because metaclasses must create classes, they incur an extra coding step in instance management roles.

In other words, neither completely subsumes the other. Strictly speaking, metaclasses might be a functional superset, as they can call decorators during class creation; but metaclasses can also be substantially heavier to understand and code, and many roles intersect completely. In practice, the need to take over class creation entirely is probably much less important than tapping into the process in general.

Rather than follow this rabbit hole further, though, let's move on to explore metaclass roles that may be a bit more typical and practical. The next section concludes this chapter with one more common use case -- applying operations to a class's methods automatically at class creation time.


