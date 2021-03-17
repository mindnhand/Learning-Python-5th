# Multiple Inheritance: “Mix-in” Classes
Our last design pattern is one of the most useful, and will serve as a subject for a more realistic example to wrap up this chapter and point toward the next. As a bonus, the code we'll write here may be a useful tool.

Many class-based designs call for combining disparate sets of methods. As we've seen, in a class statement, more than one superclass can be listed in parentheses in the header line. When you do this, you leverage multiple inheritance—the class and its instances inherit names from all the listed superclasses.

When searching for an attribute, Python's inheritance search traverses all superclasses in the class header from left to right until a match is found. Technically, because any of the superclasses may have superclasses of its own, this search can be a bit more complex for larger class trees:
- In classic classes (the default until Python 3.0), the attribute search in all cases proceeds depth-first all the way to the top of the inheritance tree, and then from left to right. This order is usually called DFLR, for its depth-first, left-to-right path.
- In new-style classes (optional in 2.X and standard in 3.X), the attribute search is usually as before, but in diamond patterns proceeds across by tree levels before moving up, in a more breadth-first fashion. This order is usually called the new-style MRO, for method resolution order, though it's used for all attributes, not just methods.

The second of these search rules is explained fully in the new-style class discussion in the next chapter.  Though difficult to understand without the next chapte's code (and somewhat rare to create yourself), diamond patterns appear when multiple classes in a tree share a common superclass; the new-style search order is designed to visit such a shared superclass just once, and after all its subclasses. In either model, though, when a class has multiple superclasses, they are searched from left to right according to the order listed in the class statement header lines.

In general, multiple inheritance is good for modeling objects that belong to more than one set. For instance, a person may be an engineer, a writer, a musician, and so on, and inherit properties from all such sets. With multiple inheritance, objects obtain the union of the behavior in all their superclasses. As we'll see ahead, multiple inheritance also allows classes to function as general packages of mixable attributes.

Though a useful pattern, multiple inheritance's chief downside is that it can pose a  conflict when the same method (or other attribute) name is defined in more than one superclass. When this occurs, the conflict is resolved either automatically by the inheritance search order, or manually in your code:
- Default: By default, inheritance chooses the first occurrence of an attribute it finds when an attribute is referenced normally—by self.method(), for example. In this mode, Python chooses the lowest and leftmost in classic classes, and in nondiamond patterns in all classes; new-style classes may choose an option to the right before one above in diamonds.
- Explicit: In some class models, you may sometimes need to select an attribute explicitly by referencing it through its class name -- with superclass.method(self),  for instance. Your code breaks the conflict and overrides the search's default--to select an option to the right of or above the inheritance search's default.

This is an issue only when the same name appears in multiple superclasses, and you do not wish to use the first one inherited. Because this isn't as common an issue in typical Python code as it may sound, we'll defer details on this topic until we study new-style classes and their MRO and super tools in the next chapter, and revisit this as a "gotcha" at the end of that chapter. First, though, the next section demonstrates a practical use case for multiple inheritance-based tools.

## Coding Mix-in Display Classes
Perhaps the most common way multiple inheritance is used is to "mix in" generalpurpose methods from superclasses.  Such superclasses are usually called mix-in classes--they provide methods you add to application classes by inheritance. In a sense, mixin classes are similar to modules: they provide packages of methods for use in their client subclasses. Unlike simple functions in modules, though, methods in mix-in classes also can participate in inheritance hierarchies, and have access to the self instance for using state information and other methods in their trees.

For example, as we've seen, Python's default way to print a class instance object isn't incredibly useful:
> ```python
> >>> class Spam:
>         def __init__(self): 		# No __repr__ or __str__
>             self.data1 = "food"
> >>> X = Spam()
> >>> print(X) 					# Default: class name + address (id)
> <__main__.Spam object at 0x00000000029CA908> 				# Same in 2.X, but says "instance"
> ```

As you saw in both Chapter 28's case study and Chapter 30's operator overloading coverage, you can provide a \_\_str\_\_ or \_\_repr\_\_ method to implement a custom string representation of your own. But, rather than coding one of these in each and every class you wish to print, why not code it once in a general-purpose tool class and inherit it in all your classes?

That's what mix-ins are for. Defining a display method in a mix-in superclass once enables us to reuse it anywhere we want to see a custom display format -- even in classes that may already have another superclass. We've already seen tools that do related work:
- Chapter 28's AttrDisplay class formatted instance attributes in a generic \_\_repr\_\_ method, but it did not climb class trees and was utilized in single-inheritance mode only.
- Chapter 29's classtree.py module defined functions for climbing and sketching class trees, but it did not display object attributes along the way and was not architected as an inheritable class.

Here, we're going to revisit these example's techniques and expand upon them to code a set of three mix-in classes that serve as generic display tools for listing instance attributes, inherited attributes, and attributes on all objects in a class tree. We'll also use our tools in multiple-inheritance mode and deploy coding techniques that make classes better suited to use as generic tools.

Unlike Chapter 28, we'll also code this with a \_\_str\_\_ instead of a \_\_repr\_\_. This is partially a style issue and limits their role to print and str, but the displays we'll be developing will be rich enough to be categorized as more user-friendly than as-code.

This policy also leaves client classes the option of coding an alternative lower-level display for interactive echoes and nested appearances with a \_\_repr\_\_. Using \_\_repr\_\_ here would still allow an alternative \_\_str\_\_, but the nature of the displays we'll be implementing more strongly suggests a \_\_str\_\_ role. See Chapter 30 for a review of these distinctions.

