# Inheritance and Instance
Because metaclasses are specified in similar ways to inheritance superclasses, they can be a bit confusing at first glance. A few key points should help summarize and clarify the model:
- **Metaclasses inherit from the type class (usually)**
  Although they have a special role, metaclasses are coded with class statements and follow the usual OOP model in Python. For example, as subclasses of type, they can redefine the type object's methods, overriding and customizing them as needed. Metaclasses typically redefine the type class's \_\_new\_\_ and \_\_init\_\_ to customize class creation and initialization. Although it's less common, they can also redefine \_\_call\_\_ if they wish to catch the end-of-class creation call directly (albeit with the complexities we saw in the prior section), and can even be simple functions or other callables that return arbitrary objects, instead of type subclasses.
- **Metaclass declarations are inherited by subclasses**
  The metaclass=M declaration in a user-defined class is inherited by the class's normal subclasses, too, so the metaclass will run for the construction of each class that inherits this specification in a superclass inheritance chain.
- **Metaclass attributes are not inherited by class instances**
  Metaclass declarations specify an instance relationship, which is not the same as what we've called inheritance thus far. Because classes are instances of metaclasses, the behavior defined in a metaclass applies to the class, but not the class's later instances. Instances obtain behavior from their classes and superclasses, but not from any metaclasses. Technically, attribute inheritance for normal instances usually searches only the \_\_dict\_\_ dictionaries of the instance, its class, and all its superclasses; metaclasses are not included in inheritance lookup for normal instances.
- **Metaclass attributes are acquired by classes**
  By contrast, classes do acquire methods of their metaclasses by virtue of the instance relationship. This is a source of class behavior that processes classes themselves. Technically, classes acquire metaclass attributes through the class's \_\_class\_\_ link just as normal instances acquire names from their class, but inheritance via \_\_dict\_\_ search is attempted first: when the same name is available to a class in both a metaclass and a superclass, the superclass (inheritance) version is used instead of that on a metaclass (instance). The class's \_\_class\_\_, however, is not followed for its own instances: metaclass attributes are made available to their instance classes, but not to instances of those instance classes (and see the earlier reference to Dr. Seuss...).

This may be easier to understand in code than in prose. To illustrate all these points, consider the following example:
> 
> > ```python
> > # File metainstance.py
> > class MetaOne(type):
> >     def __new__(meta, classname, supers, classdict): 			# Redefine type method
> >         print('In MetaOne.new:', classname)
> >         return type.__new__(meta, classname, supers, classdict)
> >     def toast(self):
> >         return 'toast'
> > 
> > class Super(metaclass=MetaOne): 								# Metaclass inherited by subs too
> >     def spam(self): 			# MetaOne run twice for two classes
> >         return 'spam'
> > 
> > class Sub(Super): 				# Superclass: inheritance versus instance
> >     def eggs(self): 			# Classes inherit from superclasses
> >         return 'eggs' 				# But not from metaclasses
> > ```
> 
> When this code is run (as a script or module), the metaclass handles construction of both client classes, and instances inherit class attributes but not metaclass attributes:
> 
> > ```python
> > >>> from metainstance import * 				# Runs class statements: metaclass run twice
> > In MetaOne.new: Super
> > In MetaOne.new: Sub
> > >>> X = Sub() 				# Normal instance of user-defined class
> > >>> X.eggs() 					# Inherited from Sub
> > 'eggs'
> > >>> X.spam() 					# Inherited from Super
> > 'spam'
> > >>> X.toast() 				# Not inherited from metaclass
> > AttributeError: 'Sub' object has no attribute 'toast'
> > ```
> 
> By contrast, classes both inherit names from their superclasses, and acquire names from their metaclass (which in this example is itself inherited from a superclass):
> 
> > ```python
> > >>> Sub.eggs(X) 				# Own method
> > 'eggs'
> > >>> Sub.spam(X) 				# Inherited from Super
> > 'spam'
> > >>> Sub.toast() 				# Acquired from metaclass
> > 'toast'
> > >>> Sub.toast(X) 				# Not a normal class method
> > TypeError: toast() takes 1 positional argument but 2 were given
> > ```
> 
> Notice how the last of the preceding calls fails when we pass in an instance, because the name resolves to a metaclass method, not a normal class method. In fact, both the object you fetch a name from and its source become crucial here. Methods acquired from metaclasses are bound to the subject class, while methods from normal classes are unbound if fetched through the class but bound when fetched through the instance:
> 
> > ```python
> > >>> Sub.toast
> > <bound method MetaOne.toast of <class 'metainstance.Sub'>>
> > >>> Sub.spam
> > <function Super.spam at 0x0298A2F0>
> > >>> X.spam
> > <bound method Sub.spam of <metainstance.Sub object at 0x02987438>>
> > ```
> 

