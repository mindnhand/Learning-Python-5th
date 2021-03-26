# The super Built-in Function: For Better or Worse?
So far, I've mentioned Python's super built-in function only briefly in passing because it is relatively uncommon and may even be controversial to use. Given this call's increased visibility in recent years, though, it merits some further elaboration in this edition. Besides introducing super, this section also serves as a language design case study to close out a chapter on so many tools whose presence may to some seem curious in a scripting language like Python.

Some of this section calls this proliferation of tools into question, and I encourage you to judge any subjective content here for yourself (and we'll return to such things at the end of this book after we've expanded on other advanced tools such as metaclasses and descriptors). Still, Python's rapid growth rate in recent years represents a strategic decision point for its community going forward, and super seems as good a representative example as any.

## The Great super Debate
As noted in Chapter 28 and Chapter 29, Python has a super built-in function that can be used to invoke superclass methods generically, but was deferred until this point of the book. This was deliberate -- because super has substantial downsides in typical code, and a sole use case that seems obscure and complex to many observers, most beginners are better served by the traditional explicit-name call scheme used so far. See the sidebar "What About super?" on page 831 in Chapter 28 for a brief summary of the rationale for this policy.

The Python community itself seems split on this subject, with online articles about it running the gamut from "Python's Super Considered Harmful" to "Python's super() considered super!" Frankly, in my live classes this call seems to be most often of interest to Java programmers starting to use Python anew, because of its conceptual similarity to a tool in that language (many a new Python feature ultimately owes its existence to programmers of other languages bringing their old habits to a new model). Python's super is not Java's -- it translates differently to Python's multiple inheritance, and has a use case beyond Java's -- but it has managed to generate both controversy and misunderstanding since its conception.

This book postponed the super call until now (and omitted it almost entirely in prior editions) because it has significant issues -- it's prohibitively cumbersome to use in 2.X, differs in form between 2.X and 3.X, is based upon unusual semantics in 3.X, and mixes poorly with Python's multiple inheritance and operator overloading in typical Python code. In fact, as we'll see, in some code super can actually mask problems, and discourage a more explicit coding style that offers better control.

In its defense, this call does have a valid use case too -- cooperative same-named method dispatch in diamond multiple inheritance trees—but it seems to ask a lot of newcomers. It requires that super be used universally and consistently (if not neurotically), much like \_\_slots\_\_ discussed earlier; relies on the arguably obscure MRO algorithm to order calls; and addresses a use case that seems far more the exception than the norm in Python programs. In this role, super seems an advanced tool based upon esoteric principles, which may be beyond much of Python’s audience, and seems artificial to real program goals. That aside, its expectation of universal use seems unrealistic for the vast amount of existing Python code.

Because of all these factors, this introductory-level book has preferred the traditional explicit-name call scheme thus far and recommends the same for newcomers. You're better off learning the traditional scheme first, and might be better off sticking with that in general, rather than using an extra special-case tool that may not work in some contexts, and relies on arcane magic in the valid but atypical use case it addresses. This is not just your author's opinion; despite its advocate's best intentions, super is not widely recognized as "best practice" in Python today, for completely valid reasons.

On the other hand, just as for other tools the increasing use of this call in Python code in recent years makes it no longer optional for many Python programmers -- the first time you see it, it's officially mandatory! For readers who may wish to experiment with super, and for other readers who may have it imposed upon them, this section provides a brief look at this tool and its rationale -- beginning with alternatives to it.

## Traditional Superclass Call Form: Portable, General
In general, this book's examples prefer to call back to superclass methods when needed by naming the superclass explicitly, because this technique is traditional in Python, because it works the same in both Python 2.X and 3.X, and because it sidesteps limitations and complexities related to this call in both 2.X and 3.X. As shown earlier, the traditional superclass method call scheme to augment a superclass method works as follows:
> ```python
> >>> class C: 				# In Python 2.X and 3.X
>         def act(self):
>             print('spam')
> 
> >>> class D(C):
>         def act(self):
>             C.act(self) 				# Name superclass explicitly, pass self
>             print('eggs')
> 
> >>> X = D()
> >>> X.act()
> spam
> eggs
> ```

This form works the same in 2.X and 3.X, follows Python's normal method call mapping model, applies to all inheritance tree forms, and does not lead to confusing behavior when operator overloading is used. To see why these distinctions matter, let's see how super compares.

## Basic super Usage and Its Tradeoffs
In this section, we'll both introduce super in basic, single-inheritance mode, and look at its perceived downsides in this role. As we'll find, in this context super does work as advertised, but is not much different from traditional calls, relies on unusual semantics, and is cumbersome to deploy in 2.X. More critically, as soon as your classes grow to use multiple inheritance, this super usage mode can both mask problems in your code and route calls in ways you may not expect.

### Odd semantics: A magic proxy in Python 3.X
The super built-in actually has two intended roles. The more esoteric of these -- cooperative multiple inheritance dispatch protocols in diamond multiple-inheritance trees (yes, a mouthful!) -- relies on the 3.X MRO, was borrowed from the Dylan language, and will be covered later in this section.

The role we're interested in here is more commonly used, and more frequently requested by people with Java backgrounds -- to allow superclasses to be named generically in inheritance trees. This is intended to promote simpler code maintenance, and to avoid having to type long superclass reference paths in calls. In Python 3.X, this call seems at least at first glance to achieve this purpose well:
> ```python
> >>> class C: 					# In Python 3.X (only: see 2.X super form ahead)
>         def act(self):
>             print('spam')
> 
> >>> class D(C):
>         def act(self):
>             super().act() 					# Reference superclass generically, omit self
>             print('eggs')
> 
> >>> X = D()
> >>> X.act()
> spam
> eggs
> ```

