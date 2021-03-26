# The "New Style" Class Model
In release 2.2, Python introduced a new flavor of classes, known as new-style classes; classes following the original and traditional model became known as classic classes when compared to the new kind. In 3.X the class story has merged, but it remains split for Python 2.X users and code:
- In Python 3.X, all classes are automatically what were formerly called "new style," whether they explicitly inherit from object or not. Coding the object superclass is optional and implied.
- In Python 2.X, classes must explicitly inherit from object (or another built-in type) to be considered "new style" and enable and obtain all new-style behavior. Classes without this are "classic."

Because all classes are automatically new-style in 3.X, the features of new-style classes are simply normal class features in that line. I've opted to keep their descriptions in this section separate, however, in deference to users of Python 2.X code -- classes in such code acquire new-style features and behavior only when they are derived from object.

In other words, when Python 3.X users see descriptions of "new style" topics in this book, they should take them to be descriptions of existing properties of their classes.

For 2.X readers, these are a set of optional changes and extensions that you may choose to enable or not, unless the code you must use already employs them. In Python 2.X, the identifying syntactic difference for new-style classes is that they are derived from either a built-in type, such as list, or a special built-in class known as object. The built-in name object is provided to serve as a superclass for new-style classes if no other built-in type is appropriate to use:
> ```python
> class newstyle(object): 			# 2.X explicit new-style derivation
>     ...normal class code... 		# Not required in 3.X: automatic
> ```

Any class derived from object, or any other built-in type, is automatically treated as a new-style class. That is, as long as a built-in type is somewhere in its superclass tree, a 2.X class acquires new-style class behavior and extensions. Classes not derived from built-ins such as object are considered classic.

## Just How New Is New-Style?
As we'll see, new-style classes come with profound differences that impact programs broadly, especially when code leverages their added advanced features. In fact, at least in terms of its OOP support, these changes on some levels transform Python into a different language altogether -- one that's mandated in the 3.X line, one that's optional in 2.X only if ignored by every programmer, and one that borrows much more from (and is often as complex as) other languages in this domain.

New-style classes stem in part from an attempt to merge the notion of class with that of type around the time of Python 2.2, though they went unnoticed by many until they were escalated to required knowledge in 3.X. You'll need to judge the success of that merging for yourself, but as we'll see, there are still distinctions in the model -- now between class and metaclass -- and one of its side effects is to make normal classes more powerful but also substantially more complex. The new-style inheritance algorithm formalized in Chapter 40, for example, grows in complexity by at least a factor of 2.

Still, some programmers using straightforward application code may notice only slight divergence from traditional "classic" classes. After all, we've managed to get to this point in this book writing substantial class examples, with mostly just passing mentions of this change. Moreover, the classic class model still available in 2.X works exactly as it has for some two decades.

However, because they modify core class behaviors, new-style classes had to be introduced in Python 2.X as a distinct tool so as to avoid impacting any existing code that depends on the prior model. For example, some subtle differences, such as diamond pattern inheritance search and the interaction of built-in operations and managed attribute methods such as \_\_getattr\_\_ can cause some existing code to fail if left unchanged. Using optional extensions in the new model such as slots can have the same effect.

The class model split is removed in Python 3.X, which mandates new-style classes, but it still exists for readers using 2.X, or reusing the vast amount of existing 2.X code in production use. Because this has been an optional extension in 2.X, code written for that line may use either class model.

The next two top-level sections provide overviews of the ways in which new-style classes differ and the new tools they provide. These topics represent potential changes to some Python 2.X readers, but simply additional advanced class topics to many Python 3.X readers. If you're in the latter group, you'll find full coverage here, though some of it is presented in the context of changes -- which you can accept as features, but only if you never must deal with any of the millions of lines of existing 2.X code.

## New-Style Class Changes
New-style classes differ from classic classes in a number of ways, some of which are subtle but can impact both existing 2.X code and common coding styles. As preview and summary, here are some of the most prominent ways they differ:
- **Attribute fetch for built-ins: instance skipped**
  The \_\_getattr\_\_ and \_\_getattribute\_\_ generic attribute interception methods are still run for attributes accessed by explicit name, but no longer for attributes implicitly fetched by built-in operations. They are not called for \_\_X\_\_ operator overloading method names in built-in contexts only -- the search for such names begins at classes, not instances. This breaks or complicates objects that serve as proxies for another object's interface, if wrapped objects implement operator overloading. 
  Such methods must be redefined for the sake of differing built-ins dispatch in newstyle classes.

- **Classes and types merged: type testing**
  Classes are now types, and types are now classes. In fact, the two are essentially synonyms, though the metaclasses that now subsume types are still somewhat distinct from normal classes. The type(I) built-in returns the class an instance is made from, instead of a generic instance type, and is normally the same as I.\_\_class\_\_.
  Moreover, classes are instances of the type class, and type may be subclassed to customize class creation with metaclasses coded with class statements. This can impact code that tests types or otherwise relies on the prior type model.

- **Automatic object root class: defaults**
  All new-style classes (and hence types) inherit from object, which comes with a small set of default operator overloading methods (e.g., \_\_repr\_\_). In 3.X, this class is added automatically above the user-defined root (i.e., topmost) classes in a tree, and need not be listed as a superclass explicitly. This can affect code that assumes the absence of method defaults and root classes.

- **Inheritance search order: MRO and diamonds**
  Diamond patterns of multiple inheritance have a slightly different search order -- roughly, at diamonds they are searched across before up, and more breadth-first than depth-first. This attribute search order, known as the MRO, can be traced with a new \_\_mro\_\_ attribute available on new-style classes. The new search order largely applies only to diamond class trees, though the new model's implied object root itself forms a diamond in all multiple inheritance trees. Code that relies on the prior order will not work the same.

- **Inheritance algorithm: Chapter 40**
  The algorithm used for inheritance in new-style classes is substantially more complex than the depth-first model of classic classes, incorporating special cases for descriptors, metaclasses, and built-ins. We won't be able to formalize this until Chapter 40 after we've studied metaclasses and descriptors in more depth, but it can impact code that does not anticipate its extra convolutions.

- **New advanced tools: code impacts**
  New-style classes have a set of new class tools, including slots, properties, descriptors, super, and the \_\_getattribute\_\_ method. Most of these have very specific tool-building purposes. Their use can also impact or break existing code, though; slots, for example, sometimes prevent creation of an instance namespace dictionary altogether, and generic attribute handlers may require different coding.
  We'll explore the extensions noted in the last of these items in a later top-level section of its own, and will defer formal inheritance algorithm coverage until Chapter 40 as noted. Because the other items on this list have the potential to break traditional Python code, though, let's take a closer look at each in turn here.

