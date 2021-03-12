# Nested Classes: The LEGB Scopes Rule Revisited

Though they are normally coded at the top level of a module, classes also sometimes
appear nested in functions that generate them—a variation on the “"factory function"
(a.k.a. closure) theme in Chapter 17, with similar state retention roles. There we noted
that class statements introduce new local scopes much like function def statements,
which follow the same LEGB scope lookup rule as function definitions.

This rule applies both to the top level of the class itself, as well as to the top level of
method functions nested within it. Both form the L layer in this rule—they are normal
local scopes, with access to their names, names in any enclosing functions, globals in
the enclosing module, and built-ins. Like modules, the class's local scope morphs into
an attribute namespace after the class statement is run.

Although classes have access to enclosing functions' scopes, though, they do not act
as enclosing scopes to code nested within the class: <u>Python searches enclosing functions
for referenced names, but never any enclosing classes. That is, a class is a local scope
and has access to enclosing local scopes, but it does not serve as an enclosing local scope
to further nested code. Because the search for names used in method functions skips
the enclosing class, class attributes must be fetched as object attributes using inheritance.</u>


For example, in the following nester function, all references to X are routed to the global
scope except the last, which picks up a local scope redefinition (the section's code is in
file classscope.py, and the output of each example is described in its last two comments):
> ```python
> X = 1
> def nester():
>     print(X) 									# Global: 1
>     class C:
>         print(X) 								# Global: 1
>         def method1(self):
>             print(X) 							# Global: 1
>         def method2(self):
>             X = 3 							# Hides global
>             print(X) 							# Local: 3
>     I = C()
>     I.method1()
>     I.method2()
> print(X) 										# Global: 1
> nester() 										# Rest: 1, 1, 1, 3
> print('-' * 40)
> ```

Watch what happens, though, when we reassign the same name in nested function
layers: the redefinitions of X create locals that hide those in enclosing scopes, just as for
simple nested functions; the enclosing class layer does not change this rule, and in fact
is irrelevant to it:
> ```python
> X = 1
> def nester():
>     X = 2 									# Hides global
>     print(X) 									# Local: 2
>     class C:
>         print(X) 								# In enclosing def (nester): 2
>         def method1(self):
>             print(X) 							# In enclosing def (nester): 2
>         def method2(self):
>             X = 3 							# Hides enclosing (nester)
>             print(X) 							# Local: 3
>     I = C()
>     I.method1()
>     I.method2()
> print(X) 										# Global: 1
> nester() 										# Rest: 2, 2, 2, 3
> print('-' * 40)
> ```

And here's what happens when we reassign the same name at multiple stops along the
way: assignments in the local scopes of both functions and classes hide globals or enclosing
function locals of the same name, regardless of the nesting involved:
> ```python
> X = 1
> def nester():
>     X = 2 								# Hides global
>     print(X) 								# Local: 2
>     class C:
>         X = 3 							# Class local hides nester's: C.X or I.X (not scoped)
>         print(X) 							# Local: 3
>         def method1(self):
>             print(X) 						# In enclosing def (not 3 in class!): 2
>             print(self.X) 				# Inherited class local: 3
>         def method2(self):
>             X = 4 						# Hides enclosing (nester, not class)
>             print(X) 						# Local: 4
>             self.X = 5 					# Hides class
>             print(self.X) 				# Located in instance: 5
>     I = C()
>     I.method1()
>     I.method2()
> 
> print(X) 									# Global: 1
> nester() 									# Rest: 2, 3, 2, 3, 4, 5
> print('-'*40)
> ```

Most importantly, the lookup rules for simple names like X never search enclosing
class statements—just defs, modules, and built-ins (it's the LEGB rule, not CLEGB!).
In method1, for example, X is found in a def outside the enclosing class that has the same
name in its local scope. To get to names assigned in the class (e.g., methods), we must
fetch them as class or instance object attributes, via self.X in this case.

Believe it or not, we'll see use cases for this nested classes coding pattern later in this
book, especially in some of Chapter 39's decorators. In this role, the enclosing function
usually both serves as a class factory and provides retained state for later use in the
enclosed class or its methods.
