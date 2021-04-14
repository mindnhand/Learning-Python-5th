# The Metaclass Model
To understand metaclasses, you first need to understand a bit more about Python's type model and what happens at the end of a class statement. As we'll see here, the two are intimately related.

## Classes Are Instances of type
So far in this book, we've done most of our work by making instances of built-in types like lists and strings, as well as instances of classes we code ourselves. As we've seen, instances of classes have some state information attributes of their own, but they also inherit behavioral attributes from the classes from which they are made. The same holds true for built-in types; list instances, for example, have values of their own, but they inherit methods from the list type.

While we can get a lot done with such instance objects, Python's type model turns out to be a bit richer than I've formally described. Really, there's a hole in the model we've seen thus far: if instances are created from classes, what is it that creates our classes? It turns out that classes are instances of something, too:
- In Python 3.X, user-defined class objects are instances of the object named type, which is itself a class.
- In Python 2.X, new-style classes inherit from object, which is a subclass of type; classic classes are instances of type and are not created from a class.

We explored the notion of types in Chapter 9 and the relationship of classes to types in Chapter 32, but let's review the basics here so we can see how they apply to metaclasses. Recall that the type built-in returns the type of any object (which is itself an object) when called with a single argument. For built-in types like lists, the type of the instance is the built-in list type, but the type of the list type is the type type itself -- the type object at the top of the hierarchy creates specific types, and specific types create instances.

You can see this for yourself at the interactive prompt. In Python 3.X, for example, the type of a list instance is the list class, and the type of the list class is the type class:
> ```python
> C:\code> py -3 				# In 3.X:
> >>> type([]), type(type([])) 				# List instance is created from list class
> (<class 'list'>, <class 'type'>) 			# List class is created from type class
> >>> type(list), type(type) 				# Same, but with type names
> (<class 'type'>, <class 'type'>) 			# Type of type is type: top of hierarchy
> ```

As we learned when studying new-style class changes in Chapter 32, the same is generally true in Python 2.X, but types are not quite the same as classes -- type is a unique kind of built-in object that caps the type hierarchy and is used to construct types:
> ```python
> C:\code> py -2
> >>> type([]), type(type([])) 				# In 2.X, type is a bit different
> (<type 'list'>, <type 'type'>)
> >>> type(list), type(type)
> (<type 'type'>, <type 'type'>)
> ```

As it happens, the type/instance relationship holds true for user-defined classes as well: instances are created from classes, and classes are created from type. In Python 3.X, though, the notion of a "type" is merged with the notion of a "class." In fact, the two are essentially synonyms -- classes are types, and types are classes. That is:
- Types are defined by classes that derive from type.
- User-defined classes are instances of type classes.
- User-defined classes are types that generate instances of their own.

As we saw earlier, this equivalence affects code that tests the type of instances: the type of an instance is the class from which it was generated. It also has implications for the way that classes are created that turn out to be the key to this chapter's subject. Because classes are normally created from a root type class by default, most programmers don't need to think about this type/class equivalence. However, it opens up new possibilities for customizing both classes and their instances.

For example, all user-defined classes in 3.X (and new-style classes in 2.X) are instances of the type class, and instance objects are instances of their classes; in fact, classes now have a \_\_class\_\_ that links to type, just as an instance has a \_\_class\_\_ that links to the class from which it was made:
> ```python
> C:\code> py -3
> >>> class C: pass 			# 3.X class object (new-style)
> >>> X = C() 					# Class instance object
> >>> type(X) 					# Instance is instance of class
> <class '__main__.C'>
> >>> X.__class__ 				# Instance's class
> <class '__main__.C'>
> >>> type(C) 					# Class is instance of type
> <class 'type'>
> >>> C.__class__ 				# Class's class is type
> <class 'type'>
> ```

Notice especially the last two lines here -- classes are instances of the type class, just as normal instances are instances of a user-defined class. This works the same for both built-ins and user-defined class types in 3.X. In fact, classes are not really a separate concept at all: they are simply user-defined types, and type itself is defined by a class.

