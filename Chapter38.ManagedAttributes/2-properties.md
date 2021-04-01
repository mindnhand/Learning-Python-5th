# Properties
The property protocol allows us to route a specific attribute's get, set, and delete operations to functions or methods we provide, enabling us to insert code to be run automatically on attribute access, intercept attribute deletions, and provide documentation for the attributes if desired.

Properties are created with the property built-in and are assigned to class attributes, just like method functions. Accordingly, they are inherited by subclasses and instances, like any other class attributes. Their access-interception functions are provided with the self instance argument, which grants access to state information and class attributes available on the subject instance.

A property manages a single, specific attribute; although it can't catch all attribute accesses generically, it allows us to control both fetch and assignment accesses and enables us to change an attribute from simple data to a computation freely, without breaking existing code. As we'll see, properties are strongly related to descriptors; in fact, they are essentially a restricted form of them.

## The Basics
A property is created by assigning the result of a built-in function to a class attribute:
> ```python
> attribute = property(fget, fset, fdel, doc)
> ```

None of this built-in's arguments are required, and all default to None if not passed. For the first three, this None means that the corresponding operation is not supported, and attempting it will raise an AttributeError exception automatically. When these arguments are used, we pass fget a function for intercepting attribute fetches, fset a function for assignments, and fdel a function for attribute deletions.

Technically, all three of these arguments accept any callable, including a class's method, having a first argument to receive the instance being qualified. When later invoked, the fget function returns the computed attribute value, fset and fdel return nothing (really, None), and all three may raise exceptions to reject access requests. The doc argument receives a documentation string for the attribute, if desired; otherwise, the property copies the docstring of the fget function, which as usual defaults to None.

This built-in property call returns a property object, which we assign to the name of the attribute to be managed in the class scope, where it will be inherited by every instance.

