# Pseudoprivate Class Attributes
Besides larger structuring goals, class designs often must address name usage too. In Chapter 28's case study, for example, we noted that methods defined within a general tool class might be modified by subclasses if exposed, and noted the tradeoffs of this policy—while it supports method customization and direct calls, itt's also open to accidental replacements.

In Part V, we learned that every name assigned at the top level of a module file is exported. By default, the same holds for classes—data hiding is a convention, and  clients may fetch or change attributes in any class or instance to which they have a reference. In fact, attributes are all "public" and "virtual," in C++ terms; they're all accessible everywhere and are looked up dynamically at runtime.

That said, Python today does support the notion of name "mangling" (i.e., expansion) to localize some names in classes. Mangled names are sometimes misleadingly called "private attributes," but really this is just a way to localize a name to the class that created it -- name mangling does not prevent access by code outside the class.  This feature is mostly intended to avoid namespace collisions in instances, not to restrict access to names in general; mangled names are therefore better called "pseudoprivate" than "private."

Pseudoprivate names are an advanced and entirely optional feature, and you probably won't find them very useful until you start writing general tools or larger class hierarchies for use in multiprogrammer projects. In fact, they are not always used even when they probably should be -- more commonly, Python programmers code internal names with a single underscore (e.g., \_X), which is just an informal convention to let you know that a name shouldn't generally be changed (it means nothing to Python itself).

Because you may see this feature in other people's code, though, you need to be somewhat aware of it, even if you don't use it yourself. And once you learn its advantages and contexts of use, you may find this feature to be more useful in your own code than some programmers realize.

## Name Mangling Overview
Here's how name mangling works: within a class statement only, any names that start with two underscores but don't end with two underscores are automatically expanded to include the name of the enclosing class at their front. For instance, a name like \_\_X within a class named Spam is changed to \_Spam\_\_X automatically: the original name is prefixed with a single underscore and the enclosing class's name. Because the modified name contains the name of the enclosing class, it's generally unique; it won't clash with similar names created by other classes in a hierarchy.

Name mangling happens only for names that appear inside a class statement's code, and then only for names that begin with two leading underscores. It works for every name preceded with double underscores, though -- both class attributes (including method names) and instance attribute names assigned to self. For example, in a class named Spam, a method named \_\_meth is mangled to \_Spam\_\_meth, and an instance attribute reference self.\_\_X is transformed to self.\_Spam\_\_X.

Despite the mangling, as long as the class uses the double underscore version everywhere it refers to the name, all its references will still work. Because more than one class may add attributes to an instance, though, this mangling helps avoid clashes -- but we  need to move on to an example to see how.

## Why Use Pseudoprivate Attributes?
One of the main issues that the pseudoprivate attribute feature is meant to alleviate has to do with the way instance attributes are stored. In Python, all instance attributes wind up in the single instance object at the bottom of the class tree, and are shared by all class-level method functions the instance is passed into. This is different from the C++ model, where each class gets its own space for data members it defines.

Within a class's method in Python, whenever a method assigns to a self attribute (e.g., self.attr = value), it changes or creates an attribute in the instance (recall that inheritance searches happen only on reference, not on assignment). Because this is true even if multiple classes in a hierarchy assign to the same attribute, collisions are possible.

For example, suppose that when a programmer codes a class, it is assumed that the class owns the attribute name X in the instance. In this class's methods, the name is set, and later fetched:
> ```python
> class C1:
>     def meth1(self): self.X = 88 				# I assume X is mine
>     def meth2(self): print(self.X)
> ```

Suppose further that another programmer, working in isolation, makes the same assumption in another class:
> ```python
> class C2:
>     def metha(self): self.X = 99 				# Me too
>     def methb(self): print(self.X)
> ```

Both of these classes work by themselves. The problem arises if the two classes are ever mixed together in the same class tree:
> ```python
> class C3(C1, C2): ...
> I = C3() 									# Only 1 X in I!
> ```