> **Note**:
> Content note: Keep in mind that new-style class changes apply to both 3.X and 2.X, even though they are an option in the latter. This chapter and book sometimes label features as 3.X changes to contrast with traditional 2.X code, but some are technically introduced by new-style
> classes -- which are mandated in 3.X, but can show up in 2.X code too.
> 
> For space, this distinction is called out often but not dogmatically here. Complicating this distinction, some 3.X class-related changes owe to new-style classes (e.g., skipping \_\_getattr\_\_ for operator methods) but some do not (e.g., replacing unbound methods with functions). Moreover, many 2.X programmers stick to classic classes, ignoring what they view as a 3.X feature. New-style classes are not new, though, and apply to both Pythons -- if they appear in 2.X code, they're required reading for 2.X users too.
>

## Attribute Fetch for Built-ins Skips Instances
We introduced this new-style class change in sidebars in both Chapter 28 and Chapter 31 because of their impact on prior examples and topics. In new-style classes (and hence all classes in 3.X), the generic instance attribute interception methods \_\_getattr\_\_ and \_\_getattribute\_\_ are no longer called by built-in operations for \_\_X\_\_ operator overloading method names -- the search for such names begins at classes, not instances. Attributes accessed by explicit name, however, are routed through these methods, even if they are \_\_X\_\_ names. Hence, this is primarily a change to the behavior of built-in operations.

More formally, if a class defines a \_\_getitem\_\_ index overload method and X is an instance of this class, then an index expression like X[I] is roughly equivalent to X.\_\_getitem\_\_(I) for classic classes, but type(X).\_\_getitem\_\_(X, I) for new-style classes -- the latter beginning its search in the class, and thus skipping a \_\_getattr\_\_ step from the instance for an undefined name.

Technically, this method search for built-in operations like X[I] uses normal inheritance beginning at the class level, and inspects only the namespace dictionaries of all the classes from which X derives -- a distinction that can matter in the metaclass model we'll meet later in this chapter and focus on in Chapter 40, where classes may acquire behavior differently. The instance, however, is omitted by built-ins' search.

### Why the lookup change?
You can find formal rationales for this change elsewhere; this book is disinclined to parrot justifications for a change that breaks many working programs. But this is imagined as both an optimization path and a solution to a seemingly obscure call pattern issue. The former rationale is supported by the frequency of built-in operations. If every +, for example, requires extra steps at the instance, it can degrade program speed -- especially so given the new-style model's many attribute-level extensions.

The latter rationale is more obscure, and is described in Python manuals; in short, it reflects a conundrum introduced by the metaclass model. Because classes are now instances of metaclasses, and because metaclasses can define built-in operator methods to process the classes they generate, a method call run for a class must skip the class itself and look one level higher to pick up a method that processes the class, rather than selecting the class's own version. Its own version would result in an unbound method call, because the class's own method processes lower instances. This is just the usual unbound method model we discussed in the prior chapter, but is potentially aggravated by the fact that classes can acquire type behavior from metaclasses too.

As a result, because classes are both types and instances in their own right, all instances are skipped for built-in operation method lookup. This is supposedly applied to normal instances for uniformity and consistency, but both non-built-in names and direct and explicit calls to built-in names still check the instance anyhow. Though perhaps a consequence of the new-style class model, to some this may seem a solution arrived at for the sake of a usage pattern that was more artificial and obscure than the widely used one it broke. Its role as optimization path seems more defensible, but also not without repercussions.

In particular, this has potentially broad implications for the delegation-based classes, often known as proxy classes, when embedded objects implement operator overloading.

In new-style classes, such a proxy object's class must generally redefine any such names to catch and delegate, either manually or with tools. The net effect is to either significantly complicate or wholly obviate an entire category of programs. We explored delegation in Chapter 28 and Chapter 31; it's a common pattern used to augment or adapt another class's interface -- to add validation, tracing, timing, and many other sorts of logic. Though proxies may be more the exception than the rule in typical Python code, many Python programs depend upon them.

### Implications for attribute interception
In simple terms, and run in Python 2.X to show how new-style classes differ, indexing and prints are routed to \_\_getattr\_\_ in traditional classes, but not for new-style classes, where printing uses a default:
> ```python
> >>> class C:
>         data = 'spam'
>         def __getattr__(self, name): 					# Classic in 2.X: catches built-ins
>             print(name)
>             return getattr(self.data, name)
> >>> X = C()
> >>> X[0]
> __getitem__
> 's'
> >>> print(X) 					# Classic doesn't inherit default
> __str__
> spam
> >>> class C(object): 			# New-style in 2.X and 3.X
>         ...rest of class unchanged...
> >>> X = C() 					# Built-ins not routed to getattr
> >>> X[0]
> TypeError: 'C' object does not support indexing
> >>> print(X)
> <__main__.C object at 0x02205780>
> ```

Though apparently rationalized in the name of class metaclass methods and optimizing built-in operations, this divergence is not addressed by special-casing normal instances having a \_\_getattr\_\_, and applies only to built-in operations -- not to normally named methods, or explicit calls to built-in methods by name:
> ```python
> >>> class C: pass 				# 2.X classic class
> >>> X = C()
> >>> X.normal = lambda: 99
> >>> X.normal()
> 99
> >>> X.__add__ = lambda(y): 88 + y
> >>> X.__add__(1)
> 89
> >>> X + 1
> 89
> >>> class C(object): pass 		# 2.X/3.X new-style class
> >>> X = C()
> >>> X.normal = lambda: 99
> >>> X.normal() 					# Normals still from instance
> 99
> >>> X.__add__ = lambda(y): 88 + y
> >>> X.__add__(1) 					# Ditto for explicit built-in names
> 89
> >>> X + 1
> TypeError: unsupported operand type(s) for +: 'C' and 'int'
> ```

This behavior winds up being inherited by the \_\_getattr\_\_ attribute interception method:
> ```python
> >>> class C(object):
>         def __getattr__(self, name): print(name)
> >>> X = C()
> >>> X.normal 						# Normal names are still routed to getattr
> normal
> >>> X.__add__ 					# Direct calls by name are too, but expressions are not!
> __add__
> >>> X + 1
> TypeError: unsupported operand type(s) for +: 'C' and 'int'
> ```

### Proxy coding requirements
In a more realistic delegation scenario, this means that built-in operations like expressions no longer work the same as their traditional direct-call equivalent. Asymmetrically, direct calls to built-in method names still work, but equivalent expressions do not because through-type calls fail for names not at the class level and above. In other words, this distinction arises in built-in operations only; explicit fetches run correctly:
> ```python
> >>> class C(object):
>         data = 'spam'
>         def __getattr__(self, name):
>             print('getattr: ' + name)
>             return getattr(self.data, name)
> >>> X = C()
> >>> X.__getitem__(1) 				# Traditional mapping works but new-style's does not
> getattr: __getitem__
> 'p'
> >>> X[1]
> TypeError: 'C' object does not support indexing
> >>> type(X).__getitem__(X, 1)
> AttributeError: type object 'C' has no attribute '__getitem__'
> >>> X.__add__('eggs') 			# Ditto for +: instance skipped for expression only
> getattr: __add__
> 'spameggs'
> >>> X + 'eggs'
> TypeError: unsupported operand type(s) for +: 'C' and 'str'
> >>> type(X).__add__(X, 'eggs')
> AttributeError: type object 'C' has no attribute '__add__'
> ```

