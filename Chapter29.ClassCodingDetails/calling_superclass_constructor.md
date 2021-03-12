Methods are normally called through instances. Calls to methods through a class,
though, do show up in a variety of special roles. One common scenario involves the
constructor method. The __init__ method, like all attributes, is looked up by inheritance.
This means that at construction time, Python locates and calls just one __init__. 
If subclass constructors need to guarantee that superclass construction-time
logic runs, too, they generally must call the superclass'  __init__ method explicitly
through the class:
> ```python
> class Super:
>     def __init__(self, x):
>         ...default code...
> class Sub(Super):
>     def __init__(self, x, y):
>         Super.__init__(self, x) 		# Run superclass __init__
> 		  ...custom code... 			# Do my init actions
> I = Sub(1, 2)
> ```
This is one of the few contexts in which your code is likely to call an operator overloading
method directly. Naturally, you should call the superclass constructor this way
only if you really want it to run—without the call, the subclass replaces it completely.
For a more realistic illustration of this technique in action, see the Manager class example
in the prior chapter's tutorial.3