### Listing instance attributes with \_\_dict\_\_
Let's get started with the simple case -- listing attributes attached to an instance. The following class, coded in the file listinstance.py, defines a mix-in called ListInstance that overloads the \_\_str\_\_ method for all classes that include it in their header lines.

Because this is coded as a class, ListInstance is a generic tool whose formatting logic can be used for instances of any subclass client:
> ```python
> #!python
> # File listinstance.py (2.X + 3.X)
> 
> class ListInstance:
>     """
>     Mix-in class that provides a formatted print() or str() of instances via
>     inheritance of __str__ coded here; displays instance attrs only; self is
>     instance of lowest class; __X names avoid clashing with client's attrs
>     """
>     def __attrnames(self):
>         result = ''
>         for attr in sorted(self.__dict__):
>             result += '\t%s=%s\n' % (attr, self.__dict__[attr])
>         return result
>     def __str__(self):
>         return '<Instance of %s, address %s:\n%s>' % (
>                 self.__class__.__name__, 				# My class's name
>                 id(self), 				# My address
>                 self.__attrnames()) 		# name=value list
> 
> if __name__ == '__main__':
>     import testmixin
>     testmixin.tester(ListInstance)
> ```

All the code in this section runs in both Python 2.X and 3.X. A coding note: this code exhibits a classic comprehension pattern, and you could save some program real estate by implementing the \_\_attrnames method here more concisely with a generator expression that is triggered by the string join method, but it's arguably less clear -- expressions that wrap lines like this should generally make you consider simpler coding alternatives:
> ```python
> def __attrnames(self):
>     return ''.join('\t%s=%s\n' % (attr, self.__dict__ [attr]) for attr in sorted(self.__dict__))
> ```

ListInstance uses some previously explored tricks to extract the instance's class name and attributes:
- Each instance has a built-in \_\_class\_\_ attribute that references the class from which it was created, and each class has a \_\_name\_\_ attribute that references the name in the header, so the expression self.\_\_class\_\_.\_\_name\_\_ fetches the name of an instance's class.
- This class does most of its work by simply scanning the instance's attribute dictionary (remember, it's exported in \_\_dict\_\_) to build up a string showing the names and values of all instance attributes. The dictionary's keys are sorted to finesse any ordering differences across Python releases.

In these respects, ListInstance is similar to Chapter 28's attribute display; in fact, it's largely just a variation on a theme. Our class here uses two additional techniques, though:
- It displays the instance's memory address by calling the id built-function, which returns any object's address (by definition, a unique object identifier, which will be useful in later mutations of this code).
- It uses the pseudoprivate naming pattern for its worker method: \_\_attrnames. As we learned earlier in this chapter, Python automatically localizes any such name to its enclosing class by expanding the attribute name to include the class name (in this case, it becomes \_ListInstance\_\_attrnames). This holds true for both class attributes (like methods) and instance attributes attached to self. As noted in Chapter 28's first-cut version, this behavior is useful in a general tool like this, as it ensures that its names don't clash with any names used in its client subclasses.

Because ListInstance defines a \_\_str\_\_ operator overloading method, instances derived from this class display their attributes automatically when printed, giving a bit more information than a simple address. Here is the class in action, in single-inheritance mode, mixed in to the previous section's class (this code works the same in both Python 3.X and 2.X, though 2.X default repr displays use the label "instance" instead of "object"):
> ```python
> >>> from listinstance import ListInstance
> >>> class Spam(ListInstance): 		# Inherit a __str__ method
>         def __init__(self):
>             self.data1 = 'food'
> >>> x = Spam()
> >>> print(x) 				# print() and str() run __str__
> <Instance of Spam, address 43034496:
> data1=food
> ```
You can also fetch and save the listing output as a string without printing it with str, and interactive echoes still use the default format because we're left \_\_repr\_\_ as an option for clients:
> ```python
> >>> display = str(x) 			# Print this to interpret escapes
> >>> display
> '<Instance of Spam, address 43034496:\n\tdata1=food\n>'
> >>> x 						# The __repr__ still is a default
> <__main__.Spam object at 0x000000000290A780>
> ```

The ListInstance class is useful for any classes you write—even classes that already have one or more superclasses.  This is where multiple inheritance comes in handy: by adding ListInstance to the list of superclasses in a class header (i.e., mixing it in), you get its \_\_str\_\_ "for free" while still inheriting from the existing superclass(es).  The file testmixin0.py demonstrates with a first-cut testing script:
> ```python
> # File testmixin0.py
> from listinstance import ListInstance 		# Get lister tool class
> 
> class Super:
>     def __init__(self): 			# Superclass __init__
>         self.data1 = 'spam' 		# Create instance attrs
>     def ham(self):
>         pass
> 
> class Sub(Super, ListInstance): 	# Mix in ham and a __str__
>     def __init__(self): 			# Listers have access to self
>         Super.__init__(self)
>         self.data2 = 'eggs' 		# More instance attrs
>         self.data3 = 42
>     def spam(self): 				# Define another method here
>         pass
> 
> if __name__ == '__main__':
>     X = Sub()
>     print(X) 						# Run mixed-in __str__
> ```

Here, Sub inherits names from both Super and ListInstance; it's a composite of its own names and names in both its superclasses. When you make a Sub instance and print it, you automatically get the custom representation mixed in from ListInstance (in this case, this script's output is the same under both Python 3.X and 2.X, except for object addresses, which can naturally vary per process):
> ```python
> c:\code> python testmixin0.py
> <Instance of Sub, address 44304144:
> data1=spam
> data2=eggs
> data3=42
> ```

This testmixin0 testing script works, but it hardcodes the tested class's name in the code, and makes it difficult to experiment with alternatives -- as we will in a moment.

