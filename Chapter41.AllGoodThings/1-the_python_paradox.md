# The Python Paradox
If you've read this book, or reasonable subsets of it, you should now be able to weigh Python's tradeoffs fairly. As you've seen, Python is a powerful, expressive, and even fun programming language, which will serve as an enabling technology for wherever you choose to go next. At the same time, you've also seen that today's Python is something of a paradox: it has expanded to incorporate tools that many consider both needlessly redundant and curiously advanced -- and at a rate that appears to be only accelerating.

For my part, as one of Python's earliest advocates, I've watched it morph over the years from simple to sophisticated tool, with a steadily shifting scope. By most measures, it seems to have grown at least as complex as other languages that drove many of us to Python in the first place. And just as in those other languages, this has inevitably fostered a growing culture in which obscurity is a badge of honor.

That's as contrary to Python's original goals as it could be. Run an `import this` in any Python interactive session to see what I mean -- the creed I've quoted from repeatedly in this book in contexts where it was clearly violated. On many levels, its core ideals of explicitness, simplicity, and lack of redundancy have been either naively forgotten or carelessly abandoned.

The end result is a language and community that could in part be described today in some of the same terms I used in the Perl sidebar of Chapter 1. While Python still has much to offer, this trend threatens to negate much of its perceived advantage, as the next section explains.

## On "Optional" Language Features
I included a quote near the start of the prior chapter about metaclasses not being of interest to 99% of Python programmers, to underscore their perceived obscurity. That statement is not quite accurate, though, and not just numerically so. The quote's author is a noted Python contributor and friend from the early days of Python, and I don't mean to pick on anyone unfairly. Moreover, I've often made such statements about language feature obscurity myself -- in the various editions of this very book, in fact.

The problem, though, is that such statements really apply only to people who work alone and only ever use code that they've written themselves. As soon as an "optional" advanced language feature is used by anyone in an organization, it is no longer optional -- it is effectively imposed on everyone in the organization. The same holds true for externally developed software you use in your systems -- if the software's author uses an advanced or extraneous language feature, it's no longer entirely optional for you, because you have to understand the feature to reuse or change the code.

This observation applies to all the advanced topics covered in this book, including those listed as "magic" hooks near the beginning of the prior chapter, and many others:
> Generators, decorators, slots, properties, descriptors, metaclasses, context managers, closures, super, namespace packages, Unicode, function annotations, relative imports, keyword-only arguments, class and static methods, and even obscure applications of comprehensions and operator overloading 

If any person or program you need to work with uses such tools, they automatically become part of your required knowledge base too.

To see just how daunting this can be, one need only consider Chapter 40's new-style inheritance procedure -- a horrifically convoluted model that can make descriptors and metaclasses prerequisite to understanding even basic name resolution. Chapter 32's super similarly ups the intellectual ante -- imposing an obscenely implicit and artificial MRO algorithm on readers of any code that uses this tool.

The net effect of such over-engineering is to either escalate learning requirements radically, or foster a user base that only partially understands the tools they employ. This is obviously less than ideal for those hoping to use Python in simpler ways, and contradictory to the scripting motif.

## Against Disquieting Improvements
This observation also applies to the many redundant features we've seen, such as Chapter 7's str.format method and Chapter 34's with statement -- tools borrowed from other languages, and overlapping with others long present in Python. When programmers use multiple ways to achieve the same goal, all become required knowledge.

Let's be honest: Python has grown rife with redundancy in recent years. As I suggested in the preface -- and as you've now seen first-hand -- today's Python world comes replete with all the functional duplications and expansions chronicled in Table 41-1, among others we've seen in this book.

***Table 41-1. A sampling of redundancy and feature explosion in Python***
|Category|Specifics|
|:-|:-|
|3 major paradigms|Procedural, functional, object-oriented|
|2 incompatible lines|2.X and 3.X, with new-style classes in both|
|3 string formatting tools|% expression, str.format, string.Template|
|4 attribute accessor tools|\_\_getattr\_\_, \_\_getattribute\_\_, propert, descriptors|
|2 finalization statements|try/finally, with|
|4 varieties of comprehension|List, generator, set, dictionary|
|3 class augmentation tools|Function calls, decorators, metaclasses|
|4 kinds of methods|Instance, static, class, metaclass|
|2 attribute storage systems|Dictionaries, slots|
|4 flavors of imports|Module, package, package relative, namespace package|
|2 superclass dispatch protocols|Direct calls, super + MRO|
|5 assignment statement forms|Basic, multiname, augmented, sequence, starred|
|2 types of functions|Normal, generator|
|5 function argument forms|Basic, name=value, \*pargs, \*\*kargs, keyword-only|
|2 class behavior sources|Superclasses, metaclasses|
|4 state retention options|Classes, closures, function attributes, mutables|
|2 class models|Classic + new-style in 2.X, mandated new-style in 3.X|
|2 Unicode models|Optional in 2.X, mandated in 3.X|
|2 PyDoc modes|GUI client, required all-browser in recent 3.X|
|2 byte code storage schemes|Original, \_\_pycache\_\_ only in recent 3.X|

