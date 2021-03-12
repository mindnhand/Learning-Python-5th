# Methods
Because you already know about functions, you also know about methods in classes.
Methods are just function objects created by def statements nested in a class statement's
body. From an abstract perspective, methods provide behavior for instance
objects to inherit. From a programming perspective, methods work in exactly the same
way as simple functions, with one crucial exception: a method's first argument always
receives the instance object that is the implied subject of the method call.
In other words, Python automatically maps instance method calls to a class's method
functions as follows. Method calls made through an instance, like this:
> `instance.method(args...)`
are automatically translated to class method function calls of this form:
> `class.method(instance, args...)`
where Python determines the class by locating the method name using the inheritance
search procedure. In fact, both call forms are valid in Python.
Besides the normal inheritance of method attribute names, the special first argument
is the only real magic behind method calls. In a class's method, the first argument is
usually called self by convention (technically, only its position is significant, not its
name). This argument provides methods with a hook back to the instance that is the
subject of the call—because classes generate many instance objects, they need to use
this argument to manage data that varies per instance.
