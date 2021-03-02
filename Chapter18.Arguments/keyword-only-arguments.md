> `Syntactically, keyword-only arguments are coded as named arguments that may appear
> after *args in the arguments list. All such arguments must be passed using keyword
> syntax in the call. For example, in the following, a may be passed by name or 
> position,b collects any extra positional arguments, and c must be passed by 
> keyword only. In 3.X:`
>
> ```python
> >>> def kwonly(a, *b, c):
> 		print(a, b, c)
> >>> kwonly(1, 2, c=3)
> 1 (2,) 3
> >>> kwonly(a=1, c=3)
> 1 () 3
> >>> kwonly(1, 2, 3)
> TypeError: kwonly() missing 1 required keyword-only argument: 'c'
> ```
>
> `We can also use a * character by itself in the arguments list to indicate that 
> a function does not accept a variable-length argument list but still expects all
> arguments following the * to be passed as keywords. In the next function, a may 
> be passed by position or name again, but b and c must be keywords, and no extra
> positionals are allowed:`
>
> ```python
> >>> def kwonly(a, *, b, c):
> 		print(a, b, c)
> >>> kwonly(1, c=3, b=2)
> 1 2 3
> >>> kwonly(c=3, b=2, a=1)
> 1 2 3
> >>> kwonly(1, 2, 3)
> TypeError: kwonly() takes 1 positional argument but 3 were given
> >>> kwonly(1)
> TypeError: kwonly() missing 2 required keyword-only arguments: 'b' and 'c'
> ```
>
> `You can still use defaults for keyword-only arguments, even though they appear after
> the * in the function header. In the following code, a may be passed by name or 
> position, and b and c are optional but must be passed by keyword if used:`
>
> ```python
> >>> def kwonly(a, *, b='spam', c='ham'):
> 		print(a, b, c)
> >>> kwonly(1)
> 1 spam ham
> >>> kwonly(1, c=3)
> 1 spam 3
> >>> kwonly(a=1)
> 1 spam ham
> >>> kwonly(c=3, b=2, a=1)
> 1 2 3
> >>> kwonly(1, 2)
> TypeError: kwonly() takes 1 positional argument but 2 were given
> ```
>
> `In fact, keyword-only arguments with defaults are optional, but those without 
> defaults effectively become required keywords for the function:`
>
> ```python
> >>> def kwonly(a, *, b, c='spam'):
> 		print(a, b, c)
> >>> kwonly(1, b='eggs')
> 1 eggs spam
> >>> kwonly(1, c='eggs')
> TypeError: kwonly() missing 1 required keyword-only argument: 'b'
> >>> kwonly(1, 2)
> TypeError: kwonly() takes 1 positional argument but 2 were given
> >>> def kwonly(a, *, b=1, c, d=2):
> 		print(a, b, c, d)
> >>> kwonly(3, c=4)
> 3 1 4 2
> >>> kwonly(3, c=4, b=5)
> 3 5 4 2
> >>> kwonly(3)
> TypeError: kwonly() missing 1 required keyword-only argument: 'c'
> >>> kwonly(1, 2, 3)
> TypeError: kwonly() takes 1 positional argument but 3 were given
> ```
>
> `Finally, note that keyword-only arguments must be specified after a single star, 
> not two—named arguments cannot appear after the **args arbitrary keywords form, 
> and a ** can’t appear by itself in the arguments list. Both attempts generate a 
> syntax error:`
>
> ```python
> >>> def kwonly(a, **pargs, b, c):
> SyntaxError: invalid syntax
> >>> def kwonly(a, **, b, c):
> SyntaxError: invalid syntax
> 
> This means that in a function header, keyword-only arguments must be coded before
> the **args arbitrary keywords form and after the *args arbitrary positional form, 
> when both are present. Whenever an argument name appears before *args, it is a 
> possibly default positional argument, not keyword-only:
> >>> def f(a, *b, **d, c=6): print(a, b, c, d) # Keyword-only before **!
> SyntaxError: invalid syntax
> >>> def f(a, *b, c=6, **d): print(a, b, c, d) # Collect args in header
> >>> f(1, 2, 3, x=4, y=5) # Default used
> 1 (2, 3) 6 {'y': 5, 'x': 4}
> >>> f(1, 2, 3, x=4, y=5, c=7) # Override default
> 1 (2, 3) 7 {'y': 5, 'x': 4}
> >>> def f(a, c=6, *b, **d): print(a, b, c, d) # c is not keyword-only here!
> >>> f(1, 2, 3, x=4)
> 1 (3,) 2 {'x': 4}
> ```
>
> `CALL ORDER
> In fact, similar ordering rules hold true in function calls: when keyword-only
> arguments are passed, they must appear before a **args form. The keyword-only 
> argument can be coded either before or after the *args, though, and may be 
> included in **args:`
>
> ```python
> >>> def f(a, *b, c=6, **d): print(a, b, c, d) # KW-only between * and **
> >>> f(1, *(2, 3), **dict(x=4, y=5)) # Unpack args at call
> 1 (2, 3) 6 {'y': 5, 'x': 4}
> >>> f(1, *(2, 3), **dict(x=4, y=5), c=7) # Keywords before **args!
> SyntaxError: invalid syntax
> >>> f(1, *(2, 3), c=7, **dict(x=4, y=5)) # Override default
> 1 (2, 3) 7 {'y': 5, 'x': 4}
> >>> f(1, c=7, *(2, 3), **dict(x=4, y=5)) # After or before *
> 1 (2, 3) 7 {'y': 5, 'x': 4}
> >>> f(1, *(2, 3), **dict(x=4, y=5, c=7)) # Keyword-only in **
> 1 (2, 3) 7 {'y': 5, 'x': 4}
> ```