We've studied the last two of these rules before in Chapter 31's bound method coverage; the first is new, but reminiscent of class methods. To understand why this works the way it does, we need to explore the metaclass instance relationship further.

## Metaclass Versus Superclass
In even simpler terms, watch what happens in the following: as an instance of the A metaclass type, class B acquires A's attribute, but this attribute is not made available for inheritance by B's own instances -- the acquisition of names by metaclass instances is distinct from the normal inheritance used for class instances:
> ```python
> >>> class A(type): attr = 1
> >>> class B(metaclass=A): pass 			# B is meta instance and acquires meta attr
> >>> I = B() 								# I inherits from class but not meta!
> >>> B.attr
> 1
> >>> I.attr
> AttributeError: 'B' object has no attribute 'attr'
> >>> 'attr' in B.__dict__, 'attr' in A.__dict__
> (False, True)
> ```

By contrast, if A morphs from metaclass to superclass, then names inherited from an A superclass become available to later instances of B, and are located by searching namespace dictionaries in classes in the tree -- that is, by checking the \_\_dict\_\_ of objects in the method resolution order (MRO), much like the mapattrs example we coded back in Chapter 32:
> ```python
> >>> class A: attr = 1
> >>> class B(A): pass 			# I inherits from class and supers
> >>> I = B()
> >>> B.attr
> 1
> >>> I.attr
> 1
> >>> 'attr' in B.__dict__, 'attr' in A.__dict__
> (False, True)
> ```

This is why metaclasses often do their work by manipulating a new class's namespace dictionary, if they wish to influence the behavior of later instance objects -- instances will see names in a class, but not its metaclass. Watch what happens, though, if the same name is available in both attribute sources -- the inheritance name is used instead of instance acquisition:
> ```python
> >>> class M(type): attr = 1
> >>> class A: attr = 2
> >>> class B(A, metaclass=M): pass 			# Supers have precedence over metas
> >>> I = B()
> >>> B.attr, I.attr
> (2, 2)
> >>> 'attr' in B.__dict__, 'attr' in A.__dict__, 'attr' in M.__dict__
> (False, True, True)
> ```

This is true regardless of the relative height of the inheritance and instance sources -- Python checks the \_\_dict\_\_ of each class on the MRO (inheritance), before falling back on metaclass acquisition (instance):
> 
> > ```python
> > >>> class M(type): attr = 1
> > >>> class A: attr = 2
> > >>> class B(A): pass
> > >>> class C(B, metaclass=M): pass 				# Super two levels above meta: still wins
> > >>> I = C()
> > >>> I.attr, C.attr
> > (2, 2)
> > >>> [x.__name__ for x in C.__mro__] 			# See Chapter 32 for all things MRO
> > ['C', 'B', 'A', 'object']
> > ```
> 
> In fact, classes acquire metaclass attributes through their \_\_class\_\_ link, in the same way that normal instances inherit from classes through their \_\_class\_\_, which makes sense, given that classes are also instances of metaclasses. The chief distinction is that instance inheritance does not follow a class's \_\_class\_\_, but instead restricts its scope to the \_\_dict\_\_ of each class in a tree per the MRO -- following \_\_bases\_\_ at each class only, and using only the instance's \_\_class\_\_ link once:
> 
> > ```python
> > >>> I.__class__ 				# Followed by inheritance: instance's class
> > <class '__main__.C'>
> > >>> C.__bases__ 				# Followed by inheritance: class's supers
> > (<class '__main__.B'>,)
> > >>> C.__class__ 				# Followed by instance acquisition: metaclass
> > <class '__main__.M'>
> > >>> C.__class__.attr 			# Another way to get to metaclass attributes
> > 1
> > ```
> 

If you study this, you'll probably notice a nearly glaring symmetry here, which leads us to the next section.

