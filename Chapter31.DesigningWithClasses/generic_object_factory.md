# Classes Are Objects: Generic Object Factories
Sometimes, class-based designs require objects to be created in response to conditions that can't be predicted
when a program is written. The factory design pattern allows such a deferred approach. Due in large part to
Python's flexibility, factories can take multiple forms, some of which don’t seem special at all.

Because classes are also "first class" objects, it's easy to pass them around a program, store them in data
structures, and so on. You can also pass classes to functions that generate arbitrary kinds of objects; such
functions are sometimes called factories in OOP design circles. Factories can be a major undertaking in a
strongly typed language such as C++ but are almost trivial to implement in Python.

For example, the call syntax we met in Chapter 18 can call any class with any number of positional or keyword
constructor arguments in one step to generate any sort of instance:
> ```python
> def factory(aClass, *pargs, **kargs): 		# Varargs tuple, dict
> 	  return aClass(*pargs, **kargs) 			# Call aClass (or apply in 2.X only)
> class Spam:
>     def doit(self, message):
>         print(message)
> 
> class Person:
>     def __init__(self, name, job=None):
>         self.name = name
>         self.job = job
> 
> object1 = factory(Spam) 						# Make a Spam object
> object2 = factory(Person, "Arthur", "King") 	# Make a Person object
> object3 = factory(Person, name='Brian') 		# Ditto, with keywords and default
> ```

In this code, we define an object generator function called factory. It expects to be passed a class object
(any class will do) along with one or more arguments for the class's constructor. The function uses special
"varargs" call syntax to call the function and return an instance.

The rest of the example simply defines two classes and generates instances of both by passing them to the
factory function. And that's the only factory function you'll ever need to write in Python; it works for
any class and any constructor arguments. If you run this live (factory.py), your objects will look like this:
> ```python
> >>> object1.doit(99)
> 99
> >>> object2.name, object2.job
> ('Arthur', 'King')
> >>> object3.name, object3.job
> ('Brian', None)
> ```

By now, you should know that everything is a "first class" object in Python—includiuding classes, which are
usually just compiler input in languages like C++. It's natural to pass them around this way. As mentioned at
the start of this part of the book, though, only objects derived from classes do full OOP in Python.

## Why Factories?
So what good is the factory function (besides providing an excuse to illustrate firstclass class objects in
this book)? Unfortunately, it's difficult to show applications of this design pattern without listing much
more code than we have space for here. In general, though, such a factory might allow code to be insulated
from the details of dynamically configured object construction.

For instance, recall the processor example presented in the abstract in Chapter 26, and then again as a
composition example earlier in this chapter. It accepts reader and writer objects for processing arbitrary
data streams. The original version of this example manually passed in instances of specialized classes like
FileWriter and SocketReader to customize the data streams being processed; later, we passed in hardcoded file,
stream, and formatter objects. In a more dynamic scenario, external devices such as configuration files or
GUIs might be used to configure the streams.
in our program ahead of time. Indeed, those classes might not even have existed at all when we wrote our code:
> ```python
> classname = ...parse from config file...
> classarg = ...parse from config file...
> import streamtypes 		# Customizable code
> aclass = getattr(streamtypes, classname) 		# Fetch from module
> reader = factory(aclass, classarg) 		# Or aclass(classarg)
> processor(reader, ...)
> ```

Here, the getattr built-in is again used to fetch a module attribute given a string name (it's like saying
obj.attr, but attr is a string). Because this code snippet assumes a single constructor argument, it doesn't
strictly need factory—we could make an instance  with just aclass(classarg). The factory function may prove
more useful in the presence of unknown argument lists, however, and the general factory coding pattern can
improve the code's flexibility.
