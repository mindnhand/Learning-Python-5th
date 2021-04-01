# \_\_getattr\_\_ and \_\_getattribute\_\_
So far, we've studied properties and descriptors -- tools for managing specific attributes. The \_\_getattr\_\_ and \_\_getattribute\_\_ operator overloading methods provide still other ways to intercept attribute fetches for class instances. Like properties and descriptors, they allow us to insert code to be run automatically when attributes are accessed.

As we'll see, though, these two methods can also be used in more general ways. Because they intercept arbitrary names, they apply in broader roles such as delegation, but may also incur extra calls in some contexts, and are too dynamic to register in dir results. Attribute fetch interception comes in two flavors, coded with two different methods:
- \_\_getattr\_\_ is run for undefined attributes -- because it is run only for attributes not stored on an instance or inherited from one of its classes, its use is straightforward.
- \_\_getattribute\_\_ is run for every attribute -- because it is all-inclusive, you must be cautious when using this method to avoid recursive loops by passing attribute accesses to a superclass.

We met the former of these in Chapter 30; it's available for all Python versions. The latter of these is available for new-style classes in 2.X, and for all (implicitly new-style) classes in 3.X. These two methods are representatives of a set of attribute interception methods that also includes \_\_setattr\_\_ and \_\_delattr\_\_. Because these methods have similar roles, though, we will generally treat them all as a single topic here.

Unlike properties and descriptors, these methods are part of Python's general operator overloading protocol -- specially named methods of a class, inherited by subclasses, and run automatically when instances are used in the implied built-in operation. Like all normal methods of a class, they each receive a first self argument when called, giving access to any required instance state information as well as other methods of the class in which they appear.

The \_\_getattr\_\_ and \_\_getattribute\_\_ methods are also more generic than properties and descriptors -- they can be used to intercept access to any (or even all) instance attribute fetches, not just a single specific name. Because of this, these two methods are well suited to general delegation-based coding patterns -- they can be used to implement wrapper (a.k.a. proxy) objects that manage all attribute accesses for an embedded object. By contrast, we must define one property or descriptor for every attribute we wish to intercept. As we'll see ahead, this role is impaired somewhat in newstyle classes for built-in operations, but still applies to all named methods in a wrapped object's interface.

Finally, these two methods are more narrowly focused than the alternatives we considered earlier: they intercept attribute fetches only, not assignments. To also catch attribute changes by assignment, we must code a \_\_setattr\_\_ method -- an operator overloading method run for every attribute fetch, which must take care to avoid recursive loops by routing attribute assignments through the instance namespace dictionary or a superclass method. Although less common, we can also code a \_\_delattr\_\_ overloading method (which must avoid looping in the same way) to intercept attribute deletions. By contrast, properties and descriptors catch get, set, and delete operations by design.

Most of these operator overloading methods were introduced earlier in the book; here, we'll expand on their usage and study their roles in larger contexts.

## The Basics
\_\_getattr\_\_ and \_\_setattr\_\_ were introduced in Chapter 30 and Chapter 32, and \_\_getattribute\_\_ was mentioned briefly in Chapter 32. In short, if a class defines or inherits the following methods, they will be run automatically when an instance is used in the context described by the comments to the right:
> ```python
> def __getattr__(self, name): 				# On undefined attribute fetch [obj.name]
> def __getattribute__(self, name): 		# On all attribute fetch [obj.name]
> def __setattr__(self, name, value): 		# On all attribute assignment [obj.name=value]
> def __delattr__(self, name): 				# On all attribute deletion [del obj.name]
> ```

In all of these, self is the subject instance object as usual, name is the string name of the attribute being accessed, and value is the object being assigned to the attribute. The two get methods normally return an attribute's value, and the other two return nothing (None). All can raise exceptions to signal prohibited access.

For example, to catch every attribute fetch, we can use either of the first two previous methods, and to catch every attribute assignment we can use the third. The following uses \_\_getattr\_\_ and works portably on both Python 2.X and 3.X, not requiring newstyle object derivation in 2.X:
> 
> > ```python
> > class Catcher:
> >     def __getattr__(self, name):
> >         print('Get: %s' % name)
> >     def __setattr__(self, name, value):
> >         print('Set: %s %s' % (name, value))
> > 
> > X = Catcher()
> > X.job 			# Prints "Get: job"
> > X.pay 			# Prints "Get: pay"
> > X.pay = 99 		# Prints "Set: pay 99"
> > ```
> 
> Using \_\_getattribute\_\_ works exactly the same in this specific case, but requires object derivation in 2.X (only), and has subtle looping potential, which we'll take up in the next section:
> 
> > ```python
> > class Catcher(object): 					# Need (object) in 2.X only
> >     def __getattribute__(self, name): 	# Works same as getattr here
> >         print('Get: %s' % name) 		# But prone to loops on general
> >         ...rest unchanged...
> > ```
> 
Such a coding structure can be used to implement the delegation design pattern we met earlier, in Chapter 31. Because all attributes are routed to our interception methods generically, we can validate and pass them along to embedded, managed objects. The following class (borrowed from Chapter 31), for example, traces every attribute fetch made to another object passed to the wrapper (proxy) class:
> ```python
> class Wrapper:
>     def __init__(self, object):
>         self.wrapped = object 				# Save object
>     def __getattr__(self, attrname):
>         print('Trace: ' + attrname) 			# Trace fetch
>         return getattr(self.wrapped, attrname) 	# Delegate fetch
> 
> X = Wrapper([1, 2, 3])
> X.append(4) 				# Prints "Trace: append"
> print(X.wrapped) 			# Prints "[1, 2, 3, 4]"
> ```

