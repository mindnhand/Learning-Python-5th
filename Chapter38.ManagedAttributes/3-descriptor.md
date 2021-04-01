# Descriptors
Descriptors provide an alternative way to intercept attribute access; they are strongly related to the properties discussed in the prior section. Really, a property is a kind of descriptor -- technically speaking, the property built-in is just a simplified way to create a specific type of descriptor that runs method functions on attribute accesses. In fact, descriptors are the underlying implementation mechanism for a variety of class tools, including both properties and slots.

Functionally speaking, the descriptor protocol allows us to route a specific attribute's get, set, and delete operations to methods of a separate class's instance object that we provide. This allows us to insert code to be run automatically on attribute fetches and assignments, intercept attribute deletions, and provide documentation for the attributes if desired.

Descriptors are created as independent classes, and they are assigned to class attributes just like method functions. Like any other class attribute, they are inherited by subclasses and instances. Their access-interception methods are provided with both a self for the descriptor instance itself, as well as the instance of the client class whose attribute references the descriptor object. Because of this, they can retain and use state information of their own, as well as state information of the subject instance. For example, a descriptor may call methods available in the client class, as well as descriptor specific methods it defines.

Like a property, a descriptor manages a single, specific attribute; although it can't catch all attribute accesses generically, it provides control over both fetch and assignment accesses and allows us to change an attribute name freely from simple data to a computation without breaking existing code. Properties really are just a convenient way to create a specific kind of descriptor, and as we shall see, they can be coded as descriptors directly.

Unlike properties, descriptors are broader in scope, and provide a more general tool. For instance, because they are coded as normal classes, descriptors have their own state, may participate in descriptor inheritance hierarchies, can use composition to aggregate objects, and provide a natural structure for coding internal methods and attribute documentation strings.

## The Basics
As mentioned previously, descriptors are coded as separate classes and provide specially named accessor methods for the attribute access operations they wish to intercept -- get, set, and deletion methods in the descriptor class are automatically run when the attribute assigned to the descriptor class instance is accessed in the corresponding way:
> ```python
> class Descriptor:
>     "docstring goes here"
>     def __get__(self, instance, owner): ... 		# Return attr value
>     def __set__(self, instance, value): ... 		# Return nothing (None)
>     def __delete__(self, instance): ... 		# Return nothing (None)
> ```

Classes with any of these methods are considered descriptors, and their methods are special when one of their instances is assigned to another class's attribute -- when the attribute is accessed, they are automatically invoked. If any of these methods are absent, it generally means that the corresponding type of access is not supported. Unlike properties, however, omitting a \_\_set\_\_ allows the descriptor attribute's name to be assigned and thus redefined in an instance, thereby hiding the descriptor -- to make an attribute read-only, you must define \_\_set\_\_ to catch assignments and raise an exception.

Descriptors with \_\_set\_\_ methods also have some special-case implications for inheritance that we'll largely defer until Chapter 40's coverage of metaclasses and the complete inheritance specification. In short, a descriptor with a \_\_set\_\_ is known formally as data descriptor, and is given precedence over other names located by normal inheritance rules. The inherited descriptor for name \_\_class\_\_, for example, overrides the same name in an instance's namespace dictionary. This also works to ensure that data descriptors you code in your own classes take precedence over others.

### Descriptor method arguments
Before we code anything realistic, let's take a brief look at some fundamentals. All three descriptor methods outlined in the prior section are passed both the descriptor class instance (self), and the instance of the client class to which the descriptor instance is attached (instance).

The \_\_get\_\_ access method additionally receives an owner argument, specifying the class to which the descriptor instance is attached. Its instance argument is either the instance through which the attribute was accessed (for instance.attr), or None when the attribute is accessed through the owner class directly (for class.attr). The former of these generally computes a value for instance access, and the latter usually returns self if descriptor object access is supported.

For example, in the following 3.X session, when X.attr is fetched, Python automatically runs the \_\_get\_\_ method of the Descriptor class instance to which the Subject.attr class attribute is assigned. In 2.X, use the print statement equivalent, and derive both classes here from object, as descriptors are a new-style class tool; in 3.X this derivation is implied and can be omitted, but doesn't hurt:
> ```python
> >>> class Descriptor: 		# Add "(object)" in 2.X
>         def __get__(self, instance, owner):
>             print(self, instance, owner, sep='\n')
> >>> class Subject: 			# Add "(object)" in 2.X
>         attr = Descriptor()	# Descriptor instance is class attr
> >>> X = Subject()
> >>> X.attr
> <__main__.Descriptor object at 0x0281E690>
> <__main__.Subject object at 0x028289B0>
> <class '__main__.Subject'>
> >>> Subject.attr
> <__main__.Descriptor object at 0x0281E690>
> None
> <class '__main__.Subject'>
> ```

