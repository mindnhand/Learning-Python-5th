# Namespace Dictionaries: Review 

We put some of these tools to work in the prior chapter, but to summarize and help
you better understand how attributes work internally, let's work through an interactive
session that traces the way namespace dictionaries grow when classes are involved.
Now that we know more about methods and superclasses, we can also embellish the
coverage here for a better look. First, let's define a superclass and a subclass with methods
that will store data in their instances:
> ```python
> >>> class Super:
>         def hello(self):
>             self.data1 = 'spam'
> >>> class Sub(Super):
>         def hola(self):
>             self.data2 = 'eggs'
> ```

When we make an instance of the subclass, the instance starts out with an empty
namespace dictionary, but it has links back to the class for the inheritance search to
follow. In fact, the inheritance tree is explicitly available in special attributes, which
you can inspect. Instances have a __class__ attribute that links to their class, and classes
have a __bases__ attribute that is a tuple containing links to higher superclasses (I'm
running this on Python 3.3; your name formats, internal attributes, and key orders may
vary):
> ```python
> >>> X = Sub()
> >>> X.__dict__ 				# Instance namespace dict
> {}
> >>> X.__class__ 				# Class of instance
> <class '__main__.Sub'>
> >>> Sub.__bases__ 			# Superclasses of class
> (<class '__main__.Super'>,)
> >>> Super.__bases__ 			# () empty tuple in Python 2.X
> (<class 'object'>,)
```

As classes assign to self attributes, they populate the instance objects—that is, attributes
wind up in the instances' attribute namespace dictionaries, not in the classes'.
An instance object's namespace records data that can vary from instance to instance,
and self is a hook into that namespace:
> ```python
> >>> Y = Sub()
> >>> X.hello()
> >>> X.__dict__
> {'data1': 'spam'}
> >>> X.hola()
> >>> X.__dict__
> {'data2': 'eggs', 'data1': 'spam'}
> >>> list(Sub.__dict__.keys())
> ['__qualname__', '__module__', '__doc__', 'hola']
> >>> list(Super.__dict__.keys())
> ['__module__', 'hello', '__dict__', '__qualname__', '__doc__', '__weakref__']
> >>> Y.__dict__
> {}
```

Notice the extra underscore names in the class dictionaries; Python sets these automatically,
and we can filter them out with the generator expressions we saw in Chapter
27 and Chapter 28 that we won't repeat here. Most are not used in typical programs,
but there are tools that use some of them (e.g., __doc__ holds the docstrings discussed
in Chapter 15).

Also, observe that Y, a second instance made at the start of this series, still has an empty
namespace dictionary at the end, even though X's dictionary has been populated by
assignments in methods. Again, each instance has an independent namespace dictionary,
which starts out empty and can record completely different attributes than those
recorded by the namespace dictionaries of other instances of the same class.
Because attributes are actually dictionary keys inside Python, there are really two ways
to fetch and assign their values—by qualification, or by key indexing:
> ```python
> >>> X.data1, X.__dict__['data1']
> ('spam', 'spam')
> >>> X.data3 = 'toast'
> >>> X.__dict__
> {'data2': 'eggs', 'data3': 'toast', 'data1': 'spam'}
> >>> X.__dict__['data3'] = 'ham'
> >>> X.data3
> 'ham'
> ```

This equivalence applies only to attributes actually attached to the instance, though.
Because attribute fetch qualification also performs an inheritance search, it can access
inherited attributes that namespace dictionary indexing cannot. The inherited attribute
X.hello, for instance, cannot be accessed by X.__dict__['hello'].

Experiment with these special attributes on your own to get a better feel for how namespaces
actually do their attribute business. Also try running these objects through the
dir function we met in the prior two chapters—dir(X) is similar to
X.__dict__.keys(), but dir sorts its list and includes some inherited and built-in attributes. 
Even if you will never use these in the kinds of programs you write, seeing that
they are just normal dictionaries can help solidify namespaces in general.