There is no such analog for properties and descriptors, short of coding accessors for every possible attribute in every possibly wrapped object. On the other hand, when such generality is not required, generic accessor methods may incur additional calls for assignments in some contexts -- a tradeoff described in Chapter 30 and mentioned in the context of the case study example we'll explore at the end of this chapter.

### Avoiding loops in attribute interception methods
These methods are generally straightforward to use; their only substantially complex aspect is the potential for looping (a.k.a. recursing). Because \_\_getattr\_\_ is called for undefined attributes only, it can freely fetch other attributes within its own code. However, because \_\_getattribute\_\_ and \_\_setattr\_\_ are run for all attributes, their code needs to be careful when accessing other attributes to avoid calling themselves again and triggering a recursive loop.

For example, another attribute fetch run inside a \_\_getattribute\_\_ method's code will trigger \_\_getattribute\_\_ again, and the code will usually loop until memory is exhausted:
> ```python
> def __getattribute__(self, name):
>     x = self.other 			# LOOPS!
> ```

> Technically, this method is even more loop-prone than this may imply -- a self attribute reference run anywhere in a class that defines this method will trigger \_\_getattribute\_\_, and also has the potential to loop depending on the class's logic. This is normally desired behavior -- intercepting every attribute fetch is this method's purpose, after all -- but you should be aware that this method catches all attribute fetches wherever they are coded. When coded within \_\_getattribute\_\_ itself, this almost always causes a loop. To avoid this loop, route the fetch through a higher superclass instead to skip this level's version -- because the object class is always a new-style superclass, it serves well in this role:
> 
> > ```python
> > def __getattribute__(self, name):
> >     x = object.__getattribute__(self, 'other') 		# Force higher to avoid me
> > ```
> 
> For \_\_setattr\_\_, the situation is similar, as summarized in Chapter 30 -- assigning any attribute inside this method triggers \_\_setattr\_\_ again and may create a similar loop:
> 
> > ```python
> > def __setattr__(self, name, value):
> >     self.other = value 			# Recurs (and might LOOP!)
> > ```
> 
> Here too, self attribute assignments anywhere in a class defining this method trigger \_\_setattr\_\_ as well, though the potential for looping is much stronger when they show up in \_\_setattr\_\_ itself. To work around this problem, you can assign the attribute as a key in the instance's \_\_dict\_\_ namespace dictionary instead. This avoids direct attribute assignment:
> 
> > ```python
> > def __setattr__(self, name, value):
> >     self.__dict__['other'] = value 			# Use attr dict to avoid me
> > ```
> 
> Although it's a less traditional approach, __setattr__ can also pass its own attribute assignments to a higher superclass to avoid looping, just like __getattribute__ (and per the upcoming note, this scheme is sometimes preferred):
> 
> > ```python
> > def __setattr__(self, name, value):
> >     object.__setattr__(self, 'other', value) 		# Force higher to avoid me
> > ```
> 
> By contrast, though, we cannot use the \_\_dict\_\_ trick to avoid loops in \_\_getattribute\_\_:
> 
> > ```python
> > def __getattribute__(self, name):
> >     x = self.__dict__['other'] 			# Loops!
> > ```
> 
> Fetching the \_\_dict\_\_ attribute itself triggers \_\_getattribute\_\_ again, causing a recursive loop. Strange but true!

The \_\_delattr\_\_ method is less commonly used in practice, but when it is, it is called for every attribute deletion (just as \_\_setattr\_\_ is called for every attribute assignment). When using this method, you must take care to avoid loops when deleting attributes, by using the same techniques: namespace dictionaries operations or superclass method calls.

> **Note:**
> As noted in Chapter 30, attributes implemented with new-style class features such as slots and properties are not physically stored in the instance's \_\_dict\_\_ namespace dictionary (and slots may even preclude its existence entirely). Because of this, code that wishes to support such attributes should code \_\_setattr\_\_ to assign with the object.\_\_setattr\_\_ scheme shown here, not by self.\_\_dict\_\_ indexing. Namespace \_\_dict\_\_ operations suffice for classes known to store data in instances, like this chapter's self-contained examples; general tools, though, should prefer object.
>

