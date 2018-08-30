q=set()
a=set([1,2,3])
b=set([3,5,7])
c=set([11,15,17])
zz=zip(a,b)

print(list(zz))
all=[a,b,c]
for each in all:
    q=q|each
print(q)
