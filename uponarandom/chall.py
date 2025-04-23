import base64
import os
import pyotp
import random
import signal
from dataclasses import dataclass

class RNG:
    def __init__(self):
        self.m = 100
        self.k = [random.randint(1, 1000) % 2 for _ in range(self.m)]
        while 1 not in self.k:
            self.k = [random.randint(1, 1000) % 2 for _ in range(self.m)]
        self.x = [random.randint(1, 1000) % 2 for _ in range(self.m)]
        while 1 not in self.x:
            self.x = [random.randint(1, 1000) % 2 for _ in range(self.m)]

    def next(self):
        res = self.x[0]
        self.x = self.x[1:] + [sum([self.k[i] * self.x[i] for i in range(self.m)]) % 2]
        self.k = self.k[1:] + [self.k[0]]
        return res

    def next_with_length(self, length):
        res = 0
        while res.bit_length() != length:
            res <<= 1
            res += self.next()
        return res

    def get_otp_secret(self, secret_length):
        return base64.b32encode(int.to_bytes(self.next_with_length(secret_length), secret_length // 8, byteorder='big')).decode()

@dataclass
class User:
    username: str
    password: str
    secret: str

    def is_authenticated(self, password, otp):
        return self.password == password and pyotp.TOTP(self.secret).verify(otp)

    def get_otp(self):
        return pyotp.TOTP(self.secret).now()

def read_flag():
    f = open('flag.txt')
    flag = f.read()
    f.close()
    return flag

def menu():
    global current_user
    print('===== Menu =====')
    if current_user != 'unauthenticated':
        print(f'Hello {current_user}!')
    print('1. Login')
    print('2. Register')
    print('3. Read Flag')
    print('4. Exit')
    choice = int(input('> '))
    return choice

def main():
    signal.alarm(180)

    rng = RNG()
    secret_length = 160
    
    users = {
        'admin': User(
            'admin',
            'abcdef', # totally secure with 2FA, right?
            rng.get_otp_secret(secret_length),
        ),
    }
    assert users['admin'].is_authenticated(users['admin'].password, users['admin'].get_otp())

    global current_user
    current_user = 'unauthenticated'
    wrong_login_attempt = 0
    threshold = 3

    while True:
        if wrong_login_attempt >= threshold:
            print('Access denied.')
            break
        try:
            choice = menu()
            if choice == 1:
                username = input('Username: ')
                password = input('Password: ')
                otp = input('OTP: ')
                if username not in users:
                    print('Access denied.')
                    users['admin'].secret = rng.get_otp_secret(secret_length)
                    wrong_login_attempt += 1
                    continue
                if not users[username].is_authenticated(password, otp):
                    wrong_login_attempt += 1
                    users['admin'].secret = rng.get_otp_secret(secret_length)
                    print('Access denied.')
                    continue
                current_user = username
            if choice == 2:
                username = input('Username: ')
                if username in users:
                    print('Access denied.')
                    continue
                password = input('Password: ')
                secret = rng.get_otp_secret(secret_length)
                print('OTP Secret:', secret)
                new_user = User(
                    username,
                    password,
                    secret,
                )
                otp = input('OTP: ')
                if not new_user.is_authenticated(password, otp):
                    print('Access denied.')
                    continue
                users[username] = new_user
            if choice == 3:
                if current_user == 'admin':
                    print(read_flag())
                else:
                    print('Access denied.')
            if choice == 4:
                break
        except:
            print('Something error happened.')
            break
    print('Bye.')

if __name__ == '__main__':
    main()