To be more flexible, we can borrow a page from Chapter 25's module reloaders, and pass in the object to be tested, as in the following improved test script, testmixin -- the one actually used by all the lister class modules' self-test code. In this context the object passed in to the tester is a mix-in class instead of a function, but the principle is similar: everything qualifies as a passable "first class" object in Python:
> ```python
> #!python
> # File testmixin.py (2.X + 3.X)
> """
> Generic lister mixin tester: similar to transitive reloader in
> Chapter 25, but passes a class object to tester (not function),
> and testByNames adds loading of both module and class by name
> strings here, in keeping with Chapter 31's factories pattern.
> """
> import importlib
> 
> def tester(listerclass, sept=False):
>     class Super:
>         def __init__(self): 				# Superclass __init__
>             self.data1 = 'spam' 			# Create instance attrs
>         def ham(self):
>             pass
> 
>     class Sub(Super, listerclass): 		# Mix in ham and a __str__
>         def __init__(self): 				# Listers have access to self
>             Super.__init__(self)
>             self.data2 = 'eggs' 			# More instance attrs
>             self.data3 = 42
>         def spam(self): 					# Define another method here
>             pass
> 
>     instance = Sub() 						# Return instance with lister's __str__
>     print(instance) 						# Run mixed-in __str__ (or via str(x))
>     if sept: print('-' * 80)
> 
> def testByNames(modname, classname, sept=False):
>     modobject = importlib.import_module(modname) 		# Import by namestring
>     listerclass = getattr(modobject, classname) 		# Fetch attr by namestring
>     tester(listerclass, sept)
> 
> if __name__ == '__main__':
>     testByNames('listinstance', 'ListInstance', True)     # Test all three here
>     testByNames('listinherited', 'ListInherited', True)
>     testByNames('listtree', 'ListTree', False)
> ```

While it's at it, this script also adds the ability to specify test module and class by name string, and leverages this in its self-test code -- an application of the factory pattern's mechanics described earlier. Here is the new script in action, being run by the lister module that imports it to test its own class (with the same results in 2.X and 3.X again); we can run the test script itself too, but that mode tests the two lister variants, which we have yet to see (or code!):
> 
> > ```python
> > c:\code> python listinstance.py
> > <Instance of Sub, address 43256968:
> > data1=spam
> > data2=eggs
> > data3=42
> > ```
> 
> > ```python
> > c:\code> python testmixin.py
> > <Instance of Sub, address 43977584:
> > data1=spam
> > data2=eggs
> > data3=42
> > ```
> 
> ...and tests of two other lister classes coming up...

The ListInstance class we've coded so far works in any class it's mixed into because self refers to an instanceof the subclass that pulls this class in, whatever that may be.

Again, in a sense, mix-in classes are the class equivalent of modules -- packages of methods useful in a variety of clients. For example, here is ListInstance working again in single-inheritance mode on a different class's instances, loaded with import, and displaying attributes assigned outside the class:
> ```python
> >>> import listinstance
> >>> class C(listinstance.ListInstance): pass
> >>> x = C()
> >>> x.a, x.b, x.c = 1, 2, 3
> >>> print(x)
> <Instance of C, address 43230824:
> a=1
> b=2
> c=3
> ```

Besides the utility they provide, mix-ins optimize code maintenance, like all classes do. For example, if you later decide to extend ListInstance's \_\_str\_\_ to also print all the class attributes that an instance inherits, you're safe; because it's an inherited method, changing \_\_str\_\_ automatically updates the display of each subclass that imports the class and mixes it in. And since it's now officially "later," let's move on to the next section to see what such an extension might look like.

### Listing inherited attributes with dir
As it is, our ListerInstance mix-in displays instance attributes only (i.e., names attached to the instance object itself). It's trivial to extend the class to display all the attributes accessible from an instance, though -- both its own and those it inherits from its classes. The trick is to use the dir built-in function instead of scanning the instance's \_\_dict\_\_ dictionary; the latter holds instance attributes only, but the former also collects all inherited attributes in Python 2.2 and later.

The following mutation codes this scheme; I've coded this in its own module to facilitate simple testing, but if existing clients were to use this version instead they would pick up the new display automatically (and recall from Chapter 25 that an import's as clause can rename a new version to a prior name being used):
> ```python
> # File listinherited.py (2.X + 3.X)
> class ListInherited:
>     """
>     Use dir() to collect both instance attrs and names inherited from
>     its classes; Python 3.X shows more names than 2.X because of the
>     implied object superclass in the new-style class model; getattr()
>     fetches inherited names not in self.__dict__; use __str__, not
>     __repr__, or else this loops when printing bound methods!
>     """
>     def __attrnames(self):
>         result = ''
>         for attr in dir(self): 				# Instance dir()
>             if attr[:2] == '__' and attr[-2:] == '__': 			# Skip internals
>                 result += '\t%s\n' % attr
>             else:
>                 result += '\t%s=%s\n' % (attr, getattr(self, attr))
>         return result
>     def __str__(self):
>         return '<Instance of %s, address %s:\n%s>' % (
>                     self.__class__.__name__, 				# My class's name
>                     id(self), 			# My address
>                     self.__attrnames()) 			# name=value list
> if __name__ == '__main__':
>     import testmixin
>     testmixin.tester(ListInherited)
> ```

Notice that this code skips \_\_X\_\_ names' values; most of these are internal names that we don't generally care about in a generic listing like this. This version also must use the getattr built-in function to fetch attributes by name string instead of using instance attribute dictionary indexing—getattr employs the inheritance search protocol, and some of the names we're listing here are not stored on the instance itself.

