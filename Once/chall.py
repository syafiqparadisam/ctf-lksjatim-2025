import string
import random
import os

f = open('flag.txt')
flag = f.read()
f.close()

assert flag.startswith('LKS')
assert all([_ in string.printable for _ in flag])

x = ''
for _ in range(len(flag)):
    x += chr(random.randint(ord('A'), ord('Z') + 1))

k = []
for _ in range(len(flag)):
    k.append(int.from_bytes(os.urandom(1), 'big'))

a = []
b = []
for i in range(len(flag)):
    a.append(ord(flag[i]) ^ k[i])
    b.append(ord(x[i]) ^ k[i])

print(bytes(a).hex())
print(bytes(b).hex())