# Coding Alternative: __iter__ plus yield

And now, for something completely implicit—but potentially useful nonetheless. In
some applications, it's possible to minimize coding requirements for user-defined iterables
by combining the __iter__ method we're exploring here and the yield generator
function statement we studied in Chapter 20. Because generator functions automatically
save local variable state and create required iterator methods, they fit this role
well, and complement the state retention and other utility we get from classes.

As a review, recall that any function that contains a yield statement is turned into a
generator function. When called, it returns a new generator object with automatic retention
of local scope and code position, an automatically created __iter__ method
that simply returns itself, and an automatically created __next__ method (next in 2.X)
that starts the function or resumes it where it last left off:
> ```python
> >>> def gen(x):
> for i in range(x): yield i ** 2
> >>> G = gen(5) 								# Create a generator with __iter__ and __next__
> >>> G.__iter__() == G 						# Both methods exist on the same object
> True
> >>> I = iter(G) 								# Runs __iter__: generator returns itself
> >>> next(I), next(I) 							# Runs __next__ (next in 2.X)
> (0, 1)
> >>> list(gen(5)) 								# Iteration contexts automatically run iter and next
> [0, 1, 4, 9, 16]
> ```

This is still true even if the generator function with a yield happens to be a method
named __iter__: whenever invoked by an iteration context tool, such a method will
return a new generator object with the requisite __next__. As an added bonus, generator
functions coded as methods in classes have access to saved state in both instance attributes
and local scope variables.