To test the new version, run its file directly -- it passes the class it defines to the testmixin.py file's test function to be used as a mix-in in a subclass. This output of this test and lister class varies per release, though, because dir results differ. In Python 2.X, we get the following; notice the name mangling at work in the lister's method name (I truncated some of the full value displays to fit on this page):
> ```python
> c:\code> c:\python27\python listinherited.py
> <Instance of Sub, address 35161352:
> _ListInherited__attrnames=<bound method Sub.__attrnames of <test...more...>>
> __doc__
> __init__
> __module__
> __str__
> data1=spam
> data2=eggs
> data3=42
> ham=<bound method Sub.ham of <testmixin.Sub instance at 0x00000...more...>>
> spam=<bound method Sub.spam of <testmixin.Sub instance at 0x00000...more...>>
> ```

In Python 3.X, more attributes are displayed because all classes are "new style" and inherit names from the implied object superclass; more on this in Chapter 32. Because so many names are inherited from the default superclass, I've omitted many here -- there are 32 in total in 3.3. Run this on your own for the full listing:
> ```python
> c:\code> c:\python33\python listinherited.py
> <Instance of Sub, address 43253152:
> _ListInherited__attrnames=<bound method Sub.__attrnames of <test...more...>>
> __class__
> __delattr__
> __dict__
> __dir__
> __doc__
> __eq__
> ...more names omitted 32 total...
> __repr__
> __setattr__
> __sizeof__
> __str__
> __subclasshook__
> __weakref__
> data1=spam
> data2=eggs
> data3=42
> ham=<bound method Sub.ham of <testmixin.tester.<locals>.Sub ...more...>>
> spam=<bound method Sub.spam of <testmixin.tester.<locals>.Sub ...more...>>
> ```

As one possible improvement to address the proliferation of inherited built-in names and long values here, the following alternative for \_\_\_attrnames in file listinherited2.py of the book example's package groups the double-underscore names separately, and minimizes line wrapping for large attribute values; notice how it escapes a % with %% so that just one remains for the final formatting operation at the end:
> ```python
> def __attrnames(self, indent=' '*4):
>     result = 'Unders%s\n%s%%s\nOthers%s\n' % ('-'*77, indent, '-'*77)
>     unders = []
>     for attr in dir(self): # Instance dir()
>         if attr[:2] == '__' and attr[-2:] == '__': # Skip internals
>             unders.append(attr)
>         else:
>             display = str(getattr(self, attr))[:82-(len(indent) + len(attr))]
>             result += '%s%s=%s\n' % (indent, attr, display)
>     return result % ', '.join(unders)
> ```

With this change, the class's test output is a bit more sophisticated, but also more concise and usable:
> 
> > ```powershell
> > c:\code> c:\python27\python listinherited2.py
> > <Instance of Sub, address 36299208:
> > Unders-----------------------------------------------------------------------------
> > __doc__, __init__, __module__, __str__
> > Others-----------------------------------------------------------------------------
> > _ListInherited__attrnames=<bound method Sub.__attrnames of <testmixin.Sub insta
> > data1=spam
> > data2=eggs
> > data3=42
> > ham=<bound method Sub.ham of <testmixin.Sub instance at 0x000000000229E1C8>>
> > spam=<bound method Sub.spam of <testmixin.Sub instance at 0x000000000229E1C8>>
> > ```
> 
> > ```powershell
> > c:\code> c:\python33\python listinherited2.py
> > <Instance of Sub, address 43318912:
> > Unders-----------------------------------------------------------------------------
> > __class__, __delattr__, __dict__, __dir__, __doc__, __eq__, __format__, __ge__,
> > __getattribute__, __gt__, __hash__, __init__, __le__, __lt__, __module__, __ne__,
> > __new__, __qualname__, __reduce__, __reduce_ex__, __repr__, __setattr__, __sizeof__,
> > __str__, __subclasshook__, __weakref__
> > Others-----------------------------------------------------------------------------
> > _ListInherited__attrnames=<bound method Sub.__attrnames of <testmixin.tester.<l
> > data1=spam
> > data2=eggs
> > data3=42
> > ham=<bound method Sub.ham of <testmixin.tester.<locals>.Sub object at 0x0000000
> > spam=<bound method Sub.spam of <testmixin.tester.<locals>.Sub object at 0x00000
> >  ```
> 

