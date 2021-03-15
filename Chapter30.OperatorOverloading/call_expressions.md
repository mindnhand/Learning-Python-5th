# Call Expressions: \_\_call\_\_
On to our next overloading method: the \_\_call\_\_ method is called when your instance is called. No, this 
isn't a circular definition—if defined, Python runs a \_\_call\_\_ method  for function call expressions 
applied to your instances, passing along whatever positional or keyword arguments were sent. This allows 
instances to conform to a functionbased API:
> ```python
> >>> class Callee:
>         def __call__(self, *pargs, **kargs):  					 # Intercept instance calls
> 		      print('Called:', pargs, kargs) 						 # Accept arbitrary arguments
> >>> C = Callee()
> >>> C(1, 2, 3) 													 # C is a callable object
> Called: (1, 2, 3) {}
> >>> C(1, 2, 3, x=4, y=5)
> Called: (1, 2, 3) {'y': 5, 'x': 4}
> ```
More formally, all the argument-passing modes we explored in Chapter 18 are supported by the \_\_call\_\_ 
method—whatever is passed to the instance is passed to this  method, along with the usual implied instance 
argument. For example, the method definitions:
> ```python
> class C:
> 	  def __call__(self, a, b, c=5, d=6): ... 						# Normals and defaults
> 
> class C:
>     def __call__(self, *pargs, **kargs): ... 					    # Collect arbitrary arguments
> 
> class C:
>     def __call__(self, *pargs, d=6, **kargs): ... 			    # 3.X keyword-only argument
> ```

all match all the following instance calls:
> ```python
> X = C()
> X(1, 2) 															# Omit defaults
> X(1, 2, 3, 4) 													# Positionals
> X(a=1, b=2, d=4) 													# Keywords
> X(*[1, 2], **dict(c=3, d=4)) 										# Unpack arbitrary arguments
> X(1, *(2,), c=3, **dict(d=4)) 									# Mixed modes
> ```

See Chapter 18 for a refresher on function arguments. The net effect is that classes and instances with a
\_\_call\_\_ support the exact same argument syntax and semantics as normal functions and methods.
Intercepting call expression like this allows class instances to emulate the look and feel of things like functions, 
but also retain state information for use during calls. We saw an example similar to the following while exploring 
scopes in Chapter 17, but you should now be familiar enough with operator overloading to understand this pattern better:
> ```python
> >>> class Prod:
>         def __init__(self, value): 								# Accept just one argument
> 		      self.value = value
> 		  def __call__(self, other):
> 			  return self.value * other
> >>> x = Prod(2) 													# "Remembers" 2 in state
> >>> x(3) 															# 3 (passed) * 2 (state)
> 6
> >>> x(4)
> 8
> ```

In this example, the \_\_call\_\_ may seem a bit gratuitous at first glance. A simple method can provide similar utility:
> ```python
> >>> class Prod:
> 	      def __init__(self, value):
> 			  self.value = value
> 		  def comp(self, other):
> 			  return self.value * other
> 
> >>> x = Prod(3)
> >>> x.comp(3)
> 9
> >>> x.comp(4)
> 12
> ```

However, \_\_call\_\_ can become more useful when interfacing with APIs (i.e., libraries) that expect functions—it allows 
us to code objects that conform to an expected function call interface, but also retain state information, and other 
class assets such as inheritance.
In fact, it may be the third most commonly used operator overloading method, behind the \_\_init\_\_ constructor and 
the \_\_str\_\_ and \_\_repr\_\_ display-format alternatives.

## Function Interfaces and Callback-Based Code
As an example, the tkinter GUI toolkit (named Tkinter in Python 2.X) allows you to register functions as event 
handlers (a.k.a. callbacks)—when events occur, tkinter calls  the registered objects. If you want an event handler
to retain state between events, you can register either a class's bound method, or an instance that conforms to 
the expected interface with \_\_call\_\_.
In the prior section's code, for example, both x.comp from the second example and x from the first can pass as 
function-like objects this way. Chapter 17's closure functions with state in enclosing scopes can achieve similar 
effects, but don't provide as much support for multiple operations or customization.
I'll have more to say about bound methods in the next chapter, but for now, here's a hypothetical example of \_\_call\_\_ 
applied to the GUI domain. The following class defines an object that supports a function-call interface, 
but also has state information that remembers the color a button should change to when it is later pressed:
> ```python
> class Callback:
>     def __init__(self, color): 								# Function + state information
>  	      self.color = color
>     def __call__(self): 										# Support calls with no arguments
>         print('turn', self.color)
> ```

