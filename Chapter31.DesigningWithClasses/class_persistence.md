# Why You Will Care: Classes and Persistence
I've mentioned Python's pickle and shelve object persistence support a few times in
this part of the book because it works especially well with class instances. In fact, these
tools are often compelling enough to motivate the use of classes in general -- by pickling
or shelving a class instance, we get data storage that contains both data and logic combined.
For example, besides allowing us to simulate real-world interactions, the pizza shop
classes developed in this chapter could also be used as the basis of a persistent restaurant
database. Instances of classes can be stored away on disk in a single step using Python's
pickle or shelve modules. We used shelves to store instances of classes in the OOP
tutorial in Chapter 28, but the object pickling interface is remarkably easy to use as well:
> ```python
> import pickle
> object = SomeClass()
> file = open(filename, 'wb') 			# Create external file
> pickle.dump(object, file) 			# Save object in file
> import pickle
> file = open(filename, 'rb')
> object = pickle.load(file) 			# Fetch it back later
> ```

Pickling converts in-memory objects to serialized byte streams (in Python, strings),
which may be stored in files, sent across a network, and so on; unpickling converts
back from byte streams to identical in-memory objects. Shelves are similar, but they
automatically pickle objects to an access-by-key database, which exports a dictionarylike
interface:
> ```python
> import shelve
> object = SomeClass()
> dbase = shelve.open(filename)
> dbase['key'] = object 			# Save under key
> import shelve
> dbase = shelve.open(filename)
> object = dbase['key'] 			# Fetch it back later
> ```

In our pizza shop example, using classes to model employees means we can get a simple
database of employees and shops with little extra work -- pickling such instance objects
to a file makes them persistent across Python program executions:
> ```python
> >>> from pizzashop import PizzaShop
> >>> shop = PizzaShop()
> >>> shop.server, shop.chef
> (<Employee: name=Pat, salary=40000>, <Employee: name=Bob, salary=50000>)
> >>> import pickle
> >>> pickle.dump(shop, open('shopfile.pkl', 'wb'))
> ```

This stores an entire composite shop object in a file all at once. To bring it back later in
another session or program, a single step suffices as well. In fact, objects restored this
way retain both state and behavior:
> ```python
> >>> import pickle
> >>> obj = pickle.load(open('shopfile.pkl', 'rb'))
> >>> obj.server, obj.chef
> (<Employee: name=Pat, salary=40000>, <Employee: name=Bob, salary=50000>)
> >>> obj.order('LSP')
> LSP orders from <Employee: name=Pat, salary=40000>
> Bob makes pizza
> oven bakes
> LSP pays for item to <Employee: name=Pat, salary=40000>
> ```

This just runs a simulation as is, but we might extend the shop to keep track of inventory,
revenue, and so on -- saving it to its file after changes would retain its updated
state. See the standard library manual and related coverage in Chapter 9, Chapter 28,
and Chapter 37 for more on pickles and shelves.
