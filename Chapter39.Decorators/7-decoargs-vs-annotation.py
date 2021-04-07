#!/usr/bin/env python3
#encoding=utf-8


#----------------------------------------------
# Usage: python3 7-decoargs-vs-annotation.py
# Description: decorator arguments versus function annotations
#----------------------------------------------



'''
In fact, using annotation instead of decorator arguments in this example actually limits its utility.
For one thing, annotation only works under Python 3.X, so 2.X is no longer supported; function 
decorators with arguments, on the other hand, work in both versions.

More importantly, by moving the validation specifications into the def header, we essentially commit 
the function to a single role -- since annotation allows us to code only one expression per argument, 
it can have only one purpose. For instance, we cannot use range-test annotations for any other role. 

By contrast, because decorator arguments are coded outside the function itself, they are both easier 
to remove and more general -- the code of the function itself does not imply a single decoration purpose. 
Crucially, by nesting decorators with arguments, we can apply multiple augmentation steps to the same 
function; annotation directly supports only one. With decorator arguments, the function itself also 
retains a simpler, normal appearance.
'''


# Using decorator arguments (3.X + 2.X)
def rangetest_deco(**args_check):
    def onDecorator(func):
        def onCall(*args, **kwargs):
            print(args_check)
            for check in args_check:
                pass                # add validation code here
            return func(*args, **kwargs)
        return onCall
    return onDecorator


# Using function annotations (3.X only)
def rangetest_anno(func):
    def onCall(*args, **kwargs):
        args_check = func.__annotations__
        print(args_check)
        for check in args_check:
            pass                    # add validation code here
        return func(*args, **kwargs)
    return onCall




if __name__ == '__main__':
    # test decorator arguments
    @rangetest_deco(a=(1, 5), c=(0.0, 1.0))
    def func_deco(a, b, c):              # func = rangetest(...)(func)
        print(a + b + c)

    func_deco(1, 2, c=3)                 # runs onCall, args_check in scope


    # test function annotations
    @rangetest_anno
    def func_anno(a:(1, 5), b, c:(0.0, 1.0)):           # func_anno = rangetest_anno(func_anno)
        print(a + b + c)

    func_anno(1, 2, c=3)