This works, and minimizes code changes -- you don't need to update the call if D's superclass changes in the future. One of the biggest downsides of this call in 3.X, though, is its reliance on deep magic: though prone to change, it operates today by inspecting the call stack in order to automatically locate the self argument and find the superclass, and pairs the two in a special proxy object that routes the later call to the superclass version of the method. If that sounds complicated and strange, it's because it is. In fact, this call form doesn't work at all outside the context of a class's method:
> ```python
> >>> super 					# A "magic" proxy object that routes later calls
> <class 'super'>
> >>> super()
> SystemError: super(): no arguments
> >>> class E(C):
>         def method(self): 			# self is implicit in super...only!
>             proxy = super() 				# This form has no meaning outside a method
>             print(proxy) 					# Show the normally hidden proxy object
>             proxy.act() 					# No arguments: implicitly calls superclass method!
> 
> >>> E().method()
> <super: <class 'E'>, <E object>>
> spam
> ```

Really, this call's semantics resembles nothing else in Python -- it's neither a bound nor unbound method, and somehow finds a self even though you omit one in the call. In single inheritance trees, a superclass is available from self via the path self.\_\_class\_\_.\_\_bases\_\_[0], but the heavily implicit nature of this call makes this difficult to see, and even flies in the face of Python's explicit self policy that holds true everywhere else. That is, this call violates a fundamental Python idiom for a single use case. It also soundly contradicts Python's longstanding EIBTI design rule (run an "import this" for more on this rule).

### Pitfall: Adding multiple inheritance naively
Besides its unusual semantics, even in 3.X this super role applies most directly to single inheritance trees, and can become problematic as soon as classes employ multiple inheritance with traditionally coded classes. This seems a major limitation of scope; due to the utility of mix-in classes in Python, multiple inheritance from disjoint and independent superclasses is probably more the norm than the exception in realistic code.

The super call seems a recipe for disaster in classes coded to naively use its basic mode, without allowing for its much more subtle implications in multiple inheritance trees. The following illustrates the trap. This code begins its life happily deploying super in single-inheritance mode to invoke a method one level up from C:
> ```python
> >>> class A: 				# In Python 3.X
>         def act(self): print('A')
> >>> class B:
>         def act(self): print('B')
> >>> class C(A):
>         def act(self):
>         super().act() 			# super applied to a single-inheritance tree
> 
> >>> X = C()
> >>> X.act()
> A
> ```

If such classes later grow to use more than one superclass, though, super can become error-prone, and even unusable -- it does not raise an exception for multiple inheritance trees, but will naively pick just the leftmost superclass having the method being run (technically, the first per the MRO), which may or may not be the one that you want:
> ```python
> >>> class C(A, B): 					# Add a B mix-in class with the same method
>         def act(self):
>             super().act() 			# Doesn't fail on multi-inher, but picks just one!
> >>> X = C()
> >>> X.act()
> A
> >>> class C(B, A):
>         def act(self):
>             super().act()				# If B is listed first, A.act() is no longer run!
> >>> X = C()
> >>> X.act()
> B
> ```

Perhaps worse, this silently masks the fact that you should probably be selecting superclasses explicitly in this case, as we learned earlier in both this chapter and its predecessor. In other words, super usage may obscure a common source of errors in Python -- one so common that it shows up again in this part's "Gotchas." If you may need to use direct calls later, why not use them earlier too?
> ```python
> >>> class C(A, B): 				# Traditional form
>         def act(self): 			# You probably need to be more explicit here
>             A.act(self) 			# This form handles both single and multiple inher
>             B.act(self) 			# And works the same in both Python 3.X and 2.X
> >>> X = C() 						# So why use the super() special case at all?
> >>> X.act()
> A
> B
> ```

As we'll see in a few moments, you might also be able to address such cases by deploying super calls in every class of the tree. But that's also one of the biggest downsides of super -- why code it in every class, when it's usually not needed, and when using the preceding simpler traditional form in a single class will usually suffice? Especially in existing code -- and new code that uses existing code -- this super requirement seems harsh, if not unrealistic.

Much more subtly, as we'll also see ahead, once you step up to multiple inheritance calls this way, the super calls in your code might not invoke the class you expect them to. They'll be routed per the MRO order, which, depending on where else super might be used, may invoke a method in a class that is not the caller's superclass at all -- an implicit ordering that might make for interesting debugging sessions! Unless you completely understand what super means once multiple inheritance is introduced, you may be better off not deploying it in single-inheritance mode either.

This coding situation isn't nearly as abstract as it may seem. Here's a real-world example of such a case, taken from the PyMailGUI case study in Programming Python -- the following very typical Python classes use multiple inheritance to mix in both application logic and window tools from independent, standalone classes, and hence must invoke both superclass constructors explicitly with direct calls by name. As coded, a super().\_\_init\_\_() here would run only one constructor, and adding super throughout this example's disjoint class trees would be more work, would be no simpler, and wouldn't make sense in tools meant for arbitrary deployment in clients that may use super or not:
> ```python
> class PyMailServerWindow(PyMailServer, windows.MainWindow):
>     "a Tk, with extra protocol and mixed-in methods"
>     def __init__(self):
>         windows.MainWindow.__init__(self, appname, srvrname)
>         PyMailServer.__init__(self)
> 
> class PyMailFileWindow(PyMailFile, windows.PopupWindow):
>     "a Toplevel, with extra protocol and mixed-in methods"
>     def __init__(self, filename):
>         windows.PopupWindow.__init__(self, appname, filename)
>         PyMailFile.__init__(self, filename)
> ```

The crucial point here is that using super for just the single inheritance cases where it applies most clearly is a potential source of error and confusion, and means that programmers must remember two ways to accomplish the same goal, when just one -- explicit direct calls -- could suffice for all cases.

