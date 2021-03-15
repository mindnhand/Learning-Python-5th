# Attribute Access: __getattr__ and __setattr__

In Python, classes can also intercept basic attribute access (a.k.a. qualification) when needed or useful. 
Specifically, for an object created from a class, the dot operator expression object.attribute can be 
implemented by your code too, for reference, assignment, and deletion contexts. We saw a limited example 
in this category in Chapter 28, but will review and expand on the topic here.

## Attribute Reference
The __getattr__ method intercepts attribute references. It's called with the attribute name as a string 
whenever you try to qualify an instance with an undefined (nonexistent) attribute name. It is not called 
if Python can find the attribute using its inheritance tree search procedure.

Because of its behavior, __getattr__ is useful as a hook for responding to attribute requests in a generic 
fashion. It's commonly used to delegate calls to embedded (or "wrapped") objects from a proxy controller 
object—of the sort introduced in Chapterr 28's introduction to delegation. This method can also be used to 
adapt classes to an interface, or add accessors for data attributes after the fact—logic in a method that
validates or computes an attribute after it's already being used with simple dot notation.

The basic mechanism underlying these goals is straightforward—the following class  catches attribute references,
computing the value for one dynamically, and triggering an error for others unsupported with the raise statement 
described earlier in this chapter for iterators (and fully covered in Part VII):
> ```python
> >>> class Empty:
>         def __getattr__(self, attrname): 						# On self.undefined
> 		      if attrname == 'age':
> 			      return 40
> 			  else:
> 			      raise AttributeError(attrname)
> >>> X = Empty()
> >>> X.age
> 40
> >>> X.name
> ...error text omitted...
> AttributeError: name
> ```

Here, the Empty class and its instance X have no real attributes of their own, so the access to X.age gets routed 
to the __getattr__ method; self is assigned the instance (X), and attrname is assigned the undefined attribute name 
string ('age'). The class makes age look like a real attribute by returning a real value as the result of the X.age 
qualification expression (40). In effect, age becomes a dynamically computed attribute—its value is  formed by running 
code, not fetching an object.

For attributes that the class doesn't know how to handle, __getattr__ raises the builtin AttributeError exception to 
tell Python that these are bona fide undefined names; asking for X.name triggers the error. You'll see __getattr__ again 
when we see delegation and properties at work in the next two chapters; let's move on to related tools here.

## Attribute Assignment and Deletion
In the same department, the __setattr__ intercepts all attribute assignments. If this method is defined or inherited, 
self.attr = value becomes self.__setattr__('attr', value). Like __getattr__, this allows your class to catch attribute 
changes, and validate or transform as desired.

This method is a bit trickier to use, though, because assigning to any self attributes within __setattr__ calls __setattr__ 
again, potentially causing an infinite recursion loop (and a fairly quick stack overflow exception!). In fact, this applies 
to all self attribute assignments anywhere in the class—all are routed to __setattr__, even those in other methods, 
and those to names other than that which may have triggered  __setattr__ in the first place. Remember, this catches 
all attribute assignments.

If you wish to use this method, you can avoid loops by coding instance attribute assignments as assignments to attribute 
dictionary keys. That is, use self.__dict__['name'] = x, not self.name = x; because you're not assigning to  __dict__ itself, 
this avoids the loop:
> ```python
> >>> class Accesscontrol:
>         def __setattr__(self, attr, value):
>             if attr == 'age':
> 			      self.__dict__[attr] = value + 10		 # Not self.name=val or setattr
> 			  else:
> 			      raise AttributeError(attr + ' not allowed')
> >>> X = Accesscontrol()
> >>> X.age = 40 							# Calls __setattr__
> >>> X.age
> 50
> >>> X.name = 'Bob'
> ...text omitted...
> AttributeError: name not allowed
> ```

If you change the __dict__ assignment in this to either of the following, it triggers the infinite recursion loop 
and exception—both dot notation and its setattr built-in functionn equivalent (the assignment analog of getattr) fail 
when age is assigned outside the class:
> ```python
> self.age = value + 10 								# Loops
> setattr(self, attr, value + 10) 						# Loops (attr is 'age')
> ```
An assignment to another name within the class triggers a recursive __setattr__ call too, though in this class ends 
less dramatically in the manual AttributeError exception:
> ```python
> self.other = 99 										# Recurs but doesn't loop: fails
> ```
It's also possible to avoid recursive loops in a class that uses __setattr__ by routing any attribute assignments to
a higher superclass with a call, instead of assigning keys in __dict__:
> ```python
> self.__dict__[attr] = value + 10 						# OK: doesn't loop
> object.__setattr__(self, attr, value + 10) 			# OK: doesn't loop (new-style only)
> ```
Because the object form requires use of new-style classes in 2.X, though, we'll postpone details on this form until 
Chapter 38's deeper look at attribute management at large.

A third attribute management method, __delattr__, is passed the attribute name string and invoked on all attribute 
deletions (i.e., del object.attr). Like __setattr__, it must avoid recursive loops by routing attribute deletions with 
the using class through  __dict__ or a superclass.

> **NOTE**
> As we'll learn in Chapter 32, attributes implemented with new-style class features such as slots and properties 
> are not physically stored in the instance's __dict__ namespace dictionary (and slots may even preclude its existence 
> entirely!). Because of this, code that wishes to support such attributes should code __setattr__ to assign with the
> object.__setattr__ scheme shown here, not by self.__dict__ indexing unless it's known that subject classes store all 
> their data in the instance itself. In Chapter 38 we'll also see that the new-style __getattribute__ has similar 
> requirements. This change is mandated in Python 3.X, but also applies to 2.X if new-style classes are used.

## Other Attribute Management Tools
These three attribute-access overloading methods allow you to control or specialize access to attributes in your objects.
They tend to play highly specialized roles, some of which we'll explore later in this book. For another example of 
__getattr__ at work, see Chapter 28's person-composite.py. And for future reference, keep in mind that there are
other ways to manage attribute access in Python:
- The __getattribute__ method intercepts all attribute fetches, not just those that are undefined, but when using it 
  you must be more cautious than with __getattr__ to avoid loops.
- The property built-in function allows us to associate methods with fetch and set operations on a specific class attribute.
- Descriptors provide a protocol for associating __get__ and __set__ methods of a class with accesses to a specific class attribute.
- Slots attributes are declared in classes but create implicit storage in each instance.

Because these are somewhat advanced tools not of interest to every Python programmer, we'll defer a look at properties 
until Chapter 32 and detailed coverage of all the attribute management techniques until Chapter 38.