## A First Example
Generic attribute management is not nearly as complicated as the prior section may have implied. To see how to put these ideas to work, here is the same first example we used for properties and descriptors in action again, this time implemented with attribute operator overloading methods. Because these methods are so generic, we test attribute names here to know when a managed attribute is being accessed; others are allowed to pass normally:
> 
> > ```python
> > class Person: 			# Portable: 2.X or 3.X
> >     def __init__(self, name): 			# On [Person()]
> >         self._name = name 				# Triggers __setattr__!
> >     def __getattr__(self, attr): 		# On [obj.undefined]
> >         print('get: ' + attr)
> >         if attr == 'name': 				# Intercept name: not stored
> >             return self._name 			# Does not loop: real attr
> >         else: 							# Others are errors
> >             raise AttributeError(attr)
> >     def __setattr__(self, attr, value): 	# On [obj.any = value]
> >         print('set: ' + attr)
> >         if attr == 'name':
> >             attr = '_name' 				# Set internal name
> >         self.__dict__[attr] = value 		# Avoid looping here
> >     def __delattr__(self, attr): 			# On [del obj.any]
> >         print('del: ' + attr)
> >         if attr == 'name':
> >             attr = '_name' 				# Avoid looping here too
> >         del self.__dict__[attr] 			# but much less common
> > 
> > bob = Person('Bob Smith') 				# bob has a managed attribute
> > print(bob.name) 			# Runs __getattr__
> > bob.name = 'Robert Smith' 	# Runs __setattr__
> > print(bob.name)
> > del bob.name 				# Runs __delattr__
> > print('-'*20)
> > sue = Person('Sue Jones') 	# sue inherits property too
> > print(sue.name)
> > #print(Person.name.__doc__) # No equivalent here
> > ```
> 
> Notice that the attribute assignment in the \_\_init\_\_ constructor triggers \_\_setattr\_\_ too -- this method catches every attribute assignment, even those anywhere within the class itself. When this code is run, the same output is produced, but this time it's the result of Python's normal operator overloading mechanism and our attribute interception methods:
> 
> > ```powershell
> > c:\code> py -3 getattr-person.py
> > set: _name
> > get: name
> > Bob Smith
> > set: name
> > get: name
> > Robert Smith
> > del: name
> > --------------------
> > set: _name
> > get: name
> > Sue Jones
> > ```
>
> Also note that, unlike with properties and descriptors, there's no direct notion of specifying documentation for our attribute here; managed attributes exist within the code of our interception methods, not as distinct objects.
> 

### Using \_\_getattribute\_\_
To achieve exactly the same results with \_\_getattribute\_\_, replace \_\_getattr\_\_ in the example with the following; because it catches all attribute fetches, this version must be careful to avoid looping by passing new fetches to a superclass, and it can't generally assume unknown names are errors:
> 
> > ```python
> > # Replace __getattr__ with this
> > def __getattribute__(self, attr): 			# On [obj.any]
> >     print('get: ' + attr)
> >     if attr == 'name': 			# Intercept all names
> >         attr = '_name' 			# Map to internal name
> >     return object.__getattribute__(self, attr) 	# Avoid looping here
> > ```
> 
> When run with this change, the output is similar, but we get an extra \_\_getattribute\_\_ call for the fetch in \_\_setattr\_\_ (the first time originating in \_\_init\_\_):
> 
> > ```powershell
> > c:\code> py -3 getattribute-person.py
> > set: _name
> > get: __dict__
> > get: name
> > Bob Smith
> > set: name
> > get: __dict__
> > get: name
> > Robert Smith
> > del: name
> > get: __dict__
> > --------------------
> > set: _name
> > get: __dict__
> > get: name
> > Sue Jones
> > ```
> 

This example is equivalent to that coded for properties and descriptors, but it's a bit artificial, and it doesn't really highlight these tools' assets. Because they are generic, \_\_getattr\_\_ and \_\_getattribute\_\_ are probably more commonly used in delegationbase code (as sketched earlier), where attribute access is validated and routed to an embedded object. Where just a single attribute must be managed, properties and descriptors might do as well or better.

## Computed Attributes
As before, our prior example doesn't really do anything but trace attribute fetches; it's not much more work to compute an attribute's value when fetched. As for properties and descriptors, the following creates a virtual attribute X that runs a calculation when fetched:
> 
> > ```python
> > class AttrSquare:
> >     def __init__(self, start):
> >         self.value = start 			# Triggers __setattr__!
> >     def __getattr__(self, attr): 		# On undefined attr fetch
> >         if attr == 'X':
> >             return self.value ** 2 	# value is not undefined
> >         else:
> >             raise AttributeError(attr)
> >     def __setattr__(self, attr, value): 	# On all attr assignments
> >         if attr == 'X':
> >             attr = 'value'
> >         self.__dict__[attr] = value
> > 
> > A = AttrSquare(3) 			# 2 instances of class with overloading
> > B = AttrSquare(32) 			# Each has different state information
> > print(A.X) 			# 3 ** 2
> > A.X = 4
> > print(A.X)            # 4 ** 2
> > print(B.X)            # 32 ** 2 (1024)
> > ```
> 
> Running this code results in the same output that we got earlier when using properties and descriptors, but this script's mechanics are based on generic attribute interception methods:
> 
> > ```powershell
> > c:\code> py -3 getattr-computed.py
> > 9
> > 16
> > 1024
> > ```
> 

