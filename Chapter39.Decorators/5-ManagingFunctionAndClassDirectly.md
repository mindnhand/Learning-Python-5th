# Managing Functions and Classes Directly
Most of our examples in this chapter have been designed to intercept function and instance creation calls. Although this is typical for decorators, they are not limited to this role. Because decorators work by running new functions and classes through decorator code, they can also be used to manage function and class objects themselves, not just later calls made to them.

Imagine, for example, that you require methods or classes used by an application to be registered to an API for later processing (perhaps that API will call the objects later, in response to events). Although you could provide a registration function to be called manually after the objects are defined, decorators make your intent more explicit.

The following simple implementation of this idea defines a decorator that can be applied to both functions and classes, to add the object to a dictionary-based registry. Because it returns the object itself instead of a wrapper, it does not intercept later calls:
> ```python
> # Registering decorated objects to an API
> from __future__ import print_function 			# 2.X
> registry = {}
> def register(obj): 					# Both class and func decorator
>     registry[obj.__name__] = obj 		# Add to registry
>     return obj 						# Return obj itself, not a wrapper
> 
> @register
> def spam(x):
>     return(x ** 2) 					# spam = register(spam)
> 
> @register
> def ham(x):
>     return(x ** 3)
> 
> @register
> class Eggs: 							# Eggs = register(Eggs)
>     def __init__(self, x):
>         self.data = x ** 4
>     def __str__(self):
>         return str(self.data)
> 
> print('Registry:')
> for name in registry:
>     print(name, '=>', registry[name], type(registry[name]))
> 
> print('\nManual calls:')
> print(spam(2)) 								# Invoke objects manually
> print(ham(2)) 								# Later calls not intercepted
> X = Eggs(2)
> print(X)
> 
> print('\nRegistry calls:')
> for name in registry:
>     print(name, '=>', registry[name](2)) 		# Invoke from registry
> ```

When this code is run the decorated objects are added to the registry by name, but they still work as originally coded when they're called later, without being routed through a wrapper layer. In fact, our objects can be run both manually and from inside the registry table:
> ```powershell
> c:\code> py -3 registry-deco.py
> Registry:
> spam => <function spam at 0x02969158> <class 'function'>
> ham => <function ham at 0x02969400> <class 'function'>
> Eggs => <class '__main__.Eggs'> <class 'type'>
> Manual calls:
> 4
> 8
> 16
> Registry calls:
> spam => 4
> ham => 8
> Eggs => 16
> ```

A user interface might use this technique, for example, to register callback handlers for user actions. Handlers might be registered by function or class name, as done here, or decorator arguments could be used to specify the subject event; an extra def statement enclosing our decorator could be used to retain such arguments for use on decoration.

This example is artificial, but its technique is very general. For example, function decorators might also be used to process function attributes, and class decorators might insert new class attributes, or even new methods, dynamically. Consider the following function decorators -- they assign function attributes to record information for later use by an API, but they do not insert a wrapper layer to intercept later calls:
> ```python
> # Augmenting decorated objects directly
> >>> def decorate(func):
>         func.marked = True 			# Assign function attribute for later use
>         return func
> 
> >>> @decorate
>     def spam(a, b):
>         return a + b
> 
> >>> spam.marked
> True
> 
> >>> def annotate(text): 				# Same, but value is decorator argument
>         def decorate(func):
>             func.label = text
>             return func
>         return decorate
> 
> >>> @annotate('spam data')
>     def spam(a, b): 					# spam = annotate(...)(spam)
>         return a + b
> 
> >>> spam(1, 2), spam.label
> (3, 'spam data')
> ```

Such decorators augment functions and classes directly, without catching later calls to them. We'll see more examples of class decorations managing classes directly in the next chapter, because this turns out to encroach on the domain of metaclasses; for the remainder of this chapter, let's turn to two larger case studies of decorators at work.

