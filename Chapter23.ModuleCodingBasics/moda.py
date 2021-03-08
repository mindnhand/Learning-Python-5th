x = 88          # x, global to this file only

def f():
    global x    # Change the file's x
    x = 99      # Cannot see names in other modules


