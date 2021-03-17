# Python and OOP
Let's begin with a review—Pythonn's implementation of OOP can be summarized by three ideas:
- Inheritance: Inheritance is based on attribute lookup in Python (in X.name expressions).
- Polymorphism: In X.method, the meaning of method depends on the type (class) of subject object X.
- Encapsulation: Methods and operators implement behavior, though data hiding is a convention by default.
By now, you should have a good feel for what inheritance is all about in Python. We've also talked about Python's 
polymorphism a few times already; it flows from Python's lack of type declarations. Because attributes are always 
resolved at runtime, objects that implement the same interfaces are automatically interchangeable; clients don't 
need to know what sorts of objects are implementing the methods they call.

Encapsulation means packaging in Python -- that is, hiding implementation details behind an objectt's interface. 
It does not mean enforced privacy, though that can be implemented with code, as we'll see in Chapter 39. 
Encapsulation is available and useful in Python nonetheless: it allows the implementation of an object's interface 
to be changed without impacting the users of that object.

## Polymorphism Means Interfaces, Not Call Signatures
Some OOP languages also define polymorphism to mean overloading functions based on the type signatures of their 
arguments -- the number passed and/or their types. Because  there are no type declarations in Python, this concept
doesn't really apply; as we've seen, polymorphism in Python is based on object interfaces, not types. If you're
pining for your C++ days, you can try to overload methods by their argument lists, like this:
> ```python
> class C:
>     def meth(self, x):
>         ...
>     def meth(self, x, y, z):
>         ...
> ```
This code will run, but because the def simply assigns an object to a name in the class's scope, the last definition 
of the method function is the only one that will be retained. Put another way, it's just as if you say X = 1 and 
then X = 2; X will be 2. Hence, there can be only one definition of a method name.
If they are truly required, you can always code type-based selections using the typetesting ideas we met in Chapter 4 
and Chapter 9, or the argument list tools introduced in Chapter 18:
> ```python
> class C:
>     def meth(self, *args):
>         if len(args) == 1: 				# Branch on number arguments
>             ...
>         elif type(arg[0]) == int: 		# Branch on argument types (or isinstance())
>             ...
```
You normally shouldn't do this, though -- it's not the Python way. As described in Chapter 16, you should write your 
code to expect only an object interface, not a specific data type. That way, it will be useful for a broader category 
of types and applications, both now and in the future:
> ```python
> class C:
>     def meth(self, x):
>         x.operation() 					# Assume x does the right thing
> ```
It's also generally considered better to use distinct method names for distinct operations, rather than relying on 
call signatures (no matter what language you code in). Although Python's object model is straightforward, much of 
the art in OOP is in the way we combine classes to achieve a program's goals. The next section begins a tour of 
some of the ways larger programs use classes to their advantage.

## OOP and Inheritance: "Is-a" Relationships
We've explored the mechanics of inheritance in depth already, but I'd now like to show you an example of how it 
can be used to model real-world relationships. From a programmer's point of view, inheritance is kicked off by 
attribute qualifications, which trigger searches for names in instances, their classes, and then any superclasses. 
From a designer's point of view, inheritance is a way to specify set membership: a class defines a set of properties
that may be inherited and customized by more specific sets (i.e., subclasses).
To illustrate, let's put that pizza-making robot we talked about at the start of this part of the book to work. 
Suppose we've decided to explore alternative career paths and open a pizza restaurant (not bad, as career paths go). 
One of the first things we'll need to do is hire employees to serve customers, prepare the food, and so on. Being 
engineers at heart, we've decided to build a robot to make the pizzas; but being politically and cybernetically 
correct, we've also decided to make our robot a full-fledged employee with a salary.
