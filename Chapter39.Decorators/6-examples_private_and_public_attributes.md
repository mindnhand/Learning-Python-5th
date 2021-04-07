# Example: "Private" and "Public" Attributes
The final two sections of this chapter present larger examples of decorator use. Both are presented with minimal description, partly because this chapter has hit its size limits, but mostly because you should already understand decorator basics well enough to study these on your own. Being general-purpose tools, these examples give us a chance to see how decorator concepts come together in more useful code.

## Implementing Private Attributes
The following class decorator implements a Private declaration for class instance attributes -- that is, attributes stored on an instance, or inherited from one of its classes. It disallows fetch and change access to such attributes from outside the decorated class, but still allows the class itself to access those names freely within its own methods. It's not exactly C++ or Java, but it provides similar access control as an option in Python.

We saw an incomplete first-cut implementation of instance attribute privacy for changes only in Chapter 30. The version here extends this concept to validate attribute fetches too, and it uses delegation instead of inheritance to implement the model. In fact, in a sense this is just an extension to the attribute tracer class decorator we met earlier.

Although this example utilizes the new syntactic sugar of class decorators to code attribute privacy, its attribute interception is ultimately still based upon the \_\_getattr\_\_ and \_\_setattr\_\_ operator overloading methods we met in prior chapters. When a private attribute access is detected, this version uses the raise statement to raise an exception, along with an error message; the exception may be caught in a try or allowed to terminate the script.

Here is the code, along with a self test at the bottom of the file. It will work under both Python 3.X and 2.X (2.6 and later) because it employs version-neutral print and raise syntax, though as coded it catches built-ins' dispatch to operator overloading method attributes in 2.X only (more on this in a moment):
> ```python
> """
> File access1.py (3.X + 2.X)
> Privacy for attributes fetched from class instances.
> See self-test code at end of file for a usage example.
> Decorator same as: Doubler = Private('data', 'size')(Doubler).
> Private returns onDecorator, onDecorator returns onInstance,
> and each onInstance instance embeds a Doubler instance.
> """
> traceMe = False
> def trace(*args):
>     if traceMe: print('[' + ' '.join(map(str, args)) + ']')
> 
> def Private(*privates): 					# privates in enclosing scope
>     def onDecorator(aClass): 				# aClass in enclosing scope
>         class onInstance: 				# wrapped in instance attribute
>             def __init__(self, *args, **kargs):
>                 self.wrapped = aClass(*args, **kargs)
>             def __getattr__(self, attr): 						# My attrs don't call getattr
>                 trace('get:', attr) 							# Others assumed in wrapped
>                 if attr in privates:
>                     raise TypeError('private attribute fetch: ' + attr)
>                 else:
>                     return getattr(self.wrapped, attr)
>             def __setattr__(self, attr, value): 				# Outside accesses
>                 trace('set:', attr, value) 					# Others run normally
>                 if attr == 'wrapped': 						# Allow my attrs
>                     self.__dict__[attr] = value 				# Avoid looping
>                 elif attr in privates:
>                     raise TypeError('private attribute change: ' + attr)
>                 else:
>                     setattr(self.wrapped, attr, value) 		# Wrapped obj attrs
>         return onInstance 				# Or use __dict__
>     return onDecorator
> 
> if __name__ == '__main__':
>     traceMe = True
>     @Private('data', 'size') 				# Doubler = Private(...)(Doubler)
>     class Doubler:
>         def __init__(self, label, start):
>             self.label = label 			# Accesses inside the subject class
>             self.data = start 			# Not intercepted: run normally
>         def size(self):
>             return len(self.data) 		# Methods run with no checking
>         def double(self): 				# Because privacy not inherited
>             for i in range(self.size()):
>                 self.data[i] = self.data[i] * 2
>         def display(self):
>             print('%s => %s' % (self.label, self.data))
> 
>     X = Doubler('X is', [1, 2, 3])
>     Y = Doubler('Y is', [-10, −20, −30])
> 
>     # The following all succeed
>     print(X.label) 				# Accesses outside subject class
>     X.display(); X.double(); X.display() 		# Intercepted: validated, delegated
>     print(Y.label)
>     Y.display(); Y.double()
>     Y.label = 'Spam'
>     Y.display()
> 
>     # The following all fail properly
>     """
>     print(X.size()) 				# prints "TypeError: private attribute fetch: size"
>     print(X.data)
>     X.data = [1, 1, 1]
>     X.size = lambda S: 0
>     print(Y.data)
>     print(Y.size())
>     """
> ```

