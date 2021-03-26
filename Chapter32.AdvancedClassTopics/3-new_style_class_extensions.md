# New-Style Class Extensions
Beyond the changes described in the prior section (some of which, frankly, may seem too academic and obscure to matter to many readers of this book), new-style classes provide a handful of more advanced class tools that have more direct and practical application -- slots, properties, descriptors, and more. The following sections provide an overview of each of these additional features, available for new-style class in Python 2.X and all classes in Python 3.X. Also in this extensions category are the \_\_mro\_\_ attribute and the super call, both covered elsewhere -- the former in the previous section to explore a change, and the latter postponed until chapter end to serve as a larger case study.

## Slots: Attribute Declarations
By assigning a sequence of string attribute names to a special \_\_slots\_\_ class attribute, we can enable a new-style class to both limit the set of legal attributes that instances of the class will have, and optimize memory usage and possibly program speed. As we'll find, though, slots should be used only in applications that clearly warrant the added complexity. They will complicate your code, may complicate or break code you may use, and require universal deployment to be effective.

### Slot basics
To use slots, assign a sequence of string names to the special \_\_slots\_\_ variable and attribute at the top level of a class statement: only those names in the \_\_slots\_\_ list can be assigned as instance attributes. However, like all names in Python, instance attribute names must still be assigned before they can be referenced, even if they're listed in \_\_slots\_\_:
> ```python
> >>> class limiter(object):
>         __slots__ = ['age', 'name', 'job']
> >>> x = limiter()
> >>> x.age 					# Must assign before use
> AttributeError: age
> >>> x.age = 40 				# Looks like instance data
> >>> x.age
> 40
> >>> x.ape = 1000 				# Illegal: not in __slots__
> AttributeError: 'limiter' object has no attribute 'ape'
> ```

This feature is envisioned as both a way to catch typo errors like this (assignments to illegal attribute names not in \_\_slots\_\_ are detected) as well as an optimization mechanism.

Allocating a namespace dictionary for every instance object can be expensive in terms of memory if many instances are created and only a few attributes are required. To save space, instead of allocating a dictionary for each instance, Python reserves just enough space in each instance to hold a value for each slot attribute, along with inherited attributes in the common class to manage slot access. This might additionally speed execution, though this benefit is less clear and might vary per program, platform, and Python.

Slots are also something of a major break with Python's core dynamic nature, which dictates that any name may be created by assignment. In fact, they imitate C++ for efficiency at the expense of flexibility, and even have the potential to break some programs. As we'll see, slots also come with a plethora of special-case usage rules. Per Python's own manual, they should not be used except in clearly warranted cases -- they are difficult to use correctly, and are, to quote the manual:
> best reserved for rare cases where there are large numbers of instances in a memorycritical application.

In other words, this is yet another feature that should be used only if clearly warranted. Unfortunately, slots seem to be showing up in Python code much more often than they should; their obscurity seems to be a draw in itself. As usual, knowledge is your best ally in such things, so let's take a quick look here.

> **NOTE**
> In Python 3.3, non-slots attribute space requirements have been reduced with a key-sharing dictionary model, where the \_\_dict\_\_ dictionaries used for objects' attributes may share part of their internal storage, including that of their keys. This may lessen some of the value of \_\_slots\_\_ as an optimization tool; per benchmark reports, this change reduces memory use by 10% to 20% for object-oriented programs, gives a small improvement in speed for programs that create many similar objects, and may be optimized further in the future. On the other hand, this won't negate the presence of \_\_slots\_\_ in existing code you may need to understand!
> 

### Slots and namespace dictionaries
Potential benefits aside, slots can complicate the class model -- and code that relies on it -- substantially. In fact, some instances with slots may not have a \_\_dict\_\_ attribute namespace dictionary at all, and others will have data attributes that this dictionary does not include. To be clear: this is a major incompatibility with the traditional class model -- one that can complicate any code that accesses attributes generically, and may even cause some programs to fail altogether.