The net effect: to code a proxy of an object whose interface may in part be invoked by built-in operations, new-style classes require both \_\_getattr\_\_ for normal names, as well as method redefinitions for all names accessed by built-in operations -- whether coded manually, obtained from superclasses, or generated by tools. When redefinitions are so incorporated, calls through both instances and types are equivalent to built-in operations, though redefined names are no longer routed to the generic \_\_getattr\_\_ undefined name handler, even for explicit name calls:
> ```python
> >>> class C(object): 				# New-style: 3.X and 2.X
>         data = 'spam'
>         def __getattr__(self, name): 		# Catch normal names
>             print('getattr: ' + name)
>             return getattr(self.data, name)
> 
>         def __getitem__(self, i): 		# Redefine built-ins
>             print('getitem: ' + str(i))
>             return self.data[i] 			# Run expr or getattr
> 
>         def __add__(self, other):
>             print('add: ' + other)
>             return getattr(self.data, '__add__')(other)
> >>> X = C()
> >>> X.upper
> getattr: upper
> <built-in method upper of str object at 0x0233D670>
> >>> X.upper()
> getattr: upper
> 'SPAM'
> >>> X[1] 					# Built-in operation (implicit)
> getitem: 1
> 'p'
> >>> X.__getitem__(1) 		# Traditional equivalence (explicit)
> getitem: 1
> 'p'
> >>> type(X).__getitem__(X, 1) 		# New-style equivalence
> getitem: 1
> 'p'
> >>> X + 'eggs' 			# Ditto for + and others
> add: eggs
> 'spameggs'
> >>> X.__add__('eggs')
> add: eggs
> 'spameggs'
> >>> type(X).__add__(X, 'eggs')
> add: eggs
> 'spameggs'

### For more details
We will revisit this change in Chapter 40 on metaclasses, and by example in the contexts of attribute management in Chapter 38 and privacy decorators in Chapter 39. In the latter of these, we'll also explore coding structures for providing proxies with the required operator methods generically -- it's not an impossible task, and may need to be coded just once if done well. For more of the sort of code influenced by this issue, see those later chapters, as well as the earlier examples in Chapter 28 and Chapter 31.

Because we'll expand on this issue later in the book, we'll cut the coverage short here. For external links and pointers on this issue, though, see the following (along with your local search engine):
- **Python Issue 643841:** this issue has been discussed widely, but its most official history seems to be documented at http://bugs.python.org/issue643841. There, it was raised as a concern for real programs and escalated to be addressed, but a proposed library remedy or broader change in Python was struck down in favor of a simple documentation change to describe the new mandated behavior.

- **Tool recipes:** also see http://code.activestate.com/recipes/252151, an Active State Python recipe that describes a tool that automatically fills in special method names as generic call dispatchers in a proxy class created with metaclass techniques introduced later in this chapter. This tool still must ask you to pass in the operator method names that a wrapped object may implement, though (it must, as interface components of a wrapped object may be inherited from arbitrary sources).

- **Other approaches:** a web search today will uncover numerous additional tools that similarly populate proxy classes with overloading methods; it's a widespread concern! Again, in Chapter 39, we'll also see how to code straightforward and general superclasses once that provide the required methods or attributes as mix-ins, without metaclasses, redundant code generation, or similarly complex techniques.

This story may evolve over time, of course, but has been an issue for many years. As this stands today, classic class proxies for objects that do any operator overloading are effectively broken as new-style classes. Such classes in both 2.X and 3.X require coding or generating wrappers for all the implicitly invoked operator methods a wrapped object may support. This is not ideal for such programs -- some proxies may require dozens of wrapper methods (potentially over 50!) -- but reflects, or is at least an artifact of, the design goals of new-style class developers.

>
> **NOTE:**
> Be sure to see Chapter 40's metaclass coverage for an additional illustration of this issue and its rationale. We'll also see there that this behavior of built-ins qualifies as a special case in new-style inheritance.
> Understanding this well requires more background on metaclasses than the current chapter can provide, a regrettable byproduct of metaclasses in general -- they've become prerequisite to more usage than their originators may have foreseen.
>

## Type Model Changes
On to our next new-style change: depending on your assessment, in new-style classes the distinction between type and class has either been greatly muted or has vanished entirely. Specifically:
- **Classes are types**
  The type object generates classes as its instances, and classes generate instances of themselves. Both are considered types, because they generate instances. In fact, there is no real difference between built-in types like lists and strings and userdefined types coded as classes. This is why we can subclass built-in types, as shown earlier in this chapter -- a subclass of a built-in type such as list qualifies as a newstyle class and becomes a new user-defined type.

- **Types are classes**
  New class-generating types may be coded in Python as the metaclasses we'll meet later in this chapter -- user-defined type subclasses that are coded with normal class statements, and control creation of the classes that are their instances. As we'll see, metaclasses are both class and type, though they are distinct enough to support a reasonable argument that the prior type/class dichotomy has become one of metaclass/class, perhaps at the cost of added complexity in normal classes.

Besides allowing us to subclass built-in types and code metaclasses, one of the most practical contexts where this type/class merging becomes most obvious is when we do explicit type testing. With Python 2.X's classic classes, the type of a class instance is a generic "instance," but the types of built-in objects are more specific:
> ```python
> C:\code> c:\python27\python
> >>> class C: pass 				# Classic classes in 2.X
> >>> I = C() 						# Instances are made from classes
> >>> type(I), I.__class__
> (<type 'instance'>, <class __main__.C at 0x02399768>)
> >>> type(C) 						# But classes are not the same as types
> <type 'classobj'>
> >>> C.__class__
> AttributeError: class C has no attribute '__class__'
> >>> type([1, 2, 3]), [1, 2, 3].__class__
> (<type 'list'>, <type 'list'>)
> >>> type(list), list.__class__
> (<type 'type'>, <type 'type'>)
> ```

But with new-style classes in 2.X, the type of a class instance is the class it's created from, since classes are simply user-defined types -- the type of an instance is its class, and the type of a user-defined class is the same as the type of a built-in object type. Classes have a \_\_class\_\_ attribute now, too, because they are instances of type:
> ```python
> C:\code> c:\python27\python
> >>> class C(object): pass 			# New-style classes in 2.X
> >>> I = C() 							# Type of instance is class it's made from
> >>> type(I), I.__class__
> (<class '__main__.C'>, <class '__main__.C'>)
> >>> type(C), C.__class__ 				# Classes are user-defined types
> (<type 'type'>, <type 'type'>)
> ```

The same is true for all classes in Python 3.X, since all classes are automatically newstyle, even if they have no explicit superclasses. In fact, the distinction between builtin types and user-defined class types seems to melt away altogether in 3.X:
> ```python
> C:\code> c:\python33\python
> >>> class C: pass
> >>> I = C() 						# All classes are new-style in 3.X
> >>> type(I), I.__class__ 			# Type of instance is class it's made from
> (<class '__main__.C'>, <class '__main__.C'>)
> >>> type(C), C.__class__ 			# Class is a type, and type is a class
> (<class 'type'>, <class 'type'>)
> >>> type([1, 2, 3]), [1, 2, 3].__class__
> (<class 'list'>, <class 'list'>)
> >>> type(list), list.__class__ 	# Classes and built-in types work the same
> (<class 'type'>, <class 'type'>)
> ```
As you can see, in 3.X classes are types, but types are also classes. Technically, each class is generated by a metaclass -- a class that is normally either type itself, or a subclass of it customized to augment or manage generated classes. Besides impacting code that does type testing, this turns out to be an important hook for tool developers. We'll talk more about metaclasses later in this chapter, and again in more detail in Chapter 40.

### Implications for type testing
Besides providing for built-in type customization and metaclass hooks, the merging of classes and types in the new-style class model can impact code that does type testing.

In Python 3.X, for example, the types of class instances compare directly and meaningfully, and in the same way as built-in type objects. This follows from the fact that classes are now types, and an instance's type is the instance's class:
> ```python
> C:\code> c:\python33\python
> >>> class C: pass
> >>> class D: pass
> >>> c, d = C(), D()
> >>> type(c) == type(d) 				# 3.X: compares the instances' classes
> False
> >>> type(c), type(d)
> (<class '__main__.C'>, <class '__main__.D'>)
> >>> c.__class__, d.__class__
> (<class '__main__.C'>, <class '__main__.D'>)
> >>> c1, c2 = C(), C()
> >>> type(c1) == type(c2)
> True
> ```

With classic classes in 2.X, though, comparing instance types is almost useless, because all instances have the same "instance" type. To truly compare types, the instance \_\_class\_\_ attributes must be compared (if you care about portability, this works in 3.X, too, but it's not required there):
> ```python
> C:\code> c:\python27\python
> >>> class C: pass
> >>> class D: pass
> >>> c, d = C(), D()
> >>> type(c) == type(d) 				# 2.X: all instances are same type!
> True
> >>> c.__class__ == d.__class__ 		# Compare classes explicitly if needed
> False
> >>> type(c), type(d)
> (<type 'instance'>, <type 'instance'>)
> >>> c.__class__, d.__class__
> (<class __main__.C at 0x024585A0>, <class __main__.D at 0x024588D0>)
> ```

And as you should expect by now, new-style classes in 2.X work the same as all classes in 3.X in this regard -- comparing instance types compares the instances' classes automatically:
> ```python
> C:\code> c:\python27\python
> >>> class C(object): pass
> >>> class D(object): pass
> >>> c, d = C(), D()
> >>> type(c) == type(d) 			# 2.X new-style: same as all in 3.X
> False
> >>> type(c), type(d)
> (<class '__main__.C'>, <class '__main__.D'>)
> >>> c.__class__, d.__class__
> (<class '__main__.C'>, <class '__main__.D'>)
> ```

Of course, as I've pointed out numerous times in this book, type checking is usually the wrong thing to do in Python programs (we code to object interfaces, not object types), and the more general isinstance built-in is more likely what you'll want to use in the rare cases where instance class types must be queried. However, knowledge of Python's type model can help clarify the class model in general.

## All Classes Derive from "object"
Another ramification of the type change in the new-style class model is that because all classes derive (inherit) from the class object either implicitly or explicitly, and because all types are now classes, every object derives from the object built-in class, whether directly or through a superclass. Consider the following interaction in Python 3.X:
> ```python
> >>> class C: pass 				# For new-style classes
> >>> X = C()
> >>> type(X), type(C) 				# Type is class instance was created from
> (<class '__main__.C'>, <class 'type'>)
> ```

As before, the type of a class instance is the class it was made from, and the type of a class is the type class because classes and types have merged. It is also true, though, that the instance and class are both derived from the built-in object class and type, an implicit or explicit superclass of every class:
> ```python
> >>> isinstance(X, object)
> True
> >>> isinstance(C, object) 		# Classes always inherit from object
> True
> ```

The preceding returns the same results for both new-style and classic classes in 2.X today, though 2.X type results differ. More importantly, as we'll see ahead, object is not added to or present in a 2.X classic class's \_\_bases\_\_ tuple, and so is not a true superclass.

The same relationship holds true for built-in types like lists and strings, because types are classes in the new-style model -- built-in types are now classes, and their instances derive from object, too:
> ```python
> >>> type('spam'), type(str)
> (<class 'str'>, <class 'type'>)
> >>> isinstance('spam', object) 		# Same for built-in types (classes)
> True
> >>> isinstance(str, object)
> True
> ```

In fact, type itself derives from object, and object derives from type, even though the two are different objects -- a circular relationship that caps the object model and stems from the fact that types are classes that generate classes:
> ```python
> >>> type(type) 						# All classes are types, and vice versa
> <class 'type'>
> >>> type(object)
> <class 'type'>
> >>> isinstance(type, object) 			# All classes derive from object, even type
> True
> >>> isinstance(object, type) 			# Types make classes, and type is a class
> True
> >>> type is object
> False
> ```

### Implications for defaults
The preceding may seem obscure, but this model has a number of practical implications. For one thing, it means that we sometimes must be aware of the method defaults that come with the explicit or implicit object root class in new-style classes only:
> ```python
> c:\code> py −2
> >>> dir(object)
> ['__class__', '__delattr__', '__doc__', '__format__', '__getattribute__', '__hash__'
> , '__init__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '
> __sizeof__', '__str__', '__subclasshook__']
> >>> class C: pass
> >>> C.__bases__ 					# Classic classes do not inherit from object
> ()
> >>> X = C()
> >>> X.__repr__
> AttributeError: C instance has no attribute '__repr__'
> >>> class C(object): pass 		# New-style classes inherit object defaults
> >>> C.__bases__
> (<type 'object'>,)
> >>> X = C()
> >>> X.__repr__
> <method-wrapper '__repr__' of C object at 0x00000000020B5978>
> c:\code> py −3
> >>> class C: pass 				# This means all classes get defaults in 3.X
> >>> C.__bases__
> (<class 'object'>,)
> >>> C().__repr__
> <method-wrapper '__repr__' of C object at 0x0000000002955630>
> ```

This model also makes for fewer special cases than the prior type/class distinction of classic classes, and it allows us to write code that can safely assume and use an object superclass (e.g., by assuming it as an "anchor" in some super built-in roles described ahead, and by passing it method calls to invoke default behavior). We'll see examples of the latter later in the book; for now, let's move on to explore the last major new-style change.

## Diamond Inheritance Change
Our final new-style class model change is also one of its most visible: its slightly different inheritance search order for so-called diamond pattern multiple inheritance trees -- a tree pattern in which more than one superclass leads to the same higher superclass further above (and whose name comes from the diamond shape of the tree if you sketch out -- a square resting on one of its corners).

The diamond pattern is a fairly advanced design concept, only occurs in multiple inheritance trees, and tends to be coded rarely in Python practice, so we won't cover this topic in full depth. In short, though, the differing search orders were introduced briefly in the prior chapter's multiple inheritance coverage:
- **For classic classes (the default in 2.X): DFLR**
  The inheritance search path is strictly depth first, and then left to right -- Python climbs all the way to the top, hugging the left side of the tree, before it backs up and begins to look further to the right. This search order is known as DFLR for the first letters in its path's directions.
- **For new-style classes (optional in 2.X and automatic in 3.X): MRO**
  The inheritance search path is more breadth-first in diamond cases -- Python first looks in any superclasses to the right of the one just searched before ascending to the common superclass at the top. In other words, this search proceeds across by levels before moving up. This search order is called the new-style MRO for "method resolution order" (and often just MRO for short when used in contrast with the DFLR order). Despite the name, this is used for all attributes in Python, not just methods.

The new-style MRO algorithm is a bit more complex than just described -- and we'll expand on it a bit more formally later -- but this is as much as many programmers need to know. Still, it has both important benefits for new-style class code, as well as program-breaking potential for existing classic class code.

For example, the new-style MRO allows lower superclasses to overload attributes of higher superclasses, regardless of the sort of multiple inheritance trees they are mixed into. Moreover, the new-style search rule avoids visiting the same superclass more than once when it is accessible from multiple subclasses. It's arguably better than DFLR, but applies to a small subset of Python user code; as we'll see, though, the new-style class model itself makes diamonds much more common, and the MRO more important.

At the same time, the new MRO will locate attributes differently, creating a potential incompatibility for 2.X classic classes. Let's move on to some code to see how its differences pan out in practice.

### Implications for diamond inheritance trees
To illustrate how the new-style MRO search differs, consider this simplistic incarnation of the diamond multiple inheritance pattern for classic classes. Here, D's superclasses B and C both lead to the same common ancestor, A:
> ```python
> >>> class A: attr = 1 				# Classic (Python 2.X)
> >>> class B(A): pass 					# B and C both lead to A
> >>> class C(A): attr = 2
> >>> class D(B, C): pass 				# Tries A before C
> >>> x = D()
> >>> x.attr 							# Searches x, D, B, A
> 1
> ```

The attribute x.attr here is found in superclass A, because with classic classes, the inheritance search climbs as high as it can before backing up and moving right. The full DFLR search order would visit x, D, B, A, C, and then A. For this attribute, the search stops as soon as attr is found in A, above B.

However, with new-style classes derived from a built-in like object (and all classes in 3.X), the search order is different: Python looks in C to the right of B, before trying A above B. The full MRO search order would visit x, D, B, C, and then A. For this attribute, the search stops as soon as attr is found in C:
> ```python
> >>> class A(object): attr = 1 		# New-style ("object" not required in 3.X)
> >>> class B(A): pass
> >>> class C(A): attr = 2
> >>> class D(B, C): pass 				# Tries C before A
> >>> x = D()
> >>> x.attr 							# Searches x, D, B, C
> 2
> ```

This change in the inheritance search procedure is based upon the assumption that if you mix in C lower in the tree, you probably intend to grab its attributes in preference to A's. It also assumes that C is always intended to override A's attributes in all contexts, which is probably true when it's used standalone but may not be when it's mixed into a diamond with classic classes -- you might not even know that C may be mixed in like this when you code it.

Since it is most likely that the programmer meant that C should override A in this case, though, new-style classes visit C first. Otherwise, C could be essentially pointless in a diamond context for any names in A too -- it could not customize A and would be used only for names unique to C.

### Explicit conflict resolution
Of course, the problem with assumptions is that they assume things! If this search order deviation seems too subtle to remember, or if you want more control over the search process, you can always force the selection of an attribute from anywhere in the tree by assigning or otherwise naming the one you want at the place where the classes are mixed together. The following, for example, chooses new-style order in a classic class by resolving the choice explicitly:
> ```python
> >>> class A: attr = 1 				# Classic
> >>> class B(A): pass
> >>> class C(A): attr = 2
> >>> class D(B, C): attr = C.attr 		# <== Choose C, to the right
> >>> x = D()
> >>> x.attr 							# Works like new-style (all 3.X)
> 2
> ```

Here, a tree of classic classes is emulating the search order of new-style classes for a specific attribute: the assignment to the attribute in D picks the version in C, thereby subverting the normal inheritance search path (D.attr will be lowest in the tree). Newstyle classes can similarly emulate classic classes by choosing the higher version of the target attribute at the place where the classes are mixed together:
> ```python
> >>> class A(object): attr = 1 					# New-style
> >>> class B(A): pass
> >>> class C(A): attr = 2
> >>> class D(B, C): attr = B.attr 				# <== Choose A.attr, above
> >>> x = D()
> >>> x.attr 					# Works like classic (default 2.X)
> 1
> ```

If you are willing to always resolve conflicts like this, you may be able to largely ignore the search order difference and not rely on assumptions about what you meant when you coded your classes.
Naturally, attributes picked this way can also be method functions -- methods are normal, assignable attributes that happen to reference callable function objects:
> ```python
> >>> class A:
>         def meth(s): print('A.meth')
> >>> class C(A):
>         def meth(s): print('C.meth')
> >>> class B(A):
>         pass
> >>> class D(B, C): pass 			# Use default search order
> >>> x = D() 						# Will vary per class type
> >>> x.meth() 						# Defaults to classic order in 2.X
> A.meth
> >>> class D(B, C): meth = C.meth 	# <== Pick C's method: new-style (and 3.X)
> >>> x = D()
> >>> x.meth()
> C.meth
> >>> class D(B, C): meth = B.meth 	# <== Pick B's method: classic
> >>> x = D()
> >>> x.meth()
> A.meth
> ```

Here, we select methods by explicitly assigning to names lower in the tree. We might also simply call the desired class explicitly; in practice, this pattern might be more common, especially for things like constructors:
> ```python
> class D(B, C):
>     def meth(self): 				# Redefine lower
>         ...
> C.meth(self) 						# <== Pick C's method by calling
> ```

Such selections by assignment or call at mix-in points can effectively insulate your code from this difference in class flavors. This applies only to the attributes you handle this way, of course, but explicitly resolving the conflicts ensures that your code won't vary per Python version, at least in terms of attribute conflict selection. In other words, this can serve as a portability technique for classes that may need to be run under both the new-style and classic class models.

>
> **NOTE:**
> Explicit is better than implicit -- for method resolution too: Even without the classic/new-style class divergence, the explicit method resolution technique shown here may come in handy in multiple inheritance scenarios in general. For instance, if you want part of a superclass on the left and part of a superclass on the right, you might need to tell Python which same-named attributes to choose by using explicit assignments or calls in subclasses. We'll revisit this notion in a "gotcha" at the end of this chapter.
> 
> Also note that diamond inheritance patterns might be more problematic in some cases than I've implied here (e.g., what if B and C both have required constructors that call to the constructor in A?). Since such contexts are rare in real-world Python, we'll defer this topic until we explore the super built-in function near the end of this chapter; besides providing generic access to superclasses in single inheritance trees, super supports a cooperative mode for resolving conflicts in multiple inheritance trees by ordering method calls per the MRO -- assuming this order makes sense in this context too!
> 

### Scope of search order change
In sum, by default, the diamond pattern is searched differently for classic and new-style classes, and this is a non-backward-compatible change. Keep in mind, though, that this change primarily affects diamond pattern cases of multiple inheritance; new-style class inheritance works the same for most other inheritance tree structures. Further, it's not impossible that this entire issue may be of more theoretical than practical importance -- because the new-style search wasn't significant enough to address until Python 2.2 and didn't become standard until 3.0, it seems unlikely to impact most Python code.

Having said that, I should also note that even though you might not code diamond patterns in classes you write yourself, because the implied object superclass is above every root class in 3.X as we saw earlier, every case of multiple inheritance exhibits the diamond pattern today. That is, in new-style classes, object automatically plays the role that the class A does in the example we just considered. Hence the new-style MRO search rule not only modifies logical semantics, but is also an important performance optimization -- it avoids visiting and searching the same class more than once, even the automatic object.

Just as important, we've also seen that the implied object superclass in the new-style model provides default methods for a variety of built-in operations, including the \_\_str\_\_ and \_\_repr\_\_ display format methods. Run a dir(object) to see which methods are provided. Without the new-style MRO search order, in multiple inheritance cases the defaults in object would always override redefinitions in user-coded classes, unless they were always made in the leftmost superclass. In other words, the new-style class model itself makes using the new-style search order more critical!

For a more visual example of the implied object superclass in 3.X, and other examples of diamond patterns created by it, see the ListTree class's output in the lister.py example in the preceding chapter, as well as the classtree.py tree walker example in Chapter 29 -- and the next section.

## More on the MRO: Method Resolution Order
To trace how new-style inheritance works by default, we can also use the new class.\_\_mro\_\_ attribute mentioned in the preceding chapter's class lister examples -- technically a new-style extension, but useful here to explore a change. This attribute returns a class's MRO -- the order in which inheritance searches classes in a new-style class tree. This MRO is based on the C3 superclass linearization algorithm initially developed in the Dylan programming language, but later adopted by other languages including Python 2.3 and Perl 6.

### The MRO algorithm
This book avoids a full description of the MRO algorithm deliberately, because many Python programmers don't need to care (this only impacts diamonds, which are relatively rare in real-world code); because it differs between 2.X and 3.X; and because the details of the MRO are a bit too arcane and academic for this text. As a rule, this book avoids formal algorithms and prefers to teach informally by example.

On the other hand, some readers may still have an interest in the formal theory behind new-style MRO. If this set includes you, it's described in full detail online; search Python's manuals and the Web for current MRO links. In short, though, the MRO essentially works like this:
1. List all the classes that an instance inherits from using the classic class's DFLR lookup rule, and include a class multiple times if it's visited more than once.
2. Scan the resulting list for duplicate classes, removing all but the last occurrence of duplicates in the list.

The resulting MRO list for a given class includes the class, its superclasses, and all higher superclasses up to the object root class at the top of the tree. It's ordered such that each class appears before its parents, and multiple parents retain the order in which they appear in the \_\_bases\_\_ superclass tuple.

Crucially, though, because common parents in diamonds appear only at the position of their last visitation, lower classes are searched first when the MRO list is later used by attribute inheritance. Moreover, each class is included and thus visited just once, no matter how many classes lead to it.

We'll see applications of this algorithm later in this chapter, including that in super -- a built-in that elevates the MRO to required reading if you wish to fully understand how methods are dispatched by this call, should you choose to use it. As we'll see, despite its name, this call invokes the next class on the MRO, which might not be a superclass at all.

### Tracing the MRO
If you just want to see how Python's new-style inheritance orders superclasses in general, though, new-style classes (and hence all classes in 3.X) have a class.\_\_mro\_\_ attribute, which is a tuple giving the linear search order Python uses to look up attributes in superclasses. Really, this attribute is the inheritance order in new-style classes, and is often as much MRO detail as many Python users need.

Here are some illustrative examples, run in 3.X; for diamond inheritance patterns only, the search is the new order we've been studying -- across before up, per the MRO for new-style classes always used in 3.X, and available as an option in 2.X:
> ```python
> >>> class A: pass
> >>> class B(A): pass 						# Diamonds: order differs for newstyle
> >>> class C(A): pass 						# Breadth-first across lower levels
> >>> class D(B, C): pass
> >>> D.__mro__
> (<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>,
> <class '__main__.A'>, <class 'object'>)
> ```
For nondiamonds, though, the search is still as it has always been (albeit with an extra object root) -- to the top, and then to the right (a.k.a. DFLR, depth first and left to right, the model used for all classic classes in 2.X):
> ```python
> >>> class A: pass
> >>> class B(A): pass 				# Nondiamonds: order same as classic
> >>> class C: pass 				# Depth first, then left to right
> >>> class D(B, C): pass
> >>> D.__mro__
> (<class '__main__.D'>, <class '__main__.B'>, <class '__main__.A'>,
> <class '__main__.C'>, <class 'object'>)
> ```

The MRO of the following tree, for example, is the same as the earlier diamond, per DFLR:
> ```python
> >>> class A: pass
> >>> class B: pass 				# Another nondiamond: DFLR
> >>> class C(A): pass
> >>> class D(B, C): pass
> >>> D.__mro__
> (<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>,
> <class '__main__.A'>, <class 'object'>)
> ```

Notice how the implied object superclass always shows up at the end of the MRO; as we've seen, it's added automatically above root (topmost) classes in new-style class trees in 3.X (and optionally in 2.X):
> ```python
> >>> A.__bases__ 					# Superclass links: object at two roots
> (<class 'object'>,)
> >>> B.__bases__
> (<class 'object'>,)
> >>> C.__bases__
> (<class '__main__.A'>,)
> >>> D.__bases__
> (<class '__main__.B'>, <class '__main__.C'>)
> ```

Technically, the implied object superclass always creates a diamond in multiple inheritance even if your classes do not -- your classes are searched as before, but the newstyle MRO ensures that object is visited last, so your classes can override its defaults:
> ```python
> >>> class X: pass
> >>> class Y: pass
> >>> class A(X): pass  			# Nondiamond: depth first then left to right
> >>> class B(Y): pass  			# Though implied "object" always forms a diamond
> >>> class D(A, B): pass
> >>> D.mro()
> [<class '__main__.D'>, <class '__main__.A'>, <class '__main__.X'>,
> <class '__main__.B'>, <class '__main__.Y'>, <class 'object'>]
> >>> X.__bases__, Y.__bases__
> ((<class 'object'>,), (<class 'object'>,))
> >>> A.__bases__, B.__bases__
> ((<class '__main__.X'>,), (<class '__main__.Y'>,))
> ```

The class.\_\_mro\_\_ attribute is available only on new-style classes; it's not present in 2.X unless classes derive from object. Strictly speaking, new-style classes also have a class.mro() method used in the prior example for variety; it's called at class instantiation time and its return value is a list used to initialize the \_\_mro\_\_ attribute when the class is created (the method is available for customization in metaclasses, described later). You can also select MRO names if classes' object displays are too detailed, though this book usually shows the objects to remind you of their true form:
> ```python
> >>> D.mro() == list(D.__mro__)
> True
> >>> [cls.__name__ for cls in D.__mro__]
> ['D', 'A', 'X', 'B', 'Y', 'object']
> ```

However you access or display them, class MRO paths might be useful to resolve confusion, and in tools that must imitate Python's inheritance search order. The next section shows the latter role in action.

## Example: Mapping Attributes to Inheritance Sources
As a prime MRO use case, we noted at the end of the prior chapter that class tree climbers -- such as the class tree lister mix-in we wrote there -- might benefit from the MRO. As coded, the tree lister gave the physical locations of attributes in a class tree.

However, by mapping the list of inherited attributes in a dir result to the linear MRO sequence (or DFLR order for classic classes), such tools can more directly associate attributes with the classes from which they are inherited -- also a useful relationship for programmers.

We won't recode our tree lister here, but as a first major step, the following file, mapattrs.py, implements tools that can be used to associate attributes with their inheritance source; as an added bonus, its mapattrs function demonstrates how inheritance actually searches for attributes in class tree objects, though the new-style MRO is largely automated for us:
> ```python
> """
> File mapattrs.py (3.X + 2.X)
> Main tool: mapattrs() maps all attributes on or inherited by an
> instance to the instance or class from which they are inherited.
> Assumes dir() gives all attributes of an instance. To simulate
> inheritance, uses either the class's MRO tuple, which gives the
> search order for new-style classes (and all in 3.X), or a recursive
> traversal to infer the DFLR order of classic classes in 2.X.
> Also here: inheritance() gives version-neutral class ordering;
> assorted dictionary tools using 3.X/2.7 comprehensions.
> """
> import pprint
> 
> def trace(X, label='', end='\n'):
>     print(label + pprint.pformat(X) + end) 			# Print nicely
> def filterdictvals(D, V):
>     """
>     dict D with entries for value V removed.
>     filterdictvals(dict(a=1, b=2, c=1), 1) => {'b': 2}
>     """
>     return {K: V2 for (K, V2) in D.items() if V2 != V}
> 
> def invertdict(D):
>     """
>     dict D with values changed to keys (grouped by values).
>     Values must all be hashable to work as dict/set keys.
>     invertdict(dict(a=1, b=2, c=1)) => {1: ['a', 'c'], 2: ['b']}
>     """
>     def keysof(V):
>         return sorted(K for K in D.keys() if D[K] == V)
>     return {V: keysof(V) for V in set(D.values())}
> 
> def dflr(cls):
>     """
>     Classic depth-first left-to-right order of class tree at cls.
>     Cycles not possible: Python disallows on __bases__ changes.
>     """
>     here = [cls]
>     for sup in cls.__bases__:
>         here += dflr(sup)
>     return here
> 
> def inheritance(instance):
>     """
>     Inheritance order sequence: new-style (MRO) or classic (DFLR)
>     """
>     if hasattr(instance.__class__, '__mro__'):
>         return (instance,) + instance.__class__.__mro__
>     else:
>         return [instance] + dflr(instance.__class__)
> 
> def mapattrs(instance, withobject=False, bysource=False):
>     """
>     dict with keys giving all inherited attributes of instance,
>     with values giving the object that each is inherited from.
>     withobject: False=remove object built-in class attributes.
>     bysource: True=group result by objects instead of attributes.
>     Supports classes with slots that preclude __dict__ in instances.
>     """
>     attr2obj = {}
>     inherits = inheritance(instance)
>     for attr in dir(instance):
>         for obj in inherits:
>             if hasattr(obj, '__dict__') and attr in obj.__dict__:    			# See slots
>                 attr2obj[attr] = obj
>                 break
>     if not withobject:
>         attr2obj = filterdictvals(attr2obj, object)
>     return attr2obj if not bysource else invertdict(attr2obj)
> 
> 
> if __name__ == '__main__':
>     print('Classic classes in 2.X, new-style in 3.X')
>     class A: attr1 = 1
>     class B(A): attr2 = 2
>     class C(A): attr1 = 3
>     class D(B, C): pass
>     I = D()
>     print('Py=>%s' % I.attr1) 				# Python's search == ours?
>     trace(inheritance(I), 'INH\n') 			# [Inheritance order]
>     trace(mapattrs(I), 'ATTRS\n') 			# Attrs => Source
>     trace(mapattrs(I, bysource=True), 'OBJS\n') 		# Source => [Attrs]
>     print()
> 
>     print('New-style classes in 2.X and 3.X')
>     class A(object): attr1 = 1 				# "(object)" optional in 3.X
>     class B(A): attr2 = 2
>     class C(A): attr1 = 3
>     class D(B, C): pass
>     I = D()
>     print('Py=>%s' % I.attr1)
>     trace(inheritance(I), 'INH\n')
>     trace(mapattrs(I), 'ATTRS\n')
>     trace(mapattrs(I, bysource=True), 'OBJS\n')
> ```

This file assumes dir gives all an instance's attributes. It maps each attribute in a dir result to its source by scanning either the MRO order for new-style classes, or the DFLR order for classic classes, searching each object's namespace \_\_dict\_\_ along the way.

For classic classes, the DFLR order is computed with a simple recursive scan. The net effect is to simulate Python's inheritance search in both class models.

This file's self-test code applies its tools to the diamond multiple-inheritance trees we saw earlier. It uses Python's pprint library module to display lists and dictionaries nicely -- pprint.pprint is its basic call, and its pformat returns a print string. Run this on Python 2.7 to see both classic DFLR and new-style MRO search orders; on Python 3.3, the object derivation is unnecessary, and both tests give the same, new-style results.  Importantly, attr1, whose value is labeled with "Py=>" and whose name appears in the results lists, is inherited from class A in classic search, but from class C in new-style search:
> ```powershell
> c:\code> py −2 mapattrs.py
> Classic classes in 2.X, new-style in 3.X
> Py=>1
> INH
> [<__main__.D instance at 0x000000000225A688>,
> <class __main__.D at 0x0000000002248828>,
> <class __main__.B at 0x0000000002248768>,
> <class __main__.A at 0x0000000002248708>,
> <class __main__.C at 0x00000000022487C8>,
> <class __main__.A at 0x0000000002248708>]
> ATTRS
> {'__doc__': <class __main__.D at 0x0000000002248828>,
> '__module__': <class __main__.D at 0x0000000002248828>,
> 'attr1': <class __main__.A at 0x0000000002248708>,
> 'attr2': <class __main__.B at 0x0000000002248768>}
> OBJS
> {<class __main__.A at 0x0000000002248708>: ['attr1'],
> <class __main__.B at 0x0000000002248768>: ['attr2'],
> <class __main__.D at 0x0000000002248828>: ['__doc__', '__module__']}
> New-style classes in 2.X and 3.X
> Py=>3
> INH
> (<__main__.D object at 0x0000000002257B38>,
> <class '__main__.D'>,
> <class '__main__.B'>,
> <class '__main__.C'>,
> <class '__main__.A'>,
> <type 'object'>)
> ATTRS
> {'__dict__': <class '__main__.A'>,
> '__doc__': <class '__main__.D'>,
> '__module__': <class '__main__.D'>,
> '__weakref__': <class '__main__.A'>,
> 'attr1': <class '__main__.C'>,
> 'attr2': <class '__main__.B'>}
> OBJS
> {<class '__main__.A'>: ['__dict__', '__weakref__'],
> <class '__main__.B'>: ['attr2'],
> <class '__main__.C'>: ['attr1'],
> <class '__main__.D'>: ['__doc__', '__module__']}
> ```

As a larger application of these tools, the following is our inheritance simulator at work in 3.3 on the preceding chapter's testmixin0.py file's test classes (I've deleted some builtin names here for space; as usual, run live for the whole list). Notice how \_\_X pseudoprivate names are mapped to their defining classes, and how ListInstance appears in the MRO before object, which has a \_\_str\_\_ that would otherwise be chosen first -- as you'll recall, mixing this method in was the whole point of the lister classes!
> ```python
> c:\code> py −3
> >>> from mapattrs import trace, dflr, inheritance, mapattrs
> >>> from testmixin0 import Sub
> >>> I = Sub() 						# Sub inherits from Super and ListInstance roots
> >>> trace(dflr(I.__class__)) 			# 2.X search order: implied object before lister!
> [<class 'testmixin0.Sub'>,
> <class 'testmixin0.Super'>,
> <class 'object'>,
> <class 'listinstance.ListInstance'>,
> <class 'object'>]
> >>> trace(inheritance(I)) 			# 3.X (+ 2.X newstyle) search order: lister first
> (<testmixin0.Sub object at 0x0000000002974630>,
> <class 'testmixin0.Sub'>,
> <class 'testmixin0.Super'>,
> <class 'listinstance.ListInstance'>,
> <class 'object'>)
> >>> trace(mapattrs(I))
> {'_ListInstance__attrnames': <class 'listinstance.ListInstance'>,
> '__init__': <class 'testmixin0.Sub'>,
> '__str__': <class 'listinstance.ListInstance'>,
> ...etc...
> 'data1': <testmixin0.Sub object at 0x0000000002974630>,
> 'data2': <testmixin0.Sub object at 0x0000000002974630>,
> 'data3': <testmixin0.Sub object at 0x0000000002974630>,
> 'ham': <class 'testmixin0.Super'>,
> 'spam': <class 'testmixin0.Sub'>}
> >>> trace(mapattrs(I, bysource=True))
> {<testmixin0.Sub object at 0x0000000002974630>: ['data1', 'data2', 'data3'],
> <class 'listinstance.ListInstance'>: ['_ListInstance__attrnames', '__str__'],
> <class 'testmixin0.Super'>: ['__dict__', '__weakref__', 'ham'],
> <class 'testmixin0.Sub'>: ['__doc__',
> '__init__',
> '__module__',
> '__qualname__',
> 'spam']}
> >>> trace(mapattrs(I, withobject=True))
> {'_ListInstance__attrnames': <class 'listinstance.ListInstance'>,
> '__class__': <class 'object'>,
> '__delattr__': <class 'object'>,
> ...etc...
> ```

Here's the bit you might run if you want to label class objects with names inherited by an instance, though you may want to filter out some built-in double-underscore names for the sake of users' eyesight!
> ```python
> >>> amap = mapattrs(I, withobject=True, bysource=True)
> >>> trace(amap)
> {<testmixin0.Sub object at 0x0000000002974630>: ['data1', 'data2', 'data3'],
> <class 'listinstance.ListInstance'>: ['_ListInstance__attrnames', '__str__'],
> <class 'testmixin0.Super'>: ['__dict__', '__weakref__', 'ham'],
> <class 'testmixin0.Sub'>: ['__doc__',
> '__init__',
> '__module__',
> '__qualname__',
> 'spam'],
> <class 'object'>: ['__class__',
> '__delattr__',
> ...etc...
> '__sizeof__',
> '__subclasshook__']}
> ```

Finally, and as both a follow-up to the prior chapter's ruminations and segue to the next section here, the following shows how this scheme works for class-based slots attributes too. Because a class's \_\_dict\_\_ includes both normal class attributes and individual entries for the instance attributes defined by its \_\_slots\_\_ list, the slots attributes inherited by an instance will be correctly associated with the implementing class from which they are acquired, even though they are not physically stored in the instance's \_\_dict\_\_ itself:
> ```python
> # mapattrs-slots.py: test __slots__ attribute inheritance
> from mapattrs import mapattrs, trace
> class A(object): __slots__ = ['a', 'b']; x = 1; y = 2
> class B(A): __slots__ = ['b', 'c']
> class C(A): x = 2
> class D(B, C):
>     z = 3
>     def __init__(self): self.name = 'Bob';
> I = D()
> trace(mapattrs(I, bysource=True)) 			# Also: trace(mapattrs(I))
> ```

For explicitly new-style classes like those in this file, the results are the same under both 2.7 and 3.3, though 3.3 adds an extra built-in name to the set. The attribute names here reflect all those inherited by the instance from user-defined classes, even those implemented by slots defined at classes and stored in space allocated in the instance:
> ```python
> c:\code> py −3 mapattrs-slots.py
> {<__main__.D object at 0x00000000028988E0>: ['name'],
> <class '__main__.C'>: ['x'],
> <class '__main__.D'>: ['__dict__',
> '__doc__',
> '__init__',
> '__module__',
> '__qualname__',
> '__weakref__',
> 'z'],
> <class '__main__.A'>: ['a', 'y'],
> <class '__main__.B'>: ['__slots__', 'b', 'c']}
> ```

But we need to move ahead to understand the role of slots better -- and understand why mapattrs must be careful to check to see if a \_\_dict\_\_ is present before fetching it!

Study this code for more insight. For the prior chapter's tree lister, your next step might be to index the mapattrs function's bysource=True dictionary result to obtain an object's attributes during the tree sketch traversal, instead of (or perhaps in addition to?) its current physical \_\_dict\_\_ scan. You'll probably need to use getattr on the instance to fetch attribute values, because some may be implemented as slots or other "virtual" attributes at their source classes, and fetching these at the class directly won't return the instance's value. If I code anymore here, though, I'll deprive readers of the remaining fun, and the next section of its subject matter.

> 
> **NOTE:**
> Python's pprint module used in this example works as shown in Pythons 3.3 and 2.7, but appears to have an issue in Pythons 3.2 and 3.1 where it raises a wrong-number-arguments exception internally for the objects displayed here. Since I've already devoted too much space to covering transitory Python defects, and since this has been repaired in the versions of Python used in this edition, we'll leave working around this in the suggested exercises column for readers running this on the infected Pythons; change trace to simple prints as needed, and mind the note on battery dependence in Chapter 1!
>

