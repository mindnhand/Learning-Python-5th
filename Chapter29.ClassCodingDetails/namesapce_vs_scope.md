# Namespaces: The Conclusion
Now that we've examined class and instance objects, the Python namespace story is
complete. For reference, I'll quickly summarize all the rules used to resolve names here.
The first things you need to remember are that qualified and unqualified names are
treated differently, and that some scopes serve to initialize object namespaces:
* Unqualified names (e.g., X) deal with scopes.
* Qualified attribute names (e.g., object.X) use object namespaces.
* Some scopes initialize object namespaces (for modules and classes).
These concepts sometimes interact—in object.X, for example, object is looked up per
scopes, and then X is looked up in the result objects. Since scopes and namespaces are
essential to understanding Python code, let’s summarize the rules in more detail.

## Simple Names: Global Unless Assigned
As we’ve learned, unqualified simple names follow the LEGB lexical scoping rule outlined
when we explored functions in Chapter 17:
* Assignment (X = value)
  Makes names local by default: creates or changes the name X in the current local
  scope, unless declared global (or nonlocal in 3.X).
* Reference (X)
  Looks for the name X in the current local scope, then any and all enclosing functions,
  then the current global scope, then the built-in scope, per the LEGB rule.
  Enclosing classes are not searched: class names are fetched as object attributes
  instead.
Also per Chapter 17, some special-case constructs localize names further (e.g., variables
in some comprehensions and try statement clauses), but the vast majority of names
follow the LEGB rule.

## Attribute Names: Object Namespaces
We've also seen that qualified attribute names refer to attributes of specific objects and
obey the rules for modules and classes. For class and instance objects, the reference
rules are augmented to include the inheritance search procedure:
* Assignment (object.X = value)
  Creates or alters the attribute name X in the namespace of the object being qualified,
  and none other. Inheritance-tree climbing happens only on attribute reference,
  not on attribute assignment.
* Reference (object.X)
  For class-based objects, searches for the attribute name X in object, then in all
  accessible classes above it, using the inheritance search procedure. For nonclass
  objects such as modules, fetches X from object directly.
As noted earlier, the preceding captures the normal and typical case. These attribute
rules can vary in classes that utilize more advanced tools, especially for new-style classes
—an option in 2.X and the standard in 3.X, which wee'll explore in Chapter 32. For
example, reference inheritance can be richer than implied here when metaclasses are
deployed, and classes which leverage attribute management tools such as properties,
descriptors, and __setattr__ can intercept and route attribute assignments arbitrarily.
In fact, some inheritance is run on assignment too, to locate descriptors with a
__set__ method in new-style classes; such tools override the normal rules for both
reference and assignment. We'll explore attribute management tools in depth in Chapter
38, and formalize inheritance and its use of descriptors in Chapter 40. For now,
most readers should focus on the normal rules given here, which cover most Python
application code.

