a = 'abc'
b = 'def'
c = a+b
print (type(c), " ", len(c), " ", c)

c = a,b
print (type(c), " ", len(c), " ", c)

c = " ".join([a, b])
print (type(c), " ", len(c), " ", c)