### Using \_\_getattribute\_\_
As before, we can achieve the same effect with \_\_getattribute\_\_ instead of \_\_getattr\_\_; the following replaces the fetch method with a \_\_getattribute\_\_ and changes the \_\_setattr\_\_ assignment method to avoid looping by using direct superclass method calls instead of \_\_dict\_\_ keys:
> ```python
> class AttrSquare: 				# Add (object) for 2.X
>     def __init__(self, start):
>         self.value = start 		# Triggers __setattr__!
>     def __getattribute__(self, attr): 		# On all attr fetches
>         if attr == 'X':
>             return self.value ** 2 			# Triggers __getattribute__ again!
>         else:
>             return object.__getattribute__(self, attr)
>     def __setattr__(self, attr, value): 		# On all attr assignments
>         if attr == 'X':
>             attr = 'value'
>         object.__setattr__(self, attr, value)
> ```

When this version, getattribute-computed.py, is run, the results are the same again. Notice, though, the implicit routing going on inside this class's methods:
- self.value=start inside the constructor triggers \_\_setattr\_\_
- self.value inside \_\_getattribute\_\_ triggers \_\_getattribute\_\_ again
In fact, \_\_getattribute\_\_ is run twice each time we fetch attribute X. This doesn't happen in the \_\_getattr\_\_ version, because the value attribute is not undefined. If you care about speed and want to avoid this, change \_\_getattribute\_\_ to use the superclass to fetch value as well:
> ```python
> def __getattribute__(self, attr):
>     if attr == 'X':
>         return object.__getattribute__(self, 'value') ** 2
> ```

Of course, this still incurs a call to the superclass method, but not an additional recursive call before we get there. Add print calls to these methods to trace how and when they run.

## \_\_getattr\_\_ and \_\_getattribute\_\_ Compared
To summarize the coding differences between \_\_getattr\_\_ and \_\_getattribute\_\_, the following example uses both to implement three attributes -- attr1 is a class attribute, attr2 is an instance attribute, and attr3 is a virtual managed attribute computed when fetched:
> 
> > ```python
> > class GetAttr:
> >     attr1 = 1
> >     def __init__(self):
> >         self.attr2 = 2
> >     def __getattr__(self, attr): 			# On undefined attrs only
> >         print('get: ' + attr) 			# Not on attr1: inherited from class
> >         if attr == 'attr3': 				# Not on attr2: stored on instance
> >             return 3
> >         else:
> >             raise AttributeError(attr)
> > 
> > X = GetAttr()
> > print(X.attr1)
> > print(X.attr2)
> > print(X.attr3)
> > print('-'*20)
> > 
> > class GetAttribute(object): 				# (object) needed in 2.X only
> >     attr1 = 1
> >     def __init__(self):
> >         self.attr2 = 2
> >     def __getattribute__(self, attr): 	# On all attr fetches
> >         print('get: ' + attr) 			# Use superclass to avoid looping here
> >         if attr == 'attr3':
> >             return 3
> >         else:
> >             return object.__getattribute__(self, attr)
> > 
> > X = GetAttribute()
> > print(X.attr1)
> > print(X.attr2)
> > print(X.attr3)
> > ```
> 
> When run, the \_\_getattr\_\_ version intercepts only attr3 accesses, because it is undefined. The \_\_getattribute\_\_ version, on the other hand, intercepts all attribute fetches and must route those it does not manage to the superclass fetcher to avoid loops:
> 
> > ```powershell
> > c:\code> py -3 getattr-v-getattr.py
> > 1
> > 2
> > get: attr3
> > 3
> > --------------------
> > get: attr1
> > 1
> > get: attr2
> > 2
> > get: attr3
> > 3
> > ```
> 

Although \_\_getattribute\_\_ can catch more attribute fetches than \_\_getattr\_\_, in practice they are often just variations on a theme -- if attributes are not physically stored, the two have the same effect.

## Management Techniques Compared
To summarize the coding differences in all four attribute management schemes we've seen in this chapter, let's quickly step through a somewhat more comprehensive computed-attribute example using each technique, coded to run in either Python 3.X or 2.X. The following first version uses properties to intercept and calculate attributes named square and cube. Notice how their base values are stored in names that begin with an underscore, so they don't clash with the names of the properties themselves:
> ```python
> # Two dynamically computed attributes with properties
> class Powers(object): 			# Need (object) in 2.X only
>     def __init__(self, square, cube):
>         self._square = square 	# _square is the base value
>         self._cube = cube 		# square is the property name
>     def getSquare(self):
>         return self._square ** 2
>     def setSquare(self, value):
>         self._square = value
>     square = property(getSquare, setSquare)
> 
>     def getCube(self):
>         return self._cube ** 3
>     cube = property(getCube)
> 
> X = Powers(3, 4)
> print(X.square) 			# 3 ** 2 = 9
> print(X.cube) 			# 4 ** 3 = 64
> X.square = 5
> print(X.square) 			# 5 ** 2 = 25
> ```

To do the same with descriptors, we define the attributes with complete classes. Note that these descriptors store base values as instance state, so they must use leading underscores again so as not to clash with the names of descriptors; as we'll see in the final example of this chapter, we could avoid this renaming requirement by storing base values as descriptor state instead, but that doesn't as directly address data that must vary per client class instance:
> ```python
> # Same, but with descriptors (per-instance state)
> class DescSquare(object):
>     def __get__(self, instance, owner):
>         return instance._square ** 2
>     def __set__(self, instance, value):
>         instance._square = value
> 
> class DescCube(object):
>     def __get__(self, instance, owner):
>         return instance._cube ** 3
> 
> class Powers(object): 			# Need all (object) in 2.X only
>     square = DescSquare()
>     cube = DescCube()
>     def __init__(self, square, cube):
>         self._square = square 	# "self.square = square" works too,
>         self._cube = cube 		# because it triggers desc __set__!
> 
> X = Powers(3, 4)
> print(X.square) 		# 3 ** 2 = 9
> print(X.cube) 		# 4 ** 3 = 64
> X.square = 5
> print(X.square) 		# 5 ** 2 = 25
> ```

