# Membership: __contains__, __iter__, and __getitem__

The iteration story is even richer than we've seen thus far. Operator overloading is often
layered: classes may provide specific methods, or more general alternatives used as fallback 
options. For example:
- Comparisons in Python 2.X use specific methods such as __lt__ for "less than" if
  present, or else the general __cmp__. Python 3.X uses only specific methods, not
  __cmp__, as discussed later in this chapter.
- Boolean tests similarly try a specific __bool__ first (to give an explicit True/False
  result), and if it's absent fall back on the more general __len__ (a nonzero length
  means True). As we'll also see later in this chapter, Python 2.X works the same but
  uses the name __nonzero__ instead of __bool__.

In the iterations domain, classes can implement the in membership operator as an iteration, 
using either the __iter__ or __getitem__ methods. To support more specific membership, though, 
classes may code a __contains__ method—when present, thiss method is preferred over __iter__, 
which is preferred over __getitem__. The __contains__ method should define membership as applying 
to keys for a mapping (and can use quick lookups), and as a search for sequences.