In other words, unless you can be sure that you will never add a second superclass to a class in a tree over your software's entire lifespan, you cannot use super in singleinheritance mode without understanding and allowing for its much more sophisticated role in multiple-inheritance trees. We'll discuss the latter ahead, but it's not optional if you deploy super at all.

From a more practical view, it's also not clear that the trivial amount of code maintenance that this super role is envisioned to avoid fully justifies its presence. In Python practice, superclass names in headers are rarely changed; when they are, there are usually at most a very small number of superclass calls to update within the class. And consider this: if you add a new superclass in the future that doesn't use super (as in the preceding example), you'll have to either wrap it in an adaptor proxy or augment all the super calls in your class to use the traditional explicit-name call scheme anyhow -- a maintenance task that seems just as likely, but perhaps more error-prone if you've grown to rely on super magic.

### Limitation: Operator overloading
As briefly noted in Python's library manual, super also doesn't fully work in the presence of \_\_X\_\_ operator overloading methods. If you study the following code, you'll see that direct named calls to overload methods in the superclass operate normally, but using the super result in an expression fails to dispatch to the superclass's overload method:
> ```python
> >>> class C: 								# In Python 3.X
>         def __getitem__(self, ix): 		# Indexing overload method
>             print('C index')
> >>> class D(C):
>         def __getitem__(self, ix): 		# Redefine to extend here
>             print('D index')
>             C.__getitem__(self, ix) 		# Traditional call form works
>             super().__getitem__(ix) 		# Direct name calls work too
>             super()[ix] 					# But operators do not! (__getattribute__)
> 
> >>> X = C()
> >>> X[99]
> C index
> >>> X = D()
> >>> X[99]
> D index
> C index
> C index
> Traceback (most recent call last):
> File "", line 1, in
> File "", line 6, in __getitem__
> TypeError: 'super' object is not subscriptable
> ```

This behavior is due to the very same new-style (and 3.X) class change described earlier in this chapter (see "Attribute Fetch for Built-ins Skips Instances" on page 987) -- because the proxy object returned by super uses \_\_getattribute\_\_ to catch and dispatch later method calls, it fails to intercept the automatic \_\_X\_\_ method invocations run by built-in operations including expressions, as these begin their search in the class instead of the instance. This may seem less severe than the multiple-inheritance limitation, but operators should generally work the same as the equivalent method call, especially for a built-in like this. Not supporting this adds another exception for super users to confront and remember.

Other languages' mileage may vary, but in Python, self is explicit, multiple-inheritance mix-ins and operator overloading are common, and superclass name updates are rare. Because super adds an odd special case to the language -- one with strange semantics, limited scope, rigid requirements, and questionable reward -- most Python programmers may be better served by the more broadly applicable traditional call scheme. While super has some advanced applications too that we'll study ahead, they may be too obscure to warrant making it a mandatory part of every Python programmer's toolbox.

### Use differs in Python 2.X: Verbose calls
If you are a Python 2.X user reading this dual-version book, you should also know that the super technique is not portable between Python lines. Its form differs between 2.X and 3.X -- and not just between classic and new-style classes. It's really a different tool in 2.X, which cannot run 3.X's simpler form.

To make this call work in Python 2.X, you must first use new-style classes. Even then, you must also explicitly pass in the immediate class name and self to super, making this call so complex and verbose that in most cases it's probably easier to avoid it completely, and simply name the superclass explicitly per the previous traditional code pattern (for brevity, I'll leave it to readers to consider what changing a class's own name means for code maintenance when using the 2.X super form!):
> ```python
> >>> class C(object): 				# In Python 2.X: for new-style classes only
>         def act(self):
>             print('spam')
> 
> >>> class D(C):
>         def act(self):
>             super(D, self).act() 	# 2.X: different call format - seems too complex
>             print('eggs') 		# "D" may be just as much to type/change as "C"!
> 
> >>> X = D()
> >>> X.act()
> spam
> eggs
> ```

Although you can use the 2.X call form in 3.X for backward compatibility, it's too cumbersome to deploy in 3.X-only code, and the more reasonable 3.X form is not usable in 2.X:
> ```python
> >>> class D(C):
>         def act(self):
>             super().act() 			# Simpler 3.X call format fails in 2.X
>             print('eggs')
> 
> >>> X = D()
> >>> X.act()
> TypeError: super() takes at least 1 argument (0 given)
> ```

On the other hand, the traditional call form with explicit class names works in 2.X in both classic and new-style classes, and exactly as it does in 3.X:
> ```python
> >>> class D(C):
>         def act(self):
>         C.act(self) 				# But traditional pattern works portably
>         print('eggs') 			# And may often be simpler in 2.X code
> 
> >>> X = D()
> >>> X.act()
> spam
> eggs
> ```

So why use a technique that works in only limited contexts instead of one that works in many more? Though its basis is complex, the next sections attempt to rally support for the super cause.

## The super Upsides: Tree Changes and Dispatch
Having just shown you the downsides of super, I should also confess that I've been tempted to use this call in code that would only ever run on 3.X, and which used a very long superclass reference path through a module package (that is, mostly for laziness, but coding brevity can matter too). To be fair, super may still be useful in some use cases, the chief among which merit a brief introduction here:
- Changing class trees at runtime: When a superclass may be changed at runtime, it's not possible to hardcode its name in a call expression, but it is possible to dispatch calls via super.
  On the other hand, this case is extremely rare in Python programming, and other techniques can often be used in this context as well.
- Cooperative multiple inheritance method dispatch: When multiple inheritance trees must dispatch to the same-named method in multiple classes, super can provide a protocol for orderly call routing.
  On the other hand, the class tree must rely upon the ordering of classes by the MRO -- a complex tool in its own right that is artificial to the problem a program is meant to address -- and must be coded or augmented to use super in each version of the method in the tree to be effective. Such dispatch can also often be implemented in other ways (e.g., via instance state).