For instance, programs that list or access instance attributes by name string may need to use more storage-neutral interfaces than \_\_dict\_\_ if slots may be used. Because an instance's data may include class-level names such as slots -- either in addition to or instead of namespace dictionary storage -- both attribute sources may need to be queried for completeness.

Let's see what this means in terms of code, and explore more about slots along the way. First off, when slots are used, instances do not normally have an attribute dictionary -- instead, Python uses the class descriptors feature introduced ahead to allocate and manage space reserved for slot attributes in the instance. In Python 3.X, and in 2.X for new-style classes derived from object:
> ```python
> >>> class C: 					# Requires "(object)" in 2.X only
>         __slots__ = ['a', 'b'] 		# __slots__ means no __dict__ by default
> >>> X = C()
> >>> X.a = 1
> >>> X.a
> 1
> >>> X.__dict__
> AttributeError: 'C' object has no attribute '__dict__'
> ```

However, we can still fetch and set slot-based attributes by name string using storageneutral tools such as getattr and setattr (which look beyond the instance \_\_dict\_\_ and thus include class-level names like slots) and dir (which collects all inherited names throughout a class tree):
> ```python
> >>> getattr(X, 'a')
> 1
> >>> setattr(X, 'b', 2) 			# But getattr() and setattr() still work
> >>> X.b
> 2
> >>> 'a' in dir(X) 				# And dir() finds slot attributes too
> True
> >>> 'b' in dir(X)
> True
> ```

Also keep in mind that without an attribute namespace dictionary, it's not possible to assign new names to instances that are not names in the slots list:
> ```python
> >>> class D: 					# Use D(object) for same result in 2.X
>         __slots__ = ['a', 'b']
>         def __init__(self):
>             self.d = 4 			# Cannot add new names if no __dict__
> >>> X = D()
> AttributeError: 'D' object has no attribute 'd'
> ```

We can still accommodate extra attributes, though, by including \_\_dict\_\_ explicitly in \_\_slots\_\_, in order to create an attribute namespace dictionary too:
> ```python
> >>> class D:
>         __slots__ = ['a', 'b', '__dict__'] 			# Name __dict__ to include one too
>         c = 3 					# Class attrs work normally
>         def __init__(self):
>             self.d = 4 				# d stored in __dict__, a is a slot
> >>> X = D()
> >>> X.d
> 4
> >>> X.c
> 3
> >>> X.a 					# All instance attrs undefined until assigned
> AttributeError: a
> >>> X.a = 1
> >>> X.b = 2
> ```

In this case, both storage mechanisms are used. This renders \_\_dict\_\_ too limited for code that wishes to treat slots as instance data, but generic tools such as getattr still allow us to process both storage forms as a single set of attributes:
> ```python
> >>> X.__dict__ 			# Some objects have both __dict__ and slot names
> {'d': 4} 					# getattr() can fetch either type of attr
> >>> X.__slots__
> ['a', 'b', '__dict__']
> >>> getattr(X, 'a'), getattr(X, 'c'), getattr(X, 'd') 			# Fetches all 3 forms
> (1, 3, 4)
> ```

Because dir also returns all inherited attributes, though, it might be too broad in some contexts; it also includes class-level methods, and even all object defaults. Code that wishes to list just instance attributes may in principle still need to allow for both storage forms explicitly. We might at first naively code this as follows:
> ```python
> >>> for attr in list(X.__dict__) + X.__slots__: 			# Wrong...
>         print(attr, '=>', getattr(X, attr))
> ```

Since either can be omitted, we may more correctly code this as follows, using get attr to allow for defaults -- a noble but nonetheless inaccurate approach, as the next section will explain:
> ```python
> >>> for attr in list(getattr(X, '__dict__', [])) + getattr(X, '__slots__', []):
>         print(attr, '=>', getattr(X, attr))
> d => 4
> a => 1 					# Less wrong...
> b => 2
> __dict__ => {'d': 4}
> ```

