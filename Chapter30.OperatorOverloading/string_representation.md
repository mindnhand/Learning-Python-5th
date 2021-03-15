# String Representation: __repr__ and __str__

Our next methods deal with display formats—a topic wee've already explored in prior chapters, but will 
summarize and formalize here. As a review, the following code exercises the __init__ constructor and the 
__add__ overload method, both of which we've already seen (+ is an in-place operation here, just to show 
that it can be; per Chapter 27, a named method may be preferred). As we've learned, the default display of
instance objects for a class like this is neither generally useful nor aesthetically pretty:
> ```python
> >>> class adder:
>         def __init__(self, value=0):
>             self.data = value 						# Initialize data
>         def __add__(self, other):
>             self.data += other 						# Add other in place (bad form?)
> >>> x = adder() 										# Default displays
> >>> print(x)
> <__main__.adder object at 0x00000000029736D8>
> >>> x
> <__main__.adder object at 0x00000000029736D8>
> ```
But coding or inheriting string representation methods allows us to customize the display—
as in the following, which defines a __repr__ method in a subclass that returns a string representation 
for its instances.
> ```python
> >>> class addrepr(adder): 							# Inherit __init__, __add__ 
>         def __repr__(self): 							# Add string representation 
>             return 'addrepr(%s)' % self.data 			# Convert to as-code string 
> >>> x = addrepr(2) 									# Runs __init__ 
> >>> x + 1 											# Runs __add__ (x.add() better?)
> >>> x 												# Runs __repr__
> addrepr(3)
> >>> print(x) 											# Runs __repr__
> addrepr(3)
> >>> str(x), repr(x) 									# Runs __repr__ for both
> ('addrepr(3)', 'addrepr(3)')
> ```
If defined, __repr__ (or its close relative, __str__) is called automatically when class
instances are printed or converted to strings. These methods allow you to define a better
display format for your objects than the default instance display. Here, __repr__ uses
basic string formatting to convert the managed self.data object to a more humanfriendly
string for display.

## Why Two Display Methods?
So far, what we've seen is largely review. But while these methods are generally straightforward
to use, their roles and behavior have some subtle implications both for design and coding. In particular, 
Python provides two display methods to support alternative displays for different audiences:
- __str__ is tried first for the print operation and the str built-in function (the internal equivalent 
  of which print runs). It generally should return a user-friendly display.
- __repr__ is used in all other contexts: for interactive echoes, the repr function, and nested appearances,
  as well as by print and str if no __str__ is present. It should generally return an as-code string that 
  could be used to re-create the object, or a detailed display for developers.

That is, __repr__ is used everywhere, except by print and str when a __str__ is defined. This means you can 
code a __repr__ to define a single display format used everywhere, and may code a __str__ to either support 
print and str exclusively, or to provide an alternative display for them.

As noted in Chapter 28, general tools may also prefer __str__ to leave other classes the option of adding an 
alternative __repr__ display for use in other contexts, as long as print and str displays suffice for the tool. 
Conversely, a general tool that codes a __repr__ still leaves clients the option of adding alternative displays 
with a __str__ for print and str. In other words, if you code either, the other is available for an additional
display. In cases where the choice isn’t clear, __str__ is generally preferred for larger  user-friendly displays, 
and __repr__ for lower-level or as-code displays and all-inclusive roles.

Let's write some code to illustrate these two methods' distinctions in more concrete terms. The prior example 
in this section showed how __repr__ is used as the fallback option in many contexts. However, while printing 
falls back on __repr__ if no __str__ is defined, the inverse is not true—other contexts, such as interactive echoes,
use __repr__ only and don’t try __str__ at all:
> ```python
> >>> class addstr(adder):
>         def __str__(self):      							# __str__ but no __repr__
>             return '[Value: %s]' % self.data 				# Convert to nice string
> >>> x = addstr(3)
> >>> x + 1
> >>> x 													# Default __repr__
> <__main__.addstr object at 0x00000000029738D0>
> >>> print(x) 												# Runs __str__
> [Value: 4]
> >>> str(x), repr(x)
> ('[Value: 4]', '<__main__.addstr object at 0x00000000029738D0>')
> ```
Because of this, __repr__ may be best if you want a single display for all contexts. By  defining both methods, 
though, you can support different displays in different contexts —for example, an end-user display with __str__, 
and a low-level display for programmers to use during development with __repr__. In effect, __str__ simply overrides
__repr__ for more user-friendly display contexts:
> ```python
> >>> class addboth(adder):
> 	      def __str__(self):
>             return '[Value: %s]' % self.data 				# User-friendly string
>         def __repr__(self):
>             return 'addboth(%s)' % self.data 				# As-code string
> >>> x = addboth(4)
> >>> x + 1
> >>> x # Runs __repr__
> addboth(5)
> >>> print(x) # Runs __str__
> [Value: 5]
> >>> str(x), repr(x)
> ('[Value: 5]', 'addboth(5)')
> ```

## Display Usage Notes
Though generally simple to use, I should mention three usage notes regarding these methods here. 
First, keep in mind that __str__ and __repr__ must both return strings; other result types are not converted and 
raise errors, so be sure to run them through a to-string converter (e.g., str or %) if needed.
Second, depending on a container’s string-conversion logic, the user-friendly display  of __str__ might only 
apply when objects appear at the top level of a print operation; objects nested in larger objects might still 
print with their __repr__ or its default. The following illustrates both of these points:
> ```python
> >>> class Printer:
> 	      def __init__(self, val):
>             self.val = val
> 		  def __str__(self): 							# Used for instance itself
>             return str(self.val) 						# Convert to a string result
> >>> objs = [Printer(2), Printer(3)]
> >>> for x in objs: print(x) 							# __str__ run when instance printed
> # But not when instance is in a list!
> 2
> 3
> >>> print(objs)
> [<__main__.Printer object at 0x000000000297AB38>, <__main__.Printer obj...etc...>]
> >>> objs
> [<__main__.Printer object at 0x000000000297AB38>, <__main__.Printer obj...etc...>]
> ```
To ensure that a custom display is run in all contexts regardless of the container, code  __repr__, not __str__; 
the former is run in all cases if the latter doesn't apply, including nested appearances:
> ```python
> >>> class Printer:
>         def __init__(self, val):
>             self.val = val
>         def __repr__(self): 							# __repr__ used by print if no __str__
>             return str(self.val) 						# __repr__ used if echoed or nested
> >>> objs = [Printer(2), Printer(3)]
> >>> for x in objs: print(x) 							# No __str__: runs __repr__
> 2
> 3
> >>> print(objs) 										# Runs __repr__, not ___str__
> [2, 3]
> >>> objs
> [2, 3]
> ```
Third, and perhaps most subtle, the display methods also have the potential to trigger infinite recursion 
loops in rare contexts—because some objects’ dsplays include displays  of other objects, it's not impossible 
that a display may trigger a display of an object being displayed, and thus loop. This is rare and obscure 
enough to skip here, but watch for an example of this looping potential to appear for these methods in a 
note near the end of the next chapter in its listinherited.py example's class, where __repr__ can loop.

In practice, __str__, and its more inclusive relative __repr__, seem to be the second most commonly used 
operator overloading methods in Python scripts, behind  __init__. Anytime you can print an object and see 
a custom display, one of these two tools is probably in use. For additional examples of these tools at work 
and the design tradeoffs they imply, see Chapter 28's case study and Chapter 31's class lister mix-ins,
as well as their role in Chapter 35's exception classes, where __str__ is required over  __repr__.
