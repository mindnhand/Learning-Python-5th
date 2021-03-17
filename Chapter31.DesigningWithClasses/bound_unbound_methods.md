# Methods Are Objects: Bound or Unbound
Methods in general, and bound methods in particular, simplify the implementation of many design goals in Python.
We met bound methods briefly while studying \_\_call\_\_ in Chapter 30. The full story, which we'll flesh out here, turns out to be more general and flexible than you might expect.

In Chapter 19, we learned how functions can be processed as normal objects. Methods are a kind of object too, and can be used generically in much the same way as other objects -- they can be assigned to names, passed to functions, stored in data structures, and so on -- and like simple functions, qualify as "first class" objects. Because a class's methods can be accessed from an instance or a class, though, they actually come in two flavors in Python:
- **Unbound (class) method objects: no self**
  Accessing a function attribute of a class by qualifying the class returns an unbound method object. To call the method, you must provide an instance object explicitly as the first argument. In Python 3.X, an unbound method is the same as a simple function and can be called through the class's name; in 2.X it's a distinct type and cannot be called without providing an instance.
- **Bound (instance) method objects: self + function pairs**
  Accessing a function attribute of a class by qualifying an instance returns a bound method object. Python automatically packages the instance with the function in the bound method object, so you don't need to pass an instance to call the method.

Both kinds of methods are full-fledged objects; they can be transferred around a program at will, just like strings and numbers. Both also require an instance in their first argument when run (i.e., a value for self). This is why we've had to pass in an instance explicitly when calling superclass methods from subclass methods in previous examples (including this chapter's employees.py); technically, such calls produce unbound method objects along the way.

When calling a bound method object, Python provides an instance for you automatically -- the instance used to create the bound method object. This means that bound method objects are usually interchangeable with simple function objects, and makes them especially useful for interfaces originally written for functions (see the sidebar "Why You Will Care: Bound Method Callbacks" on page 953 for a realistic use case in GUIs).

To illustrate in simple terms, suppose we define the following class:
> ```python
> class Spam:
>     def doit(self, message):
>         print(message)
> ```

Now, in normal operation, we make an instance and call its method in a single step to print the passed-in argument:
> ```python
> object1 = Spam()
> object1.doit('hello world')
> ```

Really, though, a bound method object is generated along the way, just before the method call's parentheses. In fact, we can fetch a bound method without actually calling it. An object.name expression evaluates to an object as all expressions do. In the following, it returns a bound method object that packages the instance (object1) with the method function (Spam.doit). We can assign this bound method pair to another name and then call it as though it were a simple function:
> ```python
> object1 = Spam()
> x = object1.doit 			# Bound method object: instance+function
> x('hello world') 			# Same effect as object1.doit('...')
> ```

On the other hand, if we qualify the class to get to doit, we get back an unbound method object, which is simply a reference to the function object. To call this type of method, we must pass in an instance as the leftmost argument -- there isn't one in the expression otherwise, and the method expects it:
> ```python
> object1 = Spam()
> t = Spam.doit 			# Unbound method object (a function in 3.X: see ahead)
> t(object1, 'howdy') 		# Pass in instance (if the method expects one in 3.X)
> ```

By extension, the same rules apply within a class's method if we reference self attributes that refer to functions in the class. A self.method expression is a bound method object because self is an instance object:
> ```python
> class Eggs:
>     def m1(self, n):
>         print(n)
>     def m2(self):
>         x = self.m1 				# Another bound method object
> 
> x(42) 							# Looks like a simple function
> Eggs().m2() 						# Prints 42
> ```

Most of the time, you call methods immediately after fetching them with attribute qualification, so you don't always notice the method objects generated along the way.

But if you start writing code that calls objects generically, you need to be careful to treat unbound methods specially -- they normally require an explicit instance object to be passed in.
> **Note:**
> For an optional exception to this rule, see the discussion of static and class methods in the next chapter, and the brief mention of one in the next section. Like bound methods, static methods can masquerade as basic functions because they do not expect instances when called. Formally speaking, Python supports three kinds of class-level methods— instance, static, and class—and 3.X allows simple functions in classes,   too. Chapter 40's metaclass methods are distinct too, but they are essentially class methods with less scope.
>

