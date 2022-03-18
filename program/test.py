import ast
a = {}
a[-60.0] = 24
a[-30.0] = 0
a[0.2] = -25
a[25] = -50
a[75] = -75
a[125] = -110

print(a)
st = str(a)
print(st)
b = ast.literal_eval(st)
for i in b.keys():
    print(i, b[i])