Now, in the context of a GUI, we can register instances of this class as event handlers for buttons, even though 
the GUI expects to be able to invoke event handlers as simple functions with no arguments:
> ```python
> # Handlers
> cb1 = Callback('blue') 										# Remember blue
> cb2 = Callback('green') 										# Remember green
> B1 = Button(command=cb1) 										# Register handlers
> B2 = Button(command=cb2)
> ```

When the button is later pressed, the instance object is called as a simple function with no arguments, exactly 
like in the following calls. Because it retains state as instance attributes, though, it remembers what to do—it 
becomes a stateful function object:
> ```python
> # Events
> cb1() 														# Prints 'turn blue'
> cb2() 														# Prints 'turn green'
> ```

In fact, many consider such classes to be the best way to retain state information in the Python language 
(per generally accepted Pythonic principles, at least). With OOP, the state remembered is made explicit 
with attribute assignments. This is different than other state retention techniques (e.g., global variables, 
enclosing function scope references, and default mutable arguments), which rely on more limited or implicit behavior.
Moreover, the added structure and customization in classes goes beyond state retention.
On the other hand, tools such as closure functions are useful in basic state retention roles too, and 3.X's nonlocal 
statement makes enclosing scopes a viable alternative in more programs. We'll revisit such tradeoffs when we start 
coding substantial decorators in Chapter 39, but here's a quick closure equivalent:
> ```python
> def callback(color): 											# Enclosing scope versus attrs
>     def oncall():
>         print('turn', color)
>     return oncall
> 
> cb3 = callback('yellow') 										# Handler to be registered
> cb3() 														# On event: prints 'turn yellow'
> ```

Before we move on, there are two other ways that Python programmers sometimes tie information to a callback 
function like this. One option is to use default arguments in lambda functions:
> ```python
> cb4 = (lambda color='red': 'turn ' + color) 					# Defaults retain state too
> print(cb4())
> ```

The other is to use bound methods of a class— a bit of a preview, but simple enough to  introduce here. A bound 
method object is a kind of object that remembers both the self instance and the referenced function. This object 
may therefore be called later as a simple function without an instance:
> ```python
> class Callback:
> 	  def __init__(self, color): 								# Class with state information
> 	  	  self.color = color
>     def changeColor(self):									# A normal named method
>         print('turn', self.color)
> 
> cb1 = Callback('blue')
> cb2 = Callback('yellow')
> B1 = Button(command=cb1.changeColor) 							# Bound method: reference, don't call
> B2 = Button(command=cb2.changeColor) 							# Remembers function + self pair
> ```

In this case, when this button is later pressed it's as if the GUI does this, which invokes the instance's
changeColor method to process the object's state information, instead of the instance itself:
> ```python
> cb1 = Callback('blue')
> obj = cb1.changeColor 										# Registered event handler
> obj() 														# On event prints 'turn blue'
> ```

Note that a lambda is not required here, because a bound method reference by itself already defers a call 
until later. This technique is simpler, but perhaps less general than overloading calls with \_\_call\_\_. 
Again, watch for more about bound methods in the next chapter.
You'll also see another \_\_call\_\_ example in Chapter 32, where we will use it to implement something known 
as a function decorator—a callable object often used to add a  layer of logic on top of an embedded function. 
Because \_\_call\_\_ allows us to attach state information to a callable object, it's a natural implementation 
technique for a function that must remember to call another function when called itself. For more \_\_call\_\_ 
examples, see the state retention preview examples in Chapter 17, and the more advanced decorators and metaclasses
of Chapter 39 and Chapter 40.