## Unbound Methods Are Functions in 3.X
In Python 3.X, the language has dropped the notion of unbound methods. What we describe as an unbound method here is treated as a simple function in 3.X. For most purposes, this makes no difference to your code; either way, an instance will be passed to a method's first argument when it's called through an instance.

Programs that do explicit type testing might be impacted, though -- if you print the type of an instance-less class-level method, it displays "unbound method" in 2.X, and "function" in 3.X.

Moreover, in 3.X it is OK to call a method without an instance, as long as the method does not expect one and you call it only through the class and never through an instance.

That is, Python 3.X will pass along an instance to methods only for through-instance calls. When calling through a class, you must pass an instance manually only if the method expects one:
> ```python
> C:\code> c:\python33\python
> >>> class Selfless:
>         def __init__(self, data):
>             self.data = data
>         def selfless(arg1, arg2): 		# A simple function in 3.X
>             return arg1 + arg2
>         def normal(self, arg1, arg2): 	# Instance expected when called
>             return self.data + arg1 + arg2
> 
> >>> X = Selfless(2)
> >>> X.normal(3, 4) 						# Instance passed to self automatically: 2+(3+4)
> 9
> >>> Selfless.normal(X, 3, 4) 				# self expected by method: pass manually
> 9
> >>> Selfless.selfless(3, 4) 				# No instance: works in 3.X, fails in 2.X!
> 7
> ```

The last test in this fails in 2.X, because unbound methods require an instance to be passed by default; it works in 3.X because such methods are treated as simple functions not requiring an instance. Although this removes some potential error trapping in 3.X (what if a programmer accidentally forgets to pass an instance?), it allows a class's methods to be used as simple functions as long as they are not passed and do not expect a "self" instance argument.

The following two calls still fail in both 3.X and 2.X, though -- the first (calling through an instance) automatically passes an instance to a method that does not expect one, while the second (calling through a class) does not pass an instance to a method that does expect one (error message text here is per 3.3):
> ```python
> >>> X.selfless(3, 4)
> TypeError: selfless() takes 2 positional arguments but 3 were given
> >>> Selfless.normal(3, 4)
> TypeError: normal() missing 1 required positional argument: 'arg2'
> ```

Because of this change, the staticmethod built-in function and decorator described in the next chapter is not needed in 3.X for methods without a self argument that are called only through the class name, and never through an instance -- such methods are  run as simple functions, without receiving an instance argument. In 2.X, such calls are errors unless an instance is passed manually or the method is marked as being static (more on static methods in the next chapter).

It's important to be aware of the differences in behavior in 3.X, but bound methods are generally more important from a practical perspective anyway. Because they pair together the instance and function in a single object, they can be treated as callables generically. The next section demonstrates what this means in code.

> **Note**
> For a more visual illustration of unbound method treatment in Python 3.X and 2.X, see also the lister.py example in the multiple inheritance section later in this chapter. Its classes print the value of methods fetched from both instances and classes, in both versions of Python -- as unbound  methods in 2.X and simple functions in 3.X. Also note that this change is inherent in 3.X itself, not the new-style class model it mandates.

## Bound Methods and Other Callable Objects
As mentioned earlier, bound methods can be processed as generic objects, just like simple functions -- they can be passed around a program arbitrarily. Moreover, because bound methods combine both a function and an instance in a single package, they can be treated like any other callable object and require no special syntax when invoked.

The following, for example, stores four bound method objects in a list and calls them later with normal call expressions:
> ```python
> >>> class Number:
>         def __init__(self, base):
>             self.base = base
>         def double(self):
>             return self.base * 2
>         def triple(self):
>             return self.base * 3
> 
> >>> x = Number(2) 		# Class instance objects
> >>> y = Number(3) 		# State + methods
> >>> z = Number(4)
> >>> x.double() 			# Normal immediate calls
> 4
> >>> acts = [x.double, y.double, y.triple, z.double]      # List of bound methods
> >>> for act in acts: 		# Calls are deferred
>         print(act()) 				# Call as though functions
> 4
> 6
> 9
> 8
> ```

Like simple functions, bound method objects have introspection information of their own, including attributes that give access to the instance object and method function they pair. Calling the bound method simply dispatches the pair:
> ```python
> >>> bound = x.double
> >>> bound.__self__, bound.__func__
> (<__main__.Number object at 0x...etc...>, <function Number.double at 0x...etc...>)
> >>> bound.__self__.base
> 2
> >>> bound() # Calls bound.__func__(bound.__self__, ...)
> 4
> ```