Notice the arguments automatically passed in to the \_\_get\_\_ method in the first attribute fetch -- when X.attr is fetched, it's as though the following translation occurs (though the Subject.attr here doesn't invoke \_\_get\_\_ again):
> ```python
> X.attr -> Descriptor.__get__(Subject.attr, X, Subject)
> ```

The descriptor knows it is being accessed directly when its instance argument is None.

### Read-only descriptors
As mentioned earlier, unlike properties, simply omitting the \_\_set\_\_ method in a descriptor isn't enough to make an attribute read-only, because the descriptor name can be assigned to an instance. In the following, the attribute assignment to X.a stores a in the instance object X, thereby hiding the descriptor stored in class C:
> ```python
> >>> class D:
>         def __get__(*args): print('get')
> >>> class C:
>         a = D() 		# Attribute a is a descriptor instance
> >>> X = C()
> >>> X.a 			# Runs inherited descriptor __get__
> get
> >>> C.a
> get
> >>> X.a = 99 		# Stored on X, hiding C.a!
> >>> X.a
> 99
> >>> list(X.__dict__.keys())
> ['a']
> >>> Y = C()
> >>> Y.a 			# Y still inherits descriptor
> get
> >>> C.a
> get
> ```

This is the way all instance attribute assignments work in Python, and it allows classes to selectively override class-level defaults in their instances. To make a descriptor-based attribute read-only, catch the assignment in the descriptor class and raise an exception to prevent attribute assignment -- when assigning an attribute that is a descriptor, Python effectively bypasses the normal instance-level assignment behavior and routes the operation to the descriptor object:
> ```python
> >>> class D:
>         def __get__(*args): print('get')
>         def __set__(*args): raise AttributeError('cannot set')
> >>> class C:
>         a = D()
> >>> X = C()
> >>> X.a 		# Routed to C.a.__get__
> get
> >>> X.a = 99 	# Routed to C.a.__set__
> AttributeError: cannot set
> ```

> **Note:**
> Also be careful not to confuse the descriptor \_\_delete\_\_ method with the general \_\_del\_\_ method. The former is called on attempts to delete the managed attribute name on an instance of the owner class; the latter is the general instance destructor method, run when an instance of any kind of class is about to be garbage-collected. \_\_delete\_\_ is more closely related to the \_\_delattr\_\_ generic attribute deletion method we'll meet later in this chapter. See Chapter 30 for more on operator overloading methods.
> 

## A First Example
To see how this all comes together in more realistic code, let's get started with the same first example we wrote for properties. The following defines a descriptor that intercepts access to an attribute named name in its clients. Its methods use their instance argument to access state information in the subject instance, where the name string is actually stored. Like properties, descriptors work properly only for new-style classes, so be sure to derive both classes in the following from object if you're using 2.X -- it's not enough to derive just the descriptor, or just its client:
> ```python
> class Name: 				# Use (object) in 2.X
>     "name descriptor docs"
>     def __get__(self, instance, owner):
>         print('fetch...')
>         return instance._name
>     def __set__(self, instance, value):
>         print('change...')
>         instance._name = value
>     def __delete__(self, instance):
>         print('remove...')
>         del instance._name
> 
> class Person: 			# Use (object) in 2.X
>     def __init__(self, name):
>         self._name = name
>     name = Name() 			# Assign descriptor to attr
> 
> bob = Person('Bob Smith') 	# bob has a managed attribute
> print(bob.name) 				# Runs Name.__get__
> bob.name = 'Robert Smith' 	# Runs Name.__set__
> print(bob.name)
> del bob.name 					# Runs Name.__delete__
> print('-'*20)
> sue = Person('Sue Jones') 	# sue inherits descriptor too
> print(sue.name)
> print(Name.__doc__) 			# Or help(Name)
> ```

Notice in this code how we assign an instance of our descriptor class to a class attribute in the client class; because of this, it is inherited by all instances of the class, just like a class's methods. Really, we must assign the descriptor to a class attribute like this -- it won't work if assigned to a self instance attribute instead. When the descriptor's \_\_get\_\_ method is run, it is passed three objects to define its context:
- self is the Name class instance.
- instance is the Person class instance.
- owner is the Person class.