### Multiple \_\_slots\_\_ lists in superclasses
The preceding code works in this specific case, but in general it's not entirely accurate. Specifically, this code addresses only slot names in the lowest \_\_slots\_\_ attribute inherited by an instance, but slot lists may appear more than once in a class tree. That is, a name's absence in the lowest \_\_slots\_\_ list does not preclude its existence in a higher \_\_slots\_\_. Because slot names become class-level attributes, instances acquire the union of all slot names anywhere in the tree, by the normal inheritance rule:
> ```python
> >>> class E:
>         __slots__ = ['c', 'd'] 			# Superclass has slots
> >>> class D(E):
>         __slots__ = ['a', '__dict__'] 	# But so does its subclass
> >>> X = D()
> >>> X.a = 1; X.b = 2; X.c = 3 			# The instance is the union (slots: a, c)
> >>> X.a, X.c
> (1, 3)
> ```

Inspecting just the inherited slots list won't pick up slots defined higher in a class tree:
> ```python
> >>> E.__slots__ 				# But slots are not concatenated
> ['c', 'd']
> >>> D.__slots__
> ['a', '__dict__']
> >>> X.__slots__ 				# Instance inherits *lowest* __slots__
> ['a', '__dict__']
> >>> X.__dict__ 					# And has its own an attr dict
> {'b': 2}
> >>> for attr in list(getattr(X, '__dict__', [])) + getattr(X, '__slots__', []):
>         print(attr, '=>', getattr(X, attr))
> b => 2 						# Other superclass slots missed!
> a => 1
> __dict__ => {'b': 2}
> >>> dir(X) 					# But dir() includes all slot names
> [...many names omitted... 'a', 'b', 'c', 'd']
> ```

In other words, in terms of listing instance attributes generically, one \_\_slots\_\_ isn't always enough -- they are potentially subject to the full inheritance search procedure. See the earlier mapattrs-slots.py for another example of slots appearing in multiple superclasses. If multiple classes in a class tree have their own \_\_slots\_\_ attributes, generic programs must develop other policies for listing attributes -- as the next section explains.

### Handling slots and other "virtual" attributes generically
At this point, you may wish to review the discussion of slots policy options at the coverage of the lister.py display mix-in classes near the end of the preceding chapter -- a prime example of why generic programs may need to care about slots. Such tools that attempt to list instance data attributes generically must account for slots, and perhaps other such "virtual" instance attributes like properties and descriptors discussed ahead -- names that similarly reside in classes but may provide attribute values for instances on request. Slots are the most data-centric of these, but are representative of a larger category.

Such attributes require inclusive approaches, special handling, or general avoidance --  the latter of which becomes unsatisfactory as soon as any programmer uses slots in subject code. Really, class-level instance attributes like slots probably necessitate a redefinition of the term instance data -- as locally stored attributes, the union of all inherited attributes, or some subset thereof.

For example, some programs might classify slot names as attributes of classes instead of instances; these attributes do not exist in instance namespace dictionaries, after all. Alternatively, as shown earlier, programs can be more inclusive by relying on dir to fetch all inherited attribute names and getattr to fetch their corresponding values for the instance -- without regard to their physical location or implementation. If you must support slots as instance data, this is likely the most robust way to proceed:
> ```python
> >>> class Slotful:
>         __slots__ = ['a', 'b', '__dict__']
>         def __init__(self, data):
>             self.c = data
> >>> I = Slotful(3)
> >>> I.a, I.b = 1, 2
> >>> I.a, I.b, I.c 				# Normal attribute fetch
> (1, 2, 3)
> >>> I.__dict__ 					# Both __dict__ and slots storage
> {'c': 3}
> >>> [x for x in dir(I) if not x.startswith('__')]
> ['a', 'b', 'c']
> >>> I.__dict__['c'] 				# __dict__ is only one attr source
> 3
> >>> getattr(I, 'c'), getattr(I, 'a') 			# dir+getattr is broader than __dict__
> (3, 1) 				# applies to slots, properties, descrip
> >>> for a in (x for x in dir(I) if not x.startswith('__')):
>         print(a, getattr(I, a))
> a 1
> b 2
> c 3
> ```

