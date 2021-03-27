# Why Exception Hierarchies?
Because there are only three possible exceptions in the prior section's example, it doesn't really do justice to the utility of class exceptions. In fact, we could achieve the same effects by coding a list of exception names in parentheses within the except clause:
> ```python
> try:
>     func()
> except (General, Specific1, Specific2): 				# Catch any of these
>     ...
> ```

This approach worked for the defunct string exception model too. For large or high exception hierarchies, however, it may be easier to catch categories using class-based categories than to list every member of a category in a single except clause. Perhaps more importantly, you can extend exception hierarchies as software needs evolve by adding new subclasses without breaking existing code.

Suppose, for example, you code a numeric programming library in Python, to be used by a large number of people. While you are writing your library, you identify two things that can go wrong with numbers in your code -- division by zero, and numeric overflow. You document these as the two standalone exceptions that your library may raise:
> ```python
> # mathlib.py
> class Divzero(Exception): pass
> class Oflow(Exception): pass
> def func():
>     ...
>     raise Divzero()
> 
> ...and so on...
> ```

Now, when people use your library, they typically wrap calls to your functions or classes in try statements that catch your two exceptions; after all, if they do not catch your exceptions, exceptions from your library will kill their code:
> ```python
> # client.py
> import mathlib
> try:
>     mathlib.func(...)
> except (mathlib.Divzero, mathlib.Oflow):
>     ...handle and recover...
> ```

This works fine, and lots of people start using your library. Six months down the road, though, you revise it (as programmers are prone to do!). Along the way, you identify a new thing that can go wrong -- underflow, perhaps -- and add that as a new exception:
> ```python
> # mathlib.py
> class Divzero(Exception): pass
> class Oflow(Exception): pass
> class Uflow(Exception): pass
> ```

Unfortunately, when you re-release your code, you create a maintenance problem for your users. If they've listed your exceptions explicitly, they now have to go back and change every place they call your library to include the newly added exception name:
> ```python
> # client.py
> try:
>     mathlib.func(...)
> except (mathlib.Divzero, mathlib.Oflow, mathlib.Uflow):
>     ...handle and recover...
> ```

This may not be the end of the world. If your library is used only in-house, you can make the changes yourself. You might also ship a Python script that tries to fix such code automatically (it would probably be only a few dozen lines, and it would guess right at least some of the time). If many people have to change all their try statements each time you alter your exception set, though, this is not exactly the most polite of upgrade policies.

Your users might try to avoid this pitfall by coding empty except clauses to catch all possible exceptions:
> ```python
> # client.py
> try:
>     mathlib.func(...)
> except: 							# Catch everything here (or catch Exception super)
>     ...handle and recover...
> ```

But this workaround might catch more than they bargained for -- things like running out of memory, keyboard interrupts (Ctrl-C), system exits, and even typos in their own try block's code will all trigger exceptions, and such things should pass, not be caught and erroneously classified as library errors. Catching the Exception super class improves on this, but still intercepts -- and thus may mask -- program errors.

And really, in this scenario users want to catch and recover from only the specific exceptions the library is defined and documented to raise. If any other exception occurs during a library call, it's likely a genuine bug in the library (and probably time to contact the vendor!). As a rule of thumb, it's usually better to be specific than general in exception handlers -- an idea we'll revisit as a "gotcha" in the next chapter.

So what to do, then? Class exception hierarchies fix this dilemma completely. Rather than defining your library's exceptions as a set of autonomous classes, arrange them into a class tree with a common superclass to encompass the entire category:
> ```python
> # mathlib.py
> class NumErr(Exception): pass
> class Divzero(NumErr): pass
> class Oflow(NumErr): pass
> 
> def func():
>     ...
>     raise DivZero()
> 
> ...and so on...
> ```

This way, users of your library simply need to list the common superclass (i.e., category) to catch all of your library's exceptions, both now and in the future:
> ```python
> # client.py
> import mathlib
> try:
>     mathlib.func(...)
> except mathlib.NumErr:
>     ...report and recover...
> ```

When you go back and hack (update) your code again, you can add new exceptions as new subclasses of the common superclass:
> ```python
> # mathlib.py
> ...
> class Uflow(NumErr): pass
> ```

The end result is that user code that catches your library's exceptions will keep working, unchanged. In fact, you are free to add, delete, and change exceptions arbitrarily in the future -- as long as clients name the superclass, and that superclass remains intact, they are insulated from changes in your exceptions set. In other words, class exceptions provide a better answer to maintenance issues than strings could.  Class-based exception hierarchies also support state retention and inheritance in ways that make them ideal in larger programs. To understand these roles, though, we first need to see how user-defined exception classes relate to the built-in exceptions from which they inherit.
