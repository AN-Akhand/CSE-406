import random
from math import gcd
import hashlib  

def primes(sieve_size):
    sieve = [True] * sieve_size
    for i in range(3, int(sieve_size ** 0.5) + 1, 2):
        if sieve[i]:
            sieve[i * i::2 * i] = [False] * ((sieve_size - i * i - 1) // (2 * i) + 1)
    return [i for i in range(3, sieve_size, 2) if sieve[i]]

def mod_exp(base, exponent, modulus):
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result

def miller_rabin(n, d):
    a = random.randrange(2, n - 1)
    x = mod_exp(a, d, n)
    if x == 1 or x == n - 1:
        return True
    while d != n - 1:
        x = mod_exp(x, 2, n)
        d *= 2
        if x == 1:
            return False
        if x == n - 1:
            return True

def miller_rabin_primality_test(n, k):
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    d = n - 1
    while d % 2 == 0:
        d //= 2

    for _ in range(k):
        if not miller_rabin(n, d):
            return False
    return True

def generate_prime(q, sieve_size):
    if q % 2 == 0:
        q += 1
    S = primes(sieve_size)
    while True:
        if any(gcd(q, r) != 1 for r in S):
            q += 2
            continue
        if not miller_rabin_primality_test(q, 5):
            q += 2
            continue
        if q % 65537 == 1:
            q += 2
            continue
        return q

def generate_key(size):
    e = 65537

    p = generate_prime(random.getrandbits(size), 64)
    q = generate_prime(random.getrandbits(size), 64)

    n = p * q

    phi = (p - 1) * (q - 1)

    d = pow(e, -1, phi)

    return (e, n), (d, n)

def encrypt(m, e, n):
    return mod_exp(m, e, n)

def decrypt(c, d, n):
    return mod_exp(c, d, n)

class RSA:
    def __init__(self, key_size):
        self.public_key, self.private_key = generate_key(key_size)

    def set_public_key(self, e, n):
        self.other_key = (e, n)
    
    def encrypt(self, m):
        return encrypt(m, *self.other_key)

    def decrypt(self, c):
        return decrypt(c, *self.private_key)

    def sign(self, m):
        hashobj = hashlib.sha256(str(m).encode())
        hash = int.from_bytes(hashobj.digest(), 'big')
        print(self.decrypt(hash))
        return encrypt(m, *self.other_key), encrypt(self.decrypt(hash), *self.other_key)

    def verify(self, m, s):
        hashobj = hashlib.sha256(str(m).encode())
        hash = int.from_bytes(hashobj.digest(), 'big')
        return self.encrypt(s) == hash
