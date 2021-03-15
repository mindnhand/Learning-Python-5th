# Right-Side and In-Place Uses: __radd__ and __iadd__

Our next group of overloading methods extends the functionality of binary operator methods such as 
__add__ and __sub__ (called for + and -), which we've already seen.  As mentioned earlier, part of 
the reason there are so many operator overloading methods is because they come in multiple flavors—for e
very binary expression, we can implement a left, right, and in-place variant. Though defaults are also 
applied if you don't to code all three, your objects' roles dictate how many variants you'll need to code.

## Right-Side Addition
For instance, the __add__ methods coded so far technically do not support the use of instance objects 
on the right side of the + operator:
> ```python
> >>> class Adder:
>         def __init__(self, value=0):
> 		      self.data = value
> 		  def __add__(self, other):
> 		      return self.data + other
> >>> x = Adder(5)
> >>> x + 2
> 7
> >>> 2 + x
> TypeError: unsupported operand type(s) for +: 'int' and 'Adder'
> ```
To implement more general expressions, and hence support commutative-style operators, code the __radd__ method 
as well. Python calls __radd__ only when the object on the right side of the + is your class instance, but the 
object on the left is not an instance of your class. The __add__ method for the object on the left is called 
instead in all other cases (all of this section's five Commuter classes are coded in file commuter.py in the
book's examples, along with a self-test):
> ```python
> class Commuter1:
>     def __init__(self, val):
>         self.val = val
>     def __add__(self, other):
>         print('add', self.val, other)
> 		  return self.val + other
>     def __radd__(self, other):
>         print('radd', self.val, other)
>         return other + self.val
> ```
> ```python
> >>> from commuter import Commuter1
> >>> x = Commuter1(88)
> >>> y = Commuter1(99)
> >>> x + 1 									# __add__: instance + noninstance
> add 88 1
> 89
> >>> 1 + y 									# __radd__: noninstance + instance
> radd 99 1
> 100
> >>> x + y 									# __add__: instance + instance, triggers __radd__
> add 88 <commuter.Commuter1 object at 0x00000000029B39E8>
> radd 99 88
> 187
> ```
Notice how the order is reversed in __radd__: self is really on the right of the +, and other is on the left.
Also note that x and y are instances of the same class here; when instances of different classes appear mixed 
in an expression, Python prefers the class of the one on the left. When we add the two instances together, 
Python runs __add__, which in turn triggers __radd__ by simplifying the left operand.

## In-Place Addition
To also implement += in-place augmented addition, code either an __iadd__ or an __add__. The latter is used 
if the former is absent. In fact, the prior section's Commuter classes already support += for this reason—Python 
runs __add__ and assigns the result manually. The __iadd__ method, though, allows for more efficient in-place 
changes to be coded where applicable:
> ```python
> >>> class Number:
>         def __init__(self, val):
>             self.val = val
>         def __iadd__(self, other): 					# __iadd__ explicit: x += y
> 			  self.val += other 						# Usually returns self
> 			  return self
> >>> x = Number(5)
> >>> x += 1
> >>> x += 1
> >>> x.val
> 7
> ```

For mutable objects, this method can often specialize for quicker in-place changes:
> ```python
> >>> y = Number([1]) 									# In-place change faster than +
> >>> y += [2]
> >>> y += [3]
> >>> y.val
> [1, 2, 3]
> ```

The normal __add__ method is run as a fallback, but may not be able optimize in-place cases:
> ```python
> >>> class Number:
> 	      def __init__(self, val):
> 		      self.val = val
> 		  def __add__(self, other): 					# __add__ fallback: x = (x + y)
> 		      return Number(self.val + other) 			# Propagates class type
> >>> x = Number(5)
> >>> x += 1
> >>> x += 1 											# And += does concatenation here
> >>> x.val
> 7
> ```

Though we've focused on + here, keep in mind that every binary operator has similar right-side and in-place 
overloading methods that work the same (e.g., __mul__, __rmul__, and __imul__). Still, right-side methods 
are an advanced topic and tend to be fairly uncommon in practice; you only code them when you need operators 
to be commutative, and then only if you need to support such operators at all. For instance, a Vector class 
may use these tools, but an Employee or Button class probably would not.
