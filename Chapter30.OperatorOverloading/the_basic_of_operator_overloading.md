# The Basics

Really "operator overloading" simply means intercepting built-in operations in a class's
methods—Python automatically invokes your methods when instances of the class
appear in built-in operations, and your method's return value becomes the result of the
corresponding operation. Here's a review of the key ideas behind overloading:
* Operator overloading lets classes intercept normal Python operations.
* Classes can overload all Python expression operators.
* Classes can also overload built-in operations such as printing, function calls, attribute
  access, etc.
* Overloading makes class instances act more like built-in types.
* Overloading is implemented by providing specially named methods in a class.

In other words, when certain specially named methods are provided in a class, Python
automatically calls them when instances of the class appear in their associated expressions.
Your class provides the behavior of the corresponding operation for instance
objects created from it.

As we've learned, operator overloading methods are never required and generally don't
have defaults (apart from a handful that some classes get from object); if you don't
code or inherit one, it just means that your class does not support the corresponding
operation. When used, though, these methods allow classes to emulate the interfaces
of built-in objects, and so appear more consistent.


