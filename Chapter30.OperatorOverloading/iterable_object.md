Although the __getitem__ technique of the prior section works, it's really just a fallback
for iteration. Today, all iteration contexts in Python will try the __iter__ method first,
before trying __getitem__. That is, they prefer the iteration protocol we learned about
in Chapter 14 to repeatedly indexing an object; only if the object does not support the
iteration protocol is indexing attempted instead. Generally speaking, you should prefer
__iter__ too—it supports general iteration contexts better than __getitem__ can.

Technically, iteration contexts work by passing an iterable object to the iter built-in
function to invoke an __iter__ method, which is expected to return an iterator object.
If it's provided, Python then repeatedly calls this iterator object's __next__ method to
produce items until a StopIteration exception is raised. A next built-in function is also
available as a convenience for manual iterations—next(I) is the same as I.__next__(). 
For a review of this model’s essentials, see Figure 14-1 in Chapter 14.

This iterable object interface is given priority and attempted first. Only if no such
__iter__ method is found, Python falls back on the __getitem__ scheme and repeatedly
indexes by offsets as before, until an IndexError exception is raised.


