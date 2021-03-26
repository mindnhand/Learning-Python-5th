# Static and Class Methods
As of Python 2.2, it is possible to define two kinds of methods within a class that can be called without an instance: static methods work roughly like simple instance-less functions inside a class, and class methods are passed a class instead of an instance. Both are similar to tools in other languages (e.g., C++ static methods). Although this feature was added in conjunction with the new-style classes discussed in the prior sections, static and class methods work for classic classes too.

To enable these method modes, you must call special built-in functions named staticmethod and classmethod within the class, or invoke them with the special @name decoration syntax we'll meet later in this chapter. These functions are required to enable these special method modes in Python 2.X, and are generally needed in 3.X. In Python 3.X, a staticmethod declaration is not required for instance-less methods called only through a class name, but is still required if such methods are called through instances.

## Why the Special Methods?
As we've learned, a class's method is normally passed an instance object in its first argument, to serve as the implied subject of the method call -- that's the "object" in "object-oriented programming." Today, though, there are two ways to modify this model. Before I explain what they are, I should explain why this might matter to you.

Sometimes, programs need to process data associated with classes instead of instances. Consider keeping track of the number of instances created from a class, or maintaining a list of all of a class's instances that are currently in memory. This type of information and its processing are associated with the class rather than its instances. That is, the information is usually stored on the class itself and processed apart from any instance.

For such tasks, simple functions coded outside a class can often suffice -- because they can access class attributes through the class name, they have access to class data and never require access to an instance. However, to better associate such code with a class, and to allow such processing to be customized with inheritance as usual, it would be better to code these types of functions inside the class itself. To make this work, we need methods in a class that are not passed, and do not expect, a self instance argument.

Python supports such goals with the notion of static methods -- simple functions with no self argument that are nested in a class and are designed to work on class attributes instead of instance attributes. Static methods never receive an automatic self argument, whether called through a class or an instance. They usually keep track of information that spans all instances, rather than providing behavior for instances.

Although less commonly used, Python also supports the notion of class methods -- methods of a class that are passed a class object in their first argument instead of an instance, regardless of whether they are called through an instance or a class. Such methods can access class data through their class argument -- what we've called self thus far -- even if called through an instance. Normal methods, now known in formal circles as instance methods, still receive a subject instance when called; static and class methods do not.

## Static Methods in 2.X and 3.X
The concept of static methods is the same in both Python 2.X and 3.X, but its implementation requirements have evolved somewhat in Python 3.X. Since this book covers both versions, I need to explain the differences in the two underlying models before we get to the code.

Really, we already began this story in the preceding chapter, when we explored the notion of unbound methods. Recall that both Python 2.X and 3.X always pass an instance to a method that is called through an instance. However, Python 3.X treats methods fetched directly from a class differently than 2.X -- a difference in Python lines that has nothing to do with new-style classes:
- Both Python 2.X and 3.X produce a bound method when a method is fetched through an instance.
- In Python 2.X, fetching a method from a class produces an unbound method, which cannot be called without manually passing an instance.
- In Python 3.X, fetching a method from a class produces a simple function, which can be called normally with no instance present.

In other words, Python 2.X class methods always require an instance to be passed in, whether they are called through an instance or a class. By contrast, in Python 3.X we are required to pass an instance to a method only if the method expects one -- methods that do not include an instance argument can be called through the class without passing an instance. That is, 3.X allows simple functions in a class, as long as they do not expect and are not passed an instance argument. The net effect is that:
- In Python 2.X, we must always declare a method as static in order to call it without an instance, whether it is called through a class or an instance.
- In Python 3.X, we need not declare such methods as static if they will be called through a class only, but we must do so in order to call them through an instance.
To illustrate, suppose we want to use class attributes to count how many instances are generated from a class. The following file, spam.py, makes a first attempt -- its class has a counter stored as a class attribute, a constructor that bumps up the counter by one each time a new instance is created, and a method that displays the counter's value.

Remember, class attributes are shared by all instances. Therefore, storing the counter in the class object itself ensures that it effectively spans all instances:
> ```python
> class Spam:
>     numInstances = 0
>     def __init__(self):
>         Spam.numInstances = Spam.numInstances + 1
>     def printNumInstances():
>         print("Number of instances created: %s" % Spam.numInstances)
> ```