When this code is run the descriptor's methods intercept accesses to the attribute, much like the property version. In fact, the output is the same again:
> ```powershell
> c:\code> py -3 desc-person.py
> fetch...
> Bob Smith
> change...
> fetch...
> Robert Smith
> remove...
> --------------------
> fetch...
> Sue Jones
> name descriptor docs
> ```

Also like in the property example, our descriptor class instance is a class attribute and thus is inherited by all instances of the client class and any subclasses. If we change the Person class in our example to the following, for instance, the output of our script is the same:
> ```python
> ...
> class Super:
>     def __init__(self, name):
>         self._name = name
>     name = Name()
> 
> class Person(Super): 				# Descriptors are inherited (class attrs)
>     pass
>     ...
> ```

Also note that when a descriptor class is not useful outside the client class, it's perfectly reasonable to embed the descriptor's definition inside its client syntactically. Here's what our example looks like if we use a nested class:
> ```python
> class Person:
>     def __init__(self, name):
>         self._name = name
> 
>     class Name: 			# Using a nested class
>         "name descriptor docs"
>         def __get__(self, instance, owner):
>             print('fetch...')
>             return instance._name
>         def __set__(self, instance, value):
>             print('change...')
>             instance._name = value
>         def __delete__(self, instance):
>             print('remove...')
>             del instance._name
> 
>     name = Name()
> ```

When coded this way, Name becomes a local variable in the scope of the Person class statement, such that it won't clash with any names outside the class. This version works the same as the original -- we've simply moved the descriptor class definition into the client class's scope -- but the last line of the testing code must change to fetch the docstring from its new location (per the example file desc-person-nested.py):
> ```python
> ...
> print(Person.Name.__doc__) # Differs: not Name.__doc__ outside class
> ```

## Computed Attributes
As was the case when using properties, our first descriptor example of the prior section didn't do much -- it simply printed trace messages for attribute accesses. In practice, descriptors can also be used to compute attribute values each time they are fetched. The following illustrates -- it's a rehash of the same example we coded for properties, which uses a descriptor to automatically square an attribute's value each time it is fetched: 
> ```python
> class DescSquare:
>     def __init__(self, start): 				# Each desc has own state
>         self.value = start
>     def __get__(self, instance, owner): 		# On attr fetch
>         return self.value ** 2
>     def __set__(self, instance, value): 		# On attr assign
>         self.value = value 			# No delete or docs
> 
> class Client1:
>     X = DescSquare(3) 			# Assign descriptor instance to class attr
> class Client2:
>     X = DescSquare(32) 			# Another instance in another client class
> 
> # Could also code two instances in same class
> c1 = Client1()
> c2 = Client2()
> print(c1.X) 			# 3 ** 2
> c1.X = 4
> print(c1.X) 			# 4 ** 2
> print(c2.X) 			# 32 ** 2 (1024)
> ```

When run, the output of this example is the same as that of the original property-based version, but here a descriptor class object is intercepting the attribute accesses:
> ```powershell
> c:\code> py -3 desc-computed.py
> 9
> 16
> 1024
> ```

## Using State Information in Descriptors
If you study the two descriptor examples we've written so far, you might notice that they get their information from different places -- the first (the name attribute example) uses data stored on the client instance, and the second (the attribute squaring example) uses data attached to the descriptor object itself (a.k.a. self). In fact, descriptors can use both instance state and descriptor state, or any combination thereof:
- Descriptor state is used to manage either data internal to the workings of the descriptor, or data that spans all instances. It can vary per attribute appearance (often, per client class).
- Instance state records information related to and possibly created by the client class. It can vary per client class instance (that is, per application object).

In other words, descriptor state is per-descriptor data and instance state is per-client instance data. As usual in OOP, you must choose state carefully. For instance, you would not normally use descriptor state to record employee names, since each client instance requires its own value -- if stored in the descriptor, each client class instance will effectively share the same single copy. On the other hand, you would not usually use instance state to record data pertaining to descriptor implementation internals -- if stored in each instance, there would be multiple varying copies.