As discussed earlier, super can also be used to select a superclass generically as long as the MRO's default makes sense, though in traditional code naming a superclass explicitly is often preferable, and may even be required. Moreover, even valid super use cases tend to be uncommon in many Python programs -- to the point of seeming academic curiosity to some. The two cases just listed, however, are most often cited as super rationales, so let's take a quick look at each.

## Runtime Class Changes and super
Superclass that might be changed at runtime dynamically preclude hardcoding their names in a subclass's methods, while super will happily look up the current superclass dynamically. Still, this case may be too rare in practice to warrant the super model by itself, and can often be implemented in other ways in the exceptional cases where it is needed. To illustrate, the following changes the superclass of C dynamically by changing the subclass's \_\_bases\_\_ tuple in 3.X:
> ```python
> >>> class X:
>         def m(self): print('X.m')
> >>> class Y:
>         def m(self): print('Y.m')
> 
> >>> class C(X): 					# Start out inheriting from X
>         def m(self): super().m() 	# Can't hardcode class name here
> 
> >>> i = C()
> >>> i.m()
> X.m
> >>> C.__bases__ = (Y,) 			# Change superclass at runtime!
> >>> i.m()
> Y.m
> ```

This works (and shares behavior-morphing goals with other deep magic, such as changing an instance's \_\_class\_\_), but seems rare in the extreme. Moreover, there may be other ways to achieve the same effect -- perhaps most simply, calling through the current superclass tuple's value indirectly: special code to be sure, but only for a very special case (and perhaps not any more special than implicit routing by MROs):
> ```python
> >>> class C(X):
>         def m(self): C.__bases__[0].m(self) 		# Special code for a special case
> >>> i = C()
> >>> i.m()
> X.m
> >>> C.__bases__ = (Y,) 			# Same effect, without super()
> >>> i.m()
> Y.m
> ```

Given the preexisting alternatives, this case alone doesn't seem to justify super, though in more complex trees, the next rationale -- based on the tree's MRO order instead of physical superclass links -- may apply here as well.

## Cooperative Multiple Inheritance Method Dispatch
The second of the use cases listed earlier is the main rationale commonly given for super, and also borrows from other programming languages (most notably, Dylan), where its use case may be more common than it is in typical Python code. It generally applies to diamond pattern multiple inheritance trees, discussed earlier in this chapter, and allows for cooperative and conformant classes to route calls to a same-named method coherently among multiple class implementations. Especially for constructors, which have multiple implementations normally, this can simplify call routing protocol when used consistently.

In this mode, each super call selects the method from a next class following it in the MRO ordering of the class of the self subject of a method call. The MRO was introduced earlier; it's the path Python follows for inheritance in new-style classes. Because the MRO's linear ordering depends on which class self was made from, the order of method dispatch orchestrated by super can vary per class tree, and visits each class just once as long as all classes use super to dispatch.

Since every class participates in a diamond under object in 3.X (and 2.X new-style classes), the applications are broader than you might expect. In fact, some of the earlier examples that demonstrated super shortcomings in multiple inheritance trees could use this call to achieve their dispatch goals. To do so, however, super must be used universally in the class tree to ensure that method call chains are passed on -- a fairly major requirement that may be difficult to enforce in much existing and new code.

### The basics: Cooperative super call in action
Let's take a look at what this role means in code. In this and the following sections, we'll both learn how super works, and explore the tradeoffs it implies along the way. To get started, consider the following traditionally coded Python classes (condensed somewhat here as usual for space):
> ```python
> >>> class B:
>         def __init__(self): print('B.__init__') 				# Disjoint class tree branches
> >>> class C:
>         def __init__(self): print('C.__init__')
> >>> class D(B, C): pass
> >>> x = D() 					# Runs leftmost only by default
> B.__init__
> ```

In this case, superclass tree branches are disjoint (they don't share a common explicit ancestor), so subclasses that combine them must call through each superclass by name -- a common situation in much existing Python code that super cannot address directly without code changes:
> ```python
> >>> class D(B, C):
>         def __init__(self): 			# Traditional form
>             B.__init__(self) 			# Invoke supers by name
>             C.__init__(self)
> 
> >>> x = D()
> B.__init__
> C.__init__
> ```

In diamond class tree patterns, though, explicit-name calls may by default trigger the top-level class's method more than once, though this might be subverted with additional protocols (e.g., status markers in the instance):
> ```python
> >>> class A:
>         def __init__(self): print('A.__init__')
> >>> class B(A):
>         def __init__(self): print('B.__init__'); A.__init__(self)
> >>> class C(A):
>         def __init__(self): print('C.__init__'); A.__init__(self)
> >>> x = B()
> B.__init__
> A.__init__
> >>> x = C() 					# Each super works by itself
> C.__init__
> A.__init__
> >>> class D(B, C): pass 		# Still runs leftmost only
> >>> x = D()
> B.__init__
> A.__init__
> >>> class D(B, C):
>         def __init__(self): 	# Traditional form
>             B.__init__(self)  # Invoke both supers by name
>             C.__init__(self)
> >>> x = D() 					# But this now invokes A twice!
> B.__init__
> A.__init__
> C.__init__
> A.__init__
> ```

By contrast, if all classes use super, or are appropriately coerced by proxies to behave as if they do, the method calls are dispatched according to class order in the MRO, such that the top-level class's method is run just once:
> ```python
> >>> class A:
>         def __init__(self): print('A.__init__')
> >>> class B(A):
>         def __init__(self): print('B.__init__'); super().__init__()
> >>> class C(A):
>         def __init__(self): print('C.__init__'); super().__init__()
> >>> x = B() 				# Runs B.__init__, A is next super in self's B MRO
> B.__init__
> A.__init__
> >>> x = C()
> C.__init__
> A.__init__
> >>> class D(B, C): pass
> >>> x = D() 				# Runs B.__init__, C is next super in self's D MRO!
> B.__init__
> C.__init__
> A.__init__
> ```

The real magic behind this is the linear MRO list constructed for the class of self -- because each class appears just once on this list, and because super dispatches to the next class on this list, it ensures an orderly invocation chain that visits each class just once. Crucially, the next class following B in the MRO differs depending on the class of self -- it's A for a B instance, but C for a D instance, accounting for the order of constructors run:
> ```python
> >>> B.__mro__
> (<class '__main__.B'>, <class '__main__.A'>, <class 'object'>)
> >>> D.__mro__
> (<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>,
> <class '__main__.A'>, <class 'object'>)
> ```

The MRO and its algorithm were presented earlier in this chapter. By selecting a next class in the MRO sequence, a super call in a class's method propagates the call through the tree, so long as all classes do the same. In this mode super does not necessarily choose a superclass at all; it picks the next in the linearized MRO, which might be a sibling -- or even a lower relative -- in the class tree of a given instance. See "Tracing the MRO" on page 1002 for other examples of the path super dispatch would follow, especially for nondiamonds.

The preceding works -- and may even seem clever at first glance -- but its scope may also appear limited to some. Most Python programs do not rely on the nuances of diamond pattern multiple inheritance trees (in fact, many Python programmers I've met do not know what the term means!). Moreover, super applies most directly to single inheritance and cooperative diamond cases, and may seem superfluous for disjoint nondiamond cases, where we might want to invoke superclass methods selectively or independently. Even cooperative diamonds can be managed in other ways that may afford programmers more control than an automatic MRO ordering can. To evaluate this tool objectively, though, we need to look deeper.

### Constraint: Call chain anchor requirement
The super call comes with complexities that may not be apparent on first encounter, and may even seem initially like features. For example, because all classes inherit from object in 3.X automatically (and explicitly in 2.X new-style classes), the MRO ordering can be used even in cases where the diamond is only implicit -- in the following, triggering constructors in independent classes automatically:
> ```python
> >>> class B:
>         def __init__(self): print('B.__init__'); super().__init__()
> >>> class C:
>         def __init__(self): print('C.__init__'); super().__init__()
> >>> x = B()    			# object is an implied super at the end of MRO
> B.__init__
> >>> x = C()
> C.__init__
> >>> class D(B, C): pass 	# Inherits B.__init__ but B's MRO differs for D
> >>> x = D() 				# Runs B.__init__, C is next super in self's D MRO!
> B.__init__
> C.__init__
> ```

Technically, this dispatch model generally requires that the method being called by super must exist, and must have the same argument signature across the class tree, and every appearance of the method but the last must use super itself. This prior example works only because the implied object superclass at the end of the MRO of all three classes happens to have a compatible \_\_init\_\_ that satisfies these rules:
> ```python
> >>> B.__mro__
> (<class '__main__.B'>, <class 'object'>)
> >>> D.__mro__
> (<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class 'object'>)
> ```

Here, for a D instance, the next class in the MRO after B is C, which is followed by object whose \_\_init\_\_ silently accepts the call from C and ends the chain. Thus, B's method calls C's, which ends in object's version, even though C is not a superclass to B.

Really, though, this example is atypical -- and perhaps even lucky. In most cases, no such suitable default will exist in object, and it may be less trivial to satisfy this model's expectations. Most trees will require an explicit -- and possibly extra -- superclass to serve the anchoring role that object does here, to accept but not forward the call. Other trees may require careful design to adhere to this requirement. Moreover, unless Python optimizes it away, the call to object (or other anchor) defaults at the end of the chain may also add extra performance costs.

By contrast, in such cases direct calls incur neither extra coding requirements nor added performance cost, and make dispatch more explicit and direct:
> ```python
> >>> class B:
>         def __init__(self): print('B.__init__')
> >>> class C:
>         def __init__(self): print('C.__init__')
> >>> class D(B, C):
>         def __init__(self): B.__init__(self); C.__init__(self)
> >>> x = D()
> B.__init__
> C.__init__
> ```

### Scope: An all-or-nothing model
Also keep in mind that traditional classes that were not written to use super in this role cannot be directly used in such cooperative dispatch trees, as they will not forward calls along the MRO chain. It's possible to incorporate such classes with proxies that wrap the original object and add the requisite super calls, but this imposes both additional coding requirements and performance costs on the model. Given that there are many millions of lines of existing Python code that do not use super, this seems a major detriment.

Watch what happens, for example, if any one class fails to pass along the call chain by omitting a super, ending the call chain prematurely -- like \_\_slots\_\_, super is generally an all-or-nothing feature:
> ```python
> >>> class B:
>         def __init__(self): print('B.__init__'); super().__init__()
> >>> class C:
>         def __init__(self): print('C.__init__'); super().__init__()
> >>> class D(B, C):
>         def __init__(self): print('D.__init__'); super().__init__()
> >>> X = D()
> D.__init__
> B.__init__
> C.__init__
> >>> D.__mro__
> (<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class 'object'>)
> # What if you must use a class that doesn't call super?
> >>> class B:
>         def __init__(self): print('B.__init__')
> >>> class D(B, C):
>         def __init__(self): print('D.__init__'); super().__init__()
> >>> X = D()
> D.__init__
> B.__init__ 					# It's an all-or-nothing tool...
> ```

Satisfying this mandatory propagation requirement may be no simpler than direct byname calls -- which you might still forget, but which you won't need to require of all the code your classes employ. As mentioned, it's possible to adapt a class like B by inheriting from a proxy class that embeds B instances, but that seems artificial to program goals, adds an extra call to each wrapped method, is subject to the new-style class problems we met earlier regarding interface proxies and built-ins, and seems an extraordinary and even stunning added coding requirement inherent in a model intended to simplify code.

### Flexibility: Call ordering assumptions
Routing with super also assumes that you really mean to pass method calls throughout all your classes per the MRO, which may or may not match your call ordering requirements. For example, imagine that -- irrespective of other inheritance ordering needs -- the following requires that the class C's version of a given method be run before B's in some contexts. If the MRO says otherwise, you're back to traditional calls, which may conflict with super usage -- in the following, invoking C's method twice:
> ```python
> # What if method call ordering needs differ from the MRO?
> >>> class B:
>         def __init__(self): print('B.__init__'); super().__init__()
> >>> class C:
>         def __init__(self): print('C.__init__'); super().__init__()
> >>> class D(B, C):
>         def __init__(self): print('D.__init__'); C.__init__(self); B.__init__(self)
> >>> X = D()
> D.__init__
> C.__init__
> B.__init__
> C.__init__ 				# It's the MRO xor explicit calls...
> ```

Similarly, if you want some methods to not run at all, the super automatic path won't apply as directly as explicit calls may, and will make it difficult to take more explicit control of the dispatch process. In realistic programs with many methods, resources, and state variables, these seem entirely plausible scenarios. While you could reorder superclasses in D for this method, that may break other expectations.

### Customization: Method replacement
On a related note, the universal deployment expectations of super may make it difficult for a single class to replace (override) an inherited method altogether. Not passing the call higher with super -- intentionally in this case -- works fine for the class itself, but may break the call chain of trees it's mixed into, thereby preventing methods elsewhere in the tree from running. Consider the following tree:
> ```python
> >>> class A:
>         def method(self): print('A.method'); super().method()
> >>> class B(A):
>         def method(self): print('B.method'); super().method()
> >>> class C:
>         def method(self): print('C.method') 				# No super: must anchor the chain!
> >>> class D(B, C):
>         def method(self): print('D.method'); super().method()
> 
> >>> X = D()
> >>> X.method()
> D.method
> B.method
> A.method 					# Dispatch to all per the MRO automatically
> C.method
> ```

Method replacement here breaks the super model, and probably leads us back to the traditional form:
> ```python
> # What if a class needs to replace a super's default entirely?
> >>> class B(A):
>         def method(self): print('B.method') 			# Drop super to replace A's method
> >>> class D(B, C):
>         def method(self): print('D.method'); super().method()
> 
> >>> X = D()
> >>> X.method()
> D.method
> B.method 					# But replacement also breaks the call chain...
> >>> class D(B, C):
>         def method(self): print('D.method'); B.method(self); C.method(self)
> >>> D().method()
> D.method
> B.method
> C.method 					# It's back to explicit calls...
> ```

Once again, the problem with assumptions is that they assume things! Although the assumption of universal routing might be reasonable for constructors, it would also seem to conflict with one of the core tenets of OOP -- unrestricted subclass customization. This might suggest restricting super usage to constructors, but even these might sometimes warrant replacement, and this adds an odd special-case requirement for one specific context. A tool that can be used only for certain categories of methods might be seen by some as redundant -- and even spurious, given the extra complexity it implies.

### Coupling: Application to mix-in classes
Subtly, when we say super selects the next class in the MRO, we really mean the next class in the MRO that implements the requested method -- it technically skips ahead until it finds a class with the requested name. This matters for independent mix-in classes, which might be added to arbitrary client trees. Without this skipping-ahead behavior, such mix-ins wouldn't work at all -- they would otherwise drop the call chain of their clients' arbitrary methods, and couldn't rely on their own super calls to work as expected.

In the following independent branches, for example, C's call to method is passed on, even though Mixin, the next class in the C instance's MRO, doesn't define that method's name. As long as method name sets are disjoint, this just works -- the call chains of each branch can exist independently:
> ```python
> # Mix-ins work for disjoint method sets
> >>> class A:
>         def other(self): print('A.other')
> >>> class Mixin(A):
>         def other(self): print('Mixin.other'); super().other()
> >>> class B:
>         def method(self): print('B.method')
> >>> class C(Mixin, B):
>         def method(self): print('C.method'); super().other(); super().method()
> 
> >>> C().method()
> C.method
> Mixin.other
> A.other
> B.method
> >>> C.__mro__
> (<class '__main__.C'>, <class '__main__.Mixin'>, <class '__main__.A'>,
> <class '__main__.B'>, <class 'object'>)
> ```

Similarly, mixing the other way doesn't break call chains of the mix-in either. For instance, in the following, even though B doesn't define other when called in C, classes do later in the MRO. In fact, the call chains work even if one of the branches doesn't use super at all -- as long as a method is defined somewhere ahead on the MRO, its call works:
> ```python
> >>> class C(B, Mixin):
>         def method(self): print('C.method'); super().other(); super().method()
> >>> C().method()
> C.method
> Mixin.other
> A.other
> B.method
> >>> C.__mro__
> 
> (<class '__main__.C'>, <class '__main__.B'>, <class '__main__.Mixin'>,
> <class '__main__.A'>, <class 'object'>)
> ```

This is also true in the presence of diamonds -- disjoint method sets are dispatched as expected, even if not implemented by each disjoint branch, because we select the next on the MRO with the method. Really, because the MRO contains the same classes in these cases, and because a subclass always appears before its superclass in the MRO, they are equivalent contexts. For example, the call in Mixin to other in the following still finds it in A, even though the next class after Mixin on the MRO is B (the call to method in C works again for similar reasons):
> ```python
> # Explicit diamonds work too
> >>> class A:
>         def other(self): print('A.other')
> >>> class Mixin(A):
>         def other(self): print('Mixin.other'); super().other()
> >>> class B(A):
>         def method(self): print('B.method')
> >>> class C(Mixin, B):
>         def method(self): print('C.method'); super().other(); super().method()
> 
> >>> C().method()
> C.method
> Mixin.other
> A.other
> B.method
> >>> C.__mro__
> (<class '__main__.C'>, <class '__main__.Mixin'>, <class '__main__.B'>,
> <class '__main__.A'>, <class 'object'>)
> # Other mix-in orderings work too
> >>> class C(B, Mixin):
>         def method(self): print('C.method'); super().other(); super().method()
> >>> C().method()
> C.method
> Mixin.other
> A.other
> B.method
> >>> C.__mro__
> (<class '__main__.C'>, <class '__main__.B'>, <class '__main__.Mixin'>,
> <class '__main__.A'>, <class 'object'>)
> ```

Still, this has an effect that is no different -- but may seem wildly more implicit -- than direct by-name calls, which also work the same in this case regardless of superclass ordering, and whether there is a diamond or not. In this case, the motivation for relying on MRO ordering seems on shaky ground, if the traditional form is both simpler and more explicit, and offers more control and flexibility:
> ```python
> # But direct calls work here too: explicit is better than implicit
> >>> class C(Mixin, B):
>         def method(self): print('C.method'); Mixin.other(self); B.method(self)
> >>> X = C()
> >>> X.method()
> C.method
> Mixin.other
> A.other
> B.method
> ```

More crucially, this example so far assumes that method names are disjoint in its branches; the dispatch order for same-named methods in diamonds like this may be much less fortuitous. In a diamond like the preceding, for example, it's not impossible that a client class could invalidate a super call's intent -- the call to method in Mixin in the following works to run A's version as expected, unless it's mixed into a tree that drops the call chain:
> ```python
> # But for nondisjoint methods: super creates overly strong coupling
> >>> class A:
>         def method(self): print('A.method')
> >>> class Mixin(A):
>         def method(self): print('Mixin.method'); super().method()
> 
> >>> Mixin().method()
> Mixin.method
> A.method
> >>> class B(A):
>         def method(self): print('B.method') 			# super here would invoke A after B
> >>> class C(Mixin, B):
>         def method(self): print('C.method'); super().method()
> >>> C().method()
> C.method
> Mixin.method
> B.method   				# We miss A in this context only!
> ```

It may be that B shouldn't redefine this method anyhow (and frankly, we may be encroaching on problems inherent in multiple inheritance in general), but this need not also break the mix-in -- direct calls give you more control in such cases, and allow mixin classes to be much more independent of usage contexts:
> ```python
> # And direct calls do not: they are immune to context of use
> >>> class A:
>         def method(self): print('A.method')
> >>> class Mixin(A):
>         def method(self): print('Mixin.method'); A.method(self) 		# C irrelevant
> >>> class C(Mixin, B):
>         def method(self): print('C.method'); Mixin.method(self)
> 
> >>> C().method()
> C.method
> Mixin.method
> A.method
> ```

More to the point, by making mix-ins more self-contained, direct calls minimize component coupling that always skews program complexity higher -- a fundamental software principle that seems neglected by super's variable and context-specific dispatch model.

### Customization: Same-argument constraints
As a final note, you should also consider the consequences of using super when method arguments differ per class -- because a class coder can't be sure which version of a method super might invoke (indeed, this may vary per tree!), every version of the method must generally accept the same arguments list, or choose its inputs with analysis of generic argument lists -- either of which imposes additional requirements on your code. In realistic programs, this constraint may in fact be a true showstopper for many potential super applications, precluding its use entirely.

To illustrate why this can matter, recall the pizza shop employee classes we wrote in Chapter 31. As coded there, both subclasses use direct by-name calls to invoke the superclass constructor, filling in an expected salary argument automatically -- the logic being that the subclass implies the pay grade:
> ```python
> >>> class Employee:
>         def __init__(self, name, salary): 			# Common superclass
>             self.name = name
>             self.salary = salary
> >>> class Chef1(Employee):
>         def __init__(self, name): 					# Differing arguments
>             Employee.__init__(self, name, 50000) 		# Dispatch by direct call
> >>> class Server1(Employee):
>         def __init__(self, name):
>             Employee.__init__(self, name, 40000)
> 
> >>> bob = Chef1('Bob')
> >>> sue = Server1('Sue')
> >>> bob.salary, sue.salary
> (50000, 40000)
> ```

This works, but since this is a single-inheritance tree, we might be tempted to deploy super here to route the constructor calls generically. Doing so works for either subclass in isolation, since its MRO includes just itself and its actual superclass:
> ```python
> >>> class Chef2(Employee):
>         def __init__(self, name):
>             super().__init__(name, 50000) 			# Dispatch by super()
> >>> class Server2(Employee):
>         def __init__(self, name):
>             super().__init__(name, 40000)
> 
> >>> bob = Chef2('Bob')
> >>> sue = Server2('Sue')
> >>> bob.salary, sue.salary
> (50000, 40000)
> ```

Watch what happens, though, when an employee is a member of both categories. Because the constructors in the tree have differing argument lists, we're in trouble:
> ```python
> >>> class TwoJobs(Chef2, Server2): pass
> >>> tom = TwoJobs('Tom')
> TypeError: __init__() takes 2 positional arguments but 3 were given
> ```

The problem here is that the super call in Chef2 no longer invokes its Employee superclass, but instead invokes its sibling class and follower on the MRO, Server2. Since this sibling has a differing argument list than the true superclass -- expecting just self and name -- the code breaks. This is inherent in super use: because the MRO can differ per tree, it might call different versions of a method in different trees -- even some you may not be able to anticipate when coding a class by itself:
> ```python
> >>> TwoJobs.__mro__
> (<class '__main__.TwoJobs'>, <class '__main__.Chef2'>, <class '__main__.Server2'>
> <class '__main__.Employee'>, <class 'object'>)
> >>> Chef2.__mro__
> (<class '__main__.Chef2'>, <class '__main__.Employee'>, <class 'object'>)
> ```

By contrast, the direct by-name call scheme still works when the classes are mixed, though the results are a bit dubious -- the combined category gets the pay of the leftmost superclass:
> ```python
> >>> class TwoJobs(Chef1, Server1): pass
> >>> tom = TwoJobs('Tom')
> >>> tom.salary
> 50000
> ```

Really, we probably want to route the call to the top-level class in this event with a new salary -- a model that is possible with direct calls but not with super alone. Moreover, calling Employee directly in this one class means our code uses two dispatch techniques when just one—direct calls -- would suffice:
> ```python
> >>> class TwoJobs(Chef1, Server1):
>         def __init__(self, name): Employee.__init__(self, name, 70000)
> >>> tom = TwoJobs('Tom')
> >>> tom.salary
> 70000
> >>> class TwoJobs(Chef2, Server2):
>         def __init__(self, name): super().__init__(name, 70000)
> >>> tom = TwoJobs('Tom')
> TypeError: __init__() takes 2 positional arguments but 3 were given
> ```

This example may warrant redesign in general -- splitting off shareable parts of Chef and Server to mix-in classes without a constructor, for example. It's also true that polymorphism in general assumes that the methods in an object's external interface have the same argument signature, though this doesn't quite apply to customization of superclass methods -- an internal implementation technique that should by nature support variation, especially in constructors.

But the crucial point here is that because direct calls do not make code dependent on a magic ordering that can vary per tree, they more directly support argument list flexibility. More broadly, the questionable (or weak) performances super turns in on method replacement, mix-in coupling, call ordering, and argument constraints should make you evaluate its deployment carefully. Even in single-inheritance mode, its potential for later impacts as trees grow is considerable.

In sum, the three requirements of super in this role are also the source of most of its usability issues:
- The method called by super must exist -- which requires extra code if no anchor is present.
- The method called by super must have the same argument signature across the class tree -- which impairs flexibility, especially for implementation-level methods like constructors.
- Every appearance of the method called by super but the last must use super itself -- which makes it difficult to use existing code, change call ordering, override methods, and code self-contained classes.

Taken together, these seem to make for a tool with both substantial complexity and significant tradeoffs -- downsides that will assert themselves the moment the code grows to incorporate multiple inheritance.

Naturally, there may be creative workarounds for the super dilemmas just posed, but additional coding steps would further dilute the call's benefits -- and we've run out of space here in any event. There are also alternative non-super solutions to some diamond method dispatch problems, but these will have to be left as a user exercise for space reasons too. In general, when superclass methods are called by explicit name, root classes of diamonds might check state in instances to avoid firing twice -- a similarly complex coding pattern, but required rarely in most code, and which to some may seem no more difficult than using super itself.

## The super Summary
So there it is -- the bad and the good. As with all Python extensions, you should be the judge on this one too. I've tried to give both sides of the debate a fair shake here to help you decide. But because the super call:
- Differs in form between 2.X and 3.X
- In 3.X, relies on arguably non-Pythonic magic, and does not fully apply to operator overloading or traditionally coded multiple-inheritance trees
- In 2.X, seems so verbose in this intended role that it may make code more complex instead of less
- Claims code maintenance benefits that may be more hypothetical than real in Python practice

even ex -- Java programmers should also consider this book's preferred traditional technique of explicit-name superclass calls to be at least as valid a solution as Python’s super  -- a call that on some levels seems an unusual and limited answer to a question that was not being asked by most Python programmers, and was not deemed important for much of Python's history.

At the same time, the super call offers one solution to the difficult problem of samenamed method dispatch in multiple inheritance trees, for programs that choose to use it universally and consistently. But therein lies one of its largest obstacles: it requires universal deployment to address a problem most programmers probably do not have.

Moreover, at this point in Python's history, asking programmers to change their existing code to use this call widely enough to make it reliable seems highly unrealistic. Perhaps the chief problem of this role, though, is the role itself -- same-named method dispatch in multiple inheritance trees is relatively rare in real Python programs, and obscure enough to have generated both much controversy and much misunderstanding surrounding this role. People don't use Python the same way they use C++, Java, or Dylan, and lessons from other such languages do not necessarily apply.

Also keep in mind that using super makes your program's behavior dependent on the MRO algorithm -- a procedure that we've covered only informally here due to its complexity, that is artificial to your program's purpose, and that seems tersely documented and understood in the Python world. As we've seen, even if you understand the MRO, its implications on customization, coupling, and flexibility are remarkably subtle. If you don't completely understand this algorithm -- or have goals that its application does not address -- you may be better served not relying on it to implicitly trigger actions in your code.

Or, to quote a Python motto from its import this creed:
> If the implementation is hard to explain, it's a bad idea.

The super call seems firmly in this category. Most programmers won't use an arcane tool aimed at a rare use case, no matter how clever it may be. This is especially true in a scripting language that bills itself as friendly to nonspecialists. Regrettably, use by any programmer can impose such a tool on others anyhow -- the real reason I've covered it here, and a theme we'll revisit at the end of this book.

As usual, time and user base will tell if this call's tradeoffs or momentum lead to broader adoption or not. At the least, it behooves you to also know about the traditional explicitname superclass call technique, as it is still commonly used and often either simpler or required in today's real-world Python programming. If you do choose to use this tool, my own advice to readers is to remember that using super:
- In single-inheritance mode can mask later problems and lead to unexpected behavior as trees grow
- In multiple-inheritance mode brings with it substantial complexity for an atypical Python use case

For other opinions on Python's super that go into further details both good and bad, search the Web for related articles. You can find plenty of additional positions, though in the end, Python's future relies as much on yours as any other.
