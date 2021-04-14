# To Metaclass or Not To Metaclass
In a sense, metaclasses simply extend the code-insertion model of decorators. As we learned in the prior chapter, function and class decorators allow us to intercept and augment function calls and class instance creation calls. In a similar spirit, metaclasses allow us to intercept and augment class creation -- they provide an API for inserting extra logic to be run at the conclusion of a class statement, albeit in different ways than decorators. Accordingly, they provide a general protocol for managing class objects in a program.

On the other hand, metaclasses open the door to a variety of coding patterns that may be difficult or impossible to achieve otherwise, and they are especially of interest to programmers seeking to write flexible APIs or programming tools for others to use. Even if you don't fall into that category, though, metaclasses can teach you much about Python's class model in general (as we'll see, they even impact inheritance), and are prerequisite to understanding code that employs them. Like other advanced tools, metaclasses have begun appearing in Python programs more often than their creators may have intended.

As in the prior chapter, part of our goal here is also to show more realistic code examples than we did earlier in this book. Although metaclasses are a core language topic and not themselves an application domain, part of this chapter's agenda is to spark your interest in exploring larger application-programming examples after you finish this book.

Metaclasses are perhaps the most advanced topic in this book, if not the Python language as a whole. To borrow a quote from the comp.lang.python newsgroup by veteran Python core developer Tim Peters (who is also the author of the famous "import this" Python motto):
> [Metaclasses] are deeper magic than 99% of users should ever worry about. If you wonder whether you need them, you don't (the people who actually need them know with certainty that they need them, and don't need an explanation about why).

In other words, metaclasses are primarily intended for a subset of programmers building APIs and tools for others to use. In many (if not most) cases, they are probably not the best choice in applications work. This is especially true if you're developing code that other people will use in the future. Coding something "because it seems cool" is not generally a reasonable justification, unless you are experimenting or learning.

Still, metaclasses have a wide variety of potential roles, and it's important to know when they can be useful. For example, they can be used to enhance classes with features like tracing, object persistence, exception logging, and more. They can also be used to construct portions of a class at runtime based upon configuration files, apply function decorators to every method of a class generically, verify conformance to expected interfaces, and so on.

In their more grandiose incarnations, metaclasses can even be used to implement alternative coding patterns such as aspect-oriented programming, object/relational mappers (ORMs) for databases, and more. Although there are often alternative ways to achieve such results -- as we'll see, the roles of class decorators and metaclasses often intersect -- metaclasses provide a formal model tailored to those tasks. We don't have space to explore all such applications first-hand in this chapter, of course, but you should feel free to search the Web for additional use cases after studying the basics here.

Probably the reason for studying metaclasses most relevant to this book is that this topic can help demystify Python's class mechanics in general. For instance, we'll see that they are an intrinsic part of the language's new-style inheritance model finally formalized in full here. Although you may or may not code or reuse them in your work, a cursory understanding of metaclasses can impart a deeper understanding of Python at large.

## Increasing Levels of "Magic"
Most of this book has focused on straightforward application-coding techniques -- the modules, functions, and classes that most programmers spend their time writing to achieve real-world goals. The majority of Python's users may use classes and make instances, and might even do a bit of operator overloading, but they probably won't get too deep into the details of how their classes actually work.

However, in this book we've also seen a variety of tools that allow us to control Python's behavior in generic ways, and that often have more to do with Python internals or tool building than with application-programming domains. As a review, and to help us place metaclasses in the tools spectrum:
- **Introspection attributes and tools**
  Special attributes like \_\_class\_\_ and \_\_dict\_\_ allow us to inspect internal implementation aspects of Python objects, in order to process them generically -- to list all attributes of an object, display a class's name, and so on. As we've also seen, tools such as `dir` and `getattr` can serve similar roles when "virtual" attributes such as slots must be supported.
- **Operator overloading methods**
  Specially named methods such as \_\_str\_\_ and \_\_add\_\_ coded in classes intercept and provide behavior for built-in operations applied to class instances, such as printing, expression operators, and so on. They are run automatically in response to built-in operations and allow classes to conform to expected interfaces.
- **Attribute interception methods**
  A special category of operator overloading methods provides a way to intercept attribute accesses on instances generically: \_\_getattr\_\_, \_\_setattr\_\_, \_\_delattr\_\_, and \_\_getattribute\_\_ allow wrapper (a.k.a. proxy) classes to insert automatically run code that may validate attribute requests and delegate them to embedded objects. They allow any number of attributes of an object to be computed when accessed -- either selected attributes, or all of them.