The printNumInstances method is designed to process class data, not instance data -- it's about all the instances, not any one in particular. Because of that, we want to be able to call it without having to pass an instance. Indeed, we don't want to make an instance to fetch the number of instances, because this would change the number of instances we're trying to fetch! In other words, we want a self-less "static" method.

Whether this code's printNumInstances works or not, though, depends on which Python you use, and which way you call the method -- through the class or through an instance. In 2.X, calls to a self-less method function through both the class and instances fail (as usual, I've omitted some error text here for space):
> ```python
> C:\code> c:\python27\python
> >>> from spam import Spam
> >>> a = Spam() 				# Cannot call unbound class methods in 2.X
> >>> b = Spam() 				# Methods expect a self object by default
> >>> c = Spam()
> >>> Spam.printNumInstances()
> TypeError: unbound method printNumInstances() must be called with Spam instance
> as first argument (got nothing instead)
> >>> a.printNumInstances()
> TypeError: printNumInstances() takes no arguments (1 given)
> ```

The problem here is that unbound instance methods aren't exactly the same as simple functions in 2.X. Even though there are no arguments in the def header, the method still expects an instance to be passed in when it's called, because the function is associated with a class. In Python 3.X, calls to self-less methods made through classes work, but calls from instances fail:
> ```python
> C:\code> c:\python33\python
> >>> from spam import Spam
> >>> a = Spam() 				# Can call functions in class in 3.X
> >>> b = Spam() 				# Calls through instances still pass a self
> >>> c = Spam()
> >>> Spam.printNumInstances() 				# Differs in 3.X
> Number of instances created: 3
> >>> a.printNumInstances()
> TypeError: printNumInstances() takes 0 positional arguments but 1 was given
> ```

That is, calls to instance-less methods like printNumInstances made through the class fail in Python 2.X but work in Python 3.X. On the other hand, calls made through an instance fail in both Pythons, because an instance is automatically passed to a method that does not have an argument to receive it:
> ```python
> Spam.printNumInstances() 				# Fails in 2.X, works in 3.X
> instance.printNumInstances() 			# Fails in both 2.X and 3.X (unless static)
> ```

If you're able to use 3.X and stick with calling self-less methods through classes only, you already have a static method feature. However, to allow self-less methods to be called through classes in 2.X and through instances in both 2.X and 3.X, you need to either adopt other designs or be able to somehow mark such methods as special. Let's look at both options in turn.

## Static Method Alternatives
Short of marking a self-less method as special, you can sometimes achieve similar results with different coding structures. For example, if you just want to call functions that access class members without an instance, perhaps the simplest idea is to use normal functions outside the class, not class methods. This way, an instance isn't expected in the call. The following mutation of spam.py illustrates, and works the same in Python 3.X and 2.X:
> ```python
> def printNumInstances():
>     print("Number of instances created: %s" % Spam.numInstances)
> 
> class Spam:
>     numInstances = 0
>     def __init__(self):
>         Spam.numInstances = Spam.numInstances + 1
> ```

> ```powershell
> C:\code> c:\python33\python
> >>> import spam
> >>> a = spam.Spam()
> >>> b = spam.Spam()
> >>> c = spam.Spam()
> >>> spam.printNumInstances() 			# But function may be too far removed
> 
> Number of instances created: 3 		# And cannot be changed via inheritance
> >>> spam.Spam.numInstances
> 3
> ```
Because the class name is accessible to the simple function as a global variable, this works fine. Also, note that the name of the function becomes global, but only to this single module; it will not clash with names in other files of the program.

Prior to static methods in Python, this structure was the general prescription. Because Python already provides modules as a namespace-partitioning tool, one could argue that there's not typically any need to package functions in classes unless they implement object behavior. Simple functions within modules like the one here do much of what instance-less class methods could, and are already associated with the class because they live in the same module.

Unfortunately, this approach is still less than ideal. For one thing, it adds to this file's scope an extra name that is used only for processing a single class. For another, the function is much less directly associated with the class by structure; in fact, its definition could be hundreds of lines away. Perhaps worse, simple functions like this cannot be customized by inheritance, since they live outside a class's namespace: subclasses cannot directly replace or extend such a function by redefining it.

