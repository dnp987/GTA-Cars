a = ['apple', 'orange', 'banana', 'grape']
print (type(a))
print (a.count('apple'))
print (a.index('apple'))
a.append('pear')
print (a, len(a))
a.reverse()
print (a, len(a))
a.sort()
print (a, len(a))
a.pop()
print (a, len(a))
b = a
print (b)
b[1] ="red"
print (b)

t = (1234, 5678, 'hello')
print (t[0], len(t), type(t))
#t[1] = 777
print (t)

set1 = {'apple', 'orange', 'banana'}
print (type(set1))
print (set1)
print ('grape' in set1)

x = 'test'
y = 'test2'
z = x + " " + y
print (x, y, z)
xx = [' '.join(z)]
print (xx)