In Python 2.X, things work similarly for new-style classes derived from object, because this enables 3.X class behavior (as we've seen, 3.X adds object to the \_\_bases\_\_ superclass tuple of top-level root classes automatically to qualify them as new-style):
> ```python
> C:\code> py -2
> >>> class C(object): pass 			# In 2.X new-style classes,
> >>> X = C() 							# classes have a class too
> >>> type(X)
> <class '__main__.C'>
> >>> X.__class__
> <class '__main__.C'>
> >>> type(C)
> <type 'type'>
> >>> C.__class__
> <type 'type'>
> ```

Classic classes in 2.X are a bit different, though -- because they reflect the original class model in older Pythons, they do not have a \_\_class\_\_ link, and like built-in types in 2.X they are instances of type, not a type class (I've shortened some of the hex addresses in object displays in this chapter for clarity):
> ```python
> C:\code> py -2
> >>> class C: pass 			# In 2.X classic classes,
> >>> X = C() 				# classes have no class themselves
> >>> type(X)
> <type 'instance'>
> >>> X.__class__
> <class __main__.C at 0x005F85A0>
> >>> type(C)
> <type 'classobj'>
> >>> C.__class__
> AttributeError: class C has no attribute '__class__'
> ```

## Metaclasses Are Subclasses of Type
Why would we care that classes are instances of a type class in 3.X? It turns out that this is the hook that allows us to code metaclasses. Because the notion of type is the same as class today, we can subclass type with normal object-oriented techniques and class syntax to customize it. And because classes are really instances of the type class, creating classes from customized subclasses of type allows us to implement custom kinds of classes. In full detail, this all works out quite naturally -- in 3.X, and in 2.X new-style classes:
- type is a class that generates user-defined classes.
- Metaclasses are subclasses of the type class.
- Class objects are instances of the type class, or a subclass thereof.
- Instance objects are generated from a class.

In other words, to control the way classes are created and augment their behavior, all we need to do is specify that a user-defined class be created from a user-defined metaclass instead of the normal type class.

Notice that this type instance relationship is not quite the same as normal inheritance. User-defined classes may also have superclasses from which they and their instances inherit attributes as usual. As we've seen, inheritance superclasses are listed in parentheses in the class statement and show up in a class's \_\_bases\_\_ tuple. The type from which a class is created, though, and of which it is an instance, is a different relationship.

Inheritance searches instance and class namespace dictionaries, but classes may also acquire behavior from their type that is not exposed to the normal inheritance search. To lay the groundwork for understanding this distinction, the next section describes the procedure Python follows to implement this instance-of type relationship.

## Class Statement Protocol
Subclassing the type class to customize it is really only half of the magic behind metaclasses. We still need to somehow route a class's creation to the metaclass, instead of the default type. To fully understand how this is arranged, we also need to know how class statements do their business.

We've already learned that when Python reaches a class statement, it runs its nested block of code to create its attributes -- all the names assigned at the top level of the nested code block generate attributes in the resulting class object. These names are usually method functions created by nested defs, but they can also be arbitrary attributes assigned to create class data shared by all instances.

Technically speaking, Python follows a standard protocol to make this happen: at the end of a class statement, and after running all its nested code in a namespace dictionary corresponding to the class's local scope, Python calls the type object to create the class object like this:
> ```python
> class = type(classname, superclasses, attributedict)
> ```

The type object in turn defines a \_\_call\_\_ operator overloading method that runs two other methods when the type object is called:
> ```python
> type.__new__(typeclass, classname, superclasses, attributedict)
> type.__init__(class, classname, superclasses, attributedict)
> ```

The \_\_new\_\_ method creates and returns the new class object, and then the \_\_init\_\_ method initializes the newly created object. As we'll see in a moment, these are the hooks that metaclass subclasses of type generally use to customize classes.

For example, given a class definition like the following for Spam:
> ```python
> class Eggs: ... 				# Inherited names here
> class Spam(Eggs): 			# Inherits from Eggs
>     data = 1 					# Class data attribute
>     def meth(self, arg): 		# Class method attribute
>         return self.data + arg
> ```

Python will internally run the nested code block to create two attributes of the class (data and meth), and then call the type object to generate the class object at the end of the class statement:
> ```python
> Spam = type('Spam', (Eggs,), {'data': 1, 'meth': meth, '__module__': '__main__'})
> ```

In fact, you can call type this way yourself to create a class dynamically -- albeit here with a fabricated method function and empty superclasses tuple (Python adds object automatically in both 3.X and 2.X):
> ```python
> >>> x = type('Spam', (), {'data': 1, 'meth': (lambda x, y: x.data + y)})
> >>> i = x()
> >>> x, i
> (<class '__main__.Spam'>, <__main__.Spam object at 0x029E7780>)
> >>> i.data, i.meth(2)
> (1, 3)
> ```

The class produced is exactly like that you'd get from running a class statement:
> ```python
> >>> x.__bases__
> (<class 'object'>,)
> >>> [(a, v) for (a, v) in x.__dict__.items() if not a.startswith('__')]
> [('data', 1), ('meth', <function <lambda> at 0x0297A158>)]
> ```

Because this type call is made automatically at the end of the class statement, though, it's an ideal hook for augmenting or otherwise processing a class. The trick lies in replacing the default type with a custom subclass that will intercept this call. The next section shows how.