## Inheritance: The Full Story
As it turns out, instance inheritance works in similar ways, whether the "instance" is created from a normal class, or is a class created from a metaclass subclass of type -- a single attribute search rule, which fosters the grander and parallel notion of metaclass inheritance hierarchies. To illustrate the basics of this conceptual merger, in the following, the instance inherits from all its classes; the class inherits from both classes and metaclasses; and metaclasses inherit from higher metaclasses (supermetaclasses?):
> 
> > ```python
> > >>> class M1(type): attr1 = 1 					# Metaclass inheritance tree
> > >>> class M2(M1): attr2 = 2 					# Gets __bases__, __class__, __mro__
> > >>> class C1: attr3 = 3 						# Superclass inheritance tree
> > >>> class C2(C1,metaclass=M2): attr4 = 4 		# Gets __bases__, __class__, __mro__
> > >>> I = C2() 									# I gets __class__ but not others
> > >>> I.attr3, I.attr4 							# Instance inherits from super tree
> > (3, 4)
> > >>> C2.attr1, C2.attr2, C2.attr3, C2.attr4 		# Class gets names from both trees!
> > (1, 2, 3, 4)
> > >>> M2.attr1, M2.attr2 							# Metaclass inherits names too!
> > (1, 2)
> > ```
> 
> Both inheritance paths -- class and metaclass -- employ the same links, though not recursively: instances do not inherit their class's metaclass names, but may request them explicitly:
> 
> > ```python
> > >>> I.__class__ 				# Links followed at instance with no __bases__
> > <class '__main__.C2'>
> > >>> C2.__bases__
> > (<class '__main__.C1'>,)
> > >>> C2.__class__ 				# Links followed at class after __bases__
> > <class '__main__.M2'>
> > >>> M2.__bases__
> > (<class '__main__.M1'>,)
> > >>> I.__class__.attr1 		# Route inheritance to the class's meta tree
> > 1
> > >>> I.attr1 					# Though class's __class__ not followed normally
> > AttributeError: 'C2' object has no attribute 'attr1'
> > >>> M2.__class__ 				# Both trees have MROs and instance links
> > <class 'type'>
> > >>> [x.__name__ for x in C2.__mro__] 			# __bases__ tree from I.__class__
> > ['C2', 'C1', 'object']
> > >>> [x.__name__ for x in M2.__mro__] 			# __bases__ tree from C2.__class__
> > ['M2', 'M1', 'type', 'object']
> > ```
> 

If you care about metaclasses, or must use code that does, study these examples, and then study them again. In effect, inheritance follows \_\_bases\_\_ before following a single \_\_class\_\_; normal instances have no \_\_bases\_\_; and classes have both -- whether normal or metaclass. In fact, understanding this example is important to Python name resolution in general, as the next section explains.

### Python's inheritance algorithm: The simple version
Now that we know about metaclass acquisition, we're finally able to formalize the inheritance rules that they augment. Technically, inheritance deploys two distinct but similar lookup routines, and is based on MROs. Because \_\_bases\_\_ are used to construct the \_\_mro\_\_ ordering at class creation time, and because a class's \_\_mro\_\_ includes itself, the prior section's generalization is the same as the following -- a first-cut definition of Python's new-style inheritance algorithm:

To look up an explicit attribute name:
1. From an instance I, search the instance, then its class, and then all its superclasses, using:
  a. The \_\_dict\_\_ of the instance I
  b. The \_\_dict\_\_ of all classes on the \_\_mro\_\_ found at I's \_\_class\_\_, from left to right
2. From a class C, search the class, then all its superclasses, and then its metaclasses tree, using:
  a. The \_\_dict\_\_ of all classes on the \_\_mro\_\_ found at C itself, from left to right
  b. The \_\_dict\_\_ of all metaclasses on the \_\_mro\_\_ found at C's \_\_class\_\_, from left to right
3. In both rule 1 and 2, give precedence to data descriptors located in step b sources (see ahead).
4. In both rule 1 and 2, skip step a and begin the search at step b for built-in operations (see ahead).

The first two steps are followed for normal, explicit attribute fetch only. There are exceptions for both built-ins and descriptors, both of which we'll clarify in a moment. In addition, a \_\_getattr\_\_ or \_\_getattribute\_\_ may also be used for missing or all names, respectively, per Chapter 38.

Most programmers need only be aware of the first of these rules, and perhaps the first step of the second -- which taken together correspond to 2.X classic class inheritance. There's an extra acquisition step added for metaclasses (2b), but it's essentially the same as others -- a fairly subtle equivalence to be sure, but metaclass acquisition is not as novel as it may seem. In fact, it's just one component of the larger model.

### The descriptors special case
At least that's the normal -- and simplistic -- case. I listed step 3 in the prior section specially, because it doesn't apply to most code, and complicates the algorithm substantially. It turns out, though, that inheritance also has a special case interaction with Chapter 38's attribute descriptors. In short, some descriptors known as data descriptors -- those that define \_\_set\_\_ methods to intercept assignments -- are given precedence, such that their names override other inheritance sources.