To achieve the same result with \_\_getattr\_\_ fetch interception, we again store base values with underscore-prefixed names so that accesses to managed names are undefined and thus invoke our method; we also need to code a \_\_setattr\_\_ to intercept assignments, and take care to avoid its potential for looping:
> ```python
> # Same, but with generic __getattr__ undefined attribute interception
> class Powers:
>     def __init__(self, square, cube):
>         self._square = square
>         self._cube = cube
>     def __getattr__(self, name):
>         if name == 'square':
>             return self._square ** 2
>         elif name == 'cube':
>             return self._cube ** 3
>         else:
>             raise TypeError('unknown attr:' + name)
>     def __setattr__(self, name, value):
>         if name == 'square':
>             self.__dict__['_square'] = value 			# Or use object
>         else:
>             self.__dict__[name] = value
> 
> X = Powers(3, 4)
> print(X.square) 			# 3 ** 2 = 9
> print(X.cube) 			# 4 ** 3 = 64
> X.square = 5
> print(X.square) 			# 5 ** 2 = 25
> ```

The final option, coding this with \_\_getattribute\_\_, is similar to the prior version. Because we catch every attribute now, though, we must also route base value fetches to a superclass to avoid looping or extra calls -- fetching self.\_square directly works too, but runs a second \_\_getattribute\_\_ call:
> 
> > ```python
> > # Same, but with generic __getattribute__ all attribute interception
> > class Powers(object): 			# Need (object) in 2.X only
> >     def __init__(self, square, cube):
> >         self._square = square
> >         self._cube = cube
> >     def __getattribute__(self, name):
> >         if name == 'square':
> >             return object.__getattribute__(self, '_square') ** 2		# call superclass's __getattribute__, avoid recursive loop
> >         elif name == 'cube':
> >             return object.__getattribute__(self, '_cube') ** 3		# call superclass's __getattribute__, avoid recursive loop
> >         else:
> >             return object.__getattribute__(self, name)		# call superclass's __getattribute__, avoid recursive loop
> >     def __setattr__(self, name, value):
> >         if name == 'square':
> >             object.__setattr__(self, '_square', value) # Or use __dict__
> >         else:
> >             object.__setattr__(self, name , value)
> >  
> > X = Powers(3, 4)
> > print(X.square) 			# 3 ** 2 = 9
> > print(X.cube) 			# 4 ** 3 = 64
> > X.square = 5
> > print(X.square) 			# 5 ** 2 = 25
> > ```
> 
> As you can see, each technique takes a different form in code, but all four produce the same result when run:
> 
> > ```powershell
> > 9
> > 64
> > 25
> > ```
> 

For more on how these alternatives compare, and other coding options, stay tuned for a more realistic application of them in the attribute validation example in the section "Example: Attribute Validations" on page 1256. First, though, we need to take a short side trip to study a new-style-class pitfall associated with two of these tools -- the generic attribute interceptors presented in this section.

## Intercepting Built-in Operation Attributes
When I introduced \_\_getattr\_\_ and \_\_getattribute\_\_, I stated that they intercept undefined and all attribute fetches, respectively, which makes them ideal for delegationbased coding patterns. While this is true for both normally named and explicitly called attributes, their behavior needs some additional clarification: for method-name attributes implicitly fetched by built-in operations, these methods may not be run at all. This means that operator overloading method calls cannot be delegated to wrapped objects unless wrapper classes somehow redefine these methods themselves.

For example, attribute fetches for the \_\_str\_\_, \_\_add\_\_, and \_\_getitem\_\_ methods run implicitly by printing, + expressions, and indexing, respectively, are not routed to the generic attribute interception methods in 3.X. Specifically:
- In Python 3.X, neither \_\_getattr\_\_ nor \_\_getattribute\_\_ is run for such attributes.
- In Python 2.X classic classes, \_\_getattr\_\_ is run for such attributes if they are undefined in the class.
- In Python 2.X, \_\_getattribute\_\_ is available for new-style classes only and works as it does in 3.X.

In other words, in all Python 3.X classes (and 2.X new-style classes), there is no direct way to generically intercept built-in operations like printing and addition. In Python 2.X's default classic classes, the methods such operations invoke are looked up at runtime in instances, like all other attributes; in Python 3.X's new-style classes such methods are looked up in classes instead. Since 3.X mandates new-style classes and 2.X defaults to classic, this is understandably attributed to 3.X, but it can happen in 2.X new-style code too. In 2.X, though, you at least have a way to avoid this change; in 3.X, you do not.