Under this dir/getattr model, you can still map attributes to their inheritance sources, and filter them more selectively by source or type if needed, by scanning the MRO -- as we did earlier in both mapattrs.py and its application to slots in mapattrs-slots.py. As an added bonus, such tools and policies for handling slots will potentially apply automatically to properties and descriptors too, though these attributes are more explicitly computed values, and less obviously instance-related data than slots.

Also keep in mind that this is not just a tools issue. Class-based instance attributes like slots also impact the traditional coding of the \_\_setattr\_\_ operator overloading method we met in Chapter 30. Because slots and some other attributes are not stored in the instance \_\_dict\_\_, and may even imply its absence, new-style classes must instead generally run attribute assignments by routing them to the object superclass. In practice, this may make this method fundamentally different in some classic and new-style classes.

### Slot usage rules
Slot declarations can appear in multiple classes in a class tree, but when they do they are subject to a number of constraints that are somewhat difficult to rationalize unless you understand the implementation of slots as class-level descriptors for each slot name that are inherited by the instances where the managed space is reserved (descriptors are an advanced tool we'll study in detail in the last part of this book):

- **Slots in subs are pointless when absent in supers:** If a subclass inherits from a superclass without a \_\_slots\_\_, the instance \_\_dict\_\_ attribute created for the superclass will always be accessible, making a \_\_slots\_\_ in the subclass largely pointless. The subclass still manages its slots, but doesn't compute their values in any way, and doesn't avoid a dictionary -- the main reason to use slots.

- **Slots in supers are pointless when absent in subs:** Similarly, because the meaning of a \_\_slots\_\_ declaration is limited to the class in which it appears, subclasses will produce an instance \_\_dict\_\_ if they do not define a \_\_slots\_\_, rendering a \_\_slots\_\_ in a superclass largely pointless.

- **Redefinition renders super slots pointless:** If a class defines the same slot name as a superclass, its redefinition hides the slot in the superclass per normal inheritance. You can access the version of the name defined by the superclass slot only by fetching its descriptor directly from the superclass.

- **Slots prevent class-level defaults:** Because slots are implemented as class-level descriptors (along with per-instance space), you cannot use class attributes of the same name to provide defaults as you can for normal instance attributes: assigning the same name in the class overwrites the slot descriptor.

- **Slots and \_\_dict\_\_:** As shown earlier, \_\_slots\_\_ preclude both an instance \_\_dict\_\_ and assigning names not listed, unless \_\_dict\_\_ is listed explicitly too.

We've already seen the last of these in action, and the earlier mapattrs-slots.py illustrates the third. It's easy to demonstrate how the new rules here translate to actual code -- most crucially, a namespace dictionary is created when any class in a tree omits slots, thereby negating the memory optimization benefit:
> ```python
> >>> class C: pass 					# Bullet 1: slots in sub but not super
> >>> class D(C): __slots__ = ['a'] 	# Makes instance dict for nonslots
> >>> X = D() 							# But slot name still managed in class
> >>> X.a = 1; X.b = 2
> >>> X.__dict__
> {'b': 2}
> >>> D.__dict__.keys()
> dict_keys([... 'a', '__slots__', ...])
> >>> class C: __slots__ = ['a'] 		# Bullet 2: slots in super but not sub
> >>> class D(C): pass 					# Makes instance dict for nonslots
> >>> X = D() 							# But slot name still managed in class
> >>> X.a = 1; X.b = 2
> >>> X.__dict__
> {'b': 2}
> >>> C.__dict__.keys()
> dict_keys([... 'a', '__slots__', ...])
> >>> class C: __slots__ = ['a'] 		# Bullet 3: only lowest slot accessible
> >>> class D(C): __slots__ = ['a']
> >>> class C: __slots__ = ['a']; a = 99 		# Bullet 4: no class-level defaults
> ValueError: 'a' in __slots__ conflicts with class variable
> ```

In other words, besides their program-breaking potential, slots essentially require both universal and careful deployment to be effective -- because slots do not compute values dynamically like properties (coming up in the next section), they are largely pointless unless each class in a tree uses them and is cautious to define only new slot names not defined by other classes. It's an all-or-nothing feature -- an unfortunate property shared by the super call discussed ahead:
> ```python
> >>> class C: __slots__ = ['a'] 			# Assumes universal use, differing names
> >>> class D(C): __slots__ = ['b']
> >>> X = D()
> >>> X.a = 1; X.b = 2
> >>> X.__dict__
> AttributeError: 'D' object has no attribute '__dict__'
> >>> C.__dict__.keys(), D.__dict__.keys()
> (dict_keys([... 'a', '__slots__', ...]), dict_keys([... 'b', '__slots__', ...]))
> ```

Such rules -- among others regarding weak references omitted here for space -- are part of the reason slots are not generally recommended, except in pathological cases where their space reduction is significant. Even then, their potential to complicate or break code should be ample cause to carefully consider the tradeoffs. Not only must they be spread almost neurotically throughout a framework, they may also break tools you rely on.

### Example impacts of slots: ListTree and mapattrs
As a more realistic example of slots' effects, due to the first bullet in the prior section, Chapter 31's ListTree class does not fail when mixed in to a class that defines \_\_slots\_\_, even though it scans instance namespace dictionaries. The lister class's own lack of slots is enough to ensure that the instance will still have a \_\_dict\_\_, and hence not trigger an exception when fetched or indexed. For example, both of the following display without error -- the second also allows names not in the slots list to be assigned as instances attributes, including any required by the superclass:
> ```python
> class C(ListTree): pass
> X = C() 						# OK: no __slots__ used
> print(X)
> class C(ListTree): __slots__ = ['a', 'b'] 			# OK: superclass produces __dict__
> X = C()
> X.c = 3
> print(X) 						# Displays c at X, a and b at C
> ```

The following classes display correctly as well -- any nonslot class like ListTree generates an instance \_\_dict\_\_, and can thus safely assume its presence:
> ```python
> class A: __slots__ = ['a'] 		# Both OK by bullet 1 above
> class B(A, ListTree): pass
> class A: __slots__ = ['a']
> class B(A, ListTree): __slots__ = ['b'] 		# Displays b at B, a at A
> ```

Although it renders subclass slots pointless, this is a positive side effect for tools classes like ListTree (and its Chapter 28 predecessor). In general, though, some tools might need to catch exceptions when \_\_dict\_\_ is absent or use a hasattr or getattr to test or provide defaults if slot usage may preclude a namespace dictionary in instance objects inspected.

For example, you should now be able to understand why the mapattrs.py program earlier in this chapter must check for the presence of a \_\_dict\_\_ before fetching it -- instance objects created from classes with \_\_slots\_\_ won't have one. In fact, if we use the highlighted alternative line in the following, the mapattrs function fails with an exception when attempting to look for an attribute name in the instance at the front of the inheritance path sequence:
> ```python
> def mapattrs(instance, withobject=False, bysource=False):
>     for attr in dir(instance):
>         for obj in inherits:
>             if attr in obj.__dict__: 				# May fail if __slots__ used
> ```

> ```python
> >>> class C: __slots__ = ['a']
> >>> X = C()
> >>> mapattrs(X)
> AttributeError: 'C' object has no attribute '__dict__'
> ```

Either of the following works around the issue, and allows the tool to support slots -- the first provides a default, and the second is more verbose but seems marginally more explicit in its intent:
> ```python
> if attr in getattr(obj, '__dict__', {}):
> if hasattr(obj, '__dict__') and attr in obj.__dict__:
> ```

As mentioned earlier, some tools may benefit from mapping dir results to objects in the MRO this way, instead of scanning an instance \_\_dict\_\_ in general -- without this more inclusive approach, attributes implemented by class-level tools like slots won't be reported as instance data. Even so, this doesn't necessarily excuse such tools from allowing for a missing \_\_dict\_\_ in the instance too!

### What about slots speed?
Finally, while slots primarily optimize memory use, their speed impact is less clear-cut.  Here's a simple test script using the timeit techniques we studied in Chapter 21. For both the slots and nonslots (instance dictionary) storage models, it makes 1,000 instances, assigns and fetches 4 attributes on each, and repeats 1,000 times -- for both models taking the best of 3 runs that each exercise a total of 8M attribute operations:
> ```python
> # File slots-test.py
> from __future__ import print_function
> import timeit
> base = """
> Is = []
> for i in range(1000):
>     X = C()
>     X.a = 1; X.b = 2; X.c = 3; X.d = 4
>     t = X.a + X.b + X.c + X.d
>     Is.append(X)
> """
> 
> stmt = """
> class C:
>     __slots__ = ['a', 'b', 'c', 'd']
> """ + base
> 
> print('Slots =>', end=' ')
> print(min(timeit.repeat(stmt, number=1000, repeat=3)))
> 
> stmt = """
> class C:
>     pass
> """ + base
> print('Nonslots=>', end=' ')
> print(min(timeit.repeat(stmt, number=1000, repeat=3)))
> ```

At least on this code, on my laptop, and in my installed versions (Python 3.3 and 2.7), the best times imply that slots are slightly quicker in 3.X and a wash in 2.X, though this says little about memory space, and is prone to change arbitrarily in the future:
> ```powershell
> c:\code> py −3 slots-test.py
> Slots => 0.7780903942045899
> Nonslots=> 0.9888108080898417
> c:\code> py −2 slots-test.py
> Slots => 0.80868754371
> Nonslots=> 0.802224740747
> ```
For more on slots in general, see the Python standard manual set. Also watch for the Private decorator case study of Chapter 39 -- an example that naturally allows for attributes based on both \_\_slots\_\_ and \_\_dict\_\_ storage, by using delegation and storageneutral accessor tools like getattr.

## Properties: Attribute Accessors
Our next new-style extension is properties -- a mechanism that provides another way for new-style classes to define methods called automatically for access or assignment to instance attributes. This feature is similar to properties (a.k.a. "getters" and "setters") in languages like Java and C#, but in Python is generally best used sparingly, as a way to add accessors to attributes after the fact as needs evolve and warrant. Where needed, though, properties allow attribute values to be computed dynamically without requiring method calls at the point of access.

Though properties cannot support generic attribute routing goals, at least for specific attributes they are an alternative to some traditional uses of the \_\_getattr\_\_ and \_\_setattr\_\_ overloading methods we first studied in Chapter 30. Properties have a similar effect to these two methods, but by contrast incur an extra method call only for accesses to names that require dynamic computation -- other nonproperty names are accessed normally with no extra calls. Although \_\_getattr\_\_ is invoked only for undefined names, the \_\_setattr\_\_ method is instead called for assignment to every attribute.

Properties and slots are related too, but serve different goals. Both implement instance attributes that are not physically stored in instance namespace dictionaries -- a sort of "virtual" attribute -- and both are based on the notion of class-level attribute descriptors. In contrast, slots manage instance storage, while properties intercept access and compute values arbitrarily. Because their underlying descriptor implementation tool is too advanced for us to cover here, properties and descriptors both get full treatment in Chapter 38.

### Property basics
As a brief introduction, though, a property is a type of object assigned to a class attribute name. You generate a property by calling the property built-in function, passing in up to three accessor methods -- handlers for get, set, and delete operations -- as well as an optional docstring for the property. If any argument is passed as None or omitted, that operation is not supported.

The resulting property object is typically assigned to a name at the top level of a class statement (e.g., name=property()), and a special @ syntax we'll meet later is available to automate this step. When thus assigned, later accesses to the class property name itself as an object attribute (e.g., obj.name) are automatically routed to one of the accessor methods passed into the property call.

For example, we've seen how the \_\_getattr\_\_ operator overloading method allows classes to intercept undefined attribute references in both classic and new-style classes:
> ```python
> >>> class operators:
>         def __getattr__(self, name):
>             if name == 'age':
>                 return 40
>             else:
>                 raise AttributeError(name)
> >>> x = operators()
> >>> x.age 					# Runs __getattr__
> 40
> >>> x.name 					# Runs __getattr__
> AttributeError: name
> ```

Here is the same example, coded with properties instead; note that properties are available for all classes but require the new-style object derivation in 2.X to work properly for intercepting attribute assignments (and won't complain if you forget this -- but will silently overwrite your property with the new data!):
> ```python
> >>> class properties(object): 			# Need object in 2.X for setters
>         def getage(self):
>             return 40
>         age = property(getage, None, None, None) 			# (get, set, del, docs), or use @
> >>> x = properties()
> >>> x.age 				# Runs getage
> 40
> >>> x.name 				# Normal fetch
> AttributeError: 'properties' object has no attribute 'name'
> ```

For some coding tasks, properties can be less complex and quicker to run than the traditional techniques. For example, when we add attribute assignment support, properties become more attractive -- there's less code to type, and no extra method calls are incurred for assignments to attributes we don't wish to compute dynamically:
> ```python
> >>> class properties(object): # Need object in 2.X for setters
>         def getage(self):
>             return 40
>         def setage(self, value):
>             print('set age: %s' % value)
>             self._age = value
>         age = property(getage, setage, None, None)
> 
> >>> x = properties()
> >>> x.age 				# Runs getage
> 40
> >>> x.age = 42 			# Runs setage
> set age: 42
> >>> x._age 				# Normal fetch: no getage call
> 42
> >>> x.age 				# Runs getage
> 40
> >>> x.job = 'trainer' 	# Normal assign: no setage call
> >>> x.job 				# Normal fetch: no getage call
> 'trainer'
> ```
> 
> # 上述代码的完善
> ```python
> In [205]: class Property:
>       ..:     def __init__(self, age):
>       ..:         self._age = age
>       ..:     def getage(self):
>       ..:         return self._age
>       ..:     def setage(self, value):
>       ..:         print('set age to %s' % value)
>       ..:         self._age = value
>       ..:     age = property(getage, setage, None, None)
>       ..: 
> 
> In [206]: f = Property(40)
> 
> In [207]: f.age
> Out[207]: 40
> 
> In [208]: f.age = 43
> set age to 43
> 
> In [209]: f.age
> Out[209]: 43
> ```

The equivalent class based on operator overloading incurs extra method calls for assignments to attributes not being managed and needs to route attribute assignments through the attribute dictionary to avoid loops (or, for new-style classes, to the object superclass's \_\_setattr\_\_ to better support "virtual" attributes such as slots and properties coded in other classes):
> ```python
> >>> class operators:
>         def __getattr__(self, name): 				# On undefined reference
>             if name == 'age':
>                 return 40
>             else:
>                 raise AttributeError(name)
>         def __setattr__(self, name, value): 		# On all assignments
>             print('set: %s %s' % (name, value))
>             if name == 'age':
>                 self.__dict__['_age'] = value 	# Or object.__setattr__()
>             else:
>                 self.__dict__[name] = value
> 
> >>> x = operators()
> >>> x.age 				# Runs __getattr__
> 40
> >>> x.age = 41 			# Runs __setattr__
> set: age 41
> >>> x._age 				# Defined: no __getattr__ call
> 41
> >>> x.age 				# Runs __getattr__
> 40
> >>> x.job = 'trainer' 	# Runs __setattr__ again
> set: job trainer
> >>> x.job 				# Defined: no __getattr__ call
> 'trainer'
> ```

Properties seem like a win for this simple example. However, some applications of \_\_getattr\_\_ and \_\_setattr\_\_ still require more dynamic or generic interfaces than properties directly provide.

For example, in many cases the set of attributes to be supported cannot be determined when the class is coded, and may not even exist in any tangible form (e.g., when delegating arbitrary attribute references to a wrapped/embedded object generically). In such contexts, a generic \_\_getattr\_\_ or a \_\_setattr\_\_ attribute handler with a passed in attribute name is usually preferable. Because such generic handlers can also support simpler cases, properties are often an optional and redundant extension -- albeit one that may avoid extra calls on assignments, and one that some programmers may prefer when applicable.

For more details on both options, stay tuned for Chapter 38 in the final part of this book. As we'll see there, it's also possible to code properties using the @ symbol function decorator syntax -- a topic introduced later in this chapter, and an equivalent and automatic alternative to manual assignment in the class scope:
> ```python
> class properties(object):
>     @property 				# Coding properties with decorators: ahead
>     def age(self):
>         ...
>     @age.setter
>     def age(self, value):
>         ...
> ```

To make sense of this decorator syntax, though, we must move ahead.

## \_\_getattribute\_\_ and Descriptors: Attribute Tools
Also in the class extensions department, the \_\_getattribute\_\_ operator overloading method, available for new-style classes only, allows a class to intercept all attribute references, not just undefined references. This makes it more potent than its \_\_getattr\_\_ cousin we used in the prior section, but also trickier to use -- it's prone to loops much like \_\_setattr\_\_, but in different ways.

For more specialized attribute interception goals, in addition to properties and operator overloading methods, Python supports the notion of attribute descriptors -- classes with \_\_get\_\_ and \_\_set\_\_ methods, assigned to class attributes and inherited by instances, that intercept read and write accesses to specific attributes. As a preview, here's one of the simplest descriptors you're likely to encounter:
> ```python
> >>> class AgeDesc(object):
>         def __get__(self, instance, owner): return 40
>         def __set__(self, instance, value): instance._age = value
> 
> >>> class descriptors(object):
>         age = AgeDesc()
> 
> >>> x = descriptors()
> >>> x.age 				# Runs AgeDesc.__get__
> 40
> >>> x.age = 42 			# Runs AgeDesc.__set__
> >>> x._age 				# Normal fetch: no AgeDesc call
> 42
> ```
> 
> # 上述代码的完善版本
> ```python
> In [26]: class AgeDesc:
>     ...:     def __init__(self, instance, age):
>     ...:         instance.age = age
>     ...:     def __get__(self, instance, owner):
>     ...:         return instance.age
>     ...:     def __set__(self, instance, value):
>     ...:         instance.age = value
>     ...:
> In [29]: class Age:
>     ...:     def __init__(self, value):
>     ...:         age = AgeDesc(self, value)
>     ...: 
>     ...: 
> 
> In [30]: a = Age(33)
> 
> In [31]: a.age
> Out[31]: 33
> 
> In [32]: a.age = 40
> 
> In [33]: a.age
> Out[33]: 40
> 
> In [34]: a.age = 440
> 
> In [35]: a.age
> Out[35]: 440
> ```

Descriptors have access to state in instances of themselves as well as their client class, and are in a sense a more general form of properties; in fact, properties are a simplified way to define a specific type of descriptor -- one that runs functions on access. Descriptors are also used to implement the slots feature we met earlier, and other Python tools.

Because \_\_getattribute\_\_ and descriptors are too substantial to cover well here, we'll defer the rest of their coverage, as well as much more on properties, to Chapter 38 in the final part of this book. We'll also employ them in examples in Chapter 39 and study how they factor into inheritance in Chapter 40.

## Other Class Changes and Extensions
As mentioned, we're also postponing coverage of the super built-in -- an additional major new-style class extension that relies on its MRO -- until the end of this chapter. Before we get there, though, we're going to explore additional class-related changes and extensions that are not necessarily bound to new-style classes, but were introduced at roughly the same time: static and class methods, decorators, and more.

Many of the changes and feature additions of new-style classes integrate with the notion of subclassable types mentioned earlier in this chapter, because subclassable types and new-style classes were introduced in conjunction with a merging of the type/class dichotomy in Python 2.2 and beyond. As we've seen, in 3.X, this merging is complete: classes are now types, and types are classes, and Python classes today still reflect both that conceptual merging and its implementation.

Along with these changes, Python also grew a more coherent and generalized protocol for coding metaclasses -- classes that subclass the type object, intercept class creation calls, and may provide behavior acquired by classes. Accordingly, they provide a welldefined hook for management and augmentation of class objects. They are also an advanced topic that is optional for most Python programmers, so we'll postpone further details here. We'll glimpse metaclasses again later in this chapter in conjunction with class decorators -- a feature whose roles often overlap -- but we'll postpone their full coverage until Chapter 40, in the final part of this book. For our purpose here, let's move on to a handful of additional class-related extensions.
