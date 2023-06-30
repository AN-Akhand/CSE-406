from math import gcd
import random
import time

def mod_exp(base, exponent, modulus):
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result

def primes(sieve_size):
    sieve = [True] * sieve_size
    for i in range(3, int(sieve_size ** 0.5) + 1, 2):
        if sieve[i]:
            sieve[i * i::2 * i] = [False] * ((sieve_size - i * i - 1) // (2 * i) + 1)
    return [i for i in range(3, sieve_size, 2) if sieve[i]]

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

def generate_safe_prime(q, sieve_size):
    if q % 2 == 0:
        q += 1
    S = primes(sieve_size)
    while True:
        if any(gcd(q, r) != 1 for r in S):
            q += 2
            continue
        if any(q % r == (r - 1) // 2 for r in S):
            q += 2
            continue
        if not miller_rabin_primality_test(q, 5):
            q += 2
            continue
        p = 2 * q + 1
        if miller_rabin_primality_test(p, 5):
            return p
        q += 2

def primitive_root(p):
    if p == 2:
        return 1
    p1 = 2
    p2 = (p - 1) // p1
    while(1):
        g = random.randint(2, p - 1)
        if not (mod_exp(g, (p - 1) // p1, p) == 1):
            if not mod_exp(g, (p - 1) // p2, p) == 1:
                return g

class Diffie_Hellman:

    def __init__(self, size, sieve_size):
        self.size = size
        self.sieve_size = sieve_size

    def set_public_modulus(self, p):
        self.p = p
    
    def set_public_base(self, g):
        self.g = g

    def set_public_key(self, B):
        self.B = B
    
    def generate_public_modulus(self):
        self.p = generate_safe_prime(random.getrandbits(self.size), self.sieve_size)

    def generate_public_base(self):
        self.g = primitive_root(self.p)

    def generate_private_key(self):
        x = random.getrandbits(self.size // 2)
        if(x % 2 == 0):
            x += 1
        while(1):
            if miller_rabin_primality_test(x, 5):
                self.a = x
                return
            x += 2

    def generate_public_key(self):
        self.A = mod_exp(self.g, self.a, self.p)

    def generate_shared_secret_key(self):
        self.secret_key = mod_exp(self.B, self.a, self.p)


#totalTime = 0
#
#for i in range(12):
#    for _ in range(100):
#        generate_safe_prime(random.getrandbits(128) + 1, 2 ** i)
#    print("Average time for sieve_size = ", 2 ** i, " : ", totalTime / 100, "ms")
#    totalTime = 0

#p = generate_safe_prime(random.getrandbits(128), 64)
#print("p = ", p, "q = ", (p - 1) // 2)

#p = generate_safe_prime(random.getrandbits(128), 64)
#g = primitive_root(p)
#a = generate_secret_key(p)
#b = generate_secret_key(p)
#A = mod_exp(g, a, p)
#sieve_size = mod_exp(g, b, p)
#
#secret_key1 = mod_exp(sieve_size, a, p)
#secret_key2 = mod_exp(A, b, p)
#
#print("p = ", p)
#print("g = ", g)
#print("a = ", a)
#print("b = ", b)
#print("A = ", A)
#print("sieve_size = ", sieve_size)
#print("secret_key1 = ", secret_key1)
#print("secret_key2 = ", secret_key2)
#print("Length = ", secret_key1.bit_length(), " bits")

#print(generate_safe_prime(random.getrandbits(128) + 1,5))