We might try to make this example work in a version-neutral way by using a normal method and always calling it through (or with) an instance, as usual:
> ```python
> class Spam:
>     numInstances = 0
>     def __init__(self):
>         Spam.numInstances = Spam.numInstances + 1
>     def printNumInstances(self):
>         print("Number of instances created: %s" % Spam.numInstances)
> ```

> ```powershell
> C:\code> c:\python33\python
> >>> from spam import Spam
> >>> a, b, c = Spam(), Spam(), Spam()
> >>> a.printNumInstances()
> Number of instances created: 3
> >>> Spam.printNumInstances(a)
> Number of instances created: 3
> >>> Spam().printNumInstances() 			# But fetching counter changes counter!
> Number of instances created: 4
> ```

Unfortunately, as mentioned earlier, such an approach is completely unworkable if we don't have an instance available, and making an instance changes the class data, as illustrated in the last line here. A better solution would be to somehow mark a method inside a class as never requiring an instance. The next section shows how.

## Using Static and Class Methods
Today, there is another option for coding simple functions associated with a class that may be called through either the class or its instances. As of Python 2.2, we can code classes with static and class methods, neither of which requires an instance argument to be passed in when invoked. To designate such methods, classes call the built-in functions staticmethod and classmethod, as hinted in the earlier discussion of new-style classes. Both mark a function object as special -- that is, as requiring no instance if static and requiring a class argument if a class method. For example, in the file bothmethods.py (which unifies 2.X and 3.X printing with lists, though displays still vary slightly for 2.X classic classes):
> ```python
> # File bothmethods.py
> class Methods:
>     def imeth(self, x): 			# Normal instance method: passed a self
>         print([self, x])
>     def smeth(x): 				# Static: no instance passed
>         print([x])
>     def cmeth(cls, x): 			# Class: gets class, not instance
>         print([cls, x])
> 
>     smeth = staticmethod(smeth)   # Make smeth a static method (or @: ahead)
>     cmeth = classmethod(cmeth) 	# Make cmeth a class method (or @: ahead)
> ```

Notice how the last two assignments in this code simply reassign (a.k.a. rebind) the method names smeth and cmeth. Attributes are created and changed by any assignment in a class statement, so these final assignments simply overwrite the assignments made earlier by the defs. As we’ll see in a few moments, the special @ syntax works here as an alternative to this just as it does for properties -- but makes little sense unless you first understand the assignment form here that it automates.

Technically, Python now supports three kinds of class-related methods, with differing argument protocols:
- Instance methods, passed a self instance object (the default)
- Static methods, passed no extra object (via staticmethod)
- Class methods, passed a class object (via classmethod, and inherent in metaclasses)

Moreover, Python 3.X extends this model by also allowing simple functions in a class to serve the role of static methods without extra protocol, when called through a class object only. Despite its name, the bothmethods.py module illustrates all three method types, so let's expand on these in turn.

Instance methods are the normal and default case that we've seen in this book. An instance method must always be called with an instance object. When you call it through an instance, Python passes the instance to the first (leftmost) argument automatically; when you call it through a class, you must pass along the instance manually:
> ```python
> >>> from bothmethods import Methods 			# Normal instance methods
> >>> obj = Methods() 							# Callable through instance or class
> >>> obj.imeth(1)
> [<bothmethods.Methods object at 0x0000000002A15710>, 1]
> >>> Methods.imeth(obj, 2)
> [<bothmethods.Methods object at 0x0000000002A15710>, 2]
> ```

Static methods, by contrast, are called without an instance argument. Unlike simple functions outside a class, their names are local to the scopes of the classes in which they are defined, and they may be looked up by inheritance. Instance-less functions can be called through a class normally in Python 3.X, but never by default in 2.X. Using the staticmethod built-in allows such methods to also be called through an instance in 3.X and through both a class and an instance in Python 2.X (that is, the first of the following works in 3.X without staticmethod, but the second does not):
> ```python
> >>> Methods.smeth(3) 						# Static method: call through class
> [3] 										# No instance passed or expected
> >>> obj.smeth(4) 							# Static method: call through instance
> [4] 										# Instance not passed
> ```