### Other callables
In fact, bound methods are just one of a handful of callable object types in Python. As the following demonstrates, simple functions coded with a def or lambda, instances that inherit a \_\_call\_\_, and bound instance methods can all be treated and called the same way:
> ```python
> >>> def square(arg):
>         return arg ** 2 			# Simple functions (def or lambda)
> 
> >>> class Sum:
>         def __init__(self, val):  # Callable instances
>             self.val = val
>         def __call__(self, arg):
> 			  return self.val + arg
> 
> >>> class Product:
>         def __init__(self, val): # Bound methods
>             self.val = val
>         def method(self, arg):
> 			  return self.val * arg
> 
> >>> sobject = Sum(2)
> >>> pobject = Product(3)
> >>> actions = [square, sobject, pobject.method] 		# Function, instance, method
> >>> for act in actions: 					# All three called same way
>         print(act(5)) 				# Call any one-arg callable
> 25
> 7
> 15
> >>> actions[-1](5) 		# Index, comprehensions, maps
> 15
> >>> [act(5) for act in actions]
> [25, 7, 15]
> >>> list(map(lambda act: act(5), actions))
> [25, 7, 15]
> ```

Technically speaking, classes belong in the callable objects category too, but we normally call them to generate instances rather than to do actual work -- a single action is  better coded as a simple function than a class with a constructor, but the class here serves to illustrate its callable nature:
> ```python
> >>> class Negate:
>         def __init__(self, val): 				# Classes are callables too
>             self.val = -val 					# But called for object, not work
>         def __repr__(self): 					# Instance print format
>             return str(self.val)
> 
> >>> actions = [square, sobject, pobject.method, Negate] 		# Call a class too
> >>> for act in actions:
>         print(act(5))
> 25
> 7
> 15
> -5
> >>> [act(5) for act in actions] 				# Runs __repr__ not __str__!
> [25, 7, 15, −5]
> >>> table = {act(5): act for act in actions}  # 3.X/2.7 dict comprehension
> >>> for (key, value) in table.items():
>         print('{0:2} => {1}'.format(key, value)) 		# 2.6+/3.X str.format
> 25 => <function square at 0x0000000002987400>
> 15 => <bound method Product.method of <__main__.Product object at ...etc...>>
> -5 => <class '__main__.Negate'>
> 7 => <__main__.Sum object at 0x000000000298BE48>
> ```

As you can see, bound methods, and Python's callable objects model in general, are some of the many ways that Python's design makes for an incredibly flexible language.

You should now understand the method object model. For other examples of bound methods at work, see the upcoming sidebar "Why You Will Care: Bound Method Callbacks" on page 953 as well as the prior chapter's discussion of callback handlers in the section on the method \_\_call\_\_.

> **Why You Will Care: Bound Method Callbacks**
> Because bound methods automatically pair an instance with a class's method function, you can use them anywhere a simple function is expected. One of the most common places you'll see this idea put to work is in code that registers methods as event callback handlers in the tkinter GUI interface (named Tkinter in Python 2.X) we've met before.
> As review, here's the simple case:
> > ```python
> > def handler():
> > ...use globals or closure scopes for state...
> > ...
> > widget = Button(text='spam', command=handler)
> > ```
> 
> To register a handler for button click events, we usually pass a callable object that takes no arguments to the command keyword argument. Function names (and lambdas) work here, and so do class-level methods -- though they must be bound methods if they expect an instance when called:
> > ```python
> > class MyGui:
> > def handler(self):
> > ...use self.attr for state...
> > def makewidgets(self):
> > b = Button(text='spam', command=self.handler)
> > ```
> 
> Here, the event handler is self.handler -- a bound method object that remembers both  self and MyGui.handler.
> Because self will refer to the original instance when handler is later invoked on events, the method will have access to instance attributes that can retain state between events, as well as class-level methods.
> With simple functions, state normally must be retained in global variables or enclosing function scopes instead.
> 
> See also the discussion of \_\_call\_\_ operator overloading in Chapter 30 for another way to make classes compatible with function-based APIs, and lambda in Chapter 19 for another tool often used in callback roles. As noted in the former of these, you don't generally need to wrap a bound method in a lambda; the bound method in the preceding example already defers the call (note that there are no parentheses to trigger one), so adding a lambda here would be pointless!
>