Per Chapter 32, the official (though tersely documented) rationale for this change appears to revolve around metaclassses and optimization of built-in operations. Regardless, given that all attributes -- both normally named and others -- still dispatch generically through the instance and these methods when accessed explicitly by name, this does not seem meant to preclude delegation in general; it seems more an optimization step for built-in operations' implicit behavior. This does, however, make delegationbased coding patterns more complex in 3.X, because object interface proxies cannot generically intercept operator overloading method calls and route them to an embedded object.

This is an inconvenience, but is not necessarily a showstopper -- wrapper classes can work around this constraint by redefining all relevant operator overloading methods in the wrapper itself, in order to delegate calls. These extra methods can be added either manually, with tools, or by definition in and inheritance from common superclasses. This does, however, make object wrappers more work than they used to be when operator overloading methods are a part of a wrapped object's interface.

Keep in mind that this issue applies only to \_\_getattr\_\_ and \_\_getattribute\_\_. Because properties and descriptors are defined for specific attributes only, they don't really apply to delegation-based classes at all -- a single property or descriptor cannot be used to intercept arbitrary attributes. Moreover, a class that defines both operator overloading methods and attribute interception will work correctly, regardless of the type of attribute interception defined. Our concern here is only with classes that do not have operator overloading methods defined, but try to intercept them generically.

Consider the following example, the file getattr-bultins.py, which tests various attribute types and built-in operations on instances of classes containing \_\_getattr\_\_ and \_\_getattribute\_\_ methods:
> 
> > ```python
> > class GetAttr:
> >     eggs = 88 				# eggs stored on class, spam on instance
> >     def __init__(self):
> >         self.spam = 77
> >     def __len__(self): 		# len here, else __getattr__ called with __len__
> >         print('__len__: 42')
> >         return 42
> >     def __getattr__(self, attr): 		# Provide __str__ if asked, else dummy func
> >         print('getattr: ' + attr)
> >         if attr == '__str__':
> >             return lambda *args: '[Getattr str]'
> >         else:
> >             return lambda *args: None
> > 
> > class GetAttribute(object): 		# object required in 2.X, implied in 3.X
> >     eggs = 88 			# In 2.X all are isinstance(object) auto
> >     def __init__(self): 	# But must derive to get new-style tools,
> >         self.spam = 77 	# incl __getattribute__, some __X__ defaults
> >     def __len__(self):
> >         print('__len__: 42')
> >         return 42
> >     def __getattribute__(self, attr):
> >         print('getattribute: ' + attr)
> >         if attr == '__str__':
> >             return lambda *args: '[GetAttribute str]'
> >         else:
> >             return lambda *args: None
> > 
> > for Class in GetAttr, GetAttribute:
> >     print('\n' + Class.__name__.ljust(50, '='))
> >     X = Class()
> >     X.eggs 			# Class attr
> >     X.spam 			# Instance attr
> >     X.other 			# Missing attr
> >     len(X) 			# __len__ defined explicitly
> >     # New-styles must support [], +, call directly: redefine
> >     try: X[0] 			# __getitem__?
> >     except: print('fail []')
> >     try: X + 99 			# __add__?
> >     except: print('fail +')
> >     try: X() 			# __call__? (implicit via built-in)
> >     except: print('fail ()')
> >     X.__call__() 			# __call__? (explicit, not inherited)
> >     print(X.__str__()) 			# __str__? (explicit, inherited from type)
> >     print(X) 				# __str__? (implicit via built-in)
> > ```
> 
> When run under Python 2.X as coded, \_\_getattr\_\_ does receive a variety of implicit attribute fetches for built-in operations, because Python looks up such attributes in instances normally. Conversely, \_\_getattribute\_\_ is not run for any of the operator overloading names invoked by built-in operations, because such names are looked up in classes only in the new-style class model:
> 
> > ```powershell
> > c:\code> py -2 getattr-builtins.py
> > GetAttr===========================================
> > getattr: other
> > __len__: 42
> > getattr: __getitem__
> > getattr: __coerce__
> > getattr: __add__
> > getattr: __call__
> > getattr: __call__
> > getattr: __str__
> > [Getattr str]
> > getattr: __str__
> > [Getattr str]
> > GetAttribute======================================
> > getattribute: eggs
> > getattribute: spam
> > getattribute: other
> > __len__: 42
> > fail []
> > fail +
> > fail ()
> > getattribute: __call__
> > getattribute: __str__
> > [GetAttribute str]
> > <__main__.GetAttribute object at 0x02287898>
> > ```
> 
> Note how \_\_getattr\_\_ intercepts both implicit and explicit fetches of \_\_call\_\_ and \_\_str\_\_ in 2.X here. By contrast, \_\_getattribute\_\_ fails to catch implicit fetches of either attribute name for built-in operations.
> 
> Really, the \_\_getattribute\_\_ case is the same in 2.X as it is in 3.X, because in 2.X classes must be made new-style by deriving from object to use this method. This code's object derivation is optional in 3.X because all classes are new-style.
> 
> When run under Python 3.X, though, results for \_\_getattr\_\_ differ -- none of the implicitly run operator overloading methods trigger either attribute interception method when their attributes are fetched by built-in operations. Python 3.X (and new-style classes in general) skips the normal instance lookup mechanism when resolving such names, though normally named methods are still intercepted as before:
> 
> > ```powershell
> > c:\code> py -3 getattr-builtins.py
> > GetAttr===========================================
> > getattr: other
> > __len__: 42
> > fail []
> > fail +
> > fail ()
> > getattr: __call__
> > <__main__.GetAttr object at 0x02987CC0>
> > <__main__.GetAttr object at 0x02987CC0>
> > GetAttribute======================================
> > getattribute: eggs
> > getattribute: spam
> > getattribute: other
> > __len__: 42
> > fail []
> > fail +
> > fail ()
> > getattribute: __call__
> > getattribute: __str__
> > [GetAttribute str]
> > <__main__.GetAttribute object at 0x02987CF8>
> > ```
> 
> Trace these outputs back to prints in the script to see how this works. Some highlights:
> - \_\_str\_\_ access fails to be caught twice by \_\_getattr\_\_ in 3.X: once for the built-in print, and once for explicit fetches because a default is inherited from the class (really, from the built-in object, which is an automatic superclass to every class in 3.X).
> - \_\_str\_\_ fails to be caught only once by the \_\_getattribute\_\_ catchall, during the built-in print operation; explicit fetches bypass the inherited version.
> - \_\_call\_\_ fails to be caught in both schemes in 3.X for built-in call expressions, but it is intercepted by both when fetched explicitly; unlike \_\_str\_\_, there is no inherited \_\_call\_\_ default for object instances to defeat \_\_getattr\_\_.
> - \_\_len\_\_ is caught by both classes, simply because it is an explicitly defined method in the classes themselves -- though its name it is not routed to either \_\_getattr\_\_ or \_\_getattribute\_\_ in 3.X if we delete the class's \_\_len\_\_ methods.
> - All other built-in operations fail to be intercepted by both schemes in 3.X.