Class methods are similar, but Python automatically passes the class (not an instance) in to a class method's first (leftmost) argument, whether it is called through a class or an instance:
> ```python
> >>> Methods.cmeth(5) 						# Class method: call through class
> [<class 'bothmethods.Methods'>, 5] 			# Becomes cmeth(Methods, 5)
> >>> obj.cmeth(6) 							# Class method: call through instance
> [<class 'bothmethods.Methods'>, 6] 			# Becomes cmeth(Methods, 6)
> ```

In Chapter 40, we'll also find that metaclass methods -- a unique, advanced, and technically distinct method type -- behave similarly to the explicitly-declared class methods we're exploring here.

## Counting Instances with Static Methods
Now, given these built-ins, here is the static method equivalent of this section's instance-counting example -- it marks the method as special, so it will never be passed an instance automatically:
> ```python
> class Spam:
>     numInstances = 0 					# Use static method for class data
>     def __init__(self):
>         Spam.numInstances += 1
>     def printNumInstances():
>         print("Number of instances: %s" % Spam.numInstances)
>     printNumInstances = staticmethod(printNumInstances)
> ```

Using the static method built-in, our code now allows the self-less method to be called through the class or any instance of it, in both Python 2.X and 3.X:
> ```python
> >>> from spam_static import Spam
> >>> a = Spam()
> >>> b = Spam()
> >>> c = Spam()
> >>> Spam.printNumInstances() 			# Call as simple function
> Number of instances: 3
> >>> a.printNumInstances() 			# Instance argument not passed
> Number of instances: 3
> ```

Compared to simply moving printNumInstances outside the class, as prescribed earlier, this version requires an extra staticmethod call (or an @ line we'll see ahead). However, it also localizes the function name in the class scope (so it won't clash with other names in the module); moves the function code closer to where it is used (inside the class statement); and allows subclasses to customize the static method with inheritance -- a more convenient and powerful approach than importing functions from the files in which superclasses are coded. The following subclass and new testing session illustrate (be sure to start a new session after changing files, so that your from imports load the latest version of the file):
> ```python
> class Sub(Spam):
>     def printNumInstances(): 				# Override a static method
>         print("Extra stuff...") 			# But call back to original
>         Spam.printNumInstances()
>     printNumInstances = staticmethod(printNumInstances)
> ```

> ```python
> >>> from spam_static import Spam, Sub
> >>> a = Sub()
> >>> b = Sub()
> >>> a.printNumInstances() 			# Call from subclass instance
> Extra stuff...
> Number of instances: 2
> >>> Sub.printNumInstances() 			# Call from subclass itself
> Extra stuff...
> Number of instances: 2
> >>> Spam.printNumInstances() 			# Call original version
> Number of instances: 2
> ```

Moreover, classes can inherit the static method without redefining it -- it is run without an instance, regardless of where it is defined in a class tree:
> ```python
> >>> class Other(Spam): pass 			# Inherit static method verbatim
> >>> c = Other()
> >>> c.printNumInstances()
> Number of instances: 3
> ```

Notice how this also bumps up the superclass's instance counter, because its constructor is inherited and run -- a behavior that begins to encroach on the next section's subject.

## Counting Instances with Class Methods
Interestingly, a class method can do similar work here -- the following has the same behavior as the static method version listed earlier, but it uses a class method that receives the instance's class in its first argument. Rather than hardcoding the class name, the class method uses the automatically passed class object generically:
> ```python
> class Spam:
>     numInstances = 0 					# Use class method instead of static
>     def __init__(self):
>         Spam.numInstances += 1
>     def printNumInstances(cls):
>         print("Number of instances: %s" % cls.numInstances)
>     printNumInstances = classmethod(printNumInstances)
> ```

This class is used in the same way as the prior versions, but its printNumInstances method receives the Spam class, not the instance, when called from both the class and an instance:
> ```python
> >>> from spam_class import Spam
> >>> a, b = Spam(), Spam()
> >>> a.printNumInstances() 			# Passes class to first argument
> Number of instances: 2
> >>> Spam.printNumInstances() 			# Also passes class to first argument
> Number of instances: 2
> ```