Now, the value that each class gets back when it says self.X will depend on which class assigned it last.
Because all assignments to self.X refer to the same single instance, there is only one X attribute -- I.X -- no matter how many classes use that attribute name.

This isn't a problem if it's expected, and indeed, this is how classes communicate -- the instance is shared memory.
To guarantee that an attribute belongs to the class that uses it, though, prefix the name with double underscores everywhere it is used in the class, as in this 2.X/3.X file, pseudoprivate.py:
> ```python
> class C1:
>     def meth1(self): self.__X = 88 		# Now X is mine
>     def meth2(self): print(self.__X) 		# Becomes _C1__X in I
> 
> class C2:
>     def metha(self): self.__X = 99 		# Me too
>     def methb(self): print(self.__X) 		# Becomes _C2__X in I
> 
> class C3(C1, C2): pass
> I = C3() 									# Two X names in I
> I.meth1(); I.metha()
> print(I.__dict__)
> I.meth2(); I.methb()
> ```

When thus prefixed, the X attributes will be expanded to include the names of their classes before being added to the instance. If you run a dir call on I or inspect its namespace dictionary after the attributes have been assigned, you'll see the expanded names, \_C1\_\_X and \_C2\_\_X, but not X. Because the expansion makes the names more unique within the instance, the class coders can be fairly safe in assuming that they truly own any names that they prefix with two underscores:
> ```python
> % python pseudoprivate.py
> {'_C2__X': 99, '_C1__X': 88}
> 88
> 99
> ```

This trick can avoid potential name collisions in the instance, but note that it does not amount to true privacy.
If you know the name of the enclosing class, you can still access either of these attributes anywhere you have a reference to the instance by using the fully expanded name (e.g., I.\_C1\_\_X = 77). Moreover, names could still collide if unknowing programmers use the expanded naming pattern explicitly (unlikely, but not impossible). On the other hand, this feature makes it less likely that you will accidentally step on a class's names.

Pseudoprivate attributes are also useful in larger frameworks or tools, both to avoid introducing new method names that might accidentally hide definitions elsewhere in the class tree and to reduce the chance of internal methods being replaced by names defined lower in the tree. If a method is intended for use only within a class that may be mixed into other classes, the double underscore prefix virtually ensures that the method won't interfere with other names in the tree, especially in multiple-inheritance scenarios:
> ```python
> class Super:
>     def method(self): ... 				# A real application method
> 
> class Tool:
>     def __method(self): ... 				# Becomes _Tool__method
>     def other(self): self.__method() 		# Use my internal method
> 
> class Sub1(Tool, Super): ...
> 	  def actions(self): self.method() 		# Runs Super.method as expected
> 
> class Sub2(Tool):
>     def __init__(self): self.method = 99  # Doesn't break Tool.__method
> ```

We met multiple inheritance briefly in Chapter 26 and will explore it in more detail later in this chapter. Recall that superclasses are searched according to their left-to-right order in class header lines. Here, this means Sub1 prefers Tool attributes to those in Super. Although in this example we could force Python to pick the application class's methods first by switching the order of the superclasses listed in the Sub1 class header, pseudoprivate attributes resolve the issue altogether. Pseudoprivate names also prevent subclasses from accidentally redefining the internal method's names, as in Sub2.

Again, I should note that this feature tends to be of use primarily for larger, multiprogrammer projects, and then only for selected names. Don't be tempted to clutter your code unnecessarily; only use this feature for names that truly need to be controlled by a single class. Although useful in some general class-based tools, for simpler programs, it's probably overkill.

For more examples that make use of the \_\_X naming feature, see the lister.py mix-in classes introduced later in this chapter in the multiple inheritance section, as well as the discussion of Private class decorators in Chapter 39.

If you care about privacy in general, you might want to review the emulation of private instance attributes sketched in the section "Attribute Access: \_\_getattr\_\_ and \_\_setattr\_\_" on page 909 in Chapter 30, and watch for the more complete Private class decorator we'll build with delegation in Chapter 39. Although it's possible to emulate true access controls in Python classes, this is rarely done in practice, even for large systems.