Again, the net effect is that operator overloading methods implicitly run by built-in operations are never routed through either attribute interception method in 3.X: Python 3.X's new-style classes search for such attributes in classes and skip instance lookup entirely. Normally named attributes do not.

This makes delegation-based wrapper classes more difficult to code in 3.X's new-style classes -- if wrapped classes may contain operator overloading methods, those methods must be redefined redundantly in the wrapper class in order to delegate to the wrapped object. In general delegation tools, this can add dozens of extra methods.

Of course, the addition of such methods can be partly automated by tools that augment classes with new methods (the class decorators and metaclasses of the next two chapters might help here). Moreover, a superclass might be able to define all these extra methods once, for inheritance in delegation-based classes. Still, delegation coding patterns require extra work in 3.X's classes.

For a more realistic illustration of this phenomenon as well as its workaround, see the Private decorator example in the following chapter. There, we'll explore alternatives for coding the operator methods required of proxies in 3.X's classes -- including reusable mix-in superclass models. We'll also see there that it's possible to insert a \_\_getattribute\_\_ in the client class to retain its original type, although this method still won't be called for operator overloading methods; printing still runs a \_\_str\_\_ defined in such a class directly, for example, instead of routing the request through \_\_getattribute\_\_.

As a more realistic example of this, the next section resurrects our class tutorial example. Now that you understand how attribute interception works, I'll be able to explain one of its stranger bits.

### Delegation-based managers revisited
The object-oriented tutorial of Chapter 28 presented a Manager class that used object embedding and method delegation to customize its superclass, rather than inheritance. Here is the code again for reference, with some irrelevant testing removed:
> 
> > ```python
> > class Person:
> >     def __init__(self, name, job=None, pay=0):
> >         self.name = name
> >         self.job = job
> >         self.pay = pay
> >     def lastName(self):
> >         return self.name.split()[-1]
> >     def giveRaise(self, percent):
> >         self.pay = int(self.pay * (1 + percent))
> >     def __repr__(self):
> >         return '[Person: %s, %s]' % (self.name, self.pay)
> > 
> > class Manager:
> >     def __init__(self, name, pay):
> >         self.person = Person(name, 'mgr', pay) 		# Embed a Person object
> >     def giveRaise(self, percent, bonus=.10):
> >         self.person.giveRaise(percent + bonus) 		# Intercept and delegate
> >     def __getattr__(self, attr):
> >         return getattr(self.person, attr) 			# Delegate all other attrs
> >     def __repr__(self):
> >         return str(self.person) 			# Must overload again (in 3.X)
> > 
> > if __name__ == '__main__':
> >     sue = Person('Sue Jones', job='dev', pay=100000)
> >     print(sue.lastName())
> >     sue.giveRaise(.10)
> >     print(sue)
> >     tom = Manager('Tom Jones', 50000) 	# Manager.__init__
> >     print(tom.lastName()) 				# Manager.__getattr__ -> Person.lastName
> >     tom.giveRaise(.10) 				# Manager.giveRaise -> Person.giveRaise
> >     print(tom) 				# Manager.__repr__ -> Person.__repr__
> > ```
> 
> Comments at the end of this file show which methods are invoked for a line's operation. In particular, notice how lastName calls are undefined in Manager, and thus are routed into the generic \_\_getattr\_\_ and from there on to the embedded Person object. Here is the script's output -- Sue receives a 10% raise from Person, but Tom gets 20% because giveRaise is customized in Manager:
> 
> > ```powershell
> > c:\code> py -3 getattr-delegate.py
> > Jones
> > [Person: Sue Jones, 110000]
> > Jones
> > [Person: Tom Jones, 60000]
> > ```
> 