When using class methods, though, keep in mind that they receive the most specific (i.e., lowest) class of the call's subject. This has some subtle implications when trying to update class data through the passed-in class. For example, if in module spam\_class.py we subclass to customize as before, augment Spam.printNumInstances to also display its cls argument, and start a new testing session:
> ```python
> class Spam:
>     numInstances = 0 					# Trace class passed in
>     def __init__(self):
>         Spam.numInstances += 1
>     def printNumInstances(cls):
>         print("Number of instances: %s %s" % (cls.numInstances, cls))
>     printNumInstances = classmethod(printNumInstances)
> 
> class Sub(Spam):
>     def printNumInstances(cls): 		# Override a class method
>         print("Extra stuff...", cls) 		# But call back to original
>         Spam.printNumInstances()
>     printNumInstances = classmethod(printNumInstances)
> class Other(Spam): pass    			# Inherit class method verbatim
> ```

The lowest class is passed in whenever a class method is run, even for subclasses that have no class methods of their own:
> ```python
> >>> from spam_class import Spam, Sub, Other
> >>> x = Sub()
> >>> y = Spam()
> >>> x.printNumInstances() 			# Call from subclass instance
> Extra stuff... <class 'spam_class.Sub'>
> Number of instances: 2 <class 'spam_class.Spam'>
> >>> Sub.printNumInstances() 			# Call from subclass itself
> Extra stuff... <class 'spam_class.Sub'>
> Number of instances: 2 <class 'spam_class.Spam'>
> >>> y.printNumInstances() 			# Call from superclass instance
> Number of instances: 2 <class 'spam_class.Spam'>
> ```

In the first call here, a class method call is made through an instance of the Sub subclass, and Python passes the lowest class, Sub, to the class method. All is well in this case -- since Sub's redefinition of the method calls the Spam superclass's version explicitly, the superclass method in Spam receives its own class in its first argument. But watch what happens for an object that inherits the class method verbatim:
> ```python
> >>> z = Other() 						# Call from lower sub's instance
> >>> z.printNumInstances()
> Number of instances: 3 <class 'spam_class.Other'>
> ```

This last call here passes Other to Spam's class method. This works in this example because fetching the counter finds it in Spam by inheritance. If this method tried to assign to the passed class's data, though, it would update Other, not Spam! In this specific case, Spam is probably better off hardcoding its own class name to update its data if it means to count instances of all its subclasses too, rather than relying on the passed-in class argument.

### Counting instances per class with class methods
In fact, because class methods always receive the lowest class in an instance's tree:
- Static methods and explicit class names may be a better solution for processing data local to a class.
- Class methods may be better suited to processing data that may differ for each class in a hierarchy.

Code that needs to manage per-class instance counters, for example, might be best off leveraging class methods. In the following, the top-level superclass uses a class method to manage state information that varies for and is stored on each class in the tree -- similar in spirit to the way instance methods manage state information that varies per class instance:
> ```python
> class Spam:
>     numInstances = 0
>     def count(cls): 					# Per-class instance counters
>         cls.numInstances += 1 		# cls is lowest class above instance
>     def __init__(self):
>         self.count() 					# Passes self.__class__ to count
>     count = classmethod(count)
> 
> class Sub(Spam):
>     numInstances = 0
>     def __init__(self): 				# Redefines __init__
>         Spam.__init__(self)
> 
> class Other(Spam):     				# Inherits __init__
>     numInstances = 0
> ```

> ```python
> >>> from spam_class2 import Spam, Sub, Other
> >>> x = Spam()
> >>> y1, y2 = Sub(), Sub()
> >>> z1, z2, z3 = Other(), Other(), Other()
> >>> x.numInstances, y1.numInstances, z1.numInstances 				# Per-class data!
> (1, 2, 3)
> >>> Spam.numInstances, Sub.numInstances, Other.numInstances
> (1, 2, 3)
> ```

Static and class methods have additional advanced roles, which we will finesse here; see other resources for more use cases. In recent Python versions, though, the static and class method designations have become even simpler with the advent of function decoration syntax -- a way to apply one function to another that has roles well beyond the static method use case that was its initial motivation. This syntax also allows us to augment classes in Python 2.X and 3.X -- to initialize data like the numInstances counter in the last example, for instance. The next section explains how.

> **NOTE:**
> For a postscript on Python's method types, be sure to watch for coverage of metaclass methods in Chapter 40 -- because these are designed to process a class that is an instance of a metaclass, they turn out to be very similar to the class methods defined here, but require no classmethod declaration, and apply only to the shadowy metaclass realm.
> 