When traceMe is True, the module file's self-test code produces the following output. Notice how the decorator catches and validates both attribute fetches and assignments run outside of the wrapped class, but does not catch attribute accesses inside the class itself:
> ```powershell
> c:\code> py -3 access1.py
> [set: wrapped <__main__.Doubler object at 0x00000000029769B0>]
> [set: wrapped <__main__.Doubler object at 0x00000000029769E8>]
> [get: label]
> X is
> [get: display]
> X is => [1, 2, 3]
> [get: double]
> [get: display]
> X is => [2, 4, 6]
> [get: label]
> Y is
> [get: display]
> Y is => [-10, −20, −30]
> [get: double]
> [set: label Spam]
> [get: display]
> Spam => [−20, −40, −60]
> ```

## Implementation Details I
This code is a bit complex, and you're probably best off tracing through it on your own to see how it works. To help you study, though, here are a few highlights worth mentioning.

### Inheritance versus delegation
The first-cut privacy example shown in Chapter 30 used inheritance to mix in a \_\_setattr\_\_ to catch accesses. Inheritance makes this difficult, however, because differentiating between accesses from inside or outside the class is not straightforward (inside access should be allowed to run normally, and outside access should be restricted).

To work around this, the Chapter 30 example requires inheriting classes to use \_\_dict\_\_ assignments to set attributes -- an incomplete solution at best. The version here uses delegation (embedding one object inside another) instead of inheritance; this pattern is better suited to our task, as it makes it much easier to distinguish between accesses inside and outside of the subject class. Attribute accesses from outside the subject class are intercepted by the wrapper layer's overloading methods and delegated to the class if valid. Accesses inside the class itself (i.e., through self within its methods' code) are not intercepted and are allowed to run normally without checks, because privacy is not inherited in this version.

### Decorator arguments
The class decorator used here accepts any number of arguments, to name private attributes. What really happens, though, is that the arguments are passed to the Private function, and Private returns the decorator function to be applied to the subject class. That is, the arguments are used before decoration ever occurs; Private returns the decorator, which in turn "remembers" the privates list as an enclosing scope reference.

### State retention and enclosing scopes
Speaking of enclosing scopes, there are actually three levels of state retention at work in this code:
- The arguments to Private are used before decoration occurs and are retained as an enclosing scope reference for use in both onDecorator and onInstance.
- The class argument to onDecorator is used at decoration time and is retained as an enclosing scope reference for use at instance construction time.
- The wrapped instance object is retained as an instance attribute in the onInstance proxy object, for use when attributes are later accessed from outside the class.
This all works fairly naturally, given Python's scope and namespace rules.

### Using \_\_dict\_\_ and \_\_slots\_\_ (and other virtual names)
The \_\_setattr\_\_ method in this code relies on an instance object's \_\_dict\_\_ attribute namespace dictionary in order to set onInstance's own wrapped attribute. As we learned in the prior chapter, this method cannot assign an attribute directly without looping.

However, it uses the setattr built-in instead of \_\_dict\_\_ to set attributes in the wrapped object itself. Moreover, getattr is used to fetch attributes in the wrapped object, since they may be stored in the object itself or inherited by it.

Because of that, this code will work for most classes -- including those with "virtual" class-level attributes based on slots, properties, descriptors, and even \_\_getattr\_\_ and its ilk. By assuming a namespace dictionary for itself only and using storage-neutral tools for the wrapped object, the wrapper class avoids limitations inherent in other tools.

For example, you may recall from Chapter 32 that new-style classes with \_\_slots\_\_ may not store attributes in a \_\_dict\_\_ (and in fact may not even have one of these at all). However, because we rely on a \_\_dict\_\_ only at the onInstance level here, and not in the wrapped instance, this concern does not apply. In addition, because setattr and getattr apply to attributes based on both \_\_dict\_\_ and \_\_slots\_\_, our decorator applies to classes using either storage scheme. By the same reasoning, the decorator also applies to new-style properties and similar tools: delegated names will be looked up anew in the wrapped instance, irrespective of attributes of the decorator proxy object itself.