By contrast, though, notice what occurs when we print a Manager at the end of the script: the wrapper class's \_\_repr\_\_ is invoked, and it delegates to the embedded Person object's \_\_repr\_\_. With that in mind, watch what happens if we delete the Manager.\_\_repr\_\_ method in this code:
> ```python
> # Delete the Manager __str__ method
> class Manager:
>     def __init__(self, name, pay):
>         self.person = Person(name, 'mgr', pay) 		# Embed a Person object
>     def giveRaise(self, percent, bonus=.10):
>         self.person.giveRaise(percent + bonus)       	# Intercept and delegate
>     def __getattr__(self, attr):
>         return getattr(self.person, attr) 			# Delegate all other attrs
> ```

Now printing does not route its attribute fetch through the generic \_\_getattr\_\_ interceptor under Python 3.X's new-style classes for Manager objects. Instead, a default \_\_repr\_\_ display method inherited from the class's implicit object superclass is looked up and run (sue still prints correctly, because Person has an explicit \_\_repr\_\_):
> ```powershell
> c:\code> py -3 getattr-delegate.py
> Jones
> [Person: Sue Jones, 110000]
> Jones
> <__main__.Manager object at 0x029E7B70>
> ```

As coded, running without a \_\_repr\_\_ like this does trigger \_\_getattr\_\_ in Python 2.X's default classic classes, because operator overloading attributes are routed through this method, and such classes do not inherit a default for \_\_repr\_\_:
> ```powershell
> c:\code> py -2 getattr-delegate.py
> Jones
> [Person: Sue Jones, 110000]
> Jones
> [Person: Tom Jones, 60000]
> ```

Switching to \_\_getattribute\_\_ won't help 3.X here either -- like \_\_getattr\_\_, it is not run for operator overloading attributes implied by built-in operations in either Python 2.X or 3.X:
> 
> > ```python
> > # Replace __getattr_ with __getattribute__
> > class Manager(object): 			# Use "(object)" in 2.X
> >     def __init__(self, name, pay):
> >         self.person = Person(name, 'mgr', pay) 		# Embed a Person object
> >     def giveRaise(self, percent, bonus=.10):
> >         self.person.giveRaise(percent + bonus) 		# Intercept and delegate
> >     def __getattribute__(self, attr):
> >         print('**', attr)
> >         if attr in ['person', 'giveRaise']:
> >             return object.__getattribute__(self, attr) 		# Fetch my attrs
> >         else:
> >             return getattr(self.person, attr) 		# Delegate all others
> > ```
> 
> Regardless of which attribute interception method is used in 3.X, we still must include a redefined \_\_repr\_\_ in Manager (as shown previously) in order to intercept printing operations and route them to the embedded Person object:
> 
> > ```powershell
> > C:\code> py -3 getattr-delegate.py
> > Jones
> > [Person: Sue Jones, 110000]
> > ** lastName
> > ** person
> > Jones
> > ** giveRaise
> > ** person
> > <__main__.Manager object at 0x028E0590>
> > ```
> 

Notice that \_\_getattribute\_\_ gets called twice here for methods -- once for the method name, and again for the self.person embedded object fetch. We could avoid that with a different coding, but we would still have to redefine \_\_repr\_\_ to catch printing, albeit differently here (self.person would cause this \_\_getattribute\_\_ to fail):
> 
> > ```python
> > # Code __getattribute__ differently to minimize extra calls
> > class Manager:
> >     def __init__(self, name, pay):
> >         self.person = Person(name, 'mgr', pay)
> >     def __getattribute__(self, attr):
> >         print('**', attr)
> >         person = object.__getattribute__(self, 'person')
> >         if attr == 'giveRaise':
> >             return lambda percent: person.giveRaise(percent+.10)
> >         else:
> >             return getattr(person, attr)
> >     def __repr__(self):
> >         person = object.__getattribute__(self, 'person')
> >         return str(person)
> > ```
> 
> When this alternative runs, our object prints properly, but only because we've added an explicit \_\_repr\_\_ in the wrapper -- this attribute is still not routed to our generic attribute interception method:
> 
> > ```powershell
> > Jones
> > [Person: Sue Jones, 110000]
> > ** lastName
> > Jones
> > ** giveRaise
> > [Person: Tom Jones, 60000]
> > ```
> 

That short story here is that delegation-based classes like Manager must redefine some operator overloading methods (like \_\_repr\_\_ and \_\_str\_\_) to route them to embedded objects in Python 3.X, but not in Python 2.X unless new-style classes are used. Our only direct options seem to be using \_\_getattr\_\_ and Python 2.X, or redefining operator overloading methods in wrapper classes redundantly in 3.X.

Again, this isn't an impossible task; many wrappers can predict the set of operator overloading methods required, and tools and superclasses can automate part of this task -- in fact, we'll study coding patterns that can fill this need in the next chapter.

Moreover, not all classes use operator overloading methods (indeed, most application classes usually should not). It is, however, something to keep in mind for delegation coding models used in Python 3.X; when operator overloading methods are part of an object's interface, wrappers must accommodate them portably by redefining them locally.  