This exception serves some practical roles. For example, it is used to ensure that the special \_\_class\_\_ and \_\_dict\_\_ attributes cannot be redefined by the same names in an instance's own \_\_dict\_\_:
> ```python
> >>> class C: pass 					# Inheritance special case #1...
> >>> I = C() 						# Class data descriptors have precedence
> >>> I.__class__, I.__dict__
> (<class '__main__.C'>, {})
> >>> I.__dict__['name'] = 'bob' 		# Dynamic data in the instance
> >>> I.__dict__['__class__'] = 'spam' 		# Assign keys, not attributes
> >>> I.__dict__['__dict__'] = {}
> >>> I.name 							# I.name comes from I.__dict__ as usual
> 'bob' 								# But I.__class__ and I.__dict__ do not!
> >>> I.__class__, I.__dict__
> (<class '__main__.C'>, {'__class__': 'spam', '__dict__': {}, 'name': 'bob'})
> ```

This data descriptor exception is tested before the preceding two inheritance rules as a preliminary step, may be more important to Python implementers than Python programmers, and can be reasonably ignored by most application code in any event -- that is, unless you code data descriptors of your own, which follow the same inheritance special case precedence rule:
> ```python
> >>> class D:
>         def __get__(self, instance, owner): print('__get__')
>         def __set__(self, instance, value): print('__set__')
> >>> class C: d = D() 					# Data descriptor attribute
> >>> I = C()
> >>> I.d 								# Inherited data descriptor access
> __get__
> >>> I.d = 1
> __set__
> >>> I.__dict__['d'] = 'spam' 			# Define same name in instance namespace dict
> >>> I.d 								# But doesn't hide data descriptor in class!
> __get__
> ```

Conversely, if this descriptor did not define a \_\_set\_\_, the name in the instance's dictionary would hide the name in its class instead, per normal inheritance:
> ```python
> >>> class D:
>         def __get__(self, instance, owner): print('__get__')
> >>> class C: d = D()
> >>> I = C()
> >>> I.d 						# Inherited nondata descriptor access
> __get__
> >>> I.__dict__['d'] = 'spam'  # Hides class names per normal inheritance rules
> >>> I.d
> 'spam'
> ```

In both cases, Python automatically runs the descriptor's \_\_get\_\_ when it's found by inheritance, rather than returning the descriptor object itself -- part of the attribute magic we met earlier in the book. The special status afforded to data descriptors, however, also modifies the meaning of attribute inheritance, and thus the meaning of names in your code.

### Python's inheritance algorithm: The somewhat-more-complete version
With both the data descriptor special case and general descriptor invocation factored in with class and metaclass trees, Python's full new-style inheritance algorithm can be stated as follows -- a complex procedure, which assumes knowledge of descriptors, metaclasses, and MROs, but is the final arbiter of attribute names nonetheless (in the following, items are attempted in sequence either as numbered, or per their left-to-right order in "or" conjunctions):

To look up an explicit attribute name:
1. From an instance I, search the instance, its class, and its superclasses, as follows:
  a. Search the \_\_dict\_\_ of all classes on the \_\_mro\_\_ found at I's \_\_class\_\_
  b. If a data descriptor was found in step a, call it and exit
  c. Else, return a value in the \_\_dict\_\_ of the instance I
  d. Else, call a nondata descriptor or return a value found in step a
2. From a class C, search the class, its superclasses, and its metaclasses tree, as follows:
  a. Search the \_\_dict\_\_ of all metaclasses on the \_\_mro\_\_ found at C's \_\_class\_\_
  b. If a data descriptor was found in step a, call it and exit
  c. Else, call a descriptor or return a value in the \_\_dict\_\_ of a class on C's own \_\_mro\_\_
  d. Else, call a nondata descriptor or return a value found in step a
3. In both rule 1 and 2, built-in operations essentially use just step a sources (see ahead)

Note here again that this applies to normal, explicit attribute fetch only. The implicit lookup of method names for built-ins doesn't follow these rules, and essentially uses just step a sources in both cases, as the next section will demonstrate.

On top of all this, method \_\_getattr\_\_ may be run if defined when an attribute is not found, and method \_\_getattribute\_\_ may be run for every attribute fetch, though they are special-case extensions to the name lookup model. See Chapter 38 for more on these tools and descriptors.

### Assignment inheritance
Also note that the prior section defines inheritance in terms of attribute reference (lookup), but parts of it apply to attribute assignment as well. As we've learned, assignment normally changes attributes in the subject object itself, but inheritance is also invoked on assignment to test first for some of Chapter 38's attribute management tools, including descriptors and properties. When present, such tools intercept attribute assignment, and may route it arbitrarily.