Descriptor methods may use either state form, but descriptor state often makes it unnecessary to use special naming conventions to avoid name collisions in the instance for data that is not instance-specific. For example, the following descriptor attaches information to its own instance, so it doesn't clash with that on the client class's instance -- but also shares that information between two client instances:
> 
> > ```python
> > class DescState: 				# Use descriptor state, (object) in 2.X
> >     def __init__(self, value):
> >         self.value = value
> >     def __get__(self, instance, owner): 		# On attr fetch
> >         print('DescState get')
> >         return self.value * 10
> >     def __set__(self, instance, value): 		# On attr assign
> >         print('DescState set')
> >         self.value = value
> > 
> > # Client class
> > class CalcAttrs:
> >     X = DescState(2) 			# Descriptor class attr
> >     Y = 3 					# Class attr
> >     def __init__(self):
> >         self.Z = 4 			# Instance attr
> > 
> > obj = CalcAttrs()
> > print(obj.X, obj.Y, obj.Z) 	# X is computed, others are not
> > obj.X = 5 					# X assignment is intercepted
> > CalcAttrs.Y = 6 				# Y reassigned in class
> > obj.Z = 7 					# Z assigned in instance
> > print(obj.X, obj.Y, obj.Z)
> > obj2 = CalcAttrs() 			# But X uses shared data, like Y!
> > print(obj2.X, obj2.Y, obj2.Z)
> > ```
> 
> This code's internal value information lives only in the descriptor, so there won't be a collision if the same name is used in the client's instance. Notice that only the descriptor attribute is managed here -- get and set accesses to X are intercepted, but accesses to Y and Z are not (Y is attached to the client class and Z to the instance). When this code is run, X is computed when fetched, but its value is also the same for all client instances because it uses descriptor-level state:
> 
> > ```powershell
> > c:\code> py -3 desc-state-desc.py
> > DescState get
> > 20 3 4
> > DescState set
> > DescState get
> > 50 6 7
> > DescState get
> > 50 6 4
> > ```
> 

It's also feasible for a descriptor to store or use an attribute attached to the client class's instance, instead of itself. Crucially, unlike data stored in the descriptor itself, this allows for data that can vary per client class instance. The descriptor in the following example assumes the instance has an attribute \_X attached by the client class, and uses it to compute the value of the attribute it represents:
> 
> > ```python
> > class InstState: 					# Using instance state, (object) in 2.X
> >     def __get__(self, instance, owner):
> >         print('InstState get') 		# Assume set by client class
> >         return instance._X * 10
> >     def __set__(self, instance, value):
> >         print('InstState set')
> >         instance._X = value
> > 
> > # Client class
> > class CalcAttrs:
> >     X = InstState() 			# Descriptor class attr
> >     Y = 3 					# Class attr
> >     def __init__(self):
> >         self._X = 2 				# Instance attr
> >         self.Z = 4 				# Instance attr
> > 
> > obj = CalcAttrs()
> > print(obj.X, obj.Y, obj.Z) 	# X is computed, others are not
> > obj.X = 5 					# X assignment is intercepted
> > CalcAttrs.Y = 6 				# Y reassigned in class
> > obj.Z = 7 					# Z assigned in instance
> > print(obj.X, obj.Y, obj.Z)
> > obj2 = CalcAttrs() 			# But X differs now, like Z!
> > print(obj2.X, obj2.Y, obj2.Z)
> > ```
> 
> Here, X is assigned to a descriptor as before that manages accesses. The new descriptor here, though, has no information itself, but it uses an attribute assumed to exist in the instance -- that attribute is named \_X, to avoid collisions with the name of the descriptor itself. When this version is run the results are similar, but the value of the descriptor attribute can vary per client instance due to the differing state policy:
> 
> > ```python
> > c:\code> py -3 desc-state-inst.py
> > InstState get
> > 20 3 4
> > InstState set
> > InstState get
> > 50 6 7
> > InstState get
> > 20 6 4
> > ```
> 

Both descriptor and instance state have roles. In fact, this is a general advantage that descriptors have over properties -- because they have state of their own, they can easily retain data internally, without adding it to the namespace of the client instance object. As a summary, the following uses both state sources -- its self.data retains per-attribute information, while its instance.data can vary per client instance:
> 
> > ```python
> > >>> class DescBoth:
> >         def __init__(self, data):
> >             self.data = data
> >         def __get__(self, instance, owner):
> >             return '%s, %s' % (self.data, instance.data)
> >         def __set__(self, instance, value):
> >             instance.data = value
> > 
> > >>> class Client:
> >         def __init__(self, data):
> >             self.data = data
> >         managed = DescBoth('spam')
> > 
> > >>> I = Client('eggs')
> > >>> I.managed 			# Show both data sources
> > 'spam, eggs'
> > >>> I.managed = 'SPAM' 	# Change instance data
> > >>> I.managed
> > 'spam, SPAM'
> > ```
> 
> We'll revisit the implications of this choice in a larger case study later in this chapter. Before we move on, recall from Chapter 32's coverage of slots that we can access "virtual" attributes like properties and descriptors with tools like dir and getattr, even though they don't exist in the instance's namespace dictionary. Whether you should access these this way probably varies per program -- properties and descriptors may run arbitrary computation, and may be less obviously instance "data" than slots:
> 
> > ```python
> > >>> I.__dict__
> > {'data': 'SPAM'}
> > >>> [x for x in dir(I) if not x.startswith('__')]
> > ['data', 'managed']
> > >>> getattr(I, 'data')
> > 'SPAM'
> > >>> getattr(I, 'managed')
> > 'spam, SPAM'
> > >>> for attr in (x for x in dir(I) if not x.startswith('__')):
> >         print('%s => %s' % (attr, getattr(I, attr)))
> > data => SPAM
> > managed => spam, SPAM
> > ```
> 

