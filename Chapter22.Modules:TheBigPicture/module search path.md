Roughly, Python's module search path is composed of the concatenation of these major components, 
some of which are preset for you and some of which you can tailor to tell Python where to look:

1. The home directory of the program
2. PYTHONPATH directories (if set)
3. Standard library directories
4. The contents of any .pth files (if present)
5. The site-packages home of third-party extensions

Ultimately, the concatenation of these four components becomes sys.path, a mutable
list of directory name strings that I'll expand upon later in this section. The first and
third elements of the search path are defined automatically. Because Python searches
the concatenation of these components from first to last, though, the second and
fourth elements can be used to extend the path to include your own source code directories.