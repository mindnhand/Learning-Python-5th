# OOP and Delegation: “Wrapper” Proxy Objects
Beside inheritance and composition, object-oriented programmers often speak of delegation, which usually 
implies controller objects that embed other objects to which they pass off operation requests. The 
controllers can take care of administrative activities, such as logging or validating accesses, adding 
extra steps to interface components, or monitoring active instances.

In a sense, delegation is a special form of composition, with a single embedded object managed by a wrapper 
(sometimes called a proxy) class that retains most or all of the embedded object's interface. The notion 
of proxies sometimes applies to other mechanisms too, such as function calls; in delegation, we're concerned 
with proxies for all of an object's behavior, including method calls and other operations.

This concept was introduced by example in Chapter 28, and in Python is often implemented with the \_\_getattr\_\_ 
method hook we studied in Chapter 30. Because this operator overloading method intercepts accesses to nonexistent 
attributes, a wrapper class can use \_\_getattr\_\_ to route arbitrary accesses to a wrapped object. Because this
method allows attribute requests to be routed generically, the wrapper class retains the interface of the wrapped 
object and may add additional operations of its own.

By way of review, consider the file trace.py (which runs the same in 2.X and 3.X):
> ```python
> class Wrapper:
>     def __init__(self, object):
>         self.wrapped = object 				# Save object
>     def __getattr__(self, attrname):
>         print('Trace: ' + attrname) 			# Trace fetch
>         return getattr(self.wrapped, attrname)    # Delegate fetch
> ```
Recall from Chapter 30 that \_\_getattr\_\_ gets the attribute name as a string. This code makes use of the getattr 
built-in function to fetch an attribute from the wrapped object by name string—getattr(X,N) is like X.N, except 
that N is an expression that evaluates to a string at runtime, not a variable. In fact, getattr(X,N) is similar
to X.\_\_dict\_\_[N], but the former also performs an inheritance search, like X.N, while the latter does not (see
Chapter 22 and Chapter 29 for more on the \_\_dict\_\_ attribute).

You can use the approach of this module's wrapper class to manage access to any object with attributes—lists, 
dictionaries, and even classes and instances. Here, the Wrapper class simply prints a trace message on each
attribute access and delegates the attribute request to the embedded wrapped object:
> ```python
> >>> from trace import Wrapper
> >>> x = Wrapper([1, 2, 3]) # Wrap a list
> >>> x.append(4) # Delegate to list method
> Trace: append
> >>> x.wrapped # Print my member
> [1, 2, 3, 4]
> >>> x = Wrapper({'a': 1, 'b': 2}) # Wrap a dictionary
> >>> list(x.keys()) # Delegate to dictionary method
> Trace: keys
> ['a', 'b']
> ```

The net effect is to augment the entire interface of the wrapped object, with additional code in the Wrapper class.
We can use this to log our method calls, route method calls to extra or custom logic, adapt a class to a new interface,
and so on.

We'll revive the notions of wrapped objects and delegated operations as one way to extend built-in types in the next
chapter. If you are interested in the delegation design pattern, also watch for the discussions in Chapter 32 and
Chapter 39 of function decorators, a strongly related concept designed to augment a specific function or method
call rather than the entire interface of an object, and class decorators, which serve as a way to automatically add
such delegation-based wrappers to all instances of a class.

> **Version skew note:** As we saw by example in Chapter 28, delegation of object interfaces by general proxies has
> changed substantially in 3.X when wrapped objects implement operator overloading methods. Technically, this is
> a new-style class difference, and can appear in 2.X code too if it enables this option; per the next chapter,
> it's mandatory in 3.X and thus often considered a 3.X change.
> 
> In Python 2.X's default classes, operator overloading methods run by built-in operations are routed through
> generic attribute interception methods like \_\_getattr\_\_. Printing a wrapped object directly, for example, calls
> this method for \_\_repr\_\_ or \_\_str\_\_, which then passes the call on to the wrapped object. This pattern holds for
> \_\_iter\_\_, \_\_add\_\_, and the other operator methods of the prior chapter.
> 
> In Python 3.X, this no longer happens: printing does not trigger \_\_getattr\_\_ (or its \_\_getattribute\_\_ cousin
> we'll study in the next chapter) and a default display is used instead. In 3.X, new-style classes look up methods
> invoked implicitly by built-in operations in classes and skip the normal instance lookup entirely. Explicit name
> attribute fetches are routed to \_\_getattr\_\_ the same way in both 2.X and 3.X, but built-in operation method lookup
> differs in ways that may impact some delegation- based tools.
> 
> We'll return to this issue in the next chapter as a new-style class change, and see it live in Chapter 38 and Chapter 39,
> in the context of managed attributes and decorators. For now, keep in mind that for delegation coding patterns, you may
> need to redefine operator overloading methods in wrapper classes (either by hand, by tools, or by superclasses) if
> they are used by embedded objects and you want them to be intercepted in new-style classes.
