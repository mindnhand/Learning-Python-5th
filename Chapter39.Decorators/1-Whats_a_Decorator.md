In the advanced class topics chapter of this book (Chapter 32), we met static and class methods, took a quick look at the @ decorator syntax Python offers for declaring them, and previewed decorator coding techniques. We also met function decorators briefly in Chapter 38, while exploring the property built-in's ability to serve as one, and in Chapter 29 while studying the notion of abstract superclasses.

This chapter picks up where this previous decorator coverage left off. Here, we'll dig deeper into the inner workings of decorators and study more advanced ways to code new decorators ourselves. As we'll see, many of the concepts we studied earlier -- especially state retention -- show up regularly in decorators.

This is a somewhat advanced topic, and decorator construction tends to be of more interest to tool builders than to application programmers. Still, given that decorators are becoming increasingly common in popular Python frameworks, a basic understanding can help demystify their role, even if you’re just a decorator user.

Besides covering decorator construction details, this chapter serves as a more realistic case study of Python in action. Because its examples grow somewhat larger than most of the others we've seen in this book, they better illustrate how code comes together into more complete systems and tools. As an extra perk, some of the code we'll write here may be used as general-purpose tools in your day-to-day programs.

# What's a Decorator
Decoration is a way to specify management or augmentation code for functions and classes. Decorators themselves take the form of callable objects (e.g., functions) that process other callable objects. As we saw earlier in this book, Python decorators come in two related flavors, neither of which requires 3.X or new-style classes:
- Function decorators, added in Python 2.4, do name rebinding at function definition time, providing a layer of logic that can manage functions and methods, or later calls to them.
- Class decorators, added in Python 2.6 and 3.0, do name rebinding at class definition time, providing a layer of logic that can manage classes, or the instances created by later calls to them.

In short, decorators provide a way to insert automatically run code at the end of function and class definition statements -- at the end of a def for function decorators, and at the end of a class for class decorators. Such code can play a variety of roles, as described in the following sections.

## Managing Calls and Instances
In typical use, this automatically run code may be used to augment calls to functions and classes. It arranges this by installing wrapper (a.k.a. proxy) objects to be invoked later:
- **Call proxies**
  Function decorators install wrapper objects to intercept later function calls and process them as needed, usually passing the call on to the original function to run the managed action.
- **Interface proxies**
  Class decorators install wrapper objects to intercept later instance creation calls and process them as required, usually passing the call on to the original class to create a managed instance.

Decorators achieve these effects by automatically rebinding function and class names to other callables, at the end of def and class statements. When later invoked, these callables can perform tasks such as tracing and timing function calls, managing access to class instance attributes, and so on.

## Managing Functions and Classes
Although most examples in this chapter deal with using wrappers to intercept later calls to functions and classes, this is not the only way decorators can be used:
- **Function managers**
  Function decorators can also be used to manage function objects, instead of or in addition to later calls to them -- to register a function to an API, for instance. Our primary focus here, though, will be on their more commonly used call wrapper application.
- **Class managers**
  Class decorators can also be used to manage class objects directly, instead of or in addition to instance creation calls -- to augment a class with new methods, for example. Because this role intersects strongly with that of metaclasses, we'll see additional use cases in the next chapter. As we'll find, both tools run at the end of the class creation process, but class decorators often offer a lighter-weight solution.

In other words, function decorators can be used to manage both function calls and function objects, and class decorators can be used to manage both class instances and classes themselves. By returning the decorated object itself instead of a wrapper, decorators become a simple post-creation step for functions and classes.

Regardless of the role they play, decorators provide a convenient and explicit way to code tools useful both during program development and in live production systems.

## Using and Defining Decorators
Depending on your job description, you might encounter decorators as a user or a provider (you might also be a maintainer, but that just means you straddle the fence). As we've seen, Python itself comes with built-in decorators that have specialized roles -- static and class method declaration, property creation, and more. In addition, many popular Python toolkits include decorators to perform tasks such as managing database or user-interface logic. In such cases, we can get by without knowing how the decorators are coded.

For more general tasks, programmers can code arbitrary decorators of their own. For example, function decorators may be used to augment functions with code that adds call tracing or logging, performs argument validity testing during debugging, automatically acquires and releases thread locks, times calls made to functions for optimization, and so on. Any behavior you can imagine adding to -- really, wrapping around -- a function call is a candidate for custom function decorators.

On the other hand, function decorators are designed to augment only a specific function or method call, not an entire object interface. Class decorators fill the latter role better -- because they can intercept instance creation calls, they can be used to implement arbitrary object interface augmentation or management tasks. For example, custom class decorators can trace, validate, or otherwise augment every attribute reference made for an object. They can also be used to implement proxy objects, singleton classes, and other common coding patterns. In fact, we'll find that many class decorators bear a strong resemblance to -- and in fact are a prime application of -- the delegation coding pattern we met in Chapter 31.

## Why Decorators?
Like many advanced Python tools, decorators are never strictly required from a purely technical perspective: we can often implement their functionality instead using simple helper function calls or other techniques. And at a base level, we can always manually code the name rebinding that decorators perform automatically.

That said, decorators provide an explicit syntax for such tasks, which makes intent clearer, can minimize augmentation code redundancy, and may help ensure correct API usage:
- Decorators have a very explicit syntax, which makes them easier to spot than helper function calls that may be arbitrarily far-removed from the subject functions or classes.
- Decorators are applied once, when the subject function or class is defined; it's not necessary to add extra code at every call to the class or function, which may have to be changed in the future.
- Because of both of the prior points, decorators make it less likely that a user of an API will forget to augment a function or class according to API requirements.

In other words, beyond their technical model, decorators offer some advantages in terms of both code maintenance and consistency. Moreover, as structuring tools, decorators naturally foster encapsulation of code, which reduces redundancy and makes future changes easier.
Decorators do have some potential drawbacks, too -- when they insert wrapper logic, they can alter the types of the decorated objects, and they may incur extra calls when used as call or interface proxies. On the other hand, the same considerations apply to any technique that adds wrapping logic to objects.

We'll explore these tradeoffs in the context of real code later in this chapter. Although the choice to use decorators is still somewhat subjective, their advantages are compelling enough that they are quickly becoming best practice in the Python world. To help you decide for yourself, let's turn to the details.

> **Decorators versus macros:** Python's decorators bear similarities to what some call aspect-oriented programming in other languages -- code inserted to run automatically before or after a function call runs. Their syntax also very closely resembles (and is likely borrowed from) Java's annotations, though Python's model is usually considered more flexible and general.

Some liken decorators to macros too, but this isn't entirely apt, and might even be misleading. Macros (e.g., C's #define preprocessor directive) are typically associated with textual replacement and expansion, and designed for generating code. By contrast, Python's decorators are a runtime operation, based upon name rebinding, callable objects, and often, proxies. While the two may have use cases that sometimes overlap, decorators and macros are fundamentally different in scope, implementation, and coding patterns. Comparing the two seems akin to comparing Python's import with a C #include, which similarly confuses a runtime object-based operation with text insertion.

Of course, the term macro has been a bit diluted over time -- to some, it now can also refer to any canned series of steps or procedure -- and users of other languages might find the analogy to descriptors useful anyhow. But they should probably also keep in mind that decorators are about callable objects managing callable objects, not text expansion. Python tends to be best understood and used in terms of Python idioms.

