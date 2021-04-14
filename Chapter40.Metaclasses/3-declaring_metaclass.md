# Declaring Metaclasses
As we've just seen, classes are created by the type class by default. To tell Python to create a class with a custom metaclass instead, you simply need to declare a metaclass to intercept the normal instance creation call in a user-defined class. How you do so depends on which Python version you are using.

## Declaration in 3.X
In Python 3.X, list the desired `metaclass` as a keyword argument in the class header:
> ```python
> class Spam(metaclass=Meta): 			# 3.X version (only)
> ```

Inheritance superclasses can be listed in the header as well. In the following, for example, the new class Spam inherits from superclass Eggs, but is also an instance of and is created by metaclass Meta:
> ```python
> class Spam(Eggs, metaclass=Meta): 	# Normal supers OK: must list first
> ```

In this form, superclasses must be listed before the metaclass; in effect, the ordering rules used for keyword arguments in function calls apply here.

## Declaration in 2.X
We can get the same effect in Python 2.X, but we must specify the metaclass differently -- using a class attribute instead of a keyword argument:
> ```python
> class Spam(object): 					# 2.X version (only), object optional?
>     __metaclass__ = Meta
> class Spam(Eggs, object): 			# Normal supers OK: object suggested
>     __metaclass__ = Meta
> ```

Technically, some classes in 2.X do not have to derive from object explicitly to make use of metaclasses. The generalized metaclass dispatch mechanism was added at the same time as new-style classes, but is not itself bound to them. It does, however, produce them -- in the presence of a \_\_metaclass\_\_ declaration, 2.X makes the resulting class new-style automatically, adding object to its \_\_bases\_\_ sequence. In the absence of this declaration, 2.X simply uses the classic class creator as the metaclass default.

Because of this, some classes in 2.X require only the \_\_metaclass\_\_ attribute. On the other hand, notice that metaclasses imply that your class will be new-style in 2.X even without an explicit object. They'll behave somewhat differently as outlined in Chapter 32, and as we'll see ahead 2.X may require that they or their superclasses derive from object explicitly, because a new-style class cannot have only classic superclasses in this context. Given this, deriving from object doesn't hurt as a sort of warning about the class's nature, and may be required to avoid potential problems.

Also in 2.X, a module level \_\_metaclass\_\_ global variable is available to link all classes in the module to a metaclass. This is no longer supported in 3.X, as it was intended as a temporary measure to make it easier to default to new-style classes without deriving every class from object. Python 3.X also ignores the 2.X class attribute, and the 3.X keyword form is a syntax error in 2.X, so there is no simple portability route. Apart from differing syntax, though, metaclass declaration in 2.X and 3.X has the same effect, which we turn to next.

## Metaclass Dispatch in Both 3.X and 2.X
When a specific metaclass is declared per the prior sections' syntax, the call to create the class object run at the end of the class statement is modified to invoke the metaclass instead of the type default:
> ```python
> class = Meta(classname, superclasses, attributedict)
> ```

And because the metaclass is a subclass of type, the type class's \_\_call\_\_ delegates the calls to create and initialize the new class object to the metaclass, if it defines custom versions of these methods:
> ```python
> Meta.__new__(Meta, classname, superclasses, attributedict)
> Meta.__init__(class, classname, superclasses, attributedict)
> ```

To demonstrate, here's the prior section's example again, augmented with a 3.X metaclass specification:
> ```python
class Spam(Eggs, metaclass=Meta): 			# Inherits from Eggs, instance of Meta
    data = 1 					# Class data attribute
    def meth(self, arg): 		# Class method attribute
        return self.data + arg
> ```

At the end of this class statement, Python internally runs the following to create the class object -- again, a call you could make manually too, but automatically run by Python's class machinery:
> ```python
> Spam = Meta('Spam', (Eggs,), {'data': 1, 'meth': meth, '__module__': '__main__'})
> ```

If the metaclass defines its own versions of \_\_new\_\_ or \_\_init\_\_, they will be invoked in turn during this call by the inherited type class's \_\_call\_\_ method, to create and initialize the new class. The net effect is to automatically run methods the metaclass provides, as part of the class construction process. The next section shows how we might go about coding this final piece of the metaclass puzzle.

> **NOTE:**
> This chapter uses Python 3.X metaclass keyword argument syntax, not the 2.X class attribute. 2.X readers will need to translate, but version neutrality is not straightforward here -- 3.X doesn't recognize the attribute and 2.X doesn't allow keyword syntax -- and listing examples twice doesn't address portability (or chapter size!).
> 