- **Class properties**
  The property built-in allows us to associate code with a specific class attribute that is automatically run when the attribute is fetched, assigned, or deleted. Though not as generic as the prior paragraph's tools, properties allow for automatic code invocation on access to specific attributes.
- **Class attribute descriptors**
  Really, property is a succinct way to define an attribute descriptor that runs functions on access automatically. Descriptors allow us to code in a separate class \_\_get\_\_, \_\_set\_\_, and \_\_delete\_\_ handler methods that are run automatically when an attribute assigned to an instance of that class is accessed. They provide a general way to insert arbitrary code that is run implicitly when a specific attribute is accessed as part of the normal attribute lookup procedure.
- **Function and class decorators**
  As we saw in Chapter 39, the special @callable syntax for decorators allows us to add logic to be automatically run when a function is called or a class instance is created. This wrapper logic can trace or time calls, validate arguments, manage all instances of a class, augment instances with extra behavior such as attribute fetch validation, and more. Decorator syntax inserts name-rebinding logic to be run at the end of function and class definition statements -- decorated function and class names may be rebound to either augmented original objects, or to object proxies that intercept later calls.
- **Metaclasses**
  The last topic of magic introduced in Chapter 32, which we take up here.

As mentioned in this chapter's introduction, metaclasses are a continuation of this story -- they allow us to insert logic to be run automatically at the end of a class statement, when a class object is being created. Though strongly reminiscent of class decorators, the metaclass mechanism doesn't rebind the class name to a decorator callable's result, but rather routes creation of the class itself to specialized logic.

## A Language of Hooks
In other words, metaclasses are ultimately just another way to define automatically run code. With the tools listed in the prior section, Python provides ways for us to interject logic in a variety of contexts -- at operator evaluation, attribute access, function calls, class instance creation, and now class object creation. It's a language with hooks galore -- a feature open to abuse like any other, but one that also offers the flexibility that some programmers desire, and that some programs may require.

As we've also seen, many of these advanced Python tools have intersecting roles. For example, attributes can often be managed with properties, descriptors, or attribute interception methods. As we'll see in this chapter, class decorators and metaclasses can often be used interchangeably as well. By way of preview:
- Although class decorators are often used to manage instances, they can also be used to manage classes instead, much like metaclasses.
- Similarly, while metaclasses are designed to augment class construction, they can also insert proxies to manage instances instead, much like class decorators.

In fact, the main functional difference between these two tools is simply their place in the timing of class creation. As we saw in the prior chapter, class decorators run after the decorated class has already been created. Thus, they are often used to add logic to be run at instance creation time. When they do provide behavior for a class, it is typically through changes or proxies, instead of a more direct relationship.

As we'll see here, metaclasses, by contrast, run during class creation to make and return the new client class. Therefore, they are often used for managing or augmenting classes themselves, and can even provide methods to process the classes that are created from them, via a direct instance relationship.

For example, metaclasses can be used to add decoration to all methods of classes automatically, register all classes in use to an API, add user-interface logic to classes automatically, create or extend classes from simplified specifications in text files, and so on. Because they can control how classes are made -- and by proxy the behavior their instances acquire -- metaclass applicability is potentially very wide.

As we'll also see here, though, these two tools are more similar than different in many common roles. Since tool choices are sometimes partly subjective, knowledge of the alternatives can help you pick the right tool for a given task. To understand the options better, let's see how metaclasses stack up.

## The Downside of "Helper" Functions
Also like the decorators of the prior chapter, metaclasses are often optional from a theoretical perspective. We can usually achieve the same effect by passing class objects through manager functions -- sometimes known as helper functions -- much as we can achieve the goals of decorators by passing functions and instances through manager code. Just like decorators, though, metaclasses:
- Provide a more formal and explicit structure
- Help ensure that application programmers won't forget to augment their classes according to an API's requirements
- Avoid code redundancy and its associated maintenance costs by factoring class customization logic into a single location, the metaclass

To illustrate, suppose we want to automatically insert a method into a set of classes. Of course, we could do this with simple inheritance, if the subject method is known when we code the classes. In that case, we can simply code the method in a superclass and have all the classes in question inherit from it:
> 
> > ```python
> > class Extras:
> >     def extra(self, args): 				# Normal inheritance: too static
> >         ...
> > 
> > class Client1(Extras): ... 				# Clients inherit extra methods
> > class Client2(Extras): ...
> > class Client3(Extras): ...
> > 
> > X = Client1() 							# Make an instance
> > X.extra() 								# Run the extra methods
> > ```
> 
> Sometimes, though, it's impossible to predict such augmentation when classes are coded. Consider the case where classes are augmented in response to choices made in a user interface at runtime, or to specifications typed in a configuration file. Although we could code every class in our imaginary set to manually check these, too, it's a lot to ask of clients (required is abstract here -- it's something to be filled in):
> 
> > ```python
> > def extra(self, arg): ...
> > 
> > class Client1: ... 						# Client augments: too distributed
> > if required():
> >     Client1.extra = extra
> > 
> > class Client2: ...
> > if required():
> >     Client2.extra = extra
> > 
> > class Client3: ...
> >     if required():
> >         Client3.extra = extra
> > 
> > X = Client1()
> > X.extra()
> > ```
> 

We can add methods to a class after the class statement like this because a class-level method is just a function that is associated with a class and has a first argument to receive the self instance. Although this works, it might become untenable for larger method sets, and puts all the burden of augmentation on client classes (and assumes they'll remember to do this at all!).

It would be better from a maintenance perspective to isolate the choice logic in a single place. We might encapsulate some of this extra work by routing classes through a manager function -- such a manager function would extend the class as required and handle all the work of runtime testing and configuration:
> 
> > ```python
> > def extra(self, arg): ...
> > 
> > def extras(Class): 				# Manager function: too manual
> >     if required():
> >         Class.extra = extra
> > 
> > class Client1: ...
> > extras(Client1)
> > 
> > class Client2: ...
> > extras(Client2)
> > 
> > class Client3: ...
> > extras(Client3)
> > 
> > X = Client1()
> > X.extra()
> > ```
> 
> This code runs the class through a manager function immediately after it is created. Although manager functions like this one can achieve our goal here, they still put a fairly heavy burden on class coders, who must understand the requirements and adhere to them in their code. It would be better if there was a simple way to enforce the augmentation in the subject classes, so that they don't need to deal with the augmentation so explicitly, and would be less likely to forget to use it altogether. In other words, we'd like to be able to insert some code to run automatically at the end of a class statement, to augment the class.
> 
> This is exactly what metaclasses do -- by declaring a metaclass, we tell Python to route the creation of the class object to another class we provide:
> 
> > ```python
> > def extra(self, arg): ...
> > 
> > class Extras(type):
> >     def __init__(Class, classname, superclasses, attributedict):
> >         if required():
> >             Class.extra = extra
> > 
> > class Client1(metaclass=Extras): ... 				# Metaclass declaration only (3.X form)
> > class Client2(metaclass=Extras): ... 				# Client class is instance of meta
> > class Client3(metaclass=Extras): ...
> > 
> > X = Client1() 									# X is instance of Client1
> > X.extra()
> > ```
> 

Because Python invokes the metaclass automatically at the end of the class statement when the new class is created, it can augment, register, or otherwise manage the class as needed. Moreover, the only requirement for the client classes is that they declare the metaclass; every class that does so will automatically acquire whatever augmentation the metaclass provides, both now and in the future if the metaclass changes.

Of course, this is the standard rationale, which you'll need to judge for yourself -- in truth, clients might forget to list a metaclass just as easily as they could forget to call a manager function! Still, the explicit nature of metaclasses may make this less likely. Moreover, metaclasses have additional potentials we haven't yet seen. Although it may be difficult to glean from this small example, metaclasses generally handle such tasks better than more manual approaches.

## Metaclasses Versus Class Decorators: Round 1
Having said that, it's also important to note that the class decorators described in the preceding chapter sometimes overlap with metaclasses -- in terms of both utility and benefit. Although they are often used for managing instances, class decorators can also augment classes, independent of any created instances. Their syntax makes their usage similarly explicit, and arguably more obvious than manager function calls.

For example, suppose we coded our manager function to return the augmented class, instead of simply modifying it in place. This would allow a greater degree of flexibility, because the manager would be free to return any type of object that implements the class's expected interface:
> ```python
> def extra(self, arg): ...
> 
> def extras(Class):
>     if required():
>         Class.extra = extra
>     return Class
> 
> class Client1: ...
> Client1 = extras(Client1)
> 
> class Client2: ...
> Client2 = extras(Client2)
> 
> class Client3: ...
> Client3 = extras(Client3)
> 
> X = Client1()
> X.extra()
> ```

If you think this is starting to look reminiscent of class decorators, you're right. In the prior chapter we emphasized class decorators' role in augmenting instance creation calls. Because they work by automatically rebinding a class name to the result of a function, though, there's no reason that we can't use them to augment the class by changing it before any instances are ever created. That is, class decorators can apply extra logic to classes, not just instances, at class creation time:
> ```python
> def extra(self, arg): ...
> 
> def extras(Class):
>     if required():
>         Class.extra = extra
>     return Class
> 
> @extras
> class Client1: ... 			# Client1 = extras(Client1)
> 
> @extras
> class Client2: ... 			# Rebinds class independent of instances
> 
> @extras
> class Client3: ...
> 
> X = Client1() 				# Makes instance of augmented class
> X.extra() 					# X is instance of original Client1
> ```

Decorators essentially automate the prior example's manual name rebinding here. Just as for metaclasses, because this decorator returns the original class, instances are made from it, not from a wrapper object. In fact, instance creation is not intercepted at all in this example.

In this specific case -- adding methods to a class when it's created -- he choice between metaclasses and decorators is somewhat arbitrary. Decorators can be used to manage both instances and classes, and intersect most strongly with metaclasses in the second of these roles, but this discrimination is not absolute. In fact, the roles of each are determined in part by their mechanics.

As we'll see ahead, decorators technically correspond to metaclass \_\_init\_\_ methods, used to initialize newly created classes. Metaclasses have additional customization hooks beyond class initialization, though, and may perform arbitrary class construction tasks that might be more difficult with decorators. This can make them more complex, but also better suited for augmenting classes as they are being formed.

For example, metaclasses also have a \_\_new\_\_ method used to create a class, which has no analogy in decorators; making a new class in a decorator would incur an extra step. Moreover, metaclasses may also provide behavior acquired by classes in the form of methods, which have no direct counterpart in decorators either; decorators must provide class behavior is less direct ways.

Conversely, because metaclasses are designed to manage classes, applying them to managing instances alone is less optimal. Because they are also responsible for making the class itself, metaclasses incur this as an extra step in instance management roles. We'll explore these differences in code later in this chapter, and will flesh out this section's partial code into a real working example later in this chapter. To understand how metaclasses do their work, though, we first need to get a clearer picture of their underlying model.

> **There's Magic, and Then There's Magic**
> This chapter's "Increasing Levels of Magic" list deals with types of magic beyond those widely seen as beneficial by programmers. Some might add Python's functional tools like closures and generators, and even its basic OOP support, to this list -- the former relying on scope retention and automatic generator object creation, and the latter on inheritance attribute search and a special first function argument. Though based on magic too, these represent paradigms that ease the task of programming by providing abstractions above and beyond the underlying hardware architecture.
> 
> For example, OOP -- Python's earlier paradigm -- is broadly accepted in the software world. It provides a model for writing programs that is more complete, explicit, and richly structured than functional tools. That is, some levels of magic are considered more warranted than others; after all, if it were not for some magic, programs would still consist of machine code (or physical switches).
> 
> It's usually the accumulation of new magic that puts systems at risk of breaching a complexity threshold -- such as adding a functional paradigm to what was always an OO language, or adding redundant or advanced ways to achieve goals that are rarely pursued in the common practice of most users. Such magic can set the entry bar far too high for a large part of your tool's audience.
> 
> Moreover, some magic is imposed on its users more than others. The translation step of a compiler, for instance, does not generally require its users to be compiler developers. By contrast, Python's super assumes full mastery and deployment of the arguably obscure and artificial MRO algorithm. The new-style inheritance algorithm presented in this chapter similarly assumes descriptors, metaclasses, and the MRO as its prerequisites -- all advanced tools in their own right. Even implicit "hooks" like descriptors remain implicit only until their first failure or maintenance cycle. Such magic exposed escalates a tool's prerequisites and downgrades its usability.
> 
> In open source systems, only time and downloads can determine where such thresholds may lie. Finding the proper balance of power and complexity depends as much on shifting opinion as on technology. Subjective factors aside, though, new magic that imposes itself on users inevitably skews a system's learning curve higher -- a topic we'll return to in the next chapter's final words.
>


