from glom import glom
target = {'a': {'b':{'c':{'d':{'e':[1,2,3,4,5,6,7]}}}}}
spec = 'a.b.c.d.e'
output = glom(target, spec)
print(output)
#输出[1, 2, 3, 4, 5, 6, 7]