Display format is an open-ended problem (e.g., Python's standard pprint "pretty printer" module may offer options here too), so we'll leave further polishing as a suggested exercise. The tree lister of the next section may be more useful in any event.
> **Note**
> Looping in __repr__: One caution here -- now that we're displaying inherited methods too, we have to use __str__ instead of __repr__ to overload printing. With __repr__, this code will fall into recursive loops -- displaying the value of a method triggers the __repr__ of the method's class, in order to display the class. That is, if the lister's __repr__ tries to display a method, displaying the method's class will trigger the lister's __repr__ again.
> Subtle, but true! Change __str__ to __repr__ here to see this for yourself. If you must use __repr__ in such a context, you can avoid the loops by using isinstance to compare the type of attribute values against types.MethodType in the standard library, to know which items to skip.
>

### Listing attributes per object in class trees
Let's code one last extension. As it is, our latest lister includes inherited names, but doesn't give any sort of designation of the classes from which the names are acquired.

As we saw in the classtree.py example near the end of Chapter 29, though, it's straightforward to climb class inheritance trees in code. The following mix-in class, coded in the file listtree.py, makes use of this same technique to display attributes grouped by the classes they live in -- it sketches the full physical class tree, displaying attributes attached to each object along the way. The reader must still infer attribute inheritance, but this gives substantially more detail than a simple flat list:
> ```python
> #!python
> # File listtree.py (2.X + 3.X)
> class ListTree:
>     """
>     Mix-in that returns an __str__ trace of the entire class tree and all
>     its objects' attrs at and above self; run by print(), str() returns
>     constructed string; uses __X attr names to avoid impacting clients;
>     recurses to superclasses explicitly, uses str.format() for clarity;
>     """
>     def __attrnames(self, obj, indent):
>         spaces = ' ' * (indent + 1)
>         result = ''
>         for attr in sorted(obj.__dict__):
>             if attr.startswith('__') and attr.endswith('__'):
>                 result += spaces + '{0}\n'.format(attr)
>             else:
>                 result += spaces + '{0}={1}\n'.format(attr, getattr(obj, attr))
>         return result
> 
>     def __listclass(self, aClass, indent):
>         dots = '.' * indent
>         if aClass in self.__visited:
>             return '\n{0}<Class {1}:, address {2}: (see above)>\n'.format(
>                          dots,
>                          aClass.__name__,
>                          id(aClass))
>         else:
>             self.__visited[aClass] = True
>             here = self.__attrnames(aClass, indent)
>             above = ''
>             for super in aClass.__bases__:
>                 above += self.__listclass(super, indent+4)
>             return '\n{0}<Class {1}, address {2}:\n{3}{4}{5}>\n'.format(
>                          dots,
>                          aClass.__name__,
>                          id(aClass),
>                          here, above,
>                          dots)
> 
>     def __str__(self):
>         self.__visited = {}
>         here = self.__attrnames(self, 0)
>         above = self.__listclass(self.__class__, 4)
>         return '<Instance of {0}, address {1}:\n{2}{3}>'.format(
>                      self.__class__.__name__,
>                      id(self),
>                      here, above)
> 
> if __name__ == '__main__':
>     import testmixin
>     testmixin.tester(ListTree)
> ```

This class achieves its goal by traversing the inheritance tree -- from an instancee's \_\_class\_\_ to its class, and then from the class's \_\_bases\_\_ to all superclasses recursively, scanning each object's attribute \_\_dict\_\_ along the way. Ultimately, it concatenates each tree portion's string as the recursion unwinds.

It can take a while to understand recursive programs like this, but given the arbitrary shape and depth of class trees, we really have no choice here (apart from explicit stack equivalents of the sorts we met in Chapter 19 and Chapter 25, which tend to be no simpler, and which we'll omit here for space and time). This class is coded to keep its business as explicit as possible, though, to maximize clarity.

For example, you could replace the \_\_listclass method's loop statement in the first of the following with the implicitly run generator expression in the second, but the second seems unnecessarily convoluted in this context -- recursive calls embedded in a generator expression -- and has no obvious performance advantage, especially given this program's limited scope (neither alternative makes a temporary list, though the first may create more temporary results depending on the internal implementation of strings, concatenation, and join -- something you'd need to time with Chapter 21's tools to determine):
> 
> > ```python
> > above = ''
> > for super in aClass.__bases__:
> >     above += self.__listclass(super, indent+4)
> > ```
> 
> ...or...
> 
> > ```python
> > above = ''.join(self.__listclass(super, indent+4) for super in aClass.__bases__)
> > ```
> 

You could also code the else clause in \_\_listclass like the following, as in the prior edition of this book -- an alternative that embeds everything in the format arguments list; relies on the fact that the join call kicks off the generator expression and its recursive calls before the format operation even begins building up the result text; and seems more difficult to understand, despite the fact that I wrote it (never a good sign!):
> ```python
> self.__visited[aClass] = True
> genabove = (self.__listclass(c, indent+4) for c in aClass.__bases__)
> return '\n{0}<Class {1}, address {2}:\n{3}{4}{5}>\n'.format(
>                 dots,
>                 aClass.__name__,
>                 id(aClass),
>                 self.__attrnames(aClass, indent),       # Runs before format!
>                 ''.join(genabove),
>                 dots)
> ```

As always, explicit is better than implicit, and your code can be as big a factor in this as the tools it uses.
Also notice how this version uses the Python 3.X and 2.6/2.7 string format method instead of % formatting expressions, in an effort to make substitutions arguably clearer; when many substitutions are applied like this, explicit argument numbers may make the code easier to decipher. In short, in this version we exchange the first of the following lines for the second:
> ```python
> return '<Instance of %s, address %s:\n%s%s>' % (...) 		# Expression
> return '<Instance of {0}, address {1}:\n{2}{3}>'.format(...) 		# Method
> ``` 

This policy has an unfortunate downside in 3.2 and 3.3 too, but we have to run the code to see why.

### Running the tree lister
Now, to test, run this class's module file as before; it passes the ListTree class to testmixin.py to be mixed in with a subclass in the test function. The file's tree-sketcher output in Python 2.X is as follows:
> ```powershell
> c:\code> c:\python27\python listtree.py
> <Instance of Sub, address 36690632:
> _ListTree__visited={}
> data1=spam
> data2=eggs
> data3=42
> ....<Class Sub, address 36652616:
> __doc__
> __init__
> __module__
> spam=<unbound method Sub.spam>
> ........<Class Super, address 36652712:
> __doc__
> __init__
> __module__
> ham=<unbound method Super.ham>
> ........>
> ........<Class ListTree, address 30795816:
> _ListTree__attrnames=<unbound method ListTree.__attrnames>
> _ListTree__listclass=<unbound method ListTree.__listclass>
> __doc__
> __module__
> __str__
> ........>
> ....>
> ```

Notice in this output how methods are unbound now under 2.X, because we fetch them from classes directly. In the previous section's version they displayed as bound methods, because ListInherited fetched these from instances with getattr instead (the first version indexed the instance \_\_dict\_\_ and did not display inherited methods on classes at all). Also observe how the lister's \_\_visited table has its name mangled in the instance's attribute dictionary; unless we're very unlucky, this won't clash with other data there. Some of the lister class's methods are mangled for pseudoprivacy as well.

Under Python 3.X in the following, we again get extra attributes which may vary within  the 3.X line, and extra superclasses -- as we'll learn in the next chapter, all top-level classes inherit from the built-in object class automatically in 3.X; Python 2.X classes do so manually if they desire new-style class behavior. Also notice that the attributes that were unbound methods in 2.X are simple functions in 3.X, as described earlier in this chapter (and that again, I've deleted most built-in attributes in object to save space here; run this on your own for the complete listing):
> ```powershell
> c:\code> c:\python33\python listtree.py
> <Instance of Sub, address 44277488:
> _ListTree__visited={}
> data1=spam
> data2=eggs
> data3=42
> ....<Class Sub, address 36990264:
> __doc__
> __init__
> __module__
> __qualname__
> spam=<function tester.<locals>.Sub.spam at 0x0000000002A3C840>
> ........<Class Super, address 36989352:
> __dict__
> __doc__
> __init__
> __module__
> __qualname__
> __weakref__
> ham=<function tester.<locals>.Super.ham at 0x0000000002A3C730>
> ............<Class object, address 506770624:
> __class__
> __delattr__
> __dir__
> __doc__
> __eq__
> ...more omitted: 22 total...
> __repr__
> __setattr__
> __sizeof__
> __str__
> __subclasshook__
> ............>
> ........>
> ........<Class ListTree, address 36988440:
> _ListTree__attrnames=<function ListTree.__attrnames at 0x0000000002A3C158>
> _ListTree__listclass=<function ListTree.__listclass at 0x0000000002A3C1E0>
> __dict__
> __doc__
> __module__
> __qualname__
> __str__
> __weakref__
> ............<Class object:, address 506770624: (see above)>
> ........>
> ....>
> ```

This version avoids listing the same class object twice by keeping a table of classes visited so far (this is why an object's id is included -- to serve as a key for a previously displayed item in the report). Like the transitive module reloader of Chapter 25, a dictionary works to avoid repeats in the output because class objects are hashable and thus may be dictionary keys; a set would provide similar functionality.

Technically, cycles are not generally possible in class inheritance trees -- a class must already have been defined to be named as a superclass, and Python raises an exception as it should if you attempt to create a cycle later by \_\_bases\_\_ changes—but the visited  mechanism here avoids relisting a class twice:
> ```python
> >>> class C: pass
> >>> class B(C): pass
> >>> C.__bases__ = (B,) 			# Deep, dark magic!
> TypeError: a __bases__ item causes an inheritance cycle
> Usage variation: Showing underscore name values
> ```

This version also takes care to avoid displaying large internal objects by skipping \_\_X\_\_ names again. If you comment out the code that treats these names specially:
> ```python
> for attr in sorted(obj.__dict__):
>     # if attr.startswith('__') and attr.endswith('__'):
>     #     result += spaces + '{0}\n'.format(attr)
>     # else:
>           result += spaces + '{0}={1}\n'.format(attr, getattr(obj, attr))
> ```
then their values will display normally. Here's the output in 2.X with this temporary change made, giving the values of every attribute in the class tree:
> ```powershell
> c:\code> c:\python27\python listtree.py
> <Instance of Sub, address 35750408:
> _ListTree__visited={}
> data1=spam
> data2=eggs
> data3=42
> ....<Class Sub, address 36353608:
> __doc__=None
> __init__=<unbound method Sub.__init__>
> __module__=testmixin
> spam=<unbound method Sub.spam>
> ........<Class Super, address 36353704:
> __doc__=None
> __init__=<unbound method Super.__init__>
> __module__=testmixin
> ham=<unbound method Super.ham>
> ........>
> ........<Class ListTree, address 31254568:
> _ListTree__attrnames=<unbound method ListTree.__attrnames>
> _ListTree__listclass=<unbound method ListTree.__listclass>
> __doc__=
> Mix-in that returns an __str__ trace of the entire class tree and all its objects' attrs at and above self; run by
> print(), str() returns constructed string; uses __X attr names to avoid impacting clients; recurses to superclasses
> explicitly, uses str.format() for clarity;
> __module__=__main__
> __str__=<unbound method ListTree.__str__>
> ........>
> ....>
> 
> ```

This test's output is much larger in 3.X and may justify isolating underscore names in general as we did earlier.
In fact, this test may not even work in some currently recent 3.X releases as is:
> ```powershell
> c:\code> c:\python33\python listtree.py
> ...etc...
> File "listtree.py", line 18, in __attrnames
> result += spaces + '{0}={1}\n'.format(attr, getattr(obj, attr))
> TypeError: Type method_descriptor doesn't define __format__
> ```

I debated recoding to work around this issue, but it serves as a fair example of debugging requirements and techniques in a dynamic open source project like Python. Per the following note, the str.format call no longer supports certain object types that are the values of built-in attribute names -- yet another reason these names are probably better skipped.

> **Note**
> Debugging a str.format issue: In 3.X, running the commented-out version works in 3.0 and 3.1, but there seems to be a bug, or at least a regression, here in 3.2 and 3.3 -- these Pythons fail with an exception because five built-in methods in object do not define a \_\_format\_\_ expected by str.format, and the default in object is apparently no longer applied correctly in such cases with empty and generic formatting targets.
> 
> To see this live, it's enough to run simplified code that isolates the problem:
> > ```powershell
> > c:\code> py −3.1
> > >>> '{0}'.format(object.__reduce__)
> > "<method '__reduce__' of 'object' objects>"
> > c:\code> py −3.3
> > >>> '{0}'.format(object.__reduce__)
> > TypeError: Type method_descriptor doesn't define __format__
> > ```
> 
> Per both prior behavior and current Python documentation, empty targets like this are supposed to convert the object to its str print string (see both the original PEP 3101 and the 3.3 language reference manual).
> 
> Oddly, the {0} and {0:s} string targets both now fail, but the {0!s} forced str conversion target works, as does manual str preconversion -- apparently reflecting a change for a type-specific case that neglected perhaps more common generic usage modes:
> 
> > ```powershell
> > c:\code> py −3.3
> > >>> '{0:s}'.format(object.__reduce__)
> > TypeError: Type method_descriptor doesn't define __format__
> > >>> '{0!s}'.format(object.__reduce__)
> > "<method '__reduce__' of 'object' objects>"
> > >>> '{0}'.format(str(object.__reduce__))
> > "<method '__reduce__' of 'object' objects>"
> > ```
> 
> To fix, wrap the format call in a try statement to catch the exception; use % formatting expressions instead of the str.format method; use one of the aforementioned still-working str.format usage modes and hope it does not change too; or wait for a repair of this in a later 3.X release.
> 
> Here's the recommended workaround using the tried-and-true % (it's also noticeably shorter, but I won't repeat Chapter 7's comparisons here):
> 
> > ```powershell
> > c:\code> py −3.3
> > >>> '%s' % object.__reduce__
> > "<method '__reduce__' of 'object' objects>"
> > ```
> 
> To apply this in the tree lister's code, change the first of these to its  follower:
> > ```python
> > result += spaces + '{0}={1}\n'.format(attr, getattr(obj, attr))
> > result += spaces + '%s=%s\n' % (attr, getattr(obj, attr))
> > ```
> 
> Python 2.X has the same regression in 2.7 but not 2.6 -- inherited from the 3.2 change, apparently -- but does not show object methods in this chapter's example. Since this example generates too much output in 3.X anyhow, it's a moot point here, but is a decent example of real-world coding. Unfortunately, using newer features like str.format sometimes puts your code in the awkward position of beta tester in the current 3.X line!
>

### Usage variation: Running on larger modules
For more fun, uncomment the underscore handler lines to enable them again, and try mixing this class into something more substantial, like the Button class of Python's tkinter GUI toolkit module. In general, you'll want to name ListTree first (leftmost) in a class header, so its \_\_str\_\_ is picked up; Button has one, too, and the leftmost superclass is always searched first in multiple inheritance.

The output of the following is fairly massive (20K characters and 330 lines in 3.X -- and 38K if you forget to uncomment the underscore detection!), so run this code on your own to see the full listing. Notice how our lister's \_\_visited dictionary attribute mixes harmlessly with those created by tkinter itself. If you're using Python 2.X, also recall that you should use Tkinter for the module name instead of tkinter:
> ```python
> >>> from listtree import ListTree
> >>> from tkinter import Button 					# Both classes have a __str__
> >>> class MyButton(ListTree, Button): pass 		# ListTree first: use its __str__
> >>> B = MyButton(text='spam')
> >>> open('savetree.txt', 'w').write(str(B)) 		# Save to a file for later viewing
> 20513
> >>> len(open('savetree.txt').readlines()) 		# Lines in the file
> 330
> >>> print(B) 					# Print the display here
> <Instance of MyButton, address 43363688:
> _ListTree__visited={}
> _name=43363688
> _tclCommands=[]
> _w=.43363688
> children={}
> master=.
> ...much more omitted...
> >
> >>> S = str(B) 			# Or print just the first part
> >>> print(S[:1000])
> ```

Experiment arbitrarily on your own. The main point here is that OOP is all about code reuse, and mix-in classes are a powerful example. Like almost everything else in programming, multiple inheritance can be a useful device when applied well. In practice, though, it is an advanced feature and can become complicated if used carelessly or excessively. We'll revisit this topic as a gotcha at the end of the next chapter.

### Collector module
Finally, to make importing our tools even easier, we can provide a collector module that combines them in a single namespace -- importing just the following gives access to all three lister mix-ins at once:
> ```python
> # File lister.py
> # Collect all three listers in one module for convenience
> from listinstance import ListInstance
> from listinherited import ListInherited
> from listtree import ListTree
> Lister = ListTree # Choose a default lister
> ```

Importers can use the individual class names as is, or alias them to a common name used in subclasses that can be modified in the import statement:
> ```python
> >>> import lister
> >>> lister.ListInstance # Use a specific lister
> <class 'listinstance.ListInstance'>
> >>> lister.Lister # Use Lister default
> <class 'listtree.ListTree'>
> >>> from lister import Lister # Use Lister default
> >>> Lister
> <class 'listtree.ListTree'>
> >>> from lister import ListInstance as Lister # Use Lister alias
> >>> Lister
> <class 'listinstance.ListInstance'>
> ```
Python often makes flexible tool APIs nearly automatic.

### Room for improvement: MRO, slots, GUIs
Like most software, there's much more we could do here. The following gives some pointers on extensions you may wish to explore. Some are interesting projects, and two serve as segue to the next chapter, but for space will have to remain in the suggested exercise category here.
- **General ideas: GUIs, built-ins**
  Grouping double-underscore names as we did earlier may help reduce the size of the tree display, though some like \_\_init\_\_ are user-defined and may merit special treatment. Sketching the tree in a GUI might be a natural next step too -- the tkinter toolkit that we utilized in the prior section's lister examples ships with Python and provides basic but easy support, and others offer richer but more complex alternatives. See the notes at the end of Chapter 28's case study for more pointers in this department.
- **Physical trees versus inheritance: using the MRO (preview)**
  In the next chapter, we'll also meet the new-style class model, which modifies the search order for one special multiple inheritance case (diamonds). There, we'll also study the class.\_\_mro\_\_ new-style class object attribute -- a tuple giving the class tree search order used by inheritance, known as the new-style MRO. 
  
  As is, our ListTree tree lister sketches the physical shape of the inheritance tree, and expects the viewer to infer from this where an attribute is inherited from. This was its goal, but a general object viewer might also use the MRO tuple to automatically associate an attribute with the class from which it is inherited -- by scanning the new-style MRO (or the classic classes' DFLR ordering) for each inherited attribute in a dir result, we can simulate Python's inheritance search, and map attributes to their source objects in the physical class tree displayed. 
  
  In fact, we will write code that comes very close to this idea in the next chapter's mapattrs module, and reuse this example's test classes there to demonstrate the idea, so stay tuned for an epilogue to this story. This might be used instead of or in addition to displaying attribute physical locations in \_\_attrnames here; both forms might be useful data for programmers to see. This approach is also one way to deal with slots, the topic of the next note.
- **Virtual data: slots, properties, and more (preview)**
  Because they scan instance \_\_dict\_\_ namespace dictionaries, the ListInstance and ListTree classes presented here raise some subtle design issues. In Python classes, some names associated with instance data may not be stored at the instance itself. This includes topics presented in the next chapter such as new-style properties, slots, and descriptors, but also attributes dynamically computed in all classes with tools like \_\_getattr\_\_. None of these "virtual" attributes' names are stored in an instance's namespace dictionary, so none will be displayed as part of an instance's own data. 
  
  Of these, slots seem the most strongly associated with an instance; they store data on instances, even though their names don't appear in instance namespace dictionaries. Properties and descriptors are associated with instances too, but they don't reserve space in the instance, their computed nature is much more explicit, and they may seem closer to class-level methods than instance data. 
  
  As we'll see in the next chapter, slots function like instance attributes, but are created and managed by automatically created items in classes. They are a relatively infrequently used new-style class option, where instance attributes are declared in a \_\_slots\_\_ class attribute, and not physically stored in an instance's \_\_dict\_\_; in fact, slots may suppress a \_\_dict\_\_ entirely. Because of this, tools that display instances by scanning their namespaces alone won't directly associate the instance with attributes stored in slots. As is, ListTree displays slots as class attributes wherever they appear (though not at the instance), and ListInstance doesn't display them at all. 
  
  Though this will make more sense after we study this feature in the next chapter, it impacts code here and similar tools. For example, if in textmixin.py we assign \_\_slots\_\_=['data1'] in Super and \_\_slots\_\_=['data3'] in Sub, only the data2 attribute is displayed in the instance by these two lister classes. ListTree also displays data1 and data3, but as attributes of the Super and Sub class objects and with a special format for their values (technically, they are class-level descriptors, another new-style tool introduced in the next chapter).  

  As the next chapter will explain, to show slot attributes as instance names, tools generally need to use dir to get a list of all attributes -- both physically present and inherited -- and then use either getattr to fetch their values from the instance, or fetch values from their inheritance source via \_\_dict\_\_ in tree scans and accept the display of the implementations of some at classes. Because dir includes the names of inherited "virtual" attributes -- including both slots and properties -- they would be included in the instance set. As we'll also find, the MRO might assist here to map dir attribute to their sources, or restrict instance displays to names coded in user-defined classes by filtering out names inherited from the built-in object.  
  
  ListInherited is immune to most of this, because it already displays the full dir results set, which include both \_\_dict\_\_ names and all classes' \_\_slots\_\_ names, though its display is of marginal use as is. A ListTree variant using the dir technique along with the MRO sequence to map attributes to classes would apply to slots too, because slots-based names appear in class's \_\_dict\_\_ results individually as slot management tools, though not in the instance \_\_dict\_\_.  
  
  Alternatively, as a policy we could simply let our code handle slot-based attributes as it currently does, rather than complicating it for a rarely used, advanced feature that's even questionable practice today. Slots and normal instance attributes are different kinds of names. In fact, displaying slots names as attributes of classes instead of instances is technically more accurate -- as we'll see in the next chapter their implementation is at classes, though their space is at instances.  
  
  Ultimately, attempting to collect all the "virtual" attributes associated with a class may be a bit of a pipe dream anyhow. Techniques like those outlined here may address slots and properties, but some attributes are entirely dynamic, with no physical basis at all: those computed on fetch by generic method such as \_\_getattr\_\_ are not data in the classic sense. Tools that attempt to display data in a wildly dynamic language Python must come with the caveat that some data is ethereal at best!

We'll also make a minor extension to this section's code in the exercises at the end of this part of the book, to list
superclass names in parentheses at the start of instance displays, so keep it filed for future reference for now. To
better understand the last of the preceding two points, we need to wrap up this chapter and move on to the next and last
in this part of the book.

# Other Design-Related Topic
In this chapter, we've studied inheritance, composition, delegation, multiple inheritance, bound methods, and factories -- all common patterns used to combine classes in Python programs. We've really only scratched the surface here in the design patterns domain, though. Elsewhere in this book you'll find coverage of other design-related topics, such as:
- Abstract superclasses (Chapter 29)
- Decorators (Chapter 32 and Chapter 39)
- Type subclasses (Chapter 32)
- Static and class methods (Chapter 32)
- Managed attributes (Chapter 32 and Chapter 38)
- Metaclasses (Chapter 32 and Chapter 40)

For more details on design patterns, though, we'll delegate to other resources on OOP at large. Although patterns are important in OOP work and are often more natural in Python than other languages, they are not specific to Python itself, and a subject that's often best acquired by experience.
