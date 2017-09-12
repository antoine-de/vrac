

def facto(x):
    print("facto {}".format(x))
    if x < 0:
        raise Exception('impossible to call facto with negtive values')
    if x == 1:
        return 1
    elif x == 0:
        return 0
    return x*facto(x-1)

def pilevide(pile):
    return pile == []

def depiler(pile):
    if pilevide(pile):
        return None
    # val = pile.pop()
    lastvar = len(pile)-1
    val = pile[lastvar]
    del pile[lastvar]
    return val

def empiler(pile,value):
    pile.append(value)

p = []
print('la pile est vide ? {} (nb elt = {})'.format(pilevide(p), len(p)))

x = depiler(p)
print('la valo depilee est {}'.format(x))

empiler(p,5)
print('la pile est vide ? {}'.format(pilevide(p)))

x = depiler(p)
print('la valo depilee est {}'.format(x))
print('la pile est vide ? {}'.format(pilevide(p)))


empiler(p, 2)
empiler(p, 2)
empiler(p, 2)
empiler(p, 4)
x = depiler(p)
print('la valo depilee est {}'.format(x))

# print("res = {}".format(facto(0)))
# print("res = {}".format(facto(5)))
# print("res = {}".format(facto(-2)))
# print("res = {}".format(facto(4)))