The more generic \_\_getattr\_\_ and \_\_getattribute\_\_ tools we'll meet later are not designed to support this functionality -- because they have no class-level attributes, their "virtual" attribute names do not appear in dir results. In exchange, they are also not limited to specific attribute names coded as properties or descriptors: tools that share even more than this behavior, as the next section explains.

## How Properties and Descriptors Relate
As mentioned earlier, properties and descriptors are strongly related -- the property built-in is just a convenient way to create a descriptor. Now that you know how both work, you should also be able to see that it's possible to simulate the property built-in with a descriptor class like the following:
> 
> > ```python
> > class Property:
> >     def __init__(self, fget=None, fset=None, fdel=None, doc=None):
> >         self.fget = fget
> >         self.fset = fset
> >         self.fdel = fdel 					# Save unbound methods
> >         self.__doc__ = doc 				# or other callables
> >     def __get__(self, instance, instancetype=None):
> >         if instance is None:
> >             return self
> >         if self.fget is None:
> >             raise AttributeError("can't get attribute")
> >         return self.fget(instance) 		# Pass instance to self
> >     										# in property accessors
> >     def __set__(self, instance, value):
> >         if self.fset is None:
> >             raise AttributeError("can't set attribute")
> >         self.fset(instance, value)
> >     def __delete__(self, instance):
> >         if self.fdel is None:
> >             raise AttributeError("can't delete attribute")
> >         self.fdel(instance)
> > 
> > class Person:
> >     def getName(self): print('getName...')
> >     def setName(self, value): print('setName...')
> >     name = Property(getName, setName) 			# Use like property()
> > 
> > x = Person()
> > x.name
> > x.name = 'Bob'
> > del x.name
> > ```
> 
> This Property class catches attribute accesses with the descriptor protocol and routes requests to functions or methods passed in and saved in descriptor state when the class is created. Attribute fetches, for example, are routed from the Person class, to the Property class's \_\_get\_\_ method, and back to the Person class's getName. With descriptors, this "just works":
> 
> > ```powershell
> > c:\code> py -3 prop-desc-equiv.py
> > getName...
> > setName...
> > AttributeError: can't delete attribute
> > ```
> 

Note that this descriptor class equivalent only handles basic property usage, though; to use @ decorator syntax to also specify set and delete operations, we'd have to extend our Property class with setter and deleter methods, which would save the decorated accessor function and return the property object (self should suffice). Since the prop erty built-in already does this, we'll omit a formal coding of this extension here.

### Descriptors and slots and more
You can also probably now at least in part imagine how descriptors are used to implement Python's slots extension: instance attribute dictionaries are avoided by creating class-level descriptors that intercept slot name access, and map those names to sequential storage space in the instance. Unlike the explicit property call, though, much of the magic behind slots is orchestrated at class creation time both automatically and implicitly, when a \_\_slots\_\_ attribute is present in a class. See Chapter 32 for more on slots (and why they're not recommended except in pathological use cases). Descriptors are also used for other class tools, but we'll omit further internals details here; see Python's manuals and source code for more details.

> **Note:**
> In Chapter 39, we'll also make use of descriptors to implement function decorators that apply to both functions and methods. As you'll see there, because descriptors receive both descriptor and subject class instances they work well in this role, though nested functions are usually a conceptually much simpler solution. We'll also deploy descriptors as one way to intercept built-in operation method fetches in Chapter 39.
> Be sure to also see Chapter 40's coverage of data descriptors' precedence in the full inheritance model mentioned earlier: with a \_\_set\_\_, descriptors override other names, and are thus fairly binding -- they cannot be hidden by names in instance dictionaries.
> 