## A First Example
To demonstrate how this translates to working code, the following class uses a property to trace access to an attribute named name; the actual stored data is named \_name so it does not clash with the property (if you're working along with the book examples package, some filenames in this chapter are implied by the command-lines that run them following their listings):
> 
> > ```python
> > class Person: 			# Add (object) in 2.X
> >     def __init__(self, name):
> >         self._name = name
> >     def getName(self):
> >         print('fetch...')
> >         return self._name
> >     def setName(self, value):
> >         print('change...')
> >         self._name = value
> >     def delName(self):
> >         print('remove...')
> >         del self._name
> >     name = property(getName, setName, delName, "name property docs")
> > 
> > bob = Person('Bob Smith') 		# bob has a managed attribute
> > print(bob.name) 					# Runs getName
> > bob.name = 'Robert Smith' 		# Runs setName
> > print(bob.name)
> > del bob.name 						# Runs delName
> > print('-'*20)
> > sue = Person('Sue Jones') 		# sue inherits property too
> > print(sue.name)
> > print(Person.name.__doc__) 		# Or help(Person.name)
> > ```
> 
> Properties are available in both 2.X and 3.X, but they require new-style object derivation in 2.X to work correctly for assignments -- add object as a superclass here to run this in 2.X. You can list the superclass in 3.X too, but it's implied and not required, and is sometimes omitted in this book to reduce clutter.
> 
> This particular property doesn't do much -- it simply intercepts and traces an attribute -- but it serves to demonstrate the protocol. When this code is run, two instances inherit the property, just as they would any other attribute attached to their class. However, their attribute accesses are caught:
> 
> > ```powershell
> > c:\code> py -3 prop-person.py
> > fetch...
> > Bob Smith
> > change...
> > fetch...
> > Robert Smith
> > remove...
> > --------------------
> > fetch...
> > Sue Jones
> > name property docs
> > ```
> 

Like all class attributes, properties are inherited by both instances and lower subclasses. If we change our example as follows, for instance:
> ```python
> class Super:
>     ...the original Person class code...
>     name = property(getName, setName, delName, 'name property docs')
> class Person(Super):
>     pass 						# Properties are inherited (class attrs)
> 
> bob = Person('Bob Smith')
> ...rest unchanged...
> ```

the output is the same -- the Person subclass inherits the name property from Super, and the bob instance gets it from Person. In terms of inheritance, properties work the same as normal methods; because they have access to the self instance argument, they can access instance state information and methods irrespective of subclass depth, as the next section further demonstrates.

## Computed Attributes
The example in the prior section simply traces attribute accesses. Usually, though, properties do much more -- computing the value of an attribute dynamically when fetched, for example. The following example illustrates:
> 
> > ```python
> > class PropSquare:
> >     def __init__(self, start):
> >         self.value = start
> >     def getX(self): 				# On attr fetch
> >         return self.value ** 2
> >     def setX(self, value): 			# On attr assign
> >         self.value = value
> >     X = property(getX, setX) 		# No delete or docs
> > 
> > P = PropSquare(3) 					# Two instances of class with property
> > Q = PropSquare(32) 					# Each has different state information
> > print(P.X) 							# 3 ** 2
> > P.X = 4
> > print(P.X) 							# 4 ** 2
> > print(Q.X) 							# 32 ** 2 (1024)
> > ```
> 
> This class defines an attribute X that is accessed as though it were static data, but really runs code to compute its value when fetched. The effect is much like an implicit method call. When the code is run, the value is stored in the instance as state information, but each time we fetch it via the managed attribute, its value is automatically squared:
> 
> > ```powershell
> > c:\code> py -3 prop-computed.py
> > 9
> > 16
> > 1024
> > ```
>

Notice that we've made two different instances -- because property methods automatically receive a self argument, they have access to the state information stored in instances. In our case, this means the fetch computes the square of the subject instance's own data.

## Coding Properties with Decorators
Although we're saving additional details until the next chapter, we introduced function decorator basics earlier, in Chapter 32. Recall that the function decorator syntax:
> 
> > ```python
> > @decorator
> > def func(args): ...
> > ```
> 
> is automatically translated to this equivalent by Python, to rebind the function name to the result of the decorator callable:
> 
> > ```python
> > def func(args): ...
> > func = decorator(func)
> > ```
> 

Because of this mapping, it turns out that the property built-in can serve as a decorator, to define a function that will run automatically when an attribute is fetched:
> ```python
> class Person:
>     @property
>     def name(self): ... 			# Rebinds: name = property(name)
> ```

When run, the decorated method is automatically passed to the first argument of the property built-in. This is really just alternative syntax for creating a property and rebinding the attribute name manually, but may be seen as more explicit in this role:
> ```python
> class Person:
>     def name(self): ...
>         name = property(name)
> ```

### Setter and deleter decorators
As of Python 2.6 and 3.0, property objects also have getter, setter, and deleter methods that assign the corresponding property accessor methods and return a copy of the property itself. We can use these to specify components of properties by decorating normal methods too, though the getter component is usually filled in automatically by the act of creating the property itself:
> 
> > ```python
> > class Person:
> >     def __init__(self, name):
> >         self._name = name
> > 
> >     @property
> >     def name(self): 			# name = property(name)
> >         "name property docs"
> >         print('fetch...')
> >         return self._name
> > 
> >     @name.setter
> >     def name(self, value): 		# name = name.setter(name)
> >         print('change...')
> >         self._name = value
> > 
> >     @name.deleter
> >     def name(self): 			# name = name.deleter(name)
> >         print('remove...')
> >         del self._name
> > 
> > bob = Person('Bob Smith') 	# bob has a managed attribute
> > print(bob.name) 			# Runs name getter (name 1)
> > bob.name = 'Robert Smith' 	# Runs name setter (name 2)
> > print(bob.name)
> > del bob.name 				# Runs name deleter (name 3)
> > print('-'*20)
> > sue = Person('Sue Jones') 	# sue inherits property too
> > print(sue.name)
> > print(Person.name.__doc__) 	# Or help(Person.name)
> > ```
> 
> In fact, this code is equivalent to the first example in this section -- decoration is just an alternative way to code properties in this case. When it's run, the results are the same:
> 
> > ```powershell
> > c:\code> py -3 prop-person-deco.py
> > fetch...
> > Bob Smith
> > change...
> > fetch...
> > Robert Smith
> > remove...
> > --------------------
> > fetch...
> > Sue Jones
> > name property docs
> > ```
>

Compared to manual assignment of property results, in this case using decorators to code properties requires just three extra lines of code -- a seemingly negligible difference. As is so often the case with alternative tools, though, the choice between the two techniques is largely subjective.