## Generalizing for Public Declarations, Too
Now that we have a Private implementation, it's straightforward to generalize the code to allow for Public declarations too -- they are essentially the inverse of Private declarations, so we need only negate the inner test. The example listed in this section allows a class to use decorators to define a set of either Private or Public instance attributes -- attributes of any kind stored on an instance or inherited from its classes -- with the following semantics:
- Private declares attributes of a class's instances that cannot be fetched or assigned, except from within the code of the class's methods. That is, any name declared Private cannot be accessed from outside the class, while any name not declared Private can be freely fetched or assigned from outside the class.
- Public declares attributes of a class's instances that can be fetched or assigned from both outside the class and within the class's methods. That is, any name declared Public can be freely accessed anywhere, while any name not declared Public cannot be accessed from outside the class.

Private and Public declarations are intended to be mutually exclusive: when using Private, all undeclared names are considered Public, and when using Public, all undeclared names are considered Private. They are essentially inverses, though undeclared names not created by a class's methods behave slightly differently -- new names can be assigned and thus created outside the class under Private (all undeclared names are accessible), but not under Public (all undeclared names are inaccessible).

Again, study this code on your own to get a feel for how this works. Notice that this scheme adds an additional fourth level of state retention at the top, beyond that described in the preceding section: the test functions used by the lambdas are saved in an extra enclosing scope. This example is coded to run under either Python 3.X or 2.X (2.6 or later), though it comes with a caveat when run under 3.X (explained briefly in the file's docstring and expanded on after the code):
> 
> > ```python
> > """
> > File access2.py (3.X + 2.X)
> > Class decorator with Private and Public attribute declarations.
> > Controls external access to attributes stored on an instance, or
> > Inherited by it from its classes. Private declares attribute names
> > that cannot be fetched or assigned outside the decorated class,
> > and Public declares all the names that can.
> > Caveat: this works in 3.X for explicitly named attributes only: __X__
> > operator overloading methods implicitly run for built-in operations
> > do not trigger either __getattr__ or __getattribute__ in new-style
> > classes. Add __X__ methods here to intercept and delegate built-ins.
> > """
> > traceMe = False
> > def trace(*args):
> >     if traceMe: print('[' + ' '.join(map(str, args)) + ']')
> > 
> > def accessControl(failIf):
> >     def onDecorator(aClass):
> >         class onInstance:
> >             def __init__(self, *args, **kargs):
> >                 self.__wrapped = aClass(*args, **kargs)
> >             def __getattr__(self, attr):
> >                 trace('get:', attr)
> >                 if failIf(attr):
> >                     raise TypeError('private attribute fetch: ' + attr)
> >                 else:
> >                     return getattr(self.__wrapped, attr)
> >             def __setattr__(self, attr, value):
> >                 trace('set:', attr, value)
> >                 if attr == '_onInstance__wrapped':
> >                     self.__dict__[attr] = value
> >                 elif failIf(attr):
> >                     raise TypeError('private attribute change: ' + attr)
> >                 else:
> >                     setattr(self.__wrapped, attr, value)
> >         return onInstance
> >     return onDecorator
> > 
> > def Private(*attributes):
> >     return accessControl(failIf=(lambda attr: attr in attributes))
> > 
> > def Public(*attributes):
> >     return accessControl(failIf=(lambda attr: attr not in attributes))
> > ```
> 
> See the prior example's self-test code for a usage example. Here's a quick look at these class decorators in action at the interactive prompt; they work the same in 2.X and 3.X for attributes referenced by explicit name like those tested here. As advertised, non-Private or Public names can be fetched and changed from outside the subject class, but Private or non-Public names cannot:
> 
> > ```python
> > >>> from access2 import Private, Public
> > >>> @Private('age') 				# Person = Private('age')(Person)
> >     class Person: 					# Person = onInstance with state
> >         def __init__(self, name, age):
> >             self.name = name
> >             self.age = age 			# Inside accesses run normally
> > 
> > >>> X = Person('Bob', 40)
> > >>> X.name 							# Outside accesses validated
> > 'Bob'
> > >>> X.name = 'Sue'
> > >>> X.name
> > 'Sue'
> > >>> X.age
> > TypeError: private attribute fetch: age
> > >>> X.age = 'Tom'
> > TypeError: private attribute change: age
> > >>> @Public('name')
> >     class Person:
> >         def __init__(self, name, age):
> >             self.name = name
> >             self.age = age
> > 
> > >>> X = Person('bob', 40) 			# X is an onInstance
> > >>> X.name 							# onInstance embeds Person
> > 'bob'
> > >>> X.name = 'Sue'
> > >>> X.name
> > 'Sue'
> > >>> X.age
> > TypeError: private attribute fetch: age
> > >>> X.age = 'Tom'
> > TypeError: private attribute change: age
> 

## Implementation Details II
To help you analyze the code, here are a few final notes on this version. Since this is just a generalization of the preceding section's version, the implementation notes there apply here as well.

### Using \_\_X pseudoprivate names
Besides generalizing, this version also makes use of Python's \_\_X pseudoprivate name mangling feature (which we met in Chapter 31) to localize the wrapped attribute to the proxy control class, by automatically prefixing it with this class's name. This avoids the prior version's risk for collisions with a wrapped attribute that may be used by the real, wrapped class, and it's useful in a general tool like this. It's not quite "privacy," though, because the mangled version of the name can be used freely outside the class.

Notice that we also have to use the fully expanded name string -- '\_onInstance\_\_wrapped' -- as a test value in \_\_setattr\_\_, because that's what Python changes it to.

### Breaking privacy
Although this example does implement access controls for attributes of an instance and its classes, it is possible to subvert these controls in various ways -- for instance, by going through the expanded version of the wrapped attribute explicitly (bob.pay might not work, but the fully mangled bob.\_onInstance\_\_wrapped.pay could!). If you have to explicitly try to do so, though, these controls are probably sufficient for normal intended use. Of course, privacy controls can generally be subverted in other languages if you try hard enough (#define private public may work in some C++ implementations, too). Although access controls can reduce accidental changes, much of this is up to programmers in any language; whenever source code may be changed, airtight access control will always be a bit of a pipe dream.

### Decorator tradeoffs
We could again achieve the same results without decorators, by using manager functions or coding the name rebinding of decorators manually; the decorator syntax, however, makes this consistent and a bit more obvious in the code. The chief potential downsides of this and any other wrapper-based approach are that attribute access incurs an extra call, and instances of decorated classes are not really instances of the original decorated class -- if you test their type with X.__class__ or isinstance(X, C), for example, you'll find that they are instances of the wrapper class. Unless you plan to do introspection on objects' types, though, the type issue is probably irrelevant, and the extra call may apply mostly to development time; as we'll see later, there are ways to remove decorations automatically if desired.

## Open Issues
As is, this example works as planned under both Python 2.X and 3.X for methods called explicitly by name. As with most software, though, there is always room for improvement. Most notably, this tool turns in mixed performance on operator overloading methods if they are used by client classes.

As coded, the proxy class is a classic class when run under 2.X, but a new-style class when run by 3.X. As such, the code supports any client class in 2.X, but in 3.X fails to validate or delegate operator overloading methods dispatched implicitly by built-in operations, unless they are redefined in the proxy. Clients that do not use operator overloading are fully supported, but others may require additional code in 3.X.
Importantly, this is not a new-style class issue here, it's a Python version issue -- the same code runs differently and fails in 3.X only. Because the nature of the wrapped object's class is irrelevant to the proxy, we are concerned only with the proxy's own code, which works under 2.X but not 3.X.

We've met this issue a few times already in this book, but let's take a quick look at its impact on the very realistic code we've written here, and explore a workaround to it.

### Caveat: Implicitly run operator overloading methods fail to delegate under 3.X
Like all delegation-based classes that use \_\_getattr\_\_, this decorator works cross-version for normally named or explicitly called attributes only. When run implicitly by built-in operations, operator overloading methods like \_\_str\_\_ and \_\_add\_\_ work differently for new-style classes. Because this code is interpreted as a new-style class in 3.X only, such operations fail to reach an embedded object that defines them when run under this Python line as currently coded.

As we learned in the prior chapter, built-in operations look for operator overloading names in instances for classic classes, but not for new-style classes -- for the latter, they skip the instance entirely and begin the search for such methods in classes (technically, in the namespace dictionaries of all classes in the instance's tree). Hence, the \_\_X\_\_ operator overloading methods implicitly run for built-in operations do not trigger either \_\_getattr\_\_ or \_\_getattribute\_\_ in new-style classes; because such attribute fetches skip our onInstance class's \_\_getattr\_\_ altogether, they cannot be validated or delegated.

Our decorator's class is not coded as explicitly new-style (by deriving from object), so it will catch operator overloading methods if run under 2.X as a default classic class.

In 3.X, though, because all classes are new-style automatically (and by mandate), such methods will fail if they are implemented by the embedded object -- because they are not caught by the proxy, they won't be passed on. The most direct workaround in 3.X is to redefine redundantly in onInstance all the operator overloading methods that can possibly be used in wrapped objects. Such extra methods can be added by hand, by tools that partly automate the task (e.g., with class decorators or the metaclasses discussed in the next chapter), or by definition in reusable superclasses. Though tedious -- and code-intensive enough to largely omit here -- we'll explore approaches to satisfying this 3.X-only requirement in a moment.

First, though, to see the difference for yourself, try applying the decorator to a class that uses operator overloading methods under 2.X; validations work as before, and both the \_\_str\_\_ method used by printing and the \_\_add\_\_ method run for + invoke the decorator's \_\_getattr\_\_ and hence wind up being validated and delegated to the subject Person object correctly:
> ```powershell
> C:\code> c:\python27\python
> >>> from access2 import Private
> >>> @Private('age')
>     class Person:
>         def __init__(self):
>             self.age = 42
>         def __str__(self):
>             return 'Person: ' + str(self.age)
>         def __add__(self, yrs):
>             self.age += yrs
> 
> >>> X = Person()
> >>> X.age 				# Name validations fail correctly
> TypeError: private attribute fetch: age
> >>> print(X) 				# __getattr__ => runs Person.__str__
> Person: 42
> >>> X + 10 				# __getattr__ => runs Person.__add__
> >>> print(X) 				# __getattr__ => runs Person.__str__
> Person: 52
> ```

When the same code is run under Python 3.X, though, the implicitly invoked \_\_str\_\_ and \_\_add\_\_ skip the decorator's \_\_getattr\_\_ and look for definitions in or above the decorator class itself; print winds up finding the default display inherited from the class type (technically, from the implied object superclass in 3.X), and + generates an error because no default is inherited:
> ```python
> C:\code> c:\python33\python
> >>> from access2 import Private
> >>> @Private('age')
>     class Person:
>         def __init__(self):
>             self.age = 42
>         def __str__(self):
>             return 'Person: ' + str(self.age)
>         def __add__(self, yrs):
>             self.age += yrs
> 
> >>> X = Person() 			# Name validations still work
> >>> X.age 				# But 3.X fails to delegate built-ins!
> TypeError: private attribute fetch: age
> >>> print(X)
> <access2.accessControl.<locals>.onDecorator.<locals>.onInstance object at ...etc>
> >>> X + 10
> TypeError: unsupported operand type(s) for +: 'onInstance' and 'int'
> >>> print(X)
> <access2.accessControl.<locals>.onDecorator.<locals>.onInstance object at ...etc>
> ```

Strangely, this occurs only for dispatch from built-in operations; explicit direct calls to overload methods are routed to \_\_getattr\_\_, though clients using operator overloading can't be expected to do the same:
> ```python
> >>> X.__add__(10) 					# Though calls by name work normally
> >>> X._onInstance__wrapped.age 		# Break privacy to view result...
> 52
> ```

In other words, this is a matter of built-in operations versus explicit calls; it has little to do with the actual names of the methods involved. Just for built-in operations, Python skips a step for 3.X's new-style classes.

Using the alternative \_\_getattribute\_\_ method won't help here -- although it is defined to catch every attribute reference (not just undefined names), it is also not run by builtin operations. Python's property feature, which we met in Chapter 38, won't help directly here either; recall that properties are automatically run code associated with specific attributes defined when a class is written, and are not designed to handle arbitrary attributes in wrapped objects.

### Approaches to redefining operator overloading methods for 3.X
As mentioned earlier, the most straightforward solution under 3.X is to redundantly redefine operator overloading names that may appear in embedded objects in delegation-based classes like our decorator. This isn't ideal because it creates some code redundancy, especially compared to 2.X solutions. However, it isn't an impossibly major coding effort; can be automated to some extent with tools or superclasses; suffices to make our decorator work in 3.X; and may allow operator overloading names to be declared Private or Public too, assuming overloading methods trigger the failIf test internally.

**Inline definition.** For instance, the following is an inline redefinition approach -- add method redefinitions to the proxy for every operator overloading method a wrapped object may define itself, to catch and delegate. We're adding just four operation interceptors to illustrate, but others are similar (new code is in bold font here):
> ```python
> def accessControl(failIf):
>     def onDecorator(aClass):
>         class onInstance:
>             def __init__(self, *args, **kargs):
>                 self.__wrapped = aClass(*args, **kargs)
> 
>             # Intercept and delegate built-in operations specifically
>             def __str__(self):
>                 return str(self.__wrapped)
>             def __add__(self, other):
>                 return self.__wrapped + other # Or getattr(x, '__add__')(y)
>             def __getitem__(self, index):
>                 return self.__wrapped[index] # If needed
>             def __call__(self, *args, **kargs):
>                 return self.__wrapped(*args, **kargs) # If needed
> 
>             # plus any others needed
>             # Intercept and delegate by-name attribute access generically
>             def __getattr__(self, attr): ...
>             def __setattr__(self, attr, value): ...
>         return onInstance
>     return onDecorator
> ```

**Mix-in superclasses.** Alternatively, these methods can be inserted by a common superclass -- given that there are dozens of such methods, an external class may be better suited to the task, especially if it is general enough to be used in any such interface proxy class. Either of the following mix-in class schemes (among likely others) suffice to catch and delegate built-ins operations:
- The first catches built-ins and forcibly reroutes down to the subclass \_\_getattr\_\_. It requires that operator overloading names be public per the decorator's specifications, but built-in operation calls will work the same as both explicit name calls and 2.X's classic classes.
- The second catches built-ins and reroutes to the wrapped object directly. It requires access to and assumes a proxy attribute named \_wrapped giving access to the embedded object -- which is less than ideal because it precludes wrapped objects from using the same name and creates a subclass dependency, but better than using the mangled and class-specific \_onInstance\_\_wrapped, and no worse than a similarly named method.

Like the inline approach, both of these mix-ins also require one method per built-in operation in general tools that proxy arbitrary objects’ interfaces. Notice how these classes catch operation calls rather than operation attribute fetches, and thus must perform the actual operation by delegating a call or expression:
> ```python
> class BuiltinsMixin:
>     def __add__(self, other):
>         return self.__class__.__getattr__(self, '__add__')(other)
>     def __str__(self):
>         return self.__class__.__getattr__(self, '__str__')()
>     def __getitem__(self, index):
>         return self.__class__.__getattr__(self, '__getitem__')(index)
>     def __call__(self, *args, **kargs):
>         return self.__class__.__getattr__(self, '__call__')(*args, **kargs)
>     # plus any others needed
> 
> def accessControl(failIf):
>     def onDecorator(aClass):
>         class onInstance(BuiltinsMixin):
>             ...rest unchanged...
>             def __getattr__(self, attr): ...
>             def __setattr__(self, attr, value): ...
> 
> class BuiltinsMixin:
>     def __add__(self, other):
>         return self._wrapped + other # Assume a _wrapped
>     def __str__(self): # Bypass __getattr__
>         return str(self._wrapped)
>     def __getitem__(self, index):
>         return self._wrapped[index]
>     def __call__(self, *args, **kargs):
>         return self._wrapped(*args, **kargs)
>     # plus any others needed
> 
> def accessControl(failIf):
>     def onDecorator(aClass):
>         class onInstance(BuiltinsMixin):
>             ...and use self._wrapped instead of self.__wrapped...
>             def __getattr__(self, attr): ...
>             def __setattr__(self, attr, value): ...
> ```

Either one of these superclass mix-ins will be extraneous code, but must be implemented only once, and seem much more straightforward than the various metaclassor decorator-based tool approaches you'll find online that populate each proxy class with the requisite methods redundantly (see the class augmentation examples in Chapter 40 for the principles behind such tools).

**Coding variations: Routers, descriptors, automation.** Naturally, both of the prior section's mixin superclasses might be improved with additional code changes we'll largely pass on here, except for two variations worth noting briefly. First, compare the following mutation of the first mix-in -- which uses a simpler coding structure but will incur an extra call per built-in operation, making it slower (though perhaps not significantly so in a proxy context):
> ```python
> class BuiltinsMixin:
>     def reroute(self, attr, *args, **kargs):
>         return self.__class__.__getattr__(self, attr)(*args, **kargs)
>     def __add__(self, other):
>         return self.reroute('__add__', other)
>     def __str__(self):
>         return self.reroute('__str__')
>     def __getitem__(self, index):
>         return self.reroute('__getitem__', index)
>     def __call__(self, *args, **kargs):
>         return self.reroute('__call__', *args, **kargs)
>     # plus any others needed
> ```

Second, all the preceding built-in mix-in classes code each operator overloading method explicitly, and intercept the call issued for the operation. With an alternative coding, we could instead generate methods from a list of names mechanically, and intercept only the attribute fetch preceding the call by creating class-level descriptors of the prior chapter -- as in the following, which, like the second mix-in alternative, assumes the proxied object is named \_wrapped in the proxy instance itself:
> ```python
> class BuiltinsMixin:
>     class ProxyDesc(object): 										# object for 2.X
>         def __init__(self, attrname):
>             self.attrname = attrname
>         def __get__(self, instance, owner):
>             return getattr(instance._wrapped, self.attrname) 		# Assume a _wrapped
> 
>     builtins = ['add', 'str', 'getitem', 'call'] 					# Plus any others
>     for attr in builtins:
>         exec('__%s__ = ProxyDesc("__%s__")' % (attr, attr))
> ```

This coding may be the most concise, but also the most implicit and complex, and is fairly tightly coupled with its subclasses by the shared name. The loop at the end of this class is equivalent to the following, run in the mix-in class's local scope -- it creates descriptors that respond to initial name lookups by fetching from the wrapped object in \_\_get\_\_, rather than catching the later operation call itself:
> ```python
> __add__ = ProxyDesc("__add__")
> __str__ = ProxyDesc("__str__")
> ...etc...
> ```

With such operator overloading methods added -- either inline or by mix-in inheritance -- the prior Private example client that overloaded + and print with \_\_str\_\_ and \_\_add\_\_ works correctly under 2.X and 3.X, as do subclasses that overload indexing and calls. If you care to experiment further, see files access2\_builtins\*.py in the book examples package for complete codings of these options; we'll also employ that third of the mix-in options in a solution to an end-of-chapter quiz.

### Should operator methods be validated?
Adding support for operator overloading methods is required of interface proxies in general, to delegate calls correctly. In our specific privacy application, though, it also raises some additional design choices. In particular, privacy of operator overloading methods differs per implementation:
- Because they invoke \_\_getattr\_\_, the rerouter mix-ins require either that all \_\_X\_\_ names accessed be listed in Public decorations, or that Private be used instead when operator overloading is present in clients. In classes that use overloading heavily, Public may be impractical.
- Because they bypass \_\_getattr\_\_ entirely, as coded here both the inline scheme and self.\_wrapped mix-ins do not have these constraints, but they preclude builtin operations from being made private, and cause built-in operation dispatch to work asymmetrically from both explicit \_\_X\_\_ calls by-name and 2.X's default classic classes.
- Python 2.X classic classes have the first bullet's constraints, simply because all \_\_X\_\_ names are routed through \_\_getattr\_\_ automatically.
- Operator overloading names and protocols differ between 2.X and 3.X, making truly cross-version decoration less than trivial (e.g., Public decorators may need to list names from both lines).

We'll leave final policy here a TBD, but some interface proxies might prefer to allow \_\_X\_\_ operator names to always pass unchecked when delegated.

In the general case, though, a substantial amount of extra code is required to accommodate 3.X's new-style classes as delegation proxies -- in principle, every operator overloading method that is no longer dispatched as a normal instance attribute automatically will need to be defined redundantly in a general tool class like this privacy decorator. This is why this extension is omitted in our code: there are potentially more than 50 such methods! Because all its classes are new-style, delegation-based code is more difficult -- though not necessarily impossible -- in Python 3.X.

### Implementation alternatives: \_\_getattribute\_\_ inserts, call stack inspection
Although redundantly defining operator overloading methods in wrappers is probably the most straightforward workaround to Python 3.X dilemma outlined in the prior section, it's not necessarily the only one. We don't have space to explore this issue much further here, so deeper investigation will have to be relegated to suggested exercise. Because one dead-end alternative illustrates class concepts well, though, it merits a brief mention.

One downside of the privacy example is that instance objects are not truly instances of the original class -- they are instances of the wrapper instead. In some programs that rely on type testing, this might matter. To support such cases, we might try to achieve similar effects by inserting a \_\_getattribute\_\_ and a \_\_setattr\_\_ method into the original class, to catch every attribute reference and assignment made on its instances. These inserted methods would pass valid requests up to their superclass to avoid loops, using the techniques we studied in the prior chapter. Here is the potential change to our class decorator's code:
> ```python
> # Method insertion: rest of access2.py code as before
> def accessControl(failIf):
>     def onDecorator(aClass):
>         def getattributes(self, attr):
>             trace('get:', attr)
>             if failIf(attr):
>                 raise TypeError('private attribute fetch: ' + attr)
>             else:
>                 return object.__getattribute__(self, attr)
> 
>         def setattributes(self, attr, value):
>             trace('set:', attr)
>             if failIf(attr):
>                 raise TypeError('private attribute change: ' + attr)
>             else:
>                 return object.__setattr__(self, attr, value)
> 
>         aClass.__getattribute__ = getattributes
>         aClass.__setattr__ = setattributes 	# Insert accessors
>         return aClass 						# Return original class
>     return onDecorator
> ```

This alternative addresses the type-testing issue but suffers from others. For one thing, this decorator can be used by new-style class clients only: because \_\_getattribute\_\_ is a new-style-only tool (as is this \_\_setattr\_\_ coding), decorated classes in 2.X must use new-style derivation, which may or may not be appropriate for their goals. In fact, the set of classes supported is even further limited: inserting methods will break clients that are already using a \_\_setattr\_\_ or \_\_getattribute\_\_ of their own.

Worse, this scheme does not address the built-in operation attributes issue described in the prior section, because \_\_getattribute\_\_ is also not run in these contexts. In our case, if Person had a \_\_str\_\_ it would be run by print operations, but only because it was actually present in that class. As before, the \_\_str\_\_ attribute would not be routed to the inserted \_\_getattribute\_\_ method generically -- printing would bypass this method altogether and call the class's \_\_str\_\_ directly.

Although this is probably better than not supporting operator overloading methods in a wrapped object at all (barring redefinition, at least), this scheme still cannot intercept and validate \_\_X\_\_ methods, making it impossible for any of them to be private. Whether operator overloading methods should be private is another matter, but this structure precludes the possibility.

Much worse, because this nonwrapper approach works by adding a \_\_getattribute\_\_ and \_\_setattr\_\_ to the decorated class, it also intercepts attribute accesses made by the class itself and validates them the same as accesses made from outside. In other words, the class's own method won't be able to use its private names either! This is a showstopper for the insertion approach.

In fact, inserting these methods this way is functionally equivalent to inheriting them, and implies the same constraints as our original Chapter 30 privacy code. To know whether an attribute access originated inside or outside the class, our methods might need to inspect frame objects on the Python call stack. This might ultimately yield a solution -- implementing private attributes as properties or descriptors that check the stack and validate for outside accesses only, for example -- but it would slow access further, and is far too dark a magic for us to explore here. (Descriptors seem to make all things possible, even when they shouldn't!)

While interesting, and possibly relevant for some other use cases, this method insertion technique doesn't meet our goals. We won't explore this option's coding pattern further here because we will study class augmentation techniques in the next chapter, in conjunction with metaclasses. As we'll see there, metaclasses are not strictly required for changing classes this way, because class decorators can often serve the same role.

## Python Isn't About Control
Now that I've gone to such great lengths to implement Private and Public attribute declarations for Python code, I must again remind you that it is not entirely Pythonic to add access controls to your classes like this. In fact, most Python programmers will probably find this example to be largely or totally irrelevant, apart from serving as a demonstration of decorators in action. Most large Python programs get by successfully without any such controls at all.

That said, you might find this tool useful in limited scopes during development. If you do wish to regulate attribute access in order to eliminate coding mistakes, or happen to be a soon-to-be-ex-C++-or-Java programmer, most things are possible with Python's operator overloading and introspection tools.

