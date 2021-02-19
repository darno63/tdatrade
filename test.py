# testing decorators

def logger(func):
    def inner():
        print('calling', func.__name__)
        func()
        print('calling', func.__name__)
    return inner

def target():
    print('In targer function')



t1 = logger(target)
t1()

@logger
def target2():
    print('In target2 function')

#target2()

def decorator(func):
    def inner(*args, **kargs):
        x, y, orders, axe = func(*args, **kargs)
        print(orders)
        return "I like " + x + " and " + str(axe)
    return inner

@decorator
def likes(orders, hammer=0, axe=2):
    x = "cats"
    y = "dogs"
    return x, y, orders, axe

print(likes(2, 3))
        