For example, when an attribute assignment is run for new-style classes, a data descriptor with a \_\_set\_\_ method is acquired from a class by inheritance using the MRO, and has precedence over the normal storage model. In terms of the prior section's rules:
- When applied to an instance, such assignments essentially follow steps a through c of rule 1, searching the instance's class tree, though step b calls \_\_set\_\_ instead of \_\_get\_\_, and step c stops and stores in the instance instead of attempting a fetch.
- When applied to a class, such assignments run the same procedure on the class's metaclass tree: roughly the same as rule 2, but step c stops and stores in the class.

Because descriptors are also the basis for other advanced attribute tools such as properties and slots, this inheritance pre-check on assignment is utilized in multiple contexts. The net effect is that descriptors are treated as an inheritance special case in newstyle classes, for both reference and assignment.

### The built-ins special case
At least that's almost the full story. As we've seen, built-ins don't follow these rules. Instances and classes may both be skipped for built-in operations only, as a special case that differs from normal or explicit name inheritance. Because this is a context-specific divergence, it's easier to demonstrate in code than to weave into a single algorithm.

In the following, str is the built-in, \_\_str\_\_ is its explicit name equivalent, and the instance is skipped for the built-in only:
> ```python
> >>> class C: 						# Inheritance special case #2...
>         attr = 1 					# Built-ins skip a step
>         def __str__(self): return('class')
> >>> I = C()
> >>> I.__str__(), str(I) 			# Both from class if not in instance
> ('class', 'class')
> >>> I.__str__ = lambda: 'instance'
> >>> I.__str__(), str(I) 			# Explicit=>instance, built-in=>class!
> ('instance', 'class')
> >>> I.attr 							# Asymmetric with normal or explicit names
> 1
> >>> I.attr = 2; I.attr
> 2
> ```

As we saw in metaclass5.py earlier, the same holds true for classes: explicit names start at the class, but built-ins start at the class's class, which is its metaclass, and defaults to type:
> ```python
> >>> class D(type):
>         def __str__(self): return('D class')
> >>> class C(D):
>         pass
> >>> C.__str__(C), str(C) 				# Explicit=>super, built-in=>metaclass!
> ('D class', "<class '__main__.C'>")
> >>> class C(D):
>         def __str__(self): return('C class')
> >>> C.__str__(C), str(C) 				# Explicit=>class, built-in=>metaclass!
> ('C class', "<class '__main__.C'>")
> >>> class C(metaclass=D):
>         def __str__(self): return('C class')
> >>> C.__str__(C), str(C) 				# Built-in=>user-defined metaclass
> ('C class', 'D class')
> ```

In fact, it can sometimes be nontrivial to know where a name comes from in this model, since all classes also inherit from object -- including the default type metaclass. In the following's explicit call, C appears to get a default \_\_str\_\_ from object instead of the metaclass, per the first source of class inheritance (the class's own MRO); by contrast, the built-in skips ahead to the metaclass as before:
> ```python
> >>> class C(metaclass=D):
>         pass
> >>> C.__str__(C), str(C) 				# Explicit=>object, built-in=>metaclass
> ("<class '__main__.C'>", 'D class')
> >>> C.__str__
> <slot wrapper '__str__' of 'object' objects>
> >>> for k in (C, C.__class__, type): print([x.__name__ for x in k.__mro__])
> ['C', 'object']
> ['D', 'type', 'object']
> ['type', 'object']
> ```

All of which leads us to this book's final import this quote -- a tenet that seems to conflict with the status given to descriptors and built-ins in the attribute inheritance mechanism of new-style classes:
> Special cases aren't special enough to break the rules.

Some practical needs warrant exceptions, of course. We'll forgo rationales here, but you should carefully consider the implications of an object-oriented language that applies inheritance -- its foundational operation -- in such an uneven and inconsistent fashion. At a minimum, this should underscore the importance of keeping your code simple, to avoid making it dependent on such convoluted rules. As always, your code's users and maintainers will be glad you did.

For more fidelity on this story, see Python's internal implementation of inheritance -- a complete saga chronicled today in its object.c and typeobject.c, the former for normal instances, and the latter for classes. Delving into internals shouldn't be required to use Python, of course, but it's the ultimate source of truth in a complex and evolving system, and sometimes the best you'll find. This is especially true in boundary cases born of accrued exceptions. For our purposes here, let's move on to the last bit of metaclass magic.