If you care about Python, you should take a moment to browse this table. It reflects a virtual explosion in functionality and toolbox size -- 59 concepts that are all fair game for newcomers. Most of its categories began with just one original member in Python; many were expanded in part to imitate other languages; and only the last few can be simplified by pretending that the latest Python is the only Python that matters to its programmers.

I've stressed avoiding unwarranted complexity in this book, but in practice, both advanced and new tools tend to encourage their own adoption -- often for no better reason than a programmer's personal desire to demonstrate prowess. The net result is that much Python code today is littered with these complex and extraneous tools. That is, nothing is truly "optional" if nothing is truly optional.

## Complexity Versus Power
This is why some Python old-timers (myself included) sometimes worry that Python seems to have grown larger and more complex over time. New features added by veterans, converts, and even amateurs may have raised the intellectual bar for newcomers.

Although Python's core ideas, like dynamic typing and built-in types, have remained essentially the same, its advanced additions can become required reading for any Python programmer. I chose to cover these topics here for this reason, despite their omission in early editions. It's not possible to skip the advanced stuff if it's in code you have to understand.

On the other hand, as mentioned in Chapter 1, to most observers Python is still noticeably simpler than most of its contemporaries, and perhaps only as complex as its many roles require. Though it's acquired many of the same tools as Java, C#, and C++, they tend to be lighter weight in the context of a dynamically typed scripting language. For all its growth over the years, Python is still relatively easy to learn and use when compared to the alternatives, and new learners can often pick up advanced topics as needed.

And frankly, application programmers tend to spend most of their time dealing with libraries and extensions, not advanced and sometimes-arcane language features. For instance, the book Programming Python -- a follow-up to this one -- deals mostly with the marriage of Python to application libraries for tasks such as GUIs, databases, and the Web, not with esoteric language tools (though Unicode still forces itself onto many stages, and the odd generator expression and yield crop up along the way).

Moreover, the flipside of this growth is that Python has become more powerful. When used well, tools like decorators and metaclasses are not only arguably "cool," but allow creative programmers to build more flexible and useful APIs for other programmers to use. As we've seen, they can also provide good solutions to problems of encapsulation and maintenance.

## Simplicity Versus Elitism
Whether this justifies the potential expansion of required Python knowledge is up to you to decide. For better or worse, a person's skill level often decides this issue by default -- more advanced programmers like more advanced tools and tend to forget about their impact on other camps. Fortunately, though, this isn't an absolute; good programmers also understand that simplicity is good engineering, and advanced tools should be used only when warranted. This is true in any programming language, but especially in one like Python that is frequently exposed to new or novice programmers as an extension tool.

And if you're still not buying this, keep in mind that many people using Python are not comfortable with even basic OOP. Trust me on this; I’ve met thousands of them. Although Python was never a trivial subject, the reports from the software trenches are very clear on this point: unwarranted added complexity is never a welcome feature, especially when it is driven by the personal preferences of an unrepresentative few.  Whether intended or not, this is often understandably perceived as elitism -- a mindset that is both unproductive and rude, and has no place in a tool as widely used as Python.

This is also a social issue, of course, and pertains as much to individual programmers as to language designers. In the "real world" where open source software is measured, though, Python-based systems that require their users to master the nuances of metaclasses, descriptors, and the like should probably scale their market expectations accordingly.

Hopefully, if this book has done its job, you'll find the importance of simplicity in programming to be one of its most important and lasting takeaways.

## Closing Thoughts
So there you have it -- some observations from someone who has been using, teaching, and advocating Python for two decades, and still wishes nothing but the best for its future. None of these concerns are entirely new, of course. Indeed, the growth of this very book over the years seems testament to the effect of Python's own growth -- if not an ironic eulogy to its original conception as a tool that would simplify programming and be accessible to both experts and nonspecialists alike. Judging by language heft alone, that dream seems to have been either neglected or abandoned entirely.

That said, Python's present rise in popularity seems to show no signs of abating -- a powerful counterargument to complexity concerns. Today’s Python world may be understandably less concerned with its original and perhaps idealistic goals than with applying its present form in their work. Python gets many a job done in the practical world of complex programming requirements, and this is still ample cause to recommend it for many tasks. Original goals aside, mass appeal does qualify as one form of success, though one whose significance will have to await the verdict of time.

If you're interested in musing further over Python's evolution and learning curve, I wrote a more in-depth article in 2012 on such things: Answer Me These Questions Three..., available online at http://learning-python.com/pyquestions3.html. These are important pragmatic questions that are crucial to Python's future, and deserve more attention than I've given here. But these are highly subjective issues; this is not a philosophy text; and this book has already exceeded its page-count targets.

More importantly, in an open source project like Python the answers to such questions must be formed anew by each wave of newcomers. I hope the wave you ride in will have as much common sense as fun while plotting Python's future.
