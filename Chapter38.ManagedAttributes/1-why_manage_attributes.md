# Why Manage Attributes
This chapter expands on the attribute interception techniques introduced earlier, introduces another, and employs them in a handful of larger examples. Like everything in this part of the book, this chapter is classified as an advanced topic and optional reading.

Especially for tools builders, though, managing attribute access can be an important part of flexible APIs. Moreover, an understanding of the descriptor model covered here can make related tools such as slots and properties more tangible, and may even be required reading if it appears in code you must use.

Object attributes are central to most Python programs -- they are where we often store information about the entities our scripts process. Normally, attributes are simply names for objects; a person's name attribute, for example, might be a simple string, fetched and set with basic attribute syntax:
> ```python
> person.name 					# Fetch attribute value
> person.name = value 			# Change attribute value
> ```

In most cases, the attribute lives in the object itself, or is inherited from a class from which it derives. That basic model suffices for most programs you will write in your Python career.

Sometimes, though, more flexibility is required. Suppose you've written a program to use a name attribute directly, but then your requirements change -- for example, you decide that names should be validated with logic when set or mutated in some way when fetched. It's straightforward to code methods to manage access to the attribute's value (valid and transform are abstract here):
> ```python
> class Person:
>     def getName(self):
>         if not valid():
>             raise TypeError('cannot fetch name')
>         else:
>             return self.name.transform()
> 
>     def setName(self, value):
>         if not valid(value):
>             raise TypeError('cannot change name')
>         else:
>             self.name = transform(value)
> 
> person = Person()
> person.getName()
> person.setName('value')
> ```

However, this also requires changing all the places where names are used in the entire program -- a possibly nontrivial task. Moreover, this approach requires the program to be aware of how values are exported: as simple names or called methods. If you begin with a method-based interface to data, clients are immune to changes; if you do not, they can become problematic.

This issue can crop up more often than you might expect. The value of a cell in a spreadsheet-like program, for instance, might begin its life as a simple discrete value, but later mutate into an arbitrary calculation. Since an object's interface should be flexible enough to support such future changes without breaking existing code, switching to methods later is less than ideal.

## Inserting Code to Run on Attribute Access
A better solution would allow you to run code automatically on attribute access, if needed. That's one of the main roles of managed attributes -- they provide ways to add attribute accessor logic after the fact. More generally, they support arbitrary attribute usage modes that go beyond simple data storage.

At various points in this book, we've met Python tools that allow our scripts to dynamically compute attribute values when fetching them and validate or change attribute values when storing them. In this chapter, we're going to expand on the tools already introduced, explore other available tools, and study some larger use-case examples in this domain. Specifically, this chapter presents four accessor techniques:
- The \_\_getattr\_\_ and \_\_setattr\_\_ methods, for routing undefined attribute fetches and all attribute assignments to generic handler methods.
- The \_\_getattribute\_\_ method, for routing all attribute fetches to a generic handler method.
- The property built-in, for routing specific attribute access to get and set handler functions.
- The descriptor protocol, for routing specific attribute accesses to instances of classes with arbitrary get and set handler methods, and the basis for other tools such as properties and slots.

The tools in the first of these bullets are available in all Pythons. The last three bullets' tools are available in Python 3.X and new-style classes in 2.X -- they first appeared in Python 2.2, along with many of the other advanced tools of Chapter 32 such as slots and super. We briefly met the first and third of these in Chapter 30 and Chapter 32, respectively; the second and fourth are largely new topics we'll explore in full here.

As we'll see, all four techniques share goals to some degree, and it's usually possible to code a given problem using any one of them. They do differ in some important ways, though. For example, the last two techniques listed here apply to specific attributes, whereas the first two are generic enough to be used by delegation-based proxy classes that must route arbitrary attributes to wrapped objects. As we'll see, all four schemes also differ in both complexity and aesthetics, in ways you must see in action to judge for yourself.

Besides studying the specifics behind the four attribute interception techniques listed in this section, this chapter also presents an opportunity to explore larger programs than we've seen elsewhere in this book. The CardHolder case study at the end, for example, should serve as a self-study example of larger classes in action. We'll also be using some of the techniques outlined here in the next chapter to code decorators, so be sure you have at least a general understanding of these topics